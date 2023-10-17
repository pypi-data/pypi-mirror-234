#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Integrates Qualys assets and vulnerabilities into RegScale CLI """

# standard python imports
import pprint
from datetime import datetime, timedelta
from json import JSONDecodeError
from pathlib import Path
from typing import Optional, Union

import click
import requests
import xmltodict
from requests import Session

from regscale.core.app.api import Api
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    create_progress_object,
    error_and_exit,
    get_current_datetime,
    save_data_to,
)
from regscale.core.app.utils.regscale_utils import lookup_reg_assets_by_parent
from regscale.models.app_models.click import NotRequiredIf, save_output_to
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.issue import Issue

####################################################################################################
#
# Qualys API Documentation:
#   https://qualysguard.qg2.apps.qualys.com/qwebhelp/fo_portal/api_doc/index.htm
#
####################################################################################################


# create global variables for the entire module
logger = create_logger()

# create progress object to add tasks to for real time updates
job_progress = create_progress_object()
HEADERS = {"X-Requested-With": "RegScale CLI"}
QUALYS_API = Session()


# Create group to handle Qualys commands
@click.group()
def qualys():
    """Performs actions from the Qualys API"""


@qualys.command(name="export_scans")
@save_output_to()
@click.option(
    "--days",
    type=int,
    default=30,
    help="The number of days to go back for completed scans, default is 30.",
)
@click.option(
    "--export",
    type=click.BOOL,
    help="To disable saving the scans as a .json file, use False. Defaults to True.",
    default=True,
    prompt=False,
    required=False,
)
def export_past_scans(save_output_to: Path, days: int, export: bool = True):
    """Export scans from Qualys Host that were completed
    in the last x days, defaults to last 30 days
    and defaults to save it as a .json file"""
    export_scans(
        save_output_to=save_output_to,
        days=days,
        export=export,
    )


@qualys.command(name="save_results")
@save_output_to()
@click.option(
    "--scan_id",
    type=click.STRING,
    help="Qualys scan reference ID to get results, defaults to all.",
    default="all",
)
def save_results(save_output_to: Path, scan_id: str):
    """Get scan results from Qualys using a scan ID or all scans and save them to a .json file."""
    save_scan_results_by_id(save_output_to=save_output_to, scan_id=scan_id)


@qualys.command(name="sync_qualys")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    required=True,
    prompt="Enter RegScale System Security Plan ID",
    help="The ID number from RegScale of the System Security Plan",
)
@click.option(
    "--create_issue",
    type=click.BOOL,
    required=False,
    help="Create Issue in RegScale from vulnerabilities in Qualys.",
    default=False,
)
@click.option(
    "--asset_group_id",
    type=click.INT,
    help="Filter assets from Qualys with an asset group ID.",
    default=None,
    cls=NotRequiredIf,
    not_required_if=["asset_group_name"],
)
@click.option(
    "--asset_group_name",
    type=click.STRING,
    help="Filter assets from Qualys with an asset group name.",
    default=None,
    cls=NotRequiredIf,
    not_required_if=["asset_group_id"],
)
def sync_qualys(
    regscale_ssp_id: int,
    create_issue: bool = False,
    asset_group_id: int = None,
    asset_group_name: str = None,
):
    """
    Query Qualys and sync assets & their associated
    vulnerabilities to a Security Plan in RegScale.
    """
    sync_qualys_to_regscale(
        regscale_ssp_id=regscale_ssp_id,
        create_issue=create_issue,
        asset_group_id=asset_group_id,
        asset_group_name=asset_group_name,
    )


@qualys.command(name="get_asset_groups")
@save_output_to()
def get_asset_groups(save_output_to: Path):
    """
    Get all asset groups from Qualys via API and save them to a .json file.
    """
    # see if user has enterprise license
    check_license()

    date = get_current_datetime("%Y%m%d")
    check_file_path(save_output_to)
    asset_groups = get_asset_groups_from_qualys()
    save_data_to(
        file=Path(f"{save_output_to}/qualys_asset_groups_{date}.json"),
        data=asset_groups,
    )


