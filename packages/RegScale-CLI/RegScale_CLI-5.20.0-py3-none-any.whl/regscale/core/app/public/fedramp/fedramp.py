#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""standard python imports"""

import dataclasses
import json
import os
import re
import zipfile
from datetime import date, datetime
from io import StringIO
from tempfile import gettempdir
from typing import Any, Optional, Dict, List, Tuple
from urllib.parse import urljoin

import click
import requests
from dateutil.relativedelta import relativedelta
from docx.table import Table
from lxml import etree
from requests import Response
from ssp import SSP

from regscale.core.app.api import Api
from regscale.core.app.application import Application

from regscale.core.app.utils.app_utils import (
    capitalize_words,
    download_file,
    error_and_exit,
    get_current_datetime,
)
from regscale.core.app.utils.regscale_utils import get_user
from regscale.models.regscale_models import Component, ControlImplementation
from regscale.models.regscale_models.control_implementation import (
    ControlImplementationStatus,
)
from regscale.models.regscale_models.files import File
from regscale.models.regscale_models.interconnects import Interconnects
from regscale.models.regscale_models.ports_protocols import PortsProtocols
from regscale.models.regscale_models.requirements import Requirement
from regscale.models.regscale_models.securityplans import SecurityPlan
from regscale.models.regscale_models.system_roles import SystemRoles
from regscale.models.regscale_models.leveraged_authorizations import (
    LeveragedAuthorizations,
)


from regscale.core.app.public.fedramp.import_fedramp_r4_ssp import (
    parse_and_load_xml_rev4,
)

from regscale.core.app.public.fedramp.ssp_logger import SSPLogger

ssp_logger = SSPLogger()
logger = ssp_logger

namespaces = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
NEW_LINE_OUTPUT = "\n------------------------------\n"
SYSTEM_TYPE = "Major Application"


@click.group()
def fedramp():
    """[BETA] Performs bulk processing of FedRAMP files (Upload trusted data only)."""


# FedRAMP Docx Support
# TODO: Exporter Takes controls maps to fedramp package.
@fedramp.command(context_settings={"show_default": True})
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the full file path of the FedRAMP document to ingest to RegScale.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--base_fedramp_profile",
    type=click.STRING,
    required=False,
    help="Enter the name of the RegScale FedRAMP profile to use.",
    default="FedRAMP - High",
)
@click.option(
    "--save_data",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to save the data as a JSON file.",
)
@click.option(
    "--add_missing",
    type=click.BOOL,
    default=False,
    required=False,
    help="Whether to create missing controls from profile in the SSP.",
)
def load_fedramp_docx(
    file_name: click.Path,
    base_fedramp_profile: click.STRING,
    save_data: click.BOOL,
    add_missing: click.BOOL,
):
    """
    [BETA] Convert a FedRAMP docx file to a RegScale SSP.
    """
    process_fedramp_docx(file_name, base_fedramp_profile, save_data, add_missing)


@fedramp.command()
@click.option(
    "--file_name",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
    required=True,
    prompt="Enter the file name of the FedRAMP JSON document to process.",
    help="RegScale will process and load the FedRAMP document.",
)
@click.option(
    "--submission_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    required=True,
    prompt="Enter the submission date of this FedRAMP document.",
    help=f"Submission date, default is today: {date.today()}.",
)
@click.option(
    "--expiration_date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str((datetime.now() + relativedelta(years=3)).date()),
    required=True,
    prompt="Enter the expiration date of this FedRAMP document.",
    help=f"Expiration date, default is {str((datetime.now() + relativedelta(years=3)).date())}.",
)
def load_fedramp_oscal(file_name, submission_date, expiration_date):
    """
    [BETA] Convert a FedRAMP OSCAL SSP json file to a RegScale SSP.
    """
    if not expiration_date:
        today_dt = date.today()
        expiration_date = date(today_dt.year + 3, today_dt.month, today_dt.day)

    process_fedramp_oscal_ssp(file_name, submission_date, expiration_date)


@fedramp.command()
@click.option(
    "--file-path",
    "-f",
    type=click.Path(exists=True),
    help="File to upload to RegScale.",
    required=True,
)
@click.option(
    "--catalogue_id",
    "-c",
    type=click.INT,
    help="The RegScale ID # of the catalogue to use for controls in the profile.",
    required=True,
)
def import_fedramp_ssp_xml_rev4(file_path: click.Path, catalogue_id: click.INT):
    """
    [BETA] Import FedRAMP Revision 4 SSP XML into RegScale
    """

    logger.info(event_msg="Importing FedRAMP Revision 4 SSP XML into RegScale")
    parse_and_load_xml_rev4(file_path, catalogue_id)


def decode_access_level(key: str) -> str:
    """
    Decodes the access level from the FedRAMP document
    :param str key: Key used to decode the access level
    :return: Access level as a string
    :rtype: str
    """
    access_levels = {
        "P": "Privileged",
        "NP": "Non-Privileged",
        "NLA": "No Logical Access",
    }
    return access_levels.get(key, "Unknown")


def create_responsible_roles(app: Application, table_data: list, ssp_id: int) -> None:
    """
    [BETA] Inserts the actual the Responsible Roles into the Security Plan.
    :param Application app: Application object
    :param list table_data: list of dicts
    :param int ssp_id: RegScale SSP ID
    :return: None
    """
    na_text = "Not Applicable"
    roles = [
        table
        for table in table_data
        if "Role" in table.keys() and "Internal or External" in table.keys()
    ]
    logger.info(
        event_msg=f"Found {len(roles)} Responsible Roles",
        record_type="role",
        model_layer="system-roles",
    )
    for role in roles:
        try:
            user_id = app.config.get("userId")
            access_level = decode_access_level(
                role.get(
                    "Privileged (P), Non-Privileged (NP), or No Logical Access (NLA)",
                    "Unknown",
                )
            )
            SystemRoles.get_or_create(
                app=app,
                role_name=role.get("Role"),
                ssp_id=ssp_id,
                roleType=role.get("Internal or External", "Internal"),
                accessLevel=access_level,
                sensitivityLevel=role.get("Sensitivity Level", na_text),
                assignedUserId=user_id,
                privilegeDescription=role.get("Authorized Privileges", na_text),
                securityPlanId=ssp_id,
                functions=[role.get("Functions Performed")],
                createdById=user_id,
            )
        except Exception as e:
            logger.error(
                f"Failed to create Responsible Roles with error: {str(e)}",
                record_type="role",
                model_layer="system-roles",
            )
    logger.info(
        "Successfully Created Responsible Roles",
        record_type="role",
        model_layer="system-roles",
    )


def post_responsible_roles(app: Application, table_data: list, ssp_id: int) -> dict:
    """
    [BETA] Insert the Responsible Roles into the Security Plan.
    :param Application app: Application object
    :param list table_data: list of dicts
    :param int ssp_id: RegScale SSP ID
    :return: dict of the control to role mappings
    :rtype: dict
    """
    data = [
        table for table in table_data if "Control Summary Information" in table.keys()
    ]
    system_roles = list()

    unique_values = set(system_roles)
    ctrl_roles = dict()
    for obj in data:
        try:
            control = (
                list(obj.keys())[0] if isinstance(obj, dict) and obj.keys() else None
            )
            for value in obj.values():
                if type(value) is str and value.startswith("Responsible Role:"):
                    # Extract the roles from the line
                    role = value.split(":", 1)[1].strip()
                    # Split the roles by comma and strip whitespace
                    if role.lower() not in unique_values:
                        unique_values.add(role.lower())
                        system_roles.append(role)
                    system_role = SystemRoles.get_or_create(
                        app=app,
                        role_name=role,
                        ssp_id=ssp_id,
                        roleType="Internal",
                        accessLevel="Privileged",
                        sensitivityLevel="Not Applicable",
                        assignedUserId=app.config.get("userId"),
                        privilegeDescription=role,
                        securityPlanId=ssp_id,
                        functions=[role],
                        createdById=app.config.get("userId"),
                    )
                    if isinstance(system_role, SystemRoles):
                        system_role = system_role.dict()
                    if control:
                        friendly_control_id = get_friendly_control_id(control)
                        if control in ctrl_roles.keys():
                            ctrl_roles[friendly_control_id].append(system_role["id"])
                        else:
                            ctrl_roles[friendly_control_id] = (
                                [system_role["id"]] if system_role else []
                            )
        except Exception as e:
            logger.error(
                f"Failed to create Responsible Roles with error: {str(e)}",
                record_type="role",
                model_layer="system-roles",
            )
    return ctrl_roles


def process_fedramp_oscal_ssp(
    file_path: click.Path, submission_date: date, expiration_date: date
) -> None:
    """
    OSCAL FedRAMP to RegScale SSP
    :param click.Path file_path: A click file path object to the oscal file
    :param date submission_date: The Submission date YYYY-MM-DD
    :param date expiration_date: The Expiration date YYYY-MM-DD
    :raises: FileNotFoundError if provided file doesn't exist
    :raises: JSONDecodeError if unable to read the JSON file
    :return: None
    """
    app = Application()
    api = Api(app)
    config = app.config
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            ssp_dict = json.load(file)
    except FileNotFoundError:
        error_and_exit(f"File not found!\n{file_path}")
    except json.JSONDecodeError as jex:
        logger.error(
            "JSONDecodeError, something is wrong with the file: %s\n%s", file_path, jex
        )

    # Create SSP
    create_ssp(api, config, ssp_dict, submission_date, expiration_date)


