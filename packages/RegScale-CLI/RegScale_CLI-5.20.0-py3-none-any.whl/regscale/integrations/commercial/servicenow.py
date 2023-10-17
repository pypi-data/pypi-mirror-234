#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Integration of ServiceNow into RegScale CLI tool """

# standard python imports
import sys
from copy import deepcopy
from json import JSONDecodeError
from pathlib import Path
from typing import Tuple

import click
import requests
from rich.progress import track

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    error_and_exit,
    save_data_to,
)
from regscale.core.app.utils.regscale_utils import verify_provided_module
from regscale.models import regscale_id, regscale_module

logger = create_logger()


# Create group to handle ServiceNow integration
@click.group()
def servicenow():
    """Auto-assigns incidents in ServiceNow for remediation."""
    check_license()


#####################################################################################################
#
# PROCESS ISSUES TO ServiceNow
# ServiceNow REST API Docs:
#   https://docs.servicenow.com/bundle/paris-application-development/page/build/applications/concept/api-rest.html
# Use the REST API Explorer in ServiceNow to select table, get URL, and select which fields to populate
#
#####################################################################################################
@servicenow.command()
@regscale_id()
@regscale_module()
@click.option(
    "--snow_assignment_group",
    type=click.STRING,
    help="RegScale will sync the issues for the record to this ServiceNow assignment group.",
    prompt="Enter the name of the project in ServiceNow",
    required=True,
)
@click.option(
    "--snow_incident_type",
    type=click.STRING,
    help="Enter the ServiceNow incident type to use when creating new issues from RegScale.",
    prompt="Enter the ServiceNow incident type",
    required=True,
)
def issues(
    regscale_id: int,
    regscale_module: str,
    snow_assignment_group: str,
    snow_incident_type: str,
):
    """Process issues to ServiceNow."""
    sync_snow_to_regscale(
        regscale_id=regscale_id,
        regscale_module=regscale_module,
        snow_assignment_group=snow_assignment_group,
        snow_incident_type=snow_incident_type,
    )


@servicenow.command(name="sync_work_notes")
def sync_work_notes():
    """Sync work notes from ServiceNow to existing issues."""
    sync_notes_to_regscale()


def sync_snow_to_regscale(
    regscale_id: int,
    regscale_module: str,
    snow_assignment_group: str,
    snow_incident_type: str,
) -> None:
    """
    Sync issues from ServiceNow to RegScale via API
    :param int regscale_id: ID # of record in RegScale to associate issues with
    :param str regscale_module: RegScale module to associate issues with
    :param str snow_assignment_group: Snow assignment group to filter for
    :param str snow_incident_type: Snow incident type to filter for
    :return: None
    """
    # initialize variables
    app = Application()
    reg_api = Api(app)
    logger = create_logger()

    # see if provided RegScale Module is an accepted option
    verify_provided_module(regscale_module)

    # load the config from init.yaml
    config = app.config

    # get secrets
    snow_url = app.config["snowUrl"]
    snow_user = app.config["snowUserName"]
    snow_pwd = app.config["snowPassword"]

    # set headers
    url_issues = (
        config["domain"]
        + "/api/issues/getAllByParent/"
        + str(regscale_id)
        + "/"
        + str(regscale_module).lower()
    )
    # get the existing issues for the parent record that are already in RegScale
    logger.info("Fetching full issue list from RegScale.")
    issue_response = reg_api.get(url_issues)
    # check for null/not found response
    if issue_response.status_code == 204:
        logger.warning("No existing issues for this RegScale record.")
        issues_data = []
    else:
        try:
            issues_data = issue_response.json()
        except JSONDecodeError as rex:
            error_and_exit(f"Unable to fetch issues from RegScale.\n{rex}")
    # make directory if it doesn't exist
    check_file_path("artifacts")

    # write out issues data to file
    if len(issues_data) > 0:
        save_data_to(
            file=Path("./artifacts/existingRecordIssues.json"),
            data=issues_data,
        )
        logger.info(
            "Writing out RegScale issue list for Record # %s to the artifacts folder (see existingRecordIssues.json).",
            regscale_id,
        )
    logger.info(
        "%s existing issues retrieved for processing from RegScale.",
        len(issues_data),
    )
    # loop over the issues and write them out
    int_new = 0
    regscale_issue_url = config["domain"] + "/api/issues/"
    snow_api = deepcopy(
        reg_api
    )  # no need to instantiate a new config, just copy object
    snow_api.auth = (snow_user, snow_pwd)
    for iss in issues_data:
        try:
            # build the issue URL for cross-linking
            str_issue_url = f'{config["domain"]}/issues/form/{iss["id"]}'
            if "serviceNowId" not in iss:
                iss["serviceNowId"] = ""
            # see if the ServiceNow ticket already exists
            if iss["serviceNowId"] == "":
                # create a new ServiceNow incident
                snow_incident = {
                    "description": iss["description"],
                    "short_description": iss["title"],
                    "assignment_group": snow_assignment_group,
                    "due_date": iss["dueDate"],
                    "comments": "RegScale Issue #"
                    + str(iss["id"])
                    + " - "
                    + str_issue_url,
                    "state": "New",
                    "urgency": snow_incident_type,
                }

                # create a SNOW incident
                incident_url = f"{snow_url}api/now/table/incident"
                snow_header = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                try:
                    # intNew += 1
                    response = snow_api.post(
                        url=incident_url,
                        headers=snow_header,
                        json=snow_incident,
                    )
                    if not response.raise_for_status():
                        int_new += 1
                    snow_response = response.json()
                    logger.debug(snow_response)
                    # log the result
                    logger.info(
                        "SNOW Incident ID %s created.",
                        snow_response["result"]["sys_id"],
                    )
                    # get the SNOW ID
                    iss["serviceNowId"] = snow_response["result"]["sys_id"]
                    # update the issue in RegScale
                    str_update_url = regscale_issue_url + str(iss["id"])
                    try:
                        update_response = reg_api.put(url=str_update_url, json=iss)
                        if not update_response.raise_for_status():
                            logger.info(
                                "%i) RegScale Issue # %s was updated with the ServiceNow link.",
                                int_new,
                                str(iss["id"]),
                            )
                        else:
                            logger.error(
                                "Unable to update RegScale Issue #%i.", iss["id"]
                            )
                    except requests.exceptions.RequestException as ex:
                        # problem updating RegScale
                        logger.error("Unable to update RegScale: %s.", ex)
                        break
                except requests.exceptions.RequestException as ex:
                    # problem creating in ServiceNow
                    logger.error(
                        "Unable to create incident %s in ServiceNow...\n%s",
                        snow_incident,
                        ex,
                    )
        except KeyError as kex:
            logger.error("Unable to find key: %s.", kex)

    # output the final result
    logger.info("%i new issue incidents opened in ServiceNow.", int_new)