def export_scans(
    save_output_to: Path,
    days: int = 30,
    export: bool = True,
) -> None:
    """
    Function to export scans from Qualys that were completed in the last x days, defaults to 30
    :param Path save_output_to: Path to save the scans to as a .json file
    :param int days: # of days of completed scans to export, defaults to 30 days
    :param bool export: Whether to save the scan data as a .json, defaults to True
    :return: None
    """
    # see if user has enterprise license
    check_license()
    date = get_current_datetime("%Y%m%d")
    results = get_detailed_scans(days)
    if export:
        check_file_path(save_output_to)
        save_data_to(
            file=Path(f"{save_output_to.name}/qualys_scans_{date}.json"),
            data=results,
        )
    else:
        pprint(results)


def save_scan_results_by_id(save_output_to: Path, scan_id: str):
    """
    Function to save the queries from Qualys using an ID a .json file
    :param Path save_output_to: Path to save the scan results to as a .json file
    :param int scan_id: Qualys scan ID to get the results for
    :return: None
    """
    # see if user has enterprise license
    check_license()

    check_file_path(save_output_to)
    with job_progress:
        if scan_id.lower() == "all":
            # get all the scan results from Qualys
            scans = get_scans_summary("all")

            # add task to job progress to let user know # of scans to fetch
            task1 = job_progress.add_task(
                f"[#f8b737]Getting scan results for {len(scans['SCAN'])} scan(s)...",
                total=len(scans["SCAN"]),
            )
            # get the scan results from Qualys
            scan_data = get_scan_results(scans, task1)
        else:
            task1 = job_progress.add_task(
                f"[#f8b737]Getting scan results for {scan_id}...", total=1
            )
            # get the scan result for the provided scan id
            scan_data = get_scan_results(scan_id, task1)
    # save the scan_data as the provided file_path
    save_data_to(file=save_output_to, data=scan_data)


def sync_qualys_to_regscale(
    regscale_ssp_id: int,
    create_issue: bool = False,
    asset_group_id: int = None,
    asset_group_name: str = None,
) -> None:
    """
    Sync Qualys assets and vulnerabilities to a security plan in RegScale
    :param int regscale_ssp_id: ID # of the SSP in RegScale
    :param bool create_issue: Flag whether to create an issue in RegScale from Qualys vulnerabilities, defaults to False
    :param int asset_group_id: Optional filter for assets in Qualys with an asset group ID, defaults to None
    :param str asset_group_name: Optional filter for assets in Qualys with an asset group name, defaults to None
    :return: None
    """
    # see if user has enterprise license
    check_license()

    # check if the user provided an asset group id or name
    if asset_group_id:
        # get the assets from Qualys using the group name
        sync_qualys_assets_and_vulns(
            ssp_id=regscale_ssp_id,
            create_issue=create_issue,
            asset_group_filter=asset_group_name,
        )
    elif asset_group_name:
        # get the assets from Qualys using the group name
        sync_qualys_assets_and_vulns(
            ssp_id=regscale_ssp_id,
            create_issue=create_issue,
            asset_group_filter=asset_group_id,
        )
    else:
        sync_qualys_assets_and_vulns(ssp_id=regscale_ssp_id, create_issue=create_issue)