def check_profile(api: Api, config: dict, title: str) -> list:
    """
    Check if the profile exists in RegScale
    :param Api api: The api instance
    :param dict config: The application configuration
    :param str title: The title of the profile in question
    :raises: ValueError if the provided title doesn't exist in RegScale
    :return: List of filtered profiles
    :rtype: list
    """
    profiles_response = api.get(config["domain"] + "/api/profiles/getList")
    if profiles_response.ok:
        profiles = profiles_response.json()
    filtered = [dat for dat in profiles if dat["name"] == title]
    if not filtered:
        raise ValueError(
            f"The profile {title} does not exist in RegScale, \
                please create it and re-run this task."
        )
    return filtered[0]["id"]


def create_port(api: Api, config: dict, dat: PortsProtocols) -> None:
    """Create a port and protocol for a component

    :param Api api: An api instance
    :param dict config: Configuration
    :param PortsProtocols dat: Port and protocol data
    :param dict headers: headers for api call
    :return: None
    """

    existing_ports = api.get(
        url=config["domain"]
        + f"/api/portsProtocols/getAllByParent/{dat.parentId}/components",
    ).json()
    if dat not in [PortsProtocols.from_dict(port) for port in existing_ports]:
        # Check if obj exists
        port_res = api.post(
            url=config["domain"] + "/api/portsProtocols",
            data=json.dumps(dat.__dict__),
        )
        if port_res.status_code == 200:
            logger.info("Port and Protocol for component %i added!", dat.parentId)
        else:
            logger.warning(
                "Unable to post Port and Protocol: %s.",
                json.dumps(dat),
            )


def create_ssp_components(
    api: Api, config: dict, components: dict, ssp_id: int
) -> None:
    """
    Creates SSP Components
    :param Api api: The API instance
    :param dict config: The application's configuration
    :param dict components: The components
    :param int ssp_id: The ID of the SSP in RegScale
    :return: None
    """
    component_types = [
        "hardware",
        "software",
        "policy",
        "service",
        "process",
        "procedure",
        "compliance artifact",
    ]
    ports = set()
    for component in components:
        comp_type = (
            component["type"]
            if component["type"].lower() in component_types
            else "compliance artifact"
        )
        status = "Inactive/Retired"
        if component["status"]["state"] == "operational":
            status = "Active"

        comp = Component(
            title=component["title"],
            securityPlansId=ssp_id,
            componentType=comp_type,
            lastUpdatedById=config["userId"],
            createdById=config["userId"],
            cmmcExclusion=False,
            componentOwnerId=config["userId"],
            description=component["description"],
            status=status,
        )

        # save component
        cmp_id = None
        url = urljoin(config["domain"], "/api/components")
        cmp_response = api.post(
            url=url,
            json=comp.dict(),
        )
        if cmp_response.ok:
            cmp = cmp_response.json()
            cmp_id = cmp["id"]
            logger.info(
                "Successfully posted new component# %i as %s for ssp# %i.",
                cmp_id,
                cmp["title"],
                ssp_id,
            )
        if cmp_id and "protocols" in component.keys():
            for protocol in component["protocols"]:
                ports_protocols = PortsProtocols(
                    service="",
                    usedBy="",
                    parentId=cmp_id,
                    purpose=component["type"],
                    startPort=int(protocol["port-ranges"][0]["start"]),
                    endPort=int(protocol["port-ranges"][0]["end"]),
                    protocol=protocol["name"],
                    parentModule="components",
                    lastUpdatedById=config["userId"],
                    createdById=config["userId"],
                )
                ports.add(ports_protocols)

        if component["type"].lower() == "interconnection" and cmp_id:
            # Create ports and protocols object
            ports_protocols = PortsProtocols(
                service="",
                usedBy="",
                parentId=cmp_id,
                purpose=component["type"],
                startPort=0,
                endPort=0,
                protocol="",
                parentModule="components",
                lastUpdatedById=config["userId"],
                createdById=config["userId"],
            )
            ports_protocols.parentId = cmp_id
            ports_protocols.purpose = component["type"]
            # loop through properties to find port number
            if "props" in component.keys():
                for prop in component["props"]:
                    if prop["name"] == "information":
                        ports_protocols.purpose = prop["value"]
                    if prop["name"] == "port":
                        ports_protocols.startPort = int(prop["value"])
                        ports_protocols.endPort = int(prop["value"])
            ports.add(ports_protocols)
        create_component_mapping(api, config, ssp_id, cmp_id)
    if ports:
        for dat in ports:
            create_port(api, config, dat)


def create_component_mapping(api: Api, config: dict, ssp_id: int, cmp_id: int) -> None:
    """
    Create Component Mapping
    :param Api api: The api instance.
    :param dict config: The application configuration.
    :param int ssp_id: The SSP ID.
    :param int cmp_id: The component ID.
    :param dict headers: A dict of headers for requests.
    :return: None
    """
    mapping = {
        "securityPlanId": ssp_id,
        "componentId": cmp_id,
        "isPublic": True,
        "createdById": config["userId"],
        "lastUpdatedById": config["userId"],
    }
    mapping_response = api.post(
        url=config["domain"] + "/api/componentmapping",
        data=json.dumps(mapping),
    )
    if mapping_response.status_code != 200:
        logger.warning("Unable to post Mapping Response: %s.", mapping)


def create_ssp_stakeholders(
    api: Api, config: dict, ssp_id: int, ssp_dict: dict
) -> None:
    """
    Create Stakeholders in RegScale
    :param Api api: The api instance.
    :param dict config: The application configuration.
    :param int ssp_id: The SSP ID.
    :param dict ssp_dict: An SSP Dictionary.
    :return: None
    """
    parties = ssp_dict["system-security-plan"]["metadata"]["parties"]
    filtered_parties = list(filter(lambda x: x["type"] == "person", parties))
    for party in filtered_parties:
        title = [dat["value"] for dat in party["props"] if dat["name"] == "job-title"]
        phone = [dat["number"] for dat in party["telephone-numbers"]]
        email = list(party["email-addresses"])
        addresses = list(party["addresses"]) if "addresses" in party.keys() else None
        stakeholder = {
            "name": party["name"],
            "title": title[0] if title else "",
            "phone": phone[0] if phone else "",
            "email": email[0] if email else "",
            "address": addresses[0]["addr-lines"][0]
            + " "
            + addresses[0]["city"]
            + " "
            + addresses[0]["state"]
            + ", "
            + addresses[0]["postal-code"]
            if addresses
            else "",
            "otherID": party["uuid"],
            "notes": email[0] if email else "",
            "parentId": ssp_id,
            "parentModule": "securityplans",
        }
        post_stakeholder(api, config, stakeholder)


def post_stakeholder(api: Api, config: dict, stakeholder: dict) -> Optional[Dict]:
    """Post Stakeholders to RegScale

    :param Api api: API instance
    :param dict config: An application configuration
    :param dict stakeholder: A stakeholder dictionary
    :return: None
    """
    response = api.post(
        url=urljoin(config["domain"], "/api/stakeholders"),
        json=stakeholder,
    )
    if response.ok:
        logger.info(
            f"Created Stakeholder {response.json()} ",
            record_type="stakeholder",
            model_layer="stakeholder",
        )
        return response.json()
    else:
        logger.warning(
            f"Unable to create stakeholder: {stakeholder}",
            record_type="stakeholder",
            model_layer="stakeholder",
        )
        return None


def create_ssp_control_implementations(
    api: Api,
    config: dict,
    ssp_id: int,
    controls: dict,
    ssp_dict: dict,
) -> None:
    """
    Create the control implementations from the oscal SSP object
    :param Api api: The api instance.
    :param dict config: The application configuration.
    :param int ssp_id: The SSP ID.
    :param dict controls: A dict of existing controls in RegScale.
    :param dict ssp_dict: An SSP Dictionary.
    :return: None
    """
    if not controls:
        return
    control_implementations = ssp_dict["system-security-plan"][
        "control-implementation"
    ]["implemented-requirements"]

    for implementation in control_implementations:
        status = ControlImplementationStatus.NotImplemented

        for prop in implementation["props"]:
            if prop["name"] == "implementation-status":
                status = capitalize_words(prop["value"].replace("-", " "))
                if prop["value"].lower() == "implemented":
                    status = ControlImplementationStatus.FullyImplemented
                if prop["value"].lower() == "partial":
                    status = ControlImplementationStatus.PartiallyImplemented

        control_id = [
            control["controlID"]
            for control in controls
            if control["controlId"].lower() == implementation["control-id"].lower()
        ][0]
        imp = ControlImplementation(
            parentId=ssp_id,
            parentModule="securityplans",
            controlID=control_id,
            controlOwnerId=config["userId"],
            lastUpdatedById=config["userId"],
            createdById=config["userId"],
            status=status,
        )
        # Post Implementation
        response = post_regscale_object(api=api, config=config, obj=imp)
        imp_id = None
        if not response.raise_for_status and response.status_code == 200:
            imp_id = response.json()["id"]
        if imp_id:
            # TODO: Add statements
            pass


def post_regscale_object(
    api: Api, config: dict, obj: Any, endpoint="controlimplementation"
) -> requests.Response:
    """
    Post RegScale control implementation
    :param Api api: API instance
    :param dict config: Application config
    :param Any obj: data object
    :param str endpoint: Endpoint to use in RegScale
    :raises: General error if unable to post object to RegScale
    :return: Response from API call to RegScale
    :rtype: requests.Response
    """
    response = None
    try:
        response = api.post(
            config["domain"] + f"/api/{endpoint}",
            data=json.dumps(obj)
            if isinstance(obj, dict)
            else json.dumps(dataclasses.asdict(obj)),
        )
    except Exception as ex:
        logger.error("Unable to Post %s: %s to RegScale.\n%s", endpoint, obj, ex)

    return response


