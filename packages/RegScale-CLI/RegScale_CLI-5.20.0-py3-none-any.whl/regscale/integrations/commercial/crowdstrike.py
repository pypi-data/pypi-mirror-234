#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CrowdStrike RegScale integration"""
import sys
from enum import Enum
from typing import Optional, Union
from urllib.parse import urljoin

import click
from falconpy import Incidents, Intel, OAuth2, UserManagement
from rich.console import Console
from rich.table import Table

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.utils.app_utils import (
    error_and_exit,
    format_data_to_html,
    get_current_datetime,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.models import regscale_id, regscale_module
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.incident import Incident

#####################################################################################################
#
# CrowdStrike API Documentation: https://dash.readme.com/to/crowdstrike-enterprise?redirect=%2Fcrowdstrike%2Fdocs

# Sync incidents from CrowdStrike EDR into RegScale

# Allow customer to set severity level of what level of alerts they want to sync, set via init.yaml

# Check to make sure alert does not already exist, if it does, update with latest info, if it doesn't, create a new one

# Ensure you can link back to the alert in CrowdStrike

# Get with Jim Townsend on access to a DEV environment or customer sandbox

#####################################################################################################

logger = create_logger()
console = Console()


class Status(Enum):
    """Enum used to describe status values."""

    NEW = 20
    REOPENED = 25
    INPROGRESS = 30
    CLOSED = 40


class StatusColor(Enum):
    """Enum to describe colors used for status displays."""

    NEW = "[cornsilk1]"
    REOPENED = "[bright_yellow]"
    INPROGRESS = "[deep_sky_blue1]"
    CLOSED = "[bright_green]"


@click.group()
def crowdstrike():
    """[BETA] CrowdStrike Integration to load threat intelligence to RegScale."""


@crowdstrike.command(name="query_incidents")
@regscale_id(help="RegScale will create and update issues as children of this record.")
@regscale_module()
@click.option(
    "--filter",
    type=click.STRING,
    default=None,
    hide_input=False,
    required=False,
    help="Falcon Query Language(FQL) string.",
)
def query_incidents(
    regscale_id: int, regscale_module: str, filter: str, limit=500
) -> None:
    """Query Incidents from CrowdStrike."""
    query_crowdstrike_incidents(regscale_id, regscale_module, filter, limit)


def determine_incident_level(fine_score: int) -> str:
    """
    Determine the incident level based on a fine_score.

    :param fine_score: The fine_score as an integer.
    :return: The incident level as a string.
    :rtype: str
    """
    # Convert fine_score to the displayed score
    displayed_score = fine_score / 10.0

    if displayed_score >= 10.0:
        return "S1 - High Severity"
    elif displayed_score >= 8.0:
        return "S1 - High Severity"
    elif displayed_score >= 6.0:
        return "S2 - Moderate Severity"
    elif displayed_score >= 4.0:
        return "S3 - Low Severity"
    elif displayed_score >= 2.0:
        return "S4 - Non-Incident"
    else:
        return "S5 - Uncategorized"


def map_status_to_phase(status_code: int) -> str:
    """
    Map a CrowdStrike status code to a RegScale phase.

    :param status_code: The status code from CrowdStrike as an integer.
    :return: The corresponding phase in RegScale as a string.
    """
    crowdstrike_to_regcale_mapping = {
        20: "Detection",
        25: "Analysis",
        30: "Containment",
        40: "Closed",
    }

    return crowdstrike_to_regcale_mapping.get(status_code, "Analysis")


def create_properties_for_incident(device_data: dict, regscale_id: int) -> None:
    """
    Create properties in RegScale based on the given device data dictionary.
    :param device_data: The device data as a dictionary.
    :param int regscale_id: The parent ID of the incidents.
    :return: None
    """
    # Simulate RegScale API or database connection
    properties = []
    app = Application()
    api = Api(app)
    domain = api.config.get("domain")
    url = urljoin(domain, "/api/properties/batchCreate")
    for key, value in device_data.items():
        # Skip list pieces
        if not isinstance(value, list):
            # Create property in RegScale (simulated)
            prop = {
                "isPublic": "true",
                "key": key,
                "value": value,
                "parentId": regscale_id,
                "parentModule": "incidents",
            }
            properties.append(prop)
    response = api.post(url=url, json=properties)
    if not response.ok:
        logger.error("Failed to create property.")


def get_existing_regscale_incidents(parent_id: int, parent_module: str) -> list[dict]:
    """
    Get existing RegScale incidents.

    :param int parent_id: The parent ID of the incidents.
    :param str parent_module: The parent module of the incidents.
    :return: The existing incidents as a list of dictionaries.
    :rtype: list[dict]
    """
    api_handler = APIHandler()
    results = api_handler.fetch_record(
        f"/api/incidents/getAllByParent/{parent_id}/{parent_module}"
    )
    return results


def incidents_exist(title: str, existing_incidents: list[dict]) -> bool:
    """
    Determine if an incident already exists in RegScale.

    :param str title: The title of the incident.
    :param List[Dict] existing_incidents: The existing incidents as a list of dictionaries.
    :return: True if the incident already exists in RegScale, False otherwise.
    :rtype: bool
    """
    if existing_incidents:
        for existing_incident in existing_incidents:
            if existing_incident["title"] == title:
                logger.info(
                    f"Incident {existing_incident['title']} already exists in RegScale."
                )
                return True
    return False


def create_regscale_incidents(
    incidents: list[dict], regscale_id: Optional[int], regscale_module: Optional[str]
) -> None:
    """Create Incidents in RegScale.
    :param incidents: Falcon Incidents
    :param regscale_id: Optional RegScale parent ID.
    :param regscale_module: Optional RegScale parent module.
    :return: None
    """

    app = Application()
    existing_incidents = get_existing_regscale_incidents(regscale_id, regscale_module)
    for incident in incidents:
        severity = determine_incident_level(incident["fine_score"])
        source_cause = ", ".join(incident["techniques"])
        title = f"CrowdStrike incidentId: {incident['incident_id']}"
        if not incidents_exist(title, existing_incidents):
            regscale_incident = Incident(
                title=title,
                severity=severity,
                sourceCause=source_cause,
                category="CAT 6 - Investigation",
                phase=map_status_to_phase(incident["status"]),
                description=format_data_to_html(incident),  # hosts_information
                detectionMethod="Intrusion Detection System",
                incidentPOCId=app.config.get("userId"),
                dateDetected=incident["created"],
                parentId=regscale_id if regscale_id is not None else None,
                parentModule=regscale_module if regscale_module is not None else None,
                lastUpdatedById=app.config.get("userId"),
                dateCreated=incident["created"],
                dateLastUpdated=get_current_datetime(),
                dateResolved=incident["end"]
                if "end" in incident
                and map_status_to_phase(incident["status"]) == "Closed"
                else None,
                createdById=app.config.get("userId"),
            )

            response = Incident.post_incident(regscale_incident)
            if response.ok:
                incident_id = response.json()["id"]
                for host in incident["hosts"]:
                    create_asset(
                        data=host,
                        parent_id=incident_id,
                        parent_module="incidents",
                        user_id=app.config.get("userId"),
                    )
                # create_properties_for_incident(host, id)
                for tactic in incident["tactics"] if "tactics" in incident else []:
                    create_properties_for_incident({"tactic": tactic}, incident_id)
                for techniques in (
                    incident["techniques"] if "techniques" in incident else []
                ):
                    create_properties_for_incident(
                        {"techniques": techniques}, incident_id
                    )
                for objectives in (
                    incident["objectives"] if "objectives" in incident else []
                ):
                    create_properties_for_incident(
                        {"objectives": objectives}, incident_id
                    )
                for users in incident["users"] if "users" in incident else []:
                    create_properties_for_incident({"users": users}, incident_id)
                logger.info(
                    f"Created Incident: {regscale_incident.title} with ID: {incident_id}"
                )
            else:
                response.raise_for_status()
                logger.error(
                    f"Failed to create Incident: {regscale_incident.title} in RegScale."
                )


def create_asset(data: dict, parent_id: int, parent_module: str, user_id: str) -> None:
    """
    Create an asset in RegScale.

    :param dict data: The asset data as a dictionary.
    :param int parent_id: The parent ID in RegScale.
    :param str parent_module: The parent module in RegScale.
    :param str user_id: The user ID in RegScale.
    :return: None
    """
    device_id = data.get("device_id", "")
    asset = Asset(
        parentId=parent_id,
        parentModule=parent_module,
        name=f'{data.get("hostname", device_id)} - {data.get("system_product_name", "Asset")}',
        description=data.get("product_type_desc", None),
        ipAddress=data.get("external_ip", None),
        macAddress=data.get("mac_address", None),
        manufacturer=data.get("bios_manufacturer", None),
        model=data.get("bios_version", None),
        serialNumber=data.get("serial-number", None),
        assetCategory="Hardware",
        assetType="Desktop",
        fqdn=data.get("fqdn", None),
        notes=data.get("remarks", None),
        operatingSystem=data.get("os_version", None),
        oSVersion=f"{data.get('major_version', None)}.{data.get('minor_version', None)}"
        if data.get("major_version", None)
        else None,
        netBIOS=data.get("netbios-name", None),
        iPv6Address=data.get("ipv6-address", None),
        ram=0,
        diskStorage=0,
        cpu=0,
        assetOwnerId=user_id,
        status="Active (On Network)",
        isPublic=True,
        dateCreated=get_current_datetime(),
        dateLastUpdated=get_current_datetime(),
    )
    api_handler = APIHandler()
    logger.debug(f"Inserting asset to RegScale.\n Asset:\n{asset.dict()}")
    response = api_handler.insert_record(endpoint="/api/assets", json=asset.dict())
    if response:
        asset.id = response["id"]
    return asset


def query_crowdstrike_incidents(
    regscale_id: int, regscale_module: str, filter: str, limit=500
) -> None:
    """Query Incidents from CrowdStrike.

    :param regscale_id: RegScale parent ID.
    :param regscale_module: RegScale parent module.
    :param filter: Falcon Query Language Filter
    :param limit: Record limit, 1-500, defaults to 500
    :return: None
    """
    incident_list = []
    avail = True
    offset = 500
    while avail:
        incidents = open_sdk().query_incidents(
            filter=filter, limit=limit, offset=offset
        )
        logger.info(f"Found {len(incidents['body']['resources'])} incidents.")
        if incidents["status_code"] != 200:
            error_and_exit(incidents["body"]["errors"][0])
        if not incidents["body"]["resources"]:
            avail = False
        else:
            offset += limit
            incident_list.extend(incidents["body"]["resources"])
    if incident_list:
        create_regscale_incidents(incident_list, regscale_id, regscale_module)


def open_sdk() -> Optional[Incidents]:
    """
    Function to create an instance of the Crowdstrike SDK
    :raises AttributeError: If the unable to authenticate with CrowdStrike API
    :return: Incidents object
    :rtype: Incidents
    """
    app = Application()
    falcon_client_id = app.config.get("crowdstrikeClientId")
    falcon_client_secret = app.config.get("crowdstrikeClientSecret")
    try:
        inc_object = Incidents(
            client_id=falcon_client_id, client_secret=falcon_client_secret
        )
        if inc_object is not None:
            logger.info("Successfully created Crowdstrike client.")
            return inc_object
        else:
            logger.error("Unable to create Crowdstrike object.")
    except AttributeError as aex:
        logger.error(aex)
        if str(aex) == """'str' object has no attribute 'authenticated'""":
            error_and_exit(
                "Unable to Authenticate with CrowdStrike API. Please check your credentials."
            )


def users():
    """Create instances of our two Service Classes and returns them."""
    return UserManagement(auth_object=open_sdk())


def get_incident_ids(sdk: Incidents, filter_string: Optional[str]) -> list:
    """
    Retrieve all available incident IDs from Crowdstrike
    :param Incidents sdk: Crowdstrike SDK object
    :param Optional[str] filter_string: Filter string to use for query
    :raises General Error: If unable to retrieve incident IDs from Crowdstrike
    :return: List of incident IDs
    :rtype: list
    """
    params = {}
    if filter_string:
        params = {"filter": filter_string}
    incident_id_lookup = sdk.query_incidents(**params)
    if incident_id_lookup["status_code"] != 200:
        error_and_exit(incident_id_lookup["body"]["errors"][0])
    if not incident_id_lookup["body"]["resources"]:
        logger.warning("No incidents found.")

    return incident_id_lookup["body"]["resources"]


def get_incident_data(id_list: list, sdk: Incidents) -> list[dict]:
    """
    Retrieve incident details using the IDs provided
    :param list id_list: List of incident IDs from Crowdstrike
    :param Incidents sdk: Crowdstrike SDK object
    :raises General Error: If unable to retrieve incident details from Crowdstrike
    :return: List of incident details
    :rtype: list
    """
    incident_detail_lookup = sdk.get_incidents(ids=id_list)
    if incident_detail_lookup["status_code"] != 200:
        error_and_exit(incident_detail_lookup["body"]["errors"][0])
    return incident_detail_lookup["body"]["resources"]


def tagging(inc_id: str, tags: list, untag: bool = False) -> None:
    """
    Assign or remove all tags provided
    :param str inc_id: Incident ID to tag
    :param list tags: List of tags to assign
    :param bool untag: Flag to remove tags instead of assign, defaults to False
    :return: None
    """
    sdk = open_sdk()
    action = {"ids": get_incident_full_id(inc_id)}
    if untag:
        action["delete_tag"] = tags
    else:
        action["add_tag"] = tags
    change_result = sdk.perform_incident_action(**action)
    if change_result["status_code"] != 200:
        error_and_exit(change_result["body"]["errors"][0])


def get_user_detail(uuid: str) -> str:
    """
    Retrieve assigned to user information for tabular display
    :param str uuid: User ID to retrieve information for in CrowdStrike
    :return: User information
    :rtype: str
    """
    lookup_result = users.retrieve_user(ids=uuid)
    if lookup_result["status_code"] != 200:
        error_and_exit(lookup_result["body"]["errors"][0])
    user_info = lookup_result["body"]["resources"][0]
    first = user_info["firstName"]
    last = user_info["lastName"]
    uid = user_info["uid"]

    return f"{first} {last} ({uid})"


def get_incident_full_id(partial: str) -> Union[str, bool]:
    """
    Retrieve the full incident ID based off of the partial ID provided
    :param str partial: Partial incident ID to search for
    :raises General Error: If api call != 200
    :raises General Error: If unable to find incident ID
    :return: Full incident ID
    :rtype: Union[str, bool]
    """
    sdk = open_sdk()
    search_result = sdk.query_incidents()
    if search_result["status_code"] != 200:
        error_and_exit(search_result["body"]["errors"][0])
    found = False
    for inc in search_result["body"]["resources"]:
        incnum = inc.split(":")[2]
        if incnum == partial:
            found = inc
            break

    if not found:
        error_and_exit("Unable to find incident ID specified.")

    return found


def assignment(inc_id: str, assign_to: str = "", unassign: bool = False) -> None:
    """
    Assign the incident specified to the user specified
    :param str inc_id: Incident ID to assign
    :param str assign_to: User ID to assign incident to
    :param bool unassign: Flag to unassign incident, defaults to False
    :raises General Error: If API Call != 200
    :return: None
    """
    sdk = open_sdk()
    if unassign:
        change_result = sdk.perform_incident_action(
            ids=get_incident_full_id(inc_id), unassign=True
        )
        if change_result["status_code"] != 200:
            error_and_exit(change_result["body"]["errors"][0])
    else:
        lookup_result = users.retrieve_user_uuid(uid=assign_to)

        if lookup_result["status_code"] != 200:
            error_and_exit(lookup_result["body"]["errors"][0])
        change_result = sdk.perform_incident_action(
            ids=get_incident_full_id(inc_id),
            update_assigned_to_v2=lookup_result["body"]["resources"][0],
        )
        if change_result["status_code"] != 200:
            error_and_exit(change_result["body"]["errors"][0])


def status_information(inc_data: dict) -> str:
    """
    Parse status information for tabular display
    :param dict inc_data: Incident data to parse
    :return: Status information
    :rtype: str
    """
    inc_status = [
        f"{StatusColor[Status(inc_data['status']).name].value}"
        f"{Status(inc_data['status']).name.title().replace('Inp','InP')}[/]"
    ]
    tag_list = inc_data.get("tags", [])
    if tag_list:
        inc_status.append(" ")
        tag_list = [f"[magenta]{tg}[/]" for tg in tag_list]
        inc_status.extend(tag_list)

    return "\n".join(inc_status)


def incident_information(inc_data: dict) -> str:
    """
    Parse incident overview information for tabular display
    :param dict inc_data: Incident data to parse
    :return: Incident overview information
    :rtype: str
    """
    inc_info = []
    inc_info.append(inc_data.get("name", ""))
    inc_info.append(f"[bold]{inc_data['incident_id'].split(':')[2]}[/]")
    inc_info.append(f"Start: {inc_data.get('start', 'Unknown').replace('T', ' ')}")
    inc_info.append(f"  End: {inc_data.get('end', 'Unknown').replace('T', ' ')}")
    assigned = inc_data.get("assigned_to", None)
    if assigned:
        inc_info.append("\n[underline]Assignment[/]")
        inc_info.append(get_user_detail(assigned))
    if inc_data.get("description", None):
        inc_info.append(" ")
        inc_info.append(chunk_long_description(inc_data["description"], 50))

    return "\n".join(inc_info)


def chunk_long_description(desc: str, col_width: int) -> str:
    """
    Chunk a long string by delimiting with CR based upon column length
    :param str desc: Description to parse
    :param int col_width: Column width to chunk by
    :return: Chunked description
    :rtype: str
    """
    desc_chunks = []
    chunk = ""
    for word in desc.split():
        new_chunk = f"{chunk}{word.strip()} "
        if len(new_chunk) >= col_width:
            desc_chunks.append(new_chunk)
            chunk = ""
        else:
            chunk = new_chunk

    delim = "\n"
    desc_chunks.append(chunk)

    return delim.join(desc_chunks)


def hosts_information(inc_data: dict) -> str:
    """
    Parse hosts information for tabular display
    :param dict inc_data: Incident data to parse
    :return: Host information
    :rtype: str
    """
    returned = ""
    if "hosts" in inc_data:
        host_str = []
        for host in inc_data["hosts"]:
            host_info = []
            host_info.append(
                f"<strong>{host.get('hostname', 'Unidentified')}</strong>"
                f" ({host.get('platform_name', 'Not available')})"
            )
            host_info.append(
                f"<span style='color:cyan'>{host.get('device_id', 'Not available')}</span>"
            )
            host_info.append(f"  Int: {host.get('local_ip', 'Not available')}")
            host_info.append(f"  Ext: {host.get('external_ip', 'Not available')}")
            first = (
                host.get("first_seen", "Unavailable")
                .replace("T", " ")
                .replace("Z", " ")
            )
            host_info.append(f"First: {first}")
            last = (
                host.get("last_seen", "Unavailable").replace("T", " ").replace("Z", " ")
            )
            host_info.append(f" Last: {last}")
            host_str.append("\n".join(host_info))
        if host_str:
            returned = "\n".join(host_str)
        else:
            returned = "Unidentified"

    return returned


def show_incident_table(incident_listing: list) -> None:
    """
    Display all returned incidents in tabular fashion
    :param list incident_listing: List of incidents to parse and print to console
    :raises General Error: If incident_listing is empty
    :return: None
    """
    if not incident_listing:
        error_and_exit(f"No incidents found, code {404}")
    table = Table(show_header=True, header_style="bold magenta", title="Incidents")
    headers = {
        "status": "[bold]Status[/] ",
        "incident": "[bold]Incident[/]",
        "hostname": "[bold]Host[/]",
        "tactics": "[bold]Tactics[/]",
        "techniques": "[bold]Techniques[/]",
        "objectives": "[bold]Objective[/]s",
    }
    for key in headers.keys():
        table.add_column(headers[key], justify="left")
    for inc in incident_listing:
        inc_detail = {}
        inc_detail["status"] = status_information(inc)
        inc_detail["incident"] = incident_information(inc)
        inc_detail["hostname"] = hosts_information(inc)
        inc_detail["tactics"] = "\n".join(inc["tactics"])
        inc_detail["techniques"] = "\n".join(inc["techniques"])
        inc_detail["objectives"] = "\n".join(inc["objectives"])
        table.add_row(
            inc_detail["status"],
            inc_detail["incident"],
            inc_detail["hostname"],
            inc_detail["tactics"],
            inc_detail["techniques"],
            inc_detail["objectives"],
        )
    console.print(table)


def get_token() -> str:
    """
    Get the token for the CrowdStrike API
    :raises General Error: If unable to authenticate with CrowdStrike API
    :return: CrowdStrike API token
    :rtype: str
    """
    app = Application()
    falcon_client_id = app.config.get("crowdstrikeClientId")
    falcon_client_secret = app.config.get("crowdstrikeClientSecret")
    falcon_url = app.config.get("crowdstrikeBaseUrl")

    if not falcon_client_id:
        falcon_client_id = click.prompt(
            "Please provide your Falcon Client API Key", hide_input=True
        )
    if not falcon_client_secret:
        falcon_client_secret = click.prompt(
            "Please provide your Falcon Client API Secret", hide_input=True
        )
    auth = OAuth2(
        client_id=falcon_client_id,
        client_secret=falcon_client_secret,
        base_url=falcon_url,
    )
    # Generate a token
    auth.token()
    if auth.token_status != 201:
        raise error_and_exit("Unable to authenticate with Crowdstrike!")
    return auth.token_value


@crowdstrike.command(name="sync_incidents")
@regscale_id(
    help="RegScale will create and update incidents as children of this record."
)
@regscale_module()
def sync_incidents(regscale_id: int, regscale_module: str):
    """Sync Incidents and Assets from CrowdStrike to RegScale."""
    sync_incidents_to_regscale(regscale_id, regscale_module)


def sync_incidents_to_regscale(regscale_id: int, regscale_module: str) -> None:
    """
    Sync Incidents and Assets from CrowdStrike to RegScale
    :param int regscale_id: RegScale record ID
    :param str regscale_module: RegScale Module
    :return: None
    """
    verify_provided_module(regscale_module)
    sdk = open_sdk()
    incident_id_list = get_incident_ids(filter_string=None, sdk=sdk)
    if not incident_id_list:
        error_and_exit("No incidents found!")
    incidents = get_incident_data(id_list=incident_id_list, sdk=sdk)
    logger.info(f"Found {len(incidents)} incidents to sync.")
    create_regscale_incidents(
        incidents=incidents, regscale_id=regscale_id, regscale_module=regscale_module
    )


def get_intel() -> Intel:
    """
    Get the Intel SDK object
    :return: Intel SDK object
    """
    app = Application()
    client_id = app.config.get("crowdstrikeClientId")
    client_secret = app.config.get("crowdstrikeClientSecret")
    intel = Intel(
        client_id=client_id,
        client_secret=client_secret,
    )
    return intel


def get_vulnerability_ids(intel, limit=100) -> list:
    """Fetch ID's from CrowdStrike for Intel Model
    :param Intel intel: The Intel SDK object
    :param int limit: The number of records to fetch from CrowdStrike, defaults to 100
    :raises General Error: If errors are returned from CrowdStrike
    :raises Exception: If unable to fetch ID's from CrowdStrike
    :return: List of vulnerability ID's
    :rtype: list
    """
    try:
        id_lookup = intel.query_vulnerabilities(limit=limit)
        if "errors" in id_lookup["body"]:
            error_and_exit(id_lookup["body"]["errors"])
        number_of_records = len(id_lookup["body"]["resources"])
        if number_of_records == 0:
            logger.info(f"Found {number_of_records} Records.")
            sys.exit(0)
        return id_lookup["body"]["resources"]
    except Exception as e:
        error_and_exit(f"Error: {e}")


def get_vulnerabilities_by_id(ids: list, intel: Intel) -> list[dict]:
    """Retrieve record details using the IDs provided.
    :param list ids: The IDs of the records to retrieve.
    :param Intel intel: The Intel SDK object.
    :return List[Dict]: A list of dictionaries containing the record details
    """
    detail_lookup = intel.get_vulnerabilities(ids=ids)
    if detail_lookup["status_code"] != 200:
        error_and_exit(detail_lookup["body"]["errors"][0])
    return detail_lookup["body"]["resources"]


# this will pull the data from the CrowdStrike API but need to figure out what the data looks like before we can map it
# @crowdstrike.command(name="fetch_vulnerabilities")
# @regscale_id(help="RegScale will create vulnerabilities as children of this record.")
# @regscale_module()
# @click.option("--limit", "-l", default=100, help="Limit the number of records")
# def sync_vulnerabilities(regscale_id: int, regscale_module: str, limit: int) -> None:
#     """
#     Fetch all vulnerabilities from CrowdStrike.
#     :param int regscale_id: The ID of the RegScale record.
#     :param str regscale_module: The module of the RegScale record.
#     :param int limit: The number of records to fetch.
#     """
#     _sync_vulnerabilities(regscale_id=regscale_id, regscale_module=regscale_module, limit=limit)
#
#
# def _sync_vulnerabilities(regscale_id: int, regscale_module: str, limit) -> None:
#     """
#     Fetch all vulnerabilities from CrowdStrike.
#     :param int regscale_id: The ID of the RegScale record.
#     :param str regscale_module: The module of the RegScale record.
#     :param int limit: The number of records to fetch.
#     """
#     intel = get_intel()
#     ids = get_vulnerability_ids(intel=intel, limit=limit)
#     data = get_vulnerabilities_by_id(ids=ids, intel=intel)
#     logger.info(json.dumps(data, indent=4))