def get_scan_results(scans: any, task) -> dict:
    """
    Function to retrieve scan results from Qualys using provided scan list and returns a dictionary
    :param any scans: list of scans to retrieve from Qualys
    :param task: task to update in the progress object
    :return: dictionary of detailed Qualys scans
    :rtype: dict
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])

    scan_data = {}
    # check number of scans requested
    if isinstance(scans, str):
        # only one scan was requested, set up variable for the for loop
        scans = {"SCAN": [{"REF": scans}]}
    for scan in scans["SCAN"]:
        # set up data and parameters for the scans query
        try:
            # try and get the scan id ref #
            scan_id = scan["REF"]
            # set the parameters for the Qualys API call
            params = {
                "action": "fetch",
                "scan_ref": scan_id,
                "mode": "extended",
                "output_format": "json_extended",
            }
            # get the scan data via API
            res = QUALYS_API.get(
                url=f"{config['qualysUrl']}/api/2.0/fo/scan/",
                headers=HEADERS,
                params=params,
            )
            # convert response to json
            if res.status_code == 200:
                try:
                    res_data = res.json()
                    scan_data[scan_id] = res_data
                except JSONDecodeError:
                    error_and_exit("Unable to convert response to JSON.")
            else:
                error_and_exit(
                    f"Received unexpected response from Qualys API: {res.status_code}: {res.text}"
                )
        except KeyError:
            # unable to get the scan id ref #
            continue
        job_progress.update(task, advance=1)
    return scan_data


def get_detailed_scans(days: int) -> list:
    """
    function to get the list of all scans from Qualys using QUALYS_API
    :param int days: # of days before today to filter scans
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: list of results from Qualys API
    :rtype: list
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])

    today = datetime.now()
    scan_date = today - timedelta(days=days)

    # set up data and parameters for the scans query
    params = {
        "action": "list",
        "scan_date_since": scan_date.strftime("%Y-%m-%d"),
        "output_format": "json",
    }
    params2 = {
        "action": "list",
        "scan_datetime_since": scan_date.strftime("%Y-%m-%dT%H:%I:%S%ZZ"),
    }
    res = QUALYS_API.get(
        url=f"{config['qualysUrl']}/api/2.0/fo/scan/summary/",
        headers=HEADERS,
        params=params,
    )
    response = QUALYS_API.get(
        url=f"{config['qualysUrl']}/api/2.0/fo/scan/vm/summary/",
        headers=HEADERS,
        params=params2,
    )
    # convert response to json
    res_data = res.json()
    try:
        response_data = xmltodict.parse(response.text)["SCAN_SUMMARY_OUTPUT"][
            "RESPONSE"
        ]["SCAN_SUMMARY_LIST"]["SCAN_SUMMARY"]
        if len(res_data) < 1:
            res_data = response_data
        else:
            res_data.extend(response_data)
    except JSONDecodeError:
        logger.error("ERROR: Unable to convert to JSON.")
    return res_data