def create_ssp(
    api: Api, config: dict, ssp_dict: dict, submission_date: date, expiration_date: date
) -> int:
    """
    Create a basic SSP in RegScale
    :param Api api: The api instance.
    :param dict config: The application configuration.
    :param dict ssp_dict: An SSP Dictionary.
    :param date submission_date: The Submission date YYYY-MM-DD
    :param date expiration_date: The Expiration date YYYY-MM-DD
    :return: A newly created RegScale security plan id.
    :rtype: int
    """
    existing_ssps = []
    metadata = ssp_dict["system-security-plan"]["metadata"]
    system = ssp_dict["system-security-plan"]["system-characteristics"]
    fedramp_profile = get_profile(
        ssp_dict["system-security-plan"]["import-profile"]["href"]
    )["profile"]
    profile_id = check_profile(api, config, fedramp_profile["metadata"]["title"])
    components = ssp_dict["system-security-plan"]["system-implementation"]["components"]
    ssp_payload = {
        "uuid": ssp_dict["system-security-plan"]["uuid"],
        "systemName": system.get("system-name", None),  # Required
        "planInformationSystemSecurityOfficerId": config["userId"],
        "planAuthorizingOfficialId": config["userId"],
        "systemOwnerId": config["userId"],
        "otherIdentifier": system["system-ids"][0]["id"],
        "confidentiality": capitalize_words(
            system["system-information"]["information-types"][0][
                "confidentiality-impact"
            ]["selected"].split("-")[2]
        ),  # Required
        "integrity": capitalize_words(
            system["system-information"]["information-types"][0]["integrity-impact"][
                "selected"
            ].split("-")[2]
        ),  # Required
        "availability": capitalize_words(
            system["system-information"]["information-types"][0]["availability-impact"][
                "selected"
            ].split("-")[2]
        ),  # Required
        "status": capitalize_words(
            system["status"].get("state", "operational")
        ),  # Required
        "description": system.get("description", None),
        "dateSubmitted": submission_date.strftime(DATE_FORMAT),
        "approvalDate": (submission_date + relativedelta(years=1)).strftime(
            DATE_FORMAT
        ),  # User must be changed
        "expirationDate": expiration_date.strftime(DATE_FORMAT),
        "systemType": SYSTEM_TYPE,  # User must change
        "purpose": metadata.get("", None),
        "conditionsOfApproval": metadata.get("", None),
        "environment": metadata.get("", None),
        "lawsAndRegulations": metadata.get("", None),
        "authorizationBoundary": metadata.get("", None),
        "networkArchitecture": metadata.get("", None),
        "dataFlow": metadata.get("", None),
        "overallCategorization": capitalize_words(
            system["security-sensitivity-level"].split("-")[2]
        ),
        "maturityTier": metadata.get("", None),
        "createdById": config["userId"],
        "hva": False,
        "practiceLevel": metadata.get("", None),
        "processLevel": metadata.get("", None),
        "cmmcLevel": metadata.get("", None),
        "cmmcStatus": metadata.get("", None),
        "isPublic": True,
        "executiveSummary": metadata.get("", None),
        "recommendations": metadata.get("", None),
        "importProfile": metadata.get("version", "fedramp1.1.0-oscal1.0.0"),
        "parentId": profile_id,
        "parentModule": "profiles",
    }
    logger.warning("Unknown System Type, defaulting to %s.", ssp_payload["systemType"])
    logger.warning("Unknown HVA status, defaulting to %r.", ssp_payload["hva"])

    existing_ssp_response = api.get(
        url=urljoin(config["domain"], "/api/securityplans/getList")
    )
    if existing_ssp_response.ok:
        existing_ssps = existing_ssp_response.json()

    if system["system-name"] in {ssp["systemName"] for ssp in existing_ssps}:
        dat = {
            ssp["id"]
            for ssp in existing_ssps
            if ssp["systemName"] == system["system-name"]
        }
        click.confirm(
            f"This SSP Title already exists in the system, \
                SSP: {dat.pop() if len(dat) < 2 else dat}.  Would you still like to continue?",
            abort=True,
        )

    response = api.post(
        url=urljoin(config["domain"], "/api/securityplans"), json=ssp_payload
    )
    if response.ok:
        logger.info("SSP Created with an id of %i!", response.json()["id"])
        ssp_id = response.json()["id"]
    controls = []
    controls_response = api.get(
        urljoin(config["domain"], f"/api/profilemapping/getByProfile/{profile_id}")
    )
    if controls_response.ok:
        controls = controls_response.json()
    create_ssp_components(api, config, components, ssp_id)
    create_ssp_control_implementations(api, config, ssp_id, controls, ssp_dict)
    create_ssp_stakeholders(api, config, ssp_id, ssp_dict)
    # update_ssp_contacts(api, config, ssp_id, ssp_dict)

    return ssp_id