def sync_notes_to_regscale() -> None:
    """
    Sync work notes from ServiceNow to existing issues
    :return: None
    """
    app = Application()
    reg_api = Api(app)
    data = []
    # get secrets
    snow_url = app.config["snowUrl"]
    snow_user = app.config["snowUserName"]
    snow_pwd = app.config["snowPassword"]
    incident_url = f"{snow_url}api/now/table/incident"
    snow_api = deepcopy(
        reg_api
    )  # no need to instantiate a new config, just copy object
    snow_api.auth = (snow_user, snow_pwd)
    offset = 0
    limit = 500
    query = "&sysparm_query=GOTO123TEXTQUERY321=regscale"
    result, offset = query_incidents(
        api=snow_api, incident_url=incident_url, offset=offset, limit=limit, query=query
    )
    data += result
    while len(result) > 0:
        result, offset = query_incidents(
            api=snow_api,
            incident_url=incident_url,
            offset=offset,
            limit=limit,
            query=query,
        )
        data = data + result
    process_work_notes(config=app.config, api=reg_api, data=data)


def process_work_notes(config: dict, api: Api, data: list) -> None:
    """
    Process and Sync the worknotes to RegScale
    :param dict config: Application config
    :param api: API object
    :param data: list of data from ServiceNow to sync with RegScale
    :raises: HTTPError if unable to find RegScale issue with ServiceNow incident ID
    :return: None
    """
    for dat in track(
        data,
        description=f"Processing {len(data):,} ServiceNow incidents",
    ):
        sys_id = str(dat["sys_id"])
        update_issues = []
        try:
            regscale_response = api.get(
                url=config["domain"] + f"/api/issues/findByServiceNowId/{sys_id}"
            )
            if regscale_response.raise_for_status():
                logger.warning("Cannot find RegScale issue with a incident %s.", sys_id)
            else:
                logger.debug("Processing ServiceNow Issue # %s", sys_id)
                if work_item := dat["work_notes"]:
                    issue = regscale_response.json()[0]
                    if work_item not in issue["description"]:
                        logger.info(
                            "Updating work item for RegScale issue # %s and ServiceNow incident # %s.",
                            issue["id"],
                            sys_id,
                        )
                        issue["description"] = (
                            f"<strong>ServiceNow Work Notes: </strong>{work_item}<br/>"
                            + issue["description"]
                        )
                        update_issues.append(issue)
        except requests.HTTPError:
            logger.warning(
                "HTTP Error: Unable to find RegScale issue with ServiceNow incident ID of %s.",
                sys_id,
            )
    if len(update_issues) > 0:
        logger.info(update_issues)
        api.update_server(
            url=config["domain"] + "/api/issues",
            message=f"Updating {len(update_issues)} issues..",
            json_list=update_issues,
        )
    else:
        logger.warning(
            "No ServiceNow work items found, No RegScale issues were updated."
        )
        sys.exit(0)


def query_incidents(
    api: Api, incident_url: str, offset: int, limit: int, query: str
) -> Tuple[list, int]:
    """
    Paginate through query results
    :param api: API object
    :param str incident_url: URL for ServiceNow incidents
    :param int offset: Used in URL for ServiceNow API call
    :param int limit: Used in URL for ServiceNow API call
    :param str query: Query string for ServiceNow API call
    :return: Tuple[Result data from API call, offset integer provided]
    :rtype: Tuple[list, int]
    """
    offset_param = f"&sysparm_offset={offset}"
    url = f"{incident_url}?sysparm_limit={limit}{offset_param}{query}"
    logger.debug(url)
    result = api.get(url=url).json()["result"]
    offset += limit
    logger.debug(len(result))
    return result, offset