def get_scans_summary(scan_choice: str) -> dict:
    """
    Get all scans from Qualys Host
    :param str scan_choice: The type of scan to retrieve from Qualys API
    :raises: KeyError if expected data isn't found in the Qualys API response
    :return: Detailed summary of scans from Qualys API as a dictionary
    :rtype: dict
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])

    # set up variables for function
    scan_data = {}
    responses = []
    scan_url = f"{config['qualysUrl']}/api/2.0/fo/scan/"

    # set up parameters for the scans query
    params = {"action": "list"}
    # check what scan list was requested and set urls list accordingly
    if scan_choice.lower() == "all":
        urls = [scan_url, scan_url + "compliance", scan_url + "scap"]
    elif scan_choice.lower() == "vm":
        urls = [scan_url]
    elif scan_choice.lower() in ["compliance", "scap"]:
        urls = [scan_url + scan_choice.lower()]
    # get the list of vm scans
    for url in urls:
        # get the scan data
        response = QUALYS_API.get(url=url, headers=HEADERS, params=params)
        # store response into a list
        responses.append(response)
    # check the responses received for data
    for response in responses:
        # see if response was successful
        if response.status_code == 200:
            # parse the data
            data = xmltodict.parse(response.text)["SCAN_LIST_OUTPUT"]["RESPONSE"]
            # see if the scan has any data
            try:
                # add the data to the scan_data dictionary
                scan_data.update(data["SCAN_LIST"])
            except KeyError:
                # no data found, continue the for loop
                continue
    return scan_data


def get_scan_details(days: int) -> list:
    """
    Retrieve completed scans from last x days from Qualys Host
    :param int days: # of days before today to filter scans
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :raises: KeyError if expected data isn't found in the Qualys API response
    :return: Detailed summary of scans from Qualys API as a dictionary
    :rtype: list
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])
    # get since date for API call
    since_date = datetime.now() - timedelta(days=days)
    # set up data and parameters for the scans query
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "RegScale CLI",
    }
    params = {
        "action": "list",
        "scan_date_since": since_date.strftime("%Y-%m-%d"),
        "output_format": "json",
    }
    params2 = {
        "action": "list",
        "scan_datetime_since": since_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    res = QUALYS_API.get(
        url=f"{config['qualysUrl']}/api/2.0/fo/scan/summary/",
        headers=headers,
        params=params,
    )
    response = QUALYS_API.get(
        url=f"{config['qualysUrl']}/api/2.0/fo/scan/vm/summary/",
        headers=headers,
        params=params2,
    )
    # convert response to json
    res_data = res.json()
    try:
        response_data = xmltodict.parse(response.text)["SCAN_SUMMARY_OUTPUT"][
            "RESPONSE"
        ]["SCAN_SUMMARY_LIST"]["SCAN_SUMMARY"]
        if len(res_data) < 1:
            res_data = response_data
        else:
            res_data.update(response_data)
    except JSONDecodeError as ex:
        error_and_exit(f"Unable to convert to JSON.\n{ex}")
    except KeyError:
        error_and_exit(f"No data found.\n{response.text}")
    return res_data


def sync_qualys_assets_and_vulns(
    ssp_id: int,
    create_issue: bool,
    asset_group_filter: Optional[Union[int, str]] = None,
) -> None:
    """
    Function to query Qualys and sync assets & associated vulnerabilities to RegScale
    :param int ssp_id: RegScale System Security Plan ID
    :param bool create_issue: Flag to create an issue in RegScale for each vulnerability from Qualys
    :param str asset_group_filter: Filter the Qualys assets by an asset group ID or name, if any
    :return: None
    """
    app = check_license()
    config = app.config
    regscale_api = Api(app)

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])

    # Get the assets from RegScale with the provided SSP ID
    logger.info("Getting assets from RegScale for SSP #%s...", ssp_id)
    reg_assets = lookup_reg_assets_by_parent(
        api=regscale_api, parent_id=ssp_id, module="securityplans"
    )
    logger.info(
        "Located %s asset(s) associated with SSP #%s in RegScale.",
        len(reg_assets),
        ssp_id,
    )
    logger.debug(reg_assets)

    if qualys_assets := get_qualys_assets_and_scan_results(asset_group_filter):
        logger.info("Received %s assets from Qualys.", len(qualys_assets))
        logger.debug(qualys_assets)
        # Get vulnerabilities from Qualys for the Qualys assets
        logger.info(
            "Getting vulnerabilities for %s asset(s) from Qualys...", len(qualys_assets)
        )
        qualys_assets_and_issues, total_vuln_count = get_issue_data_for_assets(
            qualys_assets
        )
        logger.info("Received %s vulnerabilities from Qualys.", total_vuln_count)
        logger.debug(qualys_assets_and_issues)
    else:
        error_and_exit("No assets found in Qualys.")

    update_assets = []
    insert_assets = []
    for (
        qualys_asset
    ) in qualys_assets:  # you can list as many input dicts as you want here
        lookup_assets = lookup_asset(reg_assets, qualys_asset["ASSET_ID"])
        # Update parent id to SSP on insert
        if len(lookup_assets) > 0:
            for asset in set(lookup_assets):
                asset.parentId = ssp_id
                asset.parentModule = "securityplans"
                asset.otherTrackingNumber = qualys_asset["ID"]
                asset.ipAddress = qualys_asset["IP"]
                asset.qualysId = qualys_asset["ASSET_ID"]
                try:
                    assert asset.id
                    # avoid duplication
                    if asset.qualysId not in [v["qualysId"] for v in update_assets]:
                        update_assets.append(asset.dict())
                except AssertionError as aex:
                    logger.error(
                        "Asset does not have an id, unable to update!\n%s", aex
                    )

    if assets_to_be_inserted := [
        qualys_asset
        for qualys_asset in qualys_assets_and_issues
        if qualys_asset["ASSET_ID"]
        not in [
            asset["ASSET_ID"]
            for asset in inner_join(reg_assets, qualys_assets_and_issues)
        ]
    ]:
        for qualys_asset in assets_to_be_inserted:
            # Do Insert
            r_asset = Asset(
                name=f'Qualys Asset #{qualys_asset["ASSET_ID"]} IP: {qualys_asset["IP"]}',
                otherTrackingNumber=qualys_asset["ID"],
                parentId=ssp_id,
                parentModule="securityplans",
                ipAddress=qualys_asset["IP"],
                assetOwnerId=config["userId"],
                assetType="Other",
                assetCategory="Hardware",
                status="Off-Network",
                qualysId=qualys_asset["ASSET_ID"],
            )
            # avoid duplication
            if r_asset.qualysId not in set(v["qualysId"] for v in insert_assets):
                insert_assets.append(r_asset.dict())
        try:
            regscale_api.update_server(
                method="post",
                url=f"{config['domain']}/api/assets",
                json_list=insert_assets,
                message=f"Inserting {len(insert_assets)} assets from Qualys to RegScale.",
            )

            logger.info("Regscale Assets successfully inserted: %i", len(insert_assets))
        except requests.exceptions.RequestException as rex:
            logger.error("Unable to Insert Qualys Assets to RegScale\n%s", rex)

    if len(update_assets) > 0:
        try:
            regscale_api.update_server(
                method="put",
                url=f"{config['domain']}/api/assets",
                json_list=update_assets,
                message=f"Updating {len(update_assets)} assets from Qualys to RegScale.",
            )
            logger.info("Regscale Assets successfully updated: %i", len(update_assets))
        except requests.RequestException as rex:
            logger.error("Unable to Update Qualys Assets to RegScale\n%s", rex)
    if create_issue:
        for asset in qualys_assets_and_issues:
            # Create issues in RegScale from Qualys vulnerabilities
            create_regscale_issue_from_vuln(
                regscale_ssp_id=ssp_id, qualys_asset=asset, vulns=asset["ISSUES"]
            )