def get_profile(url: str) -> dict:
    """
    Downloads the FedRAMP profile
    :param str url: A profile URL.
    :return: A dictionary with the profile json data.
    :rtype: dict
    """
    dl_path = download_file(url)
    with open(dl_path, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def get_tables(document) -> list:
    """
    Return all document tables
    :param document: document object
    :return: List of all document tables
    :rtype: list
    """
    tables = list(document.tables)
    for t_table in document.tables:
        for row in t_table.rows:
            for cell in row.cells:
                tables.extend(iter(cell.tables))
    return tables


# TODO - replace these dangerous default mutables or document why they are used
def get_xpath_data_detailed(
    tables: Table, key: str, ident: str, xpath: str, count_array: list = [2, 3, 4]
) -> dict:
    """
    Use Xpath to pull data from XML tables.
    :param Table tables: XML tables
    :param str key: specific key in XML table
    :param str ident:
    :param str xpath: xpath of the element
    :param list count_array: array of numbers, default is [2, 3, 4]
    :return: Dictionary of items found
    :rtype: dict
    """
    tables = iter(tables)
    confidentiality = None
    integrity = None
    availability = None
    for t_var in tables:
        if key in t_var._element.xml:
            f = StringIO(t_var._element.xml)
            tree = etree.parse(f)
            tags = tree.xpath(xpath, namespaces=namespaces)
            for p_var in tags:
                t_tags = p_var.xpath("//w:r/w:t", namespaces=namespaces)
                count = 0
                for t_var in t_tags:
                    if t_var.text == ident or count > 0:
                        count += 1
                        if count == count_array[0]:
                            confidentiality = t_var.text
                        if count == count_array[1]:
                            integrity = t_var.text
                        if count == count_array[2]:
                            availability = t_var.text
    return {
        "type": key,
        "nist_ident": ident,
        "confidentiality": confidentiality,
        "integrity": integrity,
        "availability": availability,
    }


def get_contact_info(tables, key: str, xpath: str) -> dict:
    """
    Use Xpath to pull data from XML tables
    :param tables: XML tables
    :param str key: key to look for
    :param str xpath: xpath of the element
    :raises: IndexError if an index error is encountered during iteration
    :return: Dictionary of sorted data
    :rtype: dict
    """
    idents = [
        "Name",
        "Title",
        "Company / Organization",
        "Address",
        "Phone Number",
        "Email Address",
    ]
    dat = {}

    def loop_and_update(element_list) -> dict:
        """
        Loop through the element list and update the data dictionary
        :param element_list:
        :return: Updated dictionary
        :rtype: dict
        """
        value = ""
        if idents:
            count = 0
            field = idents.pop(0)

            while count < len(element_list) - 1:
                if element_list[count].text == field:
                    value = "".join([value, element_list[count + 1].text])
                    dat[field] = value
                    value = ""
                    count += 1
                try:
                    if element_list[count + 1].text in idents:
                        field = idents.pop(0)
                    else:
                        if field in dat:
                            dat[field] = "".join(
                                [dat[field], element_list[count + 1].text]
                            )
                        count += 1
                except IndexError:
                    logger.debug("Unable to continue, index error on row: %i.", count)

    tables = iter(tables)

    tag_data = []
    for _, t_enum in enumerate(tables):
        if key in t_enum._element.xml:
            f_var = StringIO(t_enum._element.xml)
            tree = etree.parse(f_var)
            tags = tree.xpath(xpath, namespaces=namespaces)
            for tag in tags:
                p_tags = tag.xpath("//w:p", namespaces=namespaces)
                for p_var in p_tags:
                    t_tags = p_var.xpath("//w:r/w:t", namespaces=namespaces)
                    for tags in t_tags:
                        tag_data.append(tags)
    loop_and_update(tag_data)

    return dat


def get_base_contact(ssp, key: Optional[str] = "Point of Contact") -> dict:
    """
    Gets contact information
    :param ssp: SSP file
    :param str key: key to parse for, defaults to 'Point of Contact'
    :return: dictionary with contact information
    :rtype: dict
    """
    result = {}
    name = None
    title = None
    company = None
    address = None
    phone = None
    email = None
    for table in ssp.document.tables:
        for i, row in enumerate(table.rows):
            text = (cell.text.strip() for cell in row.cells)
            if i == 0:
                keys = tuple(text)
                if not title:
                    dat = [x.strip() for x in keys if x].pop().split("\n")
                    title = dat[1] if len(dat) > 1 else dat[0]
                continue
            if key == keys[0]:
                # Use python-docx to get the embedded xml text.
                for i, cell in enumerate(table._cells):
                    if i == 3:
                        name = cell.text
                        result["name"] = name
                    if i == 5:
                        title = cell.text
                        result["title"] = title
                    if i == 7:
                        company = cell.text
                        result["company"] = company
                    if i == 9:
                        address = cell.text
                        result["address"] = address
                    if i == 11:
                        phone = cell.text
                        result["phone"] = phone
                    if i == 13:
                        email = cell.text
                        result["email"] = email
                return result


def post_interconnects(app: Application, table_data: list, regscale_ssp: dict) -> None:
    """
    Interconnects map to SSP in RegScale
    :param Application app: Application object
    :param table_data: List of tables
    :param SecurityPlan regscale_ssp: SecurityPlan object
    :return: None
    """
    # TODO: Update ssp_id to pull the full ssp object down.
    api = Api(app)
    user_id = app.config["userId"]
    user = get_user(api=api, user_id=user_id)
    if len(user) == 0:
        user = {"firstName": user_id, "lastName": "userId: "}
    key = "SP* IP Address and Interface"
    existing_interconnects = []
    dat = [table for table in table_data if key in table.keys()]
    existing_interconnect_response = api.get(
        app.config["domain"]
        + f"/api/interconnections/getAllByParent/{regscale_ssp['id']}/securityplans"
    )
    if not existing_interconnect_response.raise_for_status() and (
        existing_interconnect_response.headers.get("content-type")
        == "application/json; charset=utf-8"
    ):
        existing_interconnects = existing_interconnect_response.json()
    for interconnect in dat:
        interconnection = Interconnects(
            name=interconnect[key],
            ao=f"{user['lastName']}, {user['firstName']}",
            aOId=user_id,
            interconnectOwner="Eaton, Bryan",
            interconnectOwnerId=user_id,
            dateCreated=get_current_datetime(),
            dateLastUpdated=get_current_datetime(),
            lastUpdatedById=user_id,
            createdBy=f"{user['lastName']}, {user['firstName']}",
            createdById=user_id,
            description=interconnect["Information Being Transmitted"]
            if "Information Being Transmitted" in interconnect.keys()
            else "",
            parentId=regscale_ssp["id"],
            parentModule="securityplans",
            agreementDate=get_current_datetime(),
            expirationDate=(datetime.now() + relativedelta(years=3)).strftime(
                DATE_FORMAT
            ),
            status="Approved",
            organization=regscale_ssp["systemName"],
            categorization=regscale_ssp["overallCategorization"],
            connectionType="Web Service or API",
            authorizationType="Interconnect Security Agreement (ISA)",
        )
        if interconnection.name + interconnection.description not in {
            inter["name"] + inter["description"] for inter in existing_interconnects
        }:
            post_regscale_object(
                api=api,
                config=app.config,
                obj=interconnection.dict(),
                endpoint="interconnections",
            )


def post_ports(app: Application, table_data: list, ssp_id: int) -> None:
    """
    Ports map to interconnects
    :param Application app: Application object
    :param list table_data: list of tables
    :param int ssp_id: RegScale SSP ID
    :return: None
    """
    api = Api(app)
    key = "Ports (TCP/UDP)*"
    dat = [table for table in table_data if "Protocols" in table.keys()]
    existing_ports = []
    existing_ports_response = api.get(
        app.config["domain"]
        + f"/api/portsProtocols/getAllByParent/{ssp_id}/securityplans"
    )
    if not existing_ports_response.raise_for_status() and (
        existing_ports_response.headers.get("content-type")
        == "application/json; charset=utf-8"
    ):
        existing_ports = existing_ports_response.json()

    for protocol in dat:
        ports_protocols = PortsProtocols(
            service=protocol["Services"],
            usedBy=protocol["Used By"],
            parentId=ssp_id,
            purpose=protocol["Purpose"],
            startPort="".join(c for c in protocol[key] if c.isdigit())
            or "".join(c for c in protocol["Protocols"] if c.isdigit()),
            endPort="".join(c for c in protocol[key] if c.isdigit())
            or "".join(c for c in protocol["Protocols"] if c.isdigit()),
            protocol="".join(c for c in protocol[key] if not c.isdigit())
            or "".join(c for c in protocol["Protocols"] if c.isdigit()),
            parentModule="securityplans",
            lastUpdatedById=app.config["userId"],
            createdById=app.config["userId"],
        )
        ports_protocols.protocol = (
            ports_protocols.protocol.strip().replace("(", "").replace(")", "")
        )
        if ports_protocols not in {
            PortsProtocols.from_dict(port) for port in existing_ports
        }:  # Hashable class
            post_regscale_object(
                api, app.config, ports_protocols.dict(), endpoint="portsProtocols"
            )


def get_current_implementations(app: Application, regscale_id: int) -> list[dict]:
    """Pull current implementations for a given regscale id
    :param Application app: Application instance
    :param int regscale_id: RegScale ID
    :return: List of dictionaries
    """
    current_imps = []
    api = Api(app)
    try:
        current_imps_response = api.get(
            url=app.config["domain"]
            + f"/api/controlImplementation/getAllByPlan/{regscale_id}",
            params=({"skip_check": True}),
        )
        if not current_imps_response.raise_for_status():
            current_imps = current_imps_response.json()
    except requests.HTTPError:  # This endpoint returns 404 when empty.
        current_imps = []
    return current_imps


def get_friendly_control_id(control_number: str) -> str:
    """Get friendly control id from control number
    :param str control_number: Control number
    :return: Friendly control id
    :rtype: str
    """
    # exp = r"^.*?\([^\d]*(\d+)[^\d]*\).*$"
    # the above regex allows for a denial of service attack
    # the below regex should mitigate that
    exp = r"\((\d+)\)"
    friendly_control_id = control_number.lower()
    if match := re.search(exp, control_number):
        friendly_control_id = f"{control_number[:match.regs[1][0] - 1].strip()}.{match.groups()[0]}".lower()
    return friendly_control_id


def post_implementations(
    app: Application,
    ssp_obj: dict,
    regscale_ssp: dict,
    mapping: dict,
    ctrl_roles: dict,
    save_data: bool = False,
    load_missing: bool = False,
) -> int:
    """
    Post implementations to RegScale
    :param Application app: Application object
    :param dict ssp_obj: SecurityPlan object (python-docx)
    :param dict regscale_ssp: RegScale ssp
    :param dict mapping: mapping
    :param dict ctrl_roles: Control roles
    :param bool save_data: Whether to save data to a file
    :raises ValueError: If there are more controls in the source document than in the base profile
    :return: int count of new implementations
    """
    api = Api(app)
    current_imps = get_current_implementations(app, regscale_ssp["id"])
    check_control_list_length(ssp_obj, mapping)
    log_controls_info(ssp_obj, current_imps)

    (
        mapped_controls_log,
        unmapped_controls_log,
        implemented_controls_log,
        new_implementations,
    ) = process_controls(
        app, api, ssp_obj, regscale_ssp, mapping, ctrl_roles, current_imps
    )

    if load_missing:
        load_non_matched_profile_controls(
            app, regscale_ssp=regscale_ssp, mapping=mapping
        )

    if save_data:
        save_control_logs(
            mapped_controls_log, unmapped_controls_log, implemented_controls_log
        )
    return new_implementations


def get_responsibility_and_status(fedramp_control: any) -> Tuple[str, str]:
    """
    Get responsibility and implementation status
    :param FedrampControl fedramp_control: FedrampControl object
    :return: Tuple of responsibility and implementation status
    """
    responsibility = None
    if fedramp_control.control_origination:
        if "Shared".lower() in fedramp_control.control_origination[0].lower():
            responsibility = "Shared"
        elif "Customer".lower() in fedramp_control.control_origination[0].lower():
            responsibility = "Customer"
        elif "Provider".lower() in fedramp_control.control_origination[0].lower():
            responsibility = "Provider"
        else:
            responsibility = fedramp_control.control_origination[0]

    if fedramp_control.implementation_status and fedramp_control.implementation_status[
        0
    ] in ["Alternative Implementation", "Implemented"]:
        implementation_status = "Fully Implemented"
    elif "Partially Implemented" in fedramp_control.implementation_status:
        implementation_status = "Partially Implemented"
    else:
        implementation_status = (
            fedramp_control.implementation_status[0]
            if fedramp_control.implementation_status
            else "Not Implemented"
        )

    return responsibility, implementation_status


def find_control_in_mapping(mapping: Dict, friendly_control_id: str) -> str:
    """
    Find control id in mapping
    :param dict mapping: Mapping
    :param str friendly_control_id: Friendly control id
    :return: ControlId
    :rtype: str
    """
    control_id = None
    if control := [
        control
        for control in mapping
        if control["controlId"].lower() == friendly_control_id
    ]:
        control_id = control[0]["controlID"]
    return control_id


def get_implementation_text(fedramp_control: any) -> str:
    """
    Get implementation text
    :param FedrampControl fedramp_control: FedrampControl object
    :return: Implementation text
    :rtype: str
    """
    if len(fedramp_control.parts) > 1:
        return "<br>".join(fedramp_control.part(x).text for x in fedramp_control.parts)
    else:
        try:
            return fedramp_control.part(None).text
        except IndexError:
            return ""


def handle_control_implementation(
    app: Application,
    api: Api,
    regscale_ssp: Dict,
    control_id: str,
    responsibility: str,
    implementation_status: str,
    implementation_text: str,
    ctrl_roles: Dict,
    friendly_control_id: str,
    new_implementations: list,
    current_imps: list,
) -> Optional[Response]:
    """
    :param Application app: Application instance
    :param Api api: API instance
    :param dict regscale_ssp: RegScale ssp
    :param str control_id: Control id
    :param str responsibility: Responsibility
    :param str implementation_status: Implementation status
    :param str implementation_text: Implementation text
    :param dict ctrl_roles: Control roles
    :param str friendly_control_id: Friendly control id
    :param list new_implementations: List of new implementations
    :param list current_imps: List of current implementations
    :return: Response object
    :rtype: Optional[Response]
    :raises ValueError: If there are more controls in the source document than in the base profile
    """
    imp_response = None
    implementation = ControlImplementation(
        parentId=regscale_ssp["id"],
        parentModule="securityplans",
        controlOwnerId=app.config["userId"],
        status=implementation_status,
        controlID=control_id,
        responsibility=responsibility,
        implementation=implementation_text,
        systemRoleId=ctrl_roles.get(friendly_control_id)[0]
        if isinstance(ctrl_roles, dict) and friendly_control_id in ctrl_roles.keys()
        else None,
    )

    imp_filter = control_id not in {
        imp["controlID"] for imp in new_implementations
    } and control_id not in {imp["controlID"] for imp in current_imps}
    if imp_filter:
        imp_response = post_regscale_object(api, app.config, implementation.dict())
        if imp_response.ok:
            new_implementations.append(imp_response.json())

    return imp_response


def handle_requirements(
    app: Application,
    api: Api,
    fedramp_control: any,
    mapping: dict,
    friendly_control_id: str,
    implementation_status: str,
    regscale_ssp: Dict,
) -> None:
    """
    :param Application app: Application instance
    :param Api api: API instance
    :param FedrampControl fedramp_control: FedrampControl object
    :param dict mapping: Mapping
    :param str friendly_control_id: Friendly control id
    :param str implementation_status: Implementation status
    :param dict regscale_ssp: RegScale ssp
    :return None:
    :rtype None:
    :raises ValueError: If there are more controls in the source document than in the base profile
    """
    parent_security_control_id = [
        control["controlID"]
        for control in mapping
        if control["controlId"] == friendly_control_id.split()[0]
    ][0]
    current_imps = get_current_implementations(app=app, regscale_id=regscale_ssp["id"])
    parent_security_control = [
        imp for imp in current_imps if imp["controlID"] == parent_security_control_id
    ][0]

    for part in fedramp_control.parts:
        implementation_text = fedramp_control.part(part).text
        title = f"{friendly_control_id.split()[0]} - Req. {part}"
        requirement = Requirement(
            id=0,
            description=implementation_text.split("\n")[0],
            implementation=implementation_text,
            title=title,
            lastUpdatedById=app.config["userId"],
            status=implementation_status,
            controlID=parent_security_control_id,
            parentId=parent_security_control["id"],
            parentModule="controls",
            requirementOwnerId=app.config["userId"],
            createdById=app.config["userId"],
        )

        existing_requirement = api.get(
            url=app.config["domain"]
            + f"/api/requirements/getByParent/{parent_security_control['id']}/controls"
        ).json()

        if title not in {req["title"] for req in existing_requirement}:
            logger.info("Posting Requirement: %s", title)
            post_regscale_object(
                api=api,
                config=app.config,
                obj=requirement,
                endpoint="requirements",
            )
        else:
            logger.info("Requirement %s already exists, skipping...", title)


def handle_parameters(
    app: Application, api: Api, fedramp_control: any, imp_response: Optional[Response]
) -> None:
    """
    :param Application app: Application instance
    :param Api api: API instance
    :param FedrampControl fedramp_control: FedrampControl object
    :param Optional[Response] imp_response: Response object
    :return None:
    :rtype None:
    """
    for parameter in fedramp_control.parameters:
        try:
            param_dict = get_parameter_value(parameter)
            param = {
                "id": 0,
                "controlImplementationId": imp_response.json()["id"],
                "name": param_dict.get("name", ""),
                "dataType": "String",
                "value": param_dict.get("value", ""),
                "createdById": app.config["userId"],
                "lastUpdatedById": app.config["userId"],
                "externalPropertyName": None,
                "oscalNamespaceMapping": [],
            }
            post_regscale_object(api, app.config, param, "parameters")
        except Exception as e:
            logger.warning("Unable to map parameter %s to RegScale: %s", parameter, e)


def process_controls(
    app: Application,
    api: Api,
    ssp_obj: dict,
    regscale_ssp: dict,
    mapping: dict,
    ctrl_roles: dict,
    current_imps: List[dict],
) -> Tuple[List[str], List[str], List[str], int]:
    """
    :param Application app: Application instance
    :param Api api: API instance
    :param dict ssp_obj: SSP object
    :param dict regscale_ssp: RegScale ssp
    :param dict mapping: Mapping
    :param dict ctrl_roles: Control roles
    :param list current_imps: List of current implementations
    :return Tuple[List[str], List[str], List[str], int]:
        List of mapped controls
        List of unmapped controls
        List of implemented controls
        Number of new implementations
    """
    mapped_controls_log = []
    unmapped_controls_log = []
    implemented_controls_log = []
    new_implementations = []
    has_requirements = False

    for fedramp_control in ssp_obj.control_list:
        responsibility, implementation_status = get_responsibility_and_status(
            fedramp_control
        )
        friendly_control_id = get_friendly_control_id(fedramp_control.number)

        control_id = find_control_in_mapping(mapping, friendly_control_id)
        if not control_id:
            unmapped_controls_log.append(friendly_control_id.upper())
            continue

        implementation_text = get_implementation_text(fedramp_control)

        imp_response = handle_control_implementation(
            app,
            api,
            regscale_ssp,
            control_id,
            responsibility,
            implementation_status,
            implementation_text,
            ctrl_roles,
            friendly_control_id,
            new_implementations,
            current_imps,
        )

        if "Req" in fedramp_control.number:
            handle_requirements(
                app,
                api,
                fedramp_control,
                mapping,
                friendly_control_id,
                implementation_status,
                regscale_ssp,
            )
            has_requirements = True

        if imp_response:
            handle_parameters(app, api, fedramp_control, imp_response)

        if has_requirements:
            has_requirements = False  # Reset for the next control

    return (
        mapped_controls_log,
        unmapped_controls_log,
        implemented_controls_log,
        len(new_implementations),
    )


def check_control_list_length(ssp_obj: dict, mapping: dict) -> None:
    """
    :param dict ssp_obj: SSP object
    :param dict mapping: Mapping
    :return None:
    :rtype None:
    :raises ValueError: If there are more controls in the source document than in the base profile
    """
    if len(ssp_obj.control_list) > len(mapping):
        raise ValueError(
            "There are more controls in the source document than in the base profile!"
        )


def log_controls_info(ssp_obj: dict, current_imps: List[dict]) -> None:
    """
    :param dict ssp_obj: SSP object
    :param List[dict] current_imps: List of current implementations
    :return None:
    :rtype None:
    """
    logger.info(
        f"Attempting to post {len(ssp_obj.control_list)} controls from this FedRAMP SSP Document to RegScale!",
        record_type="control",
        model_layer="control-implementation",
    )
    if len(current_imps) > 0:
        logger.info(
            f"This RegScale Security plan already has {len(current_imps)} implementations..",
            record_type="control",
            model_layer="control-implementation",
        )


def save_control_logs(
    mapped_controls_log: List[str],
    unmapped_controls_log: List[str],
    implemented_controls_log: List[str],
) -> None:
    """
    :param List[str] mapped_controls_log: List of mapped controls
    :param List[str] unmapped_controls_log: List of unmapped controls
    :param List[str] implemented_controls_log: List of implemented controls
    :return None:
    :rtype None:
    """
    with open("artifacts/control_implementation.log", "w") as f:
        f.write("|*** Unmapped Controls ***|\n")
        f.write(NEW_LINE_OUTPUT)
        f.write("\n".join(unmapped_controls_log))
        f.write(NEW_LINE_OUTPUT)
        f.write("|*** Mapped Controls ***|\n")
        f.write(NEW_LINE_OUTPUT)
        f.write("\n".join(mapped_controls_log))
        f.write(NEW_LINE_OUTPUT)
        f.write("|*** Already Implemented Controls ***|\n")
        f.write(NEW_LINE_OUTPUT)
        f.write("\n".join(implemented_controls_log))
        f.write(NEW_LINE_OUTPUT)


def get_parameter_value(param: str) -> Dict:
    """
    Get the value of a Parameter
    :param str param: Parameter as a string
    :rtype: dict
    """
    param_dict = dict()
    if ":" in param:
        param_dict["name"] = param.split(":")[0]
        param_dict["value"] = (
            param.split(":")[1] if len(param.split(":")) > 1 else param
        )
    else:
        param_dict["name"] = param
        param_dict["value"] = param
    return param_dict


def load_non_matched_profile_controls(
    app: Application, regscale_ssp: dict, mapping: dict
) -> None:
    """Load controls from a given profile mapping that are not matched by the document

    :param Application app: Application instance
    :param dict regscale_ssp: RegScale SSP as a dictionary
    :param dict mapping: Profile mapping
    :rtype: None
    """
    api = Api(app)
    current_imps = get_current_implementations(app, regscale_ssp["id"])
    if ssp := [
        ssp
        for ssp in api.get(
            url=urljoin(app.config["domain"], "/api/securityplans/getList")
        ).json()
        if ssp["title"] == regscale_ssp["systemName"]
    ]:
        ssp_id = ssp[0]["id"]
        existing_controls = {imp["controlID"] for imp in current_imps}
        controls_to_add = [
            control
            for control in mapping
            if control["controlID"] not in existing_controls
        ]
        logger.info(
            f"Adding {len(controls_to_add)} additional controls from profile",
            record_type="control",
            model_layer="control-implementation",
        )
        existing_control_ids = {imp["controlID"] for imp in current_imps}
        for control in controls_to_add:
            if control["controlID"] not in existing_control_ids:
                implementation = ControlImplementation(
                    parentId=ssp_id,
                    parentModule="securityplans",
                    controlOwnerId=app.config["userId"],
                    status="Not Implemented",
                    controlID=control["controlID"],
                    responsibility=None,
                    implementation=None,
                ).dict()
                logger.info(
                    f"Posting implementation: {control['controlId']}.",
                    record_type="control",
                    model_layer="control-implementation",
                )
                post_regscale_object(api, app.config, implementation)


def post_attachments(api: Api, link: str, regscale_ssp: dict) -> None:
    """
        Download and post Attachments to RegScale
        :param Api api: API object
        :param str link: link to download file
    onary of RegScale SSP
        :raises: General error if unable to download file
        :return: None
    """
    try:
        dl_path = download_file(link["link"])
        logger.info(
            f"Posting linked image to RegScale.. {link}",
            record_type="attachments",
            model_layer="attachments",
        )
        File.upload_file_to_regscale(
            file_name=(dl_path.absolute()),
            parent_id=regscale_ssp["id"],
            parent_module="securityplans",
            api=api,
        )

    except Exception as ex:
        logger.warning(
            f"Unable to download file: {link}\n{ex}",
            record_type="attachments",
            model_layer="attachments",
        )


def posted_embedded_attachments(api: Api, ssp_obj: SSP, regscale_ssp: dict) -> None:
    """
    Find and post embedded picture files to RegScale
    :param Api api: API object
    :param SSP ssp_obj: SSP object
    :param dict regscale_ssp: RegScale SSP
    :return None:
    """
    filename = ssp_obj.source
    with zipfile.ZipFile(filename, mode="r") as archive:
        file_dump_path = gettempdir() + os.sep + "imagedump"
        for file in archive.filelist:
            if (
                file.filename.startswith("word/media/") and file.file_size > 200000
            ):  # 200KB filter
                archive.extract(file, path=file_dump_path)
        # Create directories in case they do not exist.
        media_path = file_dump_path + os.sep + "word" + os.sep + "media"
        if not os.path.exists(media_path):
            os.makedirs(media_path)
        for filename in os.listdir(file_dump_path + os.sep + "word" + os.sep + "media"):
            full_file_path = os.path.join(
                file_dump_path + os.sep + "word" + os.sep + "media", filename
            )
            if os.path.isfile(full_file_path):
                logger.info(
                    f"Posting embedded image to RegScale... {full_file_path}",
                    record_type="attachments",
                    model_layer="attachments",
                )
                File.upload_file_to_regscale(
                    file_name=full_file_path,
                    parent_id=regscale_ssp["id"],
                    parent_module="securityplans",
                    api=api,
                )


def post_links(
    config: dict, api: Api, ssp_obj: SSP, regscale_ssp: dict, post_embeds: bool = True
) -> None:
    """
    Use Xpath to pull data from XML tables'
    :param dict config: Application config
    :param Api api: Api object
    :param SSP ssp_obj: SSP object
    :param dict regscale_ssp: RegScale SSP
    :param bool post_embeds: Whether to post embedded items to RegScale
    :return: None
    """
    # Find and post attachments
    # TODO: Add issue for link titles to pull from XML table instead of hyperlink name.
    # TODO: Add table title to link information
    attachments = []
    titles = []
    if post_embeds:
        posted_embedded_attachments(api, ssp_obj, regscale_ssp)
    for table in ssp_obj.document.tables:
        if table._cells and "Identification Number" in table.cell(0, 0).text.strip():
            previous = None
            id_text = None
            title = None
            link_text = None
            link_date = None
            dat = {}
            for index, e_id in enumerate(
                table._element.xpath(".//w:r/w:t")
            ):  # Loop through every column + 1 record
                dat_text = e_id.text.strip()
                previous = "" if index == 0 else previous
                if dat_text:
                    if previous.lower() == "link":
                        id_text = dat_text
                        dat["id"] = id_text
                        link_text = None
                    elif id_text:
                        title = dat_text
                        id_text = None
                    elif validate_date_str(dat_text):
                        title = " ".join([title, previous]) if title else previous
                        dat["title"] = title.strip()
                        link_date = e_id.text.strip()
                        dat["date"] = link_date.strip()
                        title = None
                    elif "date" in dat:
                        link_text = e_id.text.strip()
                        dat["link"] = link_text
                        titles.append(dat)
                        previous = "link"
                        link_text = None
                    previous = e_id.text.strip() if len(dat) != 4 else "link"
                    if len(dat) == 4:
                        dat = {}
                    link_date = None
            titles.reverse()
            for link in table._element.xpath(".//w:hyperlink"):
                inner_run = link.xpath("w:r", namespaces=link.nsmap)[0]

                # matches = [tit['title'] for tit in titles if tit['link'] == inner_run.text]
                # if matches:\
                # TODO: Improve this.
                title = titles.pop()["title"] if titles else inner_run.text
                # print link relationship id
                r_id = link.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                )
                # print link URL
                attachments.append(
                    {"title": title, "link": ssp_obj.document._part.rels[r_id]._target}
                )
    # Post Links
    existing_links = api.get(
        config["domain"]
        + f"/api/links/getAllByParent/{regscale_ssp['id']}/securityplans"
    ).json()
    for reg_link in list({v["link"]: v for v in attachments}.values()):
        dat_text = {
            "id": 0,
            "url": reg_link["link"],
            "title": reg_link["title"],
            "parentID": regscale_ssp["id"],
            "parentModule": "securityplans",
        }
        if reg_link["link"] not in {link["url"] for link in existing_links}:
            post_regscale_object(api, config, dat_text, endpoint="links")
            post_attachments(api=api, link=reg_link, regscale_ssp=regscale_ssp)
        else:
            logger.info(
                f"{reg_link['link']} already exists in Security Plan, skipping..",
                record_type="links",
                model_layer="links",
            )


def validate_date_str(date_text, fmt="%m/%d/%Y") -> bool:
    """
    Validate provided text is a date in mm/dd/yyyy format
    :param str date_text: Date as a string
    :param str fmt: date format of the date_text, defaults to %m/%d/%Y
    :return: Whether provided text can be converted as a date
    :rtype: bool
    """
    try:
        datetime.strptime(date_text, fmt)
    except ValueError:
        return False
    return True


def get_text(document, full_text, start_header, start_text, end_text) -> str:
    """
    Parses text from a document
    :param document: Document to parse
    :param full_text: Full text of the document
    :param start_header: Starting header
    :param start_text: Where the text starts
    :param end_text: Where the text ends
    :return: String parsed from document
    :rtype: str
    """
    description_num = [
        i for i, j in enumerate(full_text) if j.lower() == start_header.lower()
    ].pop()
    description_text = []
    keep_going = True
    start_run = False
    while keep_going:
        for index, para in enumerate(document.paragraphs):
            if index > description_num:
                for run in para.runs:
                    if run.text.lower().strip() == start_text.lower().strip():
                        start_run = True
                        break
                    if start_run and run.text.strip() != end_text.strip():
                        description_text.append(run.text)
                    if run.text.lower().strip() == end_text.strip().lower():
                        start_run = False
                        keep_going = False
                        break
    return "".join(description_text)