def get_qualys_assets_and_scan_results(
    asset_group_filter: Optional[Union[int, str]] = None
) -> list:
    """
    function to gather all assets from Qualys API host along with their scan results
    :param Optional[Union[int, str]] asset_group_filter: Qualys asset group ID or name to filter by, if provided
    :return: list of dictionaries containing asset data
    :rtype: list
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])
    # set url
    url = f'{config["qualysUrl"]}api/2.0/fo/asset/host/vm/detection?action=list&show_asset_id=1'

    # check if an asset group filter was provided and append it to the url
    if asset_group_filter:
        if isinstance(asset_group_filter, str):
            # Get the asset group ID from Qualys
            url += f"&ag_titles={asset_group_filter}"
            logger.info(
                "Getting assets from Qualys by group name: %s...", asset_group_filter
            )
        else:
            url += f"&ag_ids={asset_group_filter}"
            logger.info(
                "Getting assets from from Qualys by group ID: #%s...",
                asset_group_filter,
            )
    else:
        # Get all assets from Qualys
        logger.info("Getting all assets from Qualys...")

    # get the data via Qualys API host
    response = QUALYS_API.get(url=url, headers=HEADERS)

    # parse the xml data from response.text and convert it to a dictionary
    response_data = xmltodict.parse(response.text)
    try:
        # try to extract the data from the parsed XML dictionary
        asset_data = response_data["HOST_LIST_VM_DETECTION_OUTPUT"]["RESPONSE"][
            "HOST_LIST"
        ]["HOST"]
    except KeyError:
        # if there is a KeyError set the dictionary to nothing
        asset_data = []
    # return the asset_data variable
    return asset_data


def get_issue_data_for_assets(asset_list: list) -> tuple[list, int]:
    """
    Function to get issue data from Qualys via API for assets in Qualys
    :param list asset_list: Assets and their scan results from Qualys
    :return:  Updated asset list of Qualys assets and their associated vulnerabilities, total number of vulnerabilities
    :rtype: tuple[list, int]
    """
    app = check_license()
    config = app.config

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])
    total_issues = 0

    with job_progress:
        fetching_vulns = job_progress.add_task(
            f"Getting vulnerability data from Qualys for {len(asset_list)} assets...",
            total=len(asset_list),
        )
        for asset in asset_list:
            issues = {}
            # check if the asset has any vulnerabilities
            if len(asset["DETECTION_LIST"]["DETECTION"]) > 0:
                vulns = asset["DETECTION_LIST"]["DETECTION"]
                analyzing_vulns = job_progress.add_task(
                    f"Analyzing {len(vulns)} vulnerabilities for asset #{asset['ASSET_ID']} from Qualys..."
                )
                # iterate through the vulnerabilities & verify they have a confirmed status
                for vuln in vulns:
                    if vuln["TYPE"] == "Confirmed":
                        issues[vuln["QID"]] = vuln
                    job_progress.update(analyzing_vulns, advance=1)

                maping_vulns = job_progress.add_task(
                    f"Mapping {len(issues)} vulnerabilities to Asset #{asset['ASSET_ID']} from Qualys...",
                    total=len(issues),
                )
                for issue in issues:
                    total_issues += 1
                    response = QUALYS_API.get(
                        url=f"{config['qualysUrl']}api/2.0/fo/knowledge_base/vuln?action=list&details=All&ids={issue}",
                        headers=HEADERS,
                    )
                    issues[issue]["ISSUE_DATA"] = xmltodict.parse(response.text)[
                        "KNOWLEDGE_BASE_VULN_LIST_OUTPUT"
                    ]["RESPONSE"]["VULN_LIST"]["VULN"]
                    job_progress.update(maping_vulns, advance=1)
                # add the issues to the asset's dictionary
                asset["ISSUES"] = issues
            # hide the sub-tasks
            job_progress.remove_task(analyzing_vulns)
            job_progress.remove_task(maping_vulns)

            # update the main task
            job_progress.update(fetching_vulns, advance=1)

    return asset_list, total_issues


def lookup_asset(asset_list: list, asset_id: str = None) -> list[Asset]:
    """
    Function to look up an asset in the asset list and returns an Asset object
    :param list asset_list: List of assets from RegScale
    :param str asset_id: Qualys asset ID to search for, defaults to None
    :return: list of Asset objects
    :rtype: list[Asset]
    """
    results = []
    if asset_id:
        results = [
            Asset.from_dict(asset)
            for asset in asset_list
            if asset.get("qualysId") == asset_id
        ]
    else:
        results = [Asset.from_dict(asset) for asset in asset_list]
    # Return unique list
    return list(set(results))


def map_qualys_severity_to_regscale(severity: int) -> tuple[str, str]:
    """
    Map Qualys vulnerability severity to RegScale Issue severity
    :param int severity: Qualys vulnerability severity
    :return: RegScale Issue severity and key for init.yaml
    :rtype: tuple[str, str]
    """
    if severity <= 2:
        return "III - Low - Other Weakness", "low"
    if severity == 3:
        return "II - Moderate - Reportable Condition", "moderate"
    if severity > 3:
        return "I - High - Significant Deficiency", "high"
    return "IV - Not Assigned", "low"


def create_regscale_issue_from_vuln(
    regscale_ssp_id: int, qualys_asset: dict, vulns: dict
) -> None:
    """
    Sync Qualys vulnerabilities to RegScale issues.
    :param int regscale_ssp_id: RegScale SSP ID
    :param dict qualys_asset: Qualys asset as a dictionary
    :param dict vulns: dictionary of Qualys vulnerabilities associated with the provided asset
    :return: None
    """
    app = check_license()
    config = app.config
    regscale_api = Api(app)

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])
    default_status = config["issues"]["qualys"]["status"]
    regscale_new_issues = []
    regscale_existing_issues = []
    existing_issues_req = regscale_api.get(
        url=f"{config['domain']}/api/issues/getAllByParent/{regscale_ssp_id}/securityplans"
    )
    if existing_issues_req.status_code == 200:
        regscale_existing_issues = existing_issues_req.json()

    for vuln in vulns.values():
        severity, key = map_qualys_severity_to_regscale(int(vuln["SEVERITY"]))

        default_due_delta = config["issues"]["qualys"][key]
        logger.debug("Processing vulnerability# %s", vuln["QID"])
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        due_date = datetime.strptime(vuln["LAST_FOUND_DATETIME"], fmt) + timedelta(
            days=default_due_delta
        )
        issue = Issue(
            title=vuln["ISSUE_DATA"]["TITLE"],
            description=vuln["ISSUE_DATA"]["CONSEQUENCE"]
            + "</br>"
            + vuln["ISSUE_DATA"]["DIAGNOSIS"],
            issueOwnerId=config["userId"],
            status=default_status,
            severityLevel=severity,
            qualysId=vuln["QID"],
            dueDate=due_date.strftime(fmt),
            identification="Vulnerability Assessment",
            parentId=regscale_ssp_id,
            parentModule="securityplans",
            recommendedActions=vuln["ISSUE_DATA"]["SOLUTION"],
            assetIdentifier=f'DNS: {qualys_asset["DNS"]} - IP: {qualys_asset["IP"]}',
        )
        if issue.qualysId in [iss["qualysId"] for iss in regscale_new_issues]:
            # Update
            update_issue = [
                iss for iss in regscale_new_issues if iss["qualysId"] == issue.qualysId
            ]
            if update_issue["assetIdentifier"] != issue.assetIdentifier:
                assets = set(update_issue["assetIdentifier"].split("<br>"))
                if issue.assetIdentifier not in assets:
                    update_issue["assetIdentifier"] = (
                        update_issue["assetIdentifier"] + "<br>" + issue.assetIdentifier
                    )
        else:
            if issue.qualysId not in [
                iss["qualysId"] for iss in regscale_existing_issues
            ]:
                # Add
                regscale_new_issues.append(issue.dict())
    logger.info(
        "Posting %i new issues to RegScale condensed from %i Qualys vulnerabilities.",
        len(regscale_new_issues),
        len(vulns),
    )
    if len(regscale_new_issues) > 0:
        regscale_api.update_server(
            url=f"{config['domain']}/api/issues",
            message=f"Posting {len(regscale_new_issues)} issues..",
            json_list=regscale_new_issues,
        )


def inner_join(reg_list: list, qualys_list: list) -> list:
    """
    Function to compare assets from Qualys and assets from RegScale
    :param list reg_list: list of assets from RegScale
    :param list qualys_list: list of assets from Qualys
    :return: list of assets that are in both RegScale and Qualys
    :rtype: list
    """
    set1 = set(lst.get("qualysId") for lst in reg_list)
    data = []
    try:
        data = [
            list_qualys
            for list_qualys in qualys_list
            if list_qualys.get("ASSET_ID") in set1
        ]
    except KeyError as ex:
        logger.error(ex)
    return data


def get_asset_groups_from_qualys() -> list:
    """
    Get all asset groups from Qualys via API
    :return: list of assets from Qualys
    :rtype: list
    """
    app = check_license()
    config = app.config
    asset_groups = []

    # set the auth for the QUALYS_API session
    QUALYS_API.auth = (config["qualysUserName"], config["qualysPassword"])
    response = QUALYS_API.get(
        url=f"{config['qualysUrl']}api/2.0/fo/asset/group?action=list", headers=HEADERS
    )
    if response.ok:
        logger.debug(response.text)
        try:
            asset_groups = xmltodict.parse(response.text)["ASSET_GROUP_LIST_OUTPUT"][
                "RESPONSE"
            ]["ASSET_GROUP_LIST"]["ASSET_GROUP"]
        except KeyError:
            logger.debug(response.text)
            error_and_exit(
                f"Unable to retrieve asset groups from Qualys.\nReceived: #{response.status_code}: {response.text}"
            )
    return asset_groups