def gather_stakeholders(tables, regscale_ssp, ssp):
    """Gather Stakeholders
    :param list tables: A list of tables from the XML document.
    :param dict regscale_ssp: A dict of RegScale SSP data.
    :param ssp: A dict of docx SSP data.
    """
    app = Application()
    api = Api(app)
    pocs = collect_points_of_contact(tables, ssp)
    existing_stakeholders = fetch_existing_stakeholders(api, app.config, regscale_ssp)
    logger.info(
        f"Found {len(existing_stakeholders)} existing stakeholders",
        record_type="stackholders",
        model_layer="stackholders",
    )
    filtered_pocs = filter_valid_pocs(pocs)

    insert_new_stakeholders(
        api, app.config, filtered_pocs, existing_stakeholders, regscale_ssp
    )


def collect_points_of_contact(tables, ssp) -> List:
    """Collect various points of contact.
    :param list tables: A list of tables from the XML document.
    :param dict ssp: A dict of docx SSP data.
    :return: A list of points of contact
    """
    pocs = list()
    pocs.append(extract_management_poc(tables, pocs))
    pocs.extend(extract_information_poc(tables, ssp))
    pocs.append(extract_csp_poc(tables, pocs))
    return pocs


def fetch_existing_stakeholders(api, config, regscale_ssp):
    """Fetch existing stakeholders from the API.
    :param Api api: An API instance
    :param dict config: A configuration dictionary
    :param dict regscale_ssp: A dict of RegScale SSP data.
    :return: A list of existing stakeholders
    """
    url = urljoin(
        config.get("domain"),
        f"/api/stakeholders/getAllByParent/{str(regscale_ssp.get('id'))}/securityplans",
    )
    response = api.get(url=url, headers={"Content-Type": "application/json"})
    if response.ok:
        logger.info(
            f"Found {len(response.json())} existing stakeholders",
            record_type="stackholders",
            model_layer="stackholders",
        )
        return response.json()
    return []


def filter_valid_pocs(pocs) -> list:
    """Filter out invalid (non-dict) points of contact.
    :param list pocs: A list of points of contact
    :return: A list of valid points of contact
    :rtype: list
    """
    return [poc for poc in pocs if isinstance(poc, dict)]


def insert_new_stakeholders(
    api, config, pocs, existing_stakeholders, regscale_ssp
) -> None:
    """Insert new stakeholders into the system.
    :param Api api: An API instance
    :param dict config: A configuration dictionary
    :param list pocs: A list of points of contact
    :param list existing_stakeholders: A list of existing stakeholders
    :param dict regscale_ssp: A dict of RegScale SSP data.
    :return: None
    """
    pocs_inserted = []
    for poc in pocs:
        stakeholder = create_stakeholder_dict(poc, regscale_ssp)
        if should_insert_stakeholder(poc, pocs_inserted, existing_stakeholders):
            post_stakeholder(api, config, stakeholder)
            pocs_inserted.append(stakeholder.get("name").strip())


def extract_management_poc(tables: list, pocs: list) -> Dict:
    """Extract Management POC.
    :param list tables: A list of tables from the XML document.
    :param dict pocs: A dict of points of contact
    :return: A dict of the Management POC
    :rtype: dict
    """
    return _extracted_from_gather_stakeholders(
        tables,
        "Owner Information",
        pocs,
        "Information System Management Point of Contact",
    )


def extract_information_poc(tables, ssp: Dict) -> List:
    """Extract Information POC.
    :param list tables: A list of tables from the XML document.
    :param dict ssp: A dict of docx SSP data.
    :return: A List of the Information POC
    :rtype: List
    """
    return [
        get_contact_info(
            tables,
            key="Information System Technical Point of Contact",
            xpath="//w:tbl/w:tr",
        ),
        get_base_contact(ssp),
    ]


def extract_csp_poc(tables: List, pocs: List) -> Dict:
    """Extract CSP POC.
    :param list tables: A list of tables from the XML document.
    :param list pocs: A list of points of contact
    :return: A dict of the CSP POC
    """
    return _extracted_from_gather_stakeholders(
        tables,
        "AO Point of Contact",
        pocs,
        "CSP Name Internal ISSO (or Equivalent) Point of Contact",
    )


def create_stakeholder_dict(poc, regscale_ssp):
    """Create a stakeholder dictionary.
    :param dict poc: A point of contact
    :param dict regscale_ssp: A dict of RegScale SSP data.
    :return: A stakeholder dictionary
    :rtype: dict
    """
    poc = {k.lower(): v for k, v in poc.items()}  # Make this case-insensitive.
    email = name = title = phone = ""
    if "email" in (keys := [key.lower() for key in poc.keys()]):
        email = poc[(_ := _check_if_string_in_list_of_string("email", keys)).lower()]
    if "name" in (keys := [key.lower() for key in poc.keys()]):
        name = poc[(_ := _check_if_string_in_list_of_string("name", keys)).lower()]
    if "title" in (keys := [key.lower() for key in poc.keys()]):
        name = poc[(_ := _check_if_string_in_list_of_string("title", keys)).lower()]
    if "phone" in (keys := [key.lower() for key in poc.keys()]):
        name = poc[(_ := _check_if_string_in_list_of_string("phone", keys)).lower()]

    stakeholder = {
        "name": name,
        "title": title,
        "phone": phone,
        "email": email,
        "address": poc.get("address", "") if "address" in poc.keys() else "",
        "parentId": regscale_ssp["id"],
        "parentModule": "securityplans",
    }
    return stakeholder


def should_insert_stakeholder(
    poc: Dict, pocs_inserted: List, existing_stakeholders: List
):
    """Check if the stakeholder should be inserted.
    :param dict poc: A point of contact
    :param list pocs_inserted: A list of pocs already inserted
    :param list existing_stakeholders: A list of existing stakeholders
    :return: True if the stakeholder should be inserted
    :rtype: bool
    """
    if "name" in poc.keys() and (
        poc["name"].strip() not in pocs_inserted
        and poc["name"].strip()
        not in {guy["name"] for guy in existing_stakeholders if "name" in guy.keys()}
    ):
        return True
    return False


def _check_if_string_in_list_of_string(string: str, list_of_strings: list) -> str:
    """
    Check if a string is in a list of strings
    :param str string: The string to check
    :return: the found string
    :rtype: str
    """
    dat = any(string in s for s in list_of_strings)
    if dat:
        return {s for s in list_of_strings if string in s}.pop()
    return ""


def _extracted_from_gather_stakeholders(
    tables, key: str, pocs: list, key2: str
) -> dict:
    """
    Extract system owner and add to pocs
    :param tables:
    :param str key: Key used to find system owner
    :param list pocs: List of points of contacts from a SSP
    :param str key2: Second key to find system owner details
    :return: Dictionary of system owner details
    :rtype: dict
    """
    system_owner = get_contact_info(tables, key=key, xpath="//w:tbl/w:tr")
    pocs.append(system_owner)
    return get_contact_info(tables, key=key2, xpath="//w:tbl/w:tr")


def post_leveraged_authorizations(
    app: Application, table_data: list, ssp_id: int
) -> None:
    """
    Function to post leveraged authorizations
    :param Application app: Application instance
    :param list table_data: Data used to post to RegScale
    :param int ssp_id: RegScale SSP ID #
    :return: None
    """
    # LeveragedAuthorizations
    key = "Leveraged Information System Name"
    data = [table for table in table_data if key in table.keys()]
    for la in data:
        if not la.get(key, None):
            continue
        leveraged_auth = LeveragedAuthorizations(
            title=la.get(key, " "),
            servicesUsed=la.get("Leveraged Service Provider Owner"),
            dateAuthorized=la.get("Date Granted"),
            createdById=app.config.get("userId"),
            securityPlanId=ssp_id,
            ownerId=app.config.get("userId"),
            lastUpdatedById=app.config.get("userId"),
            dateLastUpdated=get_current_datetime(),
            dateCreated=get_current_datetime(),
        )
        try:
            LeveragedAuthorizations.insert_leveraged_authorizations(app, leveraged_auth)
            logger.info(
                f"Leveraged Authorizations for {la.get(key)} created in RegScale.",
                record_type="leveraged-authorizations",
                model_layer="leveraged-authorizations",
            )
        except Exception as e:
            logger.error(
                f"Error creating leveraged authorizations: {e}",
                record_type="leveraged-authorizations",
                model_layer="leveraged-authorizations",
            )


def find_profile_by_name(profile_name: str) -> Dict:
    app = Application()
    api = Api(app)
    logger.info(
        f"Using the {profile_name} profile to import controls.",
        record_type="profile",
        model_layer="profile",
    )
    profile_response = api.get(
        url=urljoin(app.config["domain"], "/api/profiles/getList")
    )

    if profile_response.ok:
        profiles = profile_response.json()
        logger.info(
            f"Found {len(profiles)} profiles in RegScale.",
            record_type="profile",
            model_layer="profile",
        )
    else:
        profiles = []
        logger.error(
            "Unable to get profiles from RegScale.",
            record_type="profile",
            model_layer="profile",
        )
        profile_response.raise_for_status()
    profile = None
    try:
        for profile_obj in profiles:
            if profile_obj["name"] == profile_name:
                profile = profile_obj
        if profile is None:
            raise ValueError(f"Unable to find profile: {profile_name}")
    except Exception as ex:
        logger.error(
            f"Unable to continue, {profile_name} is not found!\n{ex}",
            record_type="profile",
            model_layer="profile",
        )
    return profile


def get_profile_info_by_id(profile_id: int) -> Dict:
    """
    Get a profile by the profile_id from the Regscale Api
    :param int profile_id: The profile_id to get
    :return: Profile
    """
    profile = None
    try:
        app = Application()
        api = Api(app)
        profile_response = api.get(
            urljoin(app.config["domain"], f"/api/profiles/{profile_id}")
        )
        if profile_response.ok:
            profile = profile_response.json()
        else:
            logger.error(
                "Unable to get profile from RegScale.",
                record_type="profile",
                model_layer="profile",
            )
    except (IndexError, AttributeError) as ex:
        logger.error(
            f"Error Profile, {profile_id} is not found!\n{ex}",
            record_type="profile",
            model_layer="profile",
        )
    return profile


def process_fedramp_docx_by_profile_id(
    file_path: click.Path,
    profile_id: int,
    save_data: bool = False,
    load_missing: bool = False,
) -> any:
    """
    Process a FedRAMP docx by the profile_id from the Regscale Api
    :param click.Path file_path: The file path to the FedRAMP docx
    :param int profile_id: The profile_id to process
    :param bool save_data: Whether to save the data
    :param bool load_missing: Whether to load missing controls
    :return: RegScale SSP
    :rtype: RegScale SSP
    """
    profile = get_profile_info_by_id(profile_id)
    _, regscale_ssp = process_fedramp_docx(
        fedramp_file_path=file_path,
        base_fedramp_profile=profile["name"],
        profile=profile,
        save_data=save_data,
        add_missing=load_missing,
    )
    # implementation_results
    logger.write_events()
    return (
        "artifacts/import-results.csv",
        {
            "ssp_title": regscale_ssp.get("systemName", "New SSP Default Name"),
            "ssp_id": regscale_ssp.get("id"),
        },
        [],
    )


def get_profile_mapping(profile_id: int):
    """
    Get a profile mapping by the profile_id from the Regscale Api
    :param int profile_id: The profile_id to get
    :return: Profile Mapping
    :rtype: Profile Mapping

    """
    app = Application()
    api = Api(app)
    profile_mapping = None
    try:
        profile_mapping_resp = api.get(
            urljoin(
                app.config["domain"],
                f"/api/profileMapping/getByProfile/{profile_id}",
            )
        )
        if profile_mapping_resp.ok:
            profile_mapping = profile_mapping_resp.json()
        else:
            logger.error(
                "Unable to get profile mapping from RegScale.",
                record_type="profile-mapping",
                model_layer="profile-mapping",
            )
    except Exception as e:
        logger.error(
            f"Failed to get profile-mappings by profile id with error: {str(e)}",
            record_type="profile-mapping",
            model_layer="profile-mapping",
        )
    return profile_mapping


def parse_ssp_docx_tables(tables: Any) -> Tuple[str, str, str, list]:
    """
    Parse the SSP docx tables
    :param tables: List of tables from the SSP docx
    :return Tuple[str, str, str, list]: System Status, System Type, Title, Table Data
    :rtype: Tuple[str, str, str, list]
    """
    count = 0
    title = None
    system_status = "Other"
    system_type = SYSTEM_TYPE
    table_data = []
    for table in tables:
        for i, row in enumerate(table.rows):
            checked = False
            rem = row._element
            check_boxes = rem.xpath(".//w14:checked")
            text = (cell.text.strip() for cell in row.cells)
            if check_boxes:
                for checks in check_boxes:
                    if checks.items()[0][1] == "1":
                        count = count + 1
                        checked = True
            # Establish the mapping based on the first row
            # headers; these will become the keys of our dictionary
            if i == 0:
                keys = tuple(text)
                if not title:
                    dat = [x.strip() for x in keys if x].pop().split("\n")
                    title = dat[1] if len(dat) > 1 else dat[0]
                continue
            row_data = dict(zip(keys, text))
            if checked:
                if "System Status" in row_data:
                    system_status = row_data["System Status"]
                if "Service Provider Architecture Layers" in row_data:
                    system_type = row_data["Service Provider Architecture Layers"]
            row_data["checked"] = checked
            row_data["element"] = rem
            table_data.append(row_data)
    return system_status, system_type, title, table_data


def process_fedramp_docx(
    fedramp_file_path: click.Path,
    base_fedramp_profile: str,
    save_data: bool = False,
    add_missing: bool = False,
    profile: Dict = None,
) -> Tuple:
    """
    Convert a FedRAMP file to a RegScale SSP
    :param click.Path fedramp_file_path: The click file path object
    :param str base_fedramp_profile: base fedramp profile
    :raises: ValueError if unable to get profile from RegScale
    :raises: IndexError, AttributeError if unable to get profile mapping by name in RegScale
    :raises: ValueError if unable to get profile mapping RegScale
    :return: Tuple[str, SSP]
    """
    # If list of controls is more than profile mapping, make sure i get them from somewhere? Get base catalog from profile.
    load_missing = add_missing
    app = Application()
    api = Api(app)
    ssp = SSP(fedramp_file_path)
    document = ssp.document
    full_text = []
    [full_text.append(para.text) for para in document.paragraphs]
    description = get_text(
        document,
        full_text,
        start_header="Information System Components and Boundaries",
        start_text="System Description:",
        end_text="Types of Users",
    )
    environment = get_text(
        document,
        full_text,
        start_header="SYSTEM ENVIRONMENT AND INVENTORY",
        start_text="PRODUCTION ENVIRONMENT: (IMPLEMENTED)",
        end_text="Data Flow",
    )

    confidentiality = "Low"
    integrity = "Low"
    availability = "Low"
    tables = get_tables(document)
    security_objective = get_xpath_data_detailed(
        tables,
        key="Security Objective",
        ident="Confidentiality",
        xpath="//w:tbl/w:tr",
        count_array=[2, 4, 6],
    )

    # TODO: add cloud deployment models

    availability = (
        security_objective["availability"].split(" ")[0]
        if "availability" in security_objective
        else availability
    )
    confidentiality = (
        security_objective["confidentiality"].split(" ")[0]
        if "confidentiality" in security_objective
        else confidentiality
    )
    integrity = (
        security_objective["integrity"].split(" ")[0]
        if "integrity" in security_objective
        else integrity
    )

    system_status, system_type, title, table_data = parse_ssp_docx_tables(
        ssp.document.tables
    )

    status = "Operational" if "in production" in system_status else "Other"
    # Links are posted to links mapped to ssp
    # post_links(app, table_data, ssp_id)
    # Parts will go in implementation fields.
    if not profile:
        profile = find_profile_by_name(base_fedramp_profile)

    profile_mapping = get_profile_mapping(profile["id"])
    if len(profile_mapping) == 0:
        raise ValueError(
            f"Unable to continue, please load {profile['name']} with controls!",
            profile["name"],
        )

    logger.info(
        f"Utilizing profile: {profile.get('name')}",
        record_type="profile",
        model_layer="profile",
    )
    args = {
        "profile": profile,
        "title": title,
        "confidentiality": confidentiality,
        "integrity": integrity,
        "availability": availability,
        "status": status,
        "system_type": system_type,
        "ssp": ssp,
        "description": description,
        "environment": environment,
    }
    regscale_ssp = create_initial_ssp(args)

    try:
        create_responsible_roles(app, table_data, ssp_id=regscale_ssp["id"])
        ctrl_roles = post_responsible_roles(app, table_data, ssp_id=regscale_ssp["id"])
    except Exception as e:
        logger.error(
            f"Unable to gather responsible roles: {e}",
            record_type="responsible-roles",
            model_layer="responsible-roles",
        )
    try:
        gather_stakeholders(tables, regscale_ssp, ssp)
    except Exception as e:
        logger.error(
            f"Unable to gather stakeholders: {e}",
            record_type="stakeholder",
            model_layer="stakeholder",
        )
    try:
        post_interconnects(app, table_data, regscale_ssp)
    except Exception as e:
        logger.error(
            f"Unable to gather interconnects: {e}",
            record_type="interconnect",
            model_layer="interconnects",
        )
    try:
        post_ports(app, table_data, ssp_id=regscale_ssp["id"])
    except Exception as e:
        logger.error(
            f"Unable to gather ports: {e}",
            record_type="ports-protocols",
            model_layer="ports-protocols",
        )
    try:
        post_links(config=app.config, api=api, ssp_obj=ssp, regscale_ssp=regscale_ssp)
    except Exception as e:
        logger.error(
            f"Unable to gather links: {e}",
            record_type="links",
            model_layer="links",
        )
    try:
        new_implementations_count = post_implementations(
            app=app,
            ssp_obj=ssp,
            regscale_ssp=regscale_ssp,
            mapping=profile_mapping,
            ctrl_roles=ctrl_roles,
            save_data=save_data,
            load_missing=load_missing,
        )
    except Exception as e:
        logger.error(
            f"Unable to gather implementations: {e}",
            record_type="implementations",
            model_layer="implementations",
        )
        new_implementations_count = 0
    try:
        post_leveraged_authorizations(app, table_data, ssp_id=regscale_ssp["id"])
    except Exception as e:
        logger.error(
            f"Unable to gather leveraged authorizations: {e}",
            record_type="leveraged-authorizations",
            model_layer="leveraged-authorizations",
        )
    return new_implementations_count, regscale_ssp


def create_initial_ssp(args: Dict) -> any:
    """
    Create an initial SSP
    :param args:
    :return SSP:
    :rtype any:
    """
    app = Application()
    api = Api(app)
    today_dt = date.today()
    expiration_date = date(today_dt.year + 3, today_dt.month, today_dt.day)
    default = "Moderate"
    profile = args.get("profile")
    title = args.get("title")
    confidentiality = capitalize_words(args.get("confidentiality", default))
    integrity = capitalize_words(args.get("integrity", default))
    availability = capitalize_words(args.get("availability", default))
    status = args.get("status", "Operational")
    system_type = args.get("system_type", SYSTEM_TYPE)
    ssp = args.get("ssp")
    description = args.get("description", "Unable to determine System Description")
    environment = args.get("environment", "")

    regscale_ssp = SecurityPlan(
        dateSubmitted=get_current_datetime(),
        expirationDate=expiration_date.strftime(DATE_FORMAT),
        approvalDate=expiration_date.strftime(DATE_FORMAT),
        parentId=profile["id"],
        parentModule="profiles",
        systemName=title if title else "Unable to determine System Name",
        confidentiality=confidentiality,
        integrity=integrity,
        availability=availability,
        status=status,
        createdById=app.config["userId"],
        lastUpdatedById=app.config["userId"],
        systemOwnerId=app.config["userId"],
        planAuthorizingOfficialId=app.config["userId"],
        planInformationSystemSecurityOfficerId=app.config["userId"],
        systemType=system_type,
        overallCategorization=ssp.system_security_level or "Moderate",
        description=description,
        environment=environment,
        executiveSummary=f"Revision: {ssp.revision}",
    ).dict()
    if regscale_ssp.get("status") != "Operational":
        regscale_ssp[
            "explanationForNonOperational"
        ] = "Unable to determine status from SSP during FedRAMP .docx import."
    existing_security_plans_reponse = api.get(
        url=urljoin(app.config["domain"], "/api/securityplans/getList"),
    )
    existing_security_plans = []
    if not existing_security_plans_reponse.ok:
        logger.info("No Security Plans found")
    else:
        existing_security_plans = existing_security_plans_reponse.json()

    if regscale_ssp["systemName"].lower() not in {
        sys["title"].lower() for sys in existing_security_plans
    }:
        regscale_ssp_response = api.post(
            url=urljoin(app.config["domain"], "/api/securityplans"),
            json=regscale_ssp,
        )
        if regscale_ssp_response.ok:
            regscale_ssp = regscale_ssp_response.json()
        else:
            regscale_ssp_response.raise_for_status()
            logger.error(f"Unable to create Security Plan: {regscale_ssp}")
    if "id" in regscale_ssp and regscale_ssp.get("id", None) is not None:
        ssp_list = api.get(
            urljoin(app.config["domain"], "/api/securityplans/getList")
        ).json()
        if regscale_ssp["systemName"] in [reg["title"] for reg in ssp_list]:
            regscale_ssp["id"] = [
                sec["id"]
                for sec in ssp_list
                if sec["title"] == regscale_ssp["systemName"]
            ][0]
    return regscale_ssp
