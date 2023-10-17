#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Tenable integration for RegScale CLI """

# standard python imports
import collections
import os
import re
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Union
from urllib.parse import urljoin

import click
import matplotlib.pyplot as plt
import pandas as pd
import requests
from pydantic import ValidationError
from requests.exceptions import RequestException
from rich.console import Console
from rich.pretty import pprint
from rich.progress import track
from tenable.io import TenableIO
from tenable.sc import TenableSC

from regscale import __version__
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_file_path,
    check_license,
    epoch_to_datetime,
    error_and_exit,
    format_dict_to_html,
    get_current_datetime,
    save_data_to,
)
from regscale.core.app.utils.regscale_utils import lookup_reg_assets_by_parent
from regscale.models.app_models.click import file_types, save_output_to
from regscale.models.integration_models.nessus import NessusReport
from regscale.models.integration_models.tenable import (
    AssetCheck,
    TenableAsset,
    TenableIOAsset,
)
from regscale.models.regscale_models import ControlImplementation
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.issue import Issue
from regscale.validation.address import validate_mac_address
from regscale.validation.record import validate_regscale_object

console = Console()

logger = create_logger()


#####################################################################################################
#
# Tenable.sc Documentation: https://docs.tenable.com/tenablesc/api/index.htm
# pyTenable GitHub repo: https://github.com/tenable/pyTenable
# Python tenable.sc documentation: https://pytenable.readthedocs.io/en/stable/api/sc/index.html
#
#####################################################################################################


# Create group to handle OSCAL processing
@click.group()
def tenable():
    """Performs actions on the Tenable APIs."""


@tenable.group(help="[BETA] Performs actions on the Tenable.io API.")
def io():
    """Performs actions on the Tenable.io API."""


@tenable.group(help="Performs actions on the Tenable.sc API. [BETA]")
def sc():
    """Performs actions on the Tenable.sc API."""


@sc.command(name="export_scans")
@save_output_to()
@file_types([".json", ".csv", ".xlsx"])
def export_scans(save_output_to: Path, file_type: str):
    """Export scans from Tenable Host to a .json, .csv or .xlsx file."""
    # get the scan results
    results = get_usable_scan_list()

    # check if file path exists
    check_file_path(save_output_to)

    # set the file name
    file_name = f"tenable_scans_{get_current_datetime('%m%d%Y')}"

    # save the data as the selected file by the user
    save_data_to(
        file=Path(f"{save_output_to}/{file_name}{file_type}"),
        data=results,
    )


def get_usable_scan_list() -> list:
    """
    Usable Scans from Tenable Host
    :return: List of scans from Tenable
    :rtype: list
    """
    results = []
    try:
        client = gen_client()
        results = client.scans.list()["usable"]
    except Exception as ex:
        logger.error(ex)
    return results


def get_detailed_scans(scan_list: list = None) -> list:
    """
    Generate list of detailed scans (Warning: this action could take 20 minutes or more to complete)
    :param list scan_list: List of scans from Tenable, defaults to usable_scan_list
    :return: Detailed list of Tenable scans
    :rtype: list
    """
    client = gen_client()
    detailed_scans = []
    for scan in track(scan_list, description="Fetching detailed scans..."):
        try:
            det = client.scans.details(id=scan["id"])
            detailed_scans.append(det)
        except RequestException as ex:  # This is the correct syntax
            raise SystemExit(ex) from ex

    return detailed_scans


@sc.command(name="save_queries")
@save_output_to()
@file_types([".json", ".csv", ".xlsx"])
def save_queries(save_output_to: Path, file_type: str):
    """Get a list of query definitions and save them as a .json, .csv or .xlsx file."""
    # get the queries from Tenable
    query_list = get_queries()

    # check if file path exists
    check_file_path(save_output_to)

    # set the file name
    file_name = f"tenable_queries_{get_current_datetime('%m%d%Y')}"

    # save the data as a .json file
    save_data_to(
        file=Path(f"{save_output_to}{os.sep}{file_name}{file_type}"),
        data=query_list,
    )


def get_queries() -> list:
    """
    List of query definitions
    :return: List of queries from Tenable
    :rtype: list
    """
    app = Application()
    tsc = gen_tsc(app.config)
    return tsc.queries.list()


@sc.command(name="query_vuln")
@click.option(
    "--query_id",
    type=click.INT,
    help="Tenable query ID to retrieve via API",
    prompt="Enter Tenable query ID",
    required=True,
)
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "--create_issue_from_recommendation",
    type=click.BOOL,
    help="Create Issue in RegScale from Vulnerability in RegScale.",
    default=False,
    required=False,
)
# Add Prompt for RegScale SSP name
def query_vuln(
    query_id: int, regscale_ssp_id: int, create_issue_from_recommendation: bool
):
    """Query Tenable vulnerabilities and sync assets to RegScale."""
    q_vuln(
        query_id=query_id,
        ssp_id=regscale_ssp_id,
        create_issue_from_recommendation=create_issue_from_recommendation,
    )


@io.command(name="sync_assets")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
# Add Prompt for RegScale SSP name
def query_assets(regscale_ssp_id: int):
    """Query Tenable Assets and sync to RegScale."""
    # Validate ssp

    if validate_regscale_security_plan(parent_id=regscale_ssp_id):
        fetch_assets(
            ssp_id=regscale_ssp_id,
        )
    else:
        raise ValueError("SSP ID does not exist in RegScale!")


def validate_regscale_security_plan(parent_id: int) -> bool:
    """
    Validate RegScale Security Plan exists
    :param parent_id: The ID number from RegScale of the System Security Plan
    :return: If API call was successful
    :rtype: bool
    """
    app = check_license()
    config = app.config
    headers = {
        "Authorization": config["token"],
    }
    url = urljoin(config["domain"], f"/api/securityplans/{parent_id}")
    response = requests.get(url, headers=headers)
    return response.ok


@io.command(name="sync_vulns")
@click.option(
    "--regscale_ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "--create_issue_from_recommendation",
    type=click.BOOL,
    help="Create RegScale issue from Tenable recommendation.",
    required=False,
)
# Add Prompt for RegScale SSP name
def query_vulns(regscale_ssp_id: int, create_issue_from_recommendation: bool = False):
    """Query Tenable Vulnerabilties and sync to RegScale."""
    # Validate ssp
    if validate_regscale_object(
        parent_id=regscale_ssp_id, parent_module="securityplans"
    ):
        sync_vulns(
            regscale_ssp_id=regscale_ssp_id,
        )
        if create_issue_from_recommendation:
            create_regscale_issue_from_vuln(regscale_ssp_id=regscale_ssp_id)
    else:
        raise ValueError("SSP ID does not exist in RegScale!")


@sc.command(name="trend_vuln")
@click.option(
    "-p",
    "--plugins",
    multiple=True,
    help="Enter one or more pluginID's separated by a space to see a trend-line. (by report date)",
    prompt="Enter one or more pluginID's",
    required=True,
)
@click.option(
    "-d",
    "--dnsname",
    multiple=False,
    type=click.STRING,
    help="Enter DNS name of asset to trend.",
    prompt="Enter DNS name of asset",
    required=True,
)
def trend_vuln(plugins: list, dnsname: str):
    """Trend vulnerabilities from vulnerability scans."""
    plugins = list(plugins)
    logger.info(plugins)
    trend_vulnerabilities(filter=plugins, dns=dnsname)


def q_vuln(query_id: int, ssp_id: int, create_issue_from_recommendation: bool) -> list:
    """
    Query Tenable vulnerabilities
    :param int query_id: Tenable query ID
    :param int ssp_id: RegScale System Security Plan ID
    :param bool create_issue_from_recommendation: Whether to create an issue in RegScale
    :raises: General error if asset doesn't have an ID
    :raises: requests.RequestException if unable to update asset via RegScale API
    :return: List of queries from Tenable
    :rtype: list
    """
    app = check_license()
    api = Api(app)
    # At SSP level, provide a list of vulnerabilities and the counts of each
    # Normalize the data based on mac address
    reg_assets = lookup_reg_assets_by_parent(
        api=api, parent_id=ssp_id, module="securityplans"
    )

    tenable_data = fetch_vulns(query_id=query_id, regscale_ssp_id=ssp_id)
    tenable_vulns = tenable_data[0]
    tenable_df = tenable_data[1]

    assets_to_be_inserted = list(
        {
            dat
            for dat in tenable_vulns
            if dat.macAddress
            not in {asset.macAddress for asset in inner_join(reg_assets, tenable_vulns)}
        }
    )
    counts = collections.Counter(s.pluginName for s in tenable_vulns)
    update_assets = []
    insert_assets = []
    for vuln in set(tenable_vulns):  # you can list as many input dicts as you want here
        vuln.count = dict(counts)[vuln.pluginName]
        lookup_assets = lookup_asset(reg_assets, vuln.macAddress, vuln.dnsName)
        # Update parent id to SSP on insert
        if len(lookup_assets) > 0:
            for asset in set(lookup_assets):
                # Do update
                # asset = reg_asset[0]
                asset.parentId = ssp_id
                asset.parentModule = "securityplans"
                asset.macAddress = vuln.macAddress.upper()
                asset.osVersion = vuln.operatingSystem
                asset.purchaseDate = "01-01-1970"
                asset.endOfLifeDate = "01-01-1970"
                if asset.ipAddress is None:
                    asset.ipAddress = vuln.ipAddress
                asset.operatingSystem = determine_os(asset.operatingSystem)
                try:
                    assert asset.id
                    # avoid duplication
                    if asset.macAddress.upper() not in {
                        v["macAddress"].upper() for v in update_assets
                    }:
                        update_assets.append(asset.dict())
                except AssertionError as aex:
                    logger.error(
                        "Asset does not have an id, unable to update!\n%s", aex
                    )

    if assets_to_be_inserted:
        for t_asset in assets_to_be_inserted:
            # Do Insert
            r_asset = Asset(
                name=t_asset.dnsName,
                otherTrackingNumber=t_asset.pluginID,
                parentId=ssp_id,
                parentModule="securityplans",
                ipAddress=t_asset.ip,
                macAddress=t_asset.macAddress,
                assetOwnerId=app.config["userId"],
                status=get_status(t_asset),
                assetType="Other",
                assetCategory="Hardware",
                operatingSystem=determine_os(t_asset.operatingSystem),
            )
            # avoid duplication
            if r_asset.macAddress.upper() not in {
                v["macAddress"].upper() for v in insert_assets
            }:
                insert_assets.append(r_asset.dict())
    try:
        headers = {
            "Authorization": app.config["token"],
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        api.update_server(
            method="post",
            headers=headers,
            url=app.config["domain"] + "/api/assets",
            json_list=insert_assets,
            message=f"Inserting {len(insert_assets)} assets from this Tenable query to RegScale.",
        )

        logger.info("RegScale Assets successfully inserted: %i.", len(insert_assets))
    except requests.exceptions.RequestException as rex:
        logger.error("Unable to Insert Tenable Assets to RegScale.\n%s", rex)
    try:
        api.update_server(
            method="put",
            url=app.config["domain"] + "/api/assets",
            json_list=update_assets,
            message=f"Updating {len(update_assets)} assets from this Tenable query to RegScale.",
        )
        logger.info("RegScale Assets successfully updated: %i.", len(update_assets))
    except requests.RequestException as rex:
        logger.error("Unable to Update Tenable Assets to RegScale.\n%s", rex)
    if create_issue_from_recommendation and not tenable_df.empty:
        today = get_current_datetime(dt_format="%Y-%m-%d")
        create_regscale_issue_from_vuln(
            regscale_ssp_id=ssp_id,
            df=tenable_df[tenable_df["report_date"] == today],
        )
    return update_assets


def determine_os(os_string: str) -> str:
    """
    Determine RegScale friendly OS name
    :param str os_string: String of the asset's OS
    :return: RegScale acceptable OS
    :rtype: str
    """
    linux_words = ["linux", "ubuntu", "hat", "centos", "rocky", "alma", "alpine"]
    if re.compile("|".join(linux_words), re.IGNORECASE).search(os_string):
        return "Linux"
    elif (os_string.lower()).startswith("windows"):
        return "Windows Server" if "server" in os_string else "Windows Desktop"
    else:
        return "Other"


def get_status(asset: TenableAsset) -> str:
    """
    Convert Tenable asset status to RegScale asset status
    :param TenableAsset asset: Asset object from Tenable
    :return: RegScale status
    :rtype: str
    """
    if asset.family.type == "active":
        return "Active (On Network)"
    return "Off-Network"  # Probably not correct


def lookup_asset(asset_list: list, mac_address: str, dns_name: str = None) -> list:
    """
    Lookup asset in Tenable and return the data from Tenable
    :param list asset_list: List of assets to lookup in Tenable
    :param str mac_address: Mac address of asset
    :param str dns_name: DNS Name of the asset, defaults to None
    :return: List of assets that fit the provided filters
    :rtype: list
    """
    results = []
    if validate_mac_address(mac_address):
        if dns_name:
            results = [
                Asset.from_dict(asset)
                for asset in asset_list
                if "macAddress" in asset
                and asset["macAddress"] == mac_address
                and asset["name"] == dns_name
                and "macAddress" in asset
                and "name" in asset
            ]
        else:
            results = [
                Asset.from_dict(asset)
                for asset in asset_list
                if asset["macAddress"] == mac_address
            ]
    # Return unique list
    return list(set(results))


def trend_vulnerabilities(
    filter: list,
    dns: str,
    filter_type="pluginID",
    filename="vulnerabilities.pkl",
) -> None:
    """
    Trend vulnerabilities data to the console
    :param list filter: Data to use for trend graph
    :param str dns: DNS to filter data
    :param str filter_type: Type of filter to apply to data
    :param str filename: Name of the file to save as
    :return: None
    """
    if not filter:
        return
    dataframe = pd.read_pickle(filename)
    dataframe = dataframe[dataframe[filter_type].isin(filter)]
    dataframe = dataframe[dataframe["dnsName"] == dns]
    unique_cols = ["pluginID", "dnsName", "severity", "report_date"]
    dataframe = dataframe[unique_cols]
    dataframe = dataframe.drop_duplicates(subset=unique_cols)
    if len(dataframe) == 0:
        error_and_exit("No Rows in Dataframe.")

    dataframe.loc[dataframe["severity"] == "Info", "severity_code"] = 0
    dataframe.loc[dataframe["severity"] == "Low", "severity_code"] = 1
    dataframe.loc[dataframe["severity"] == "Medium", "severity_code"] = 2
    dataframe.loc[dataframe["severity"] == "High", "severity_code"] = 3
    dataframe.loc[dataframe["severity"] == "Critical", "severity_code"] = 4
    # Deal with linux wayland sessions
    if "XDG_SESSION_TYPE" in os.environ and os.getenv("XDG_SESSION_TYPE") == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "wayland"
    # plotting graph
    for filt in filter:
        plt.plot(dataframe["report_date"], dataframe["severity_code"], label=filt)
    logger.info("Plotting %s rows of data.\n", len(dataframe))
    logger.info(dataframe.head())
    plt.legend()
    plt.show(block=True)


def get_existing_regscale_issues(app: Application, regscale_ssp_id: int) -> List[dict]:
    """
    Gets existing RegScale issues for a System Security Plan
    :param Application app: Application object
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :return: List of issues from RegScale
    :rtype: List[dict]
    """
    api = Api(app)
    existing_issues_req = api.get(
        app.config["domain"]
        + f"/api/issues/getAllByParent/{regscale_ssp_id}/securityplans"
    )
    if existing_issues_req.status_code == 200:
        return existing_issues_req.json()
    else:
        return []


def create_issue_from_vuln(
    app: Application, row: pd.Series, default_due_delta: int
) -> "Issue":
    """Creates an Issue object from a Tenable vulnerability

    :param Application app: Application object
    :param pd.Series row: Row of data from Tenable
    :param int default_due_delta: Default due delta
    :return: Issue object
    :rtype: Issue
    """
    default_status = app.config["issues"]["tenable"]["status"]
    fmt = "%Y-%m-%d %H:%M:%S"
    plugin_id = row["pluginID"]
    port = row["port"]
    protocol = row["protocol"]
    due_date = datetime.strptime(row["last_scan"], fmt) + timedelta(
        days=default_due_delta
    )
    if due_date < datetime.now():
        due_date = datetime.now() + timedelta(days=default_due_delta)
    if "synopsis" in row:
        title = row["synopsis"]
    return Issue(
        title=title or row["pluginName"],
        description=row["description"]
        or row["pluginName"] + f"<br>Port: {port}<br>Protocol: {protocol}",
        issueOwnerId=app.config["userId"],
        status=default_status,
        severityLevel=Issue.assign_severity(row["severity"]),
        dueDate=due_date.strftime(fmt),
        identification="Vulnerability Assessment",
        parentId=row["regscale_ssp_id"],
        parentModule="securityplans",
        pluginId=plugin_id,
        vendorActions=row["solution"],
        assetIdentifier=f'DNS: {row["dnsName"]} - IP: {row["ip"]}',
    )


def update_existing_issue(
    existing_issues: List[dict], new_issue: "Issue"
) -> List[dict]:
    """
    Updates an existing issue with new asset identifier
    :param list[dict] existing_issues: Existing issues
    :param Issue new_issue: New issue
    :return: List of issues
    :rtype: List[dict]
    """
    for issue in existing_issues:
        if issue["title"] == new_issue.title:
            assets = set(issue["assetIdentifier"].split("<br>"))
            if new_issue.assetIdentifier not in assets:
                issue["assetIdentifier"] = (
                    issue["assetIdentifier"] + "<br>" + new_issue.assetIdentifier
                )
            return existing_issues
    return existing_issues + [new_issue.dict()]


def prepare_issues_for_sync(
    app: Application, df: pd.DataFrame, regscale_ssp_id: int
) -> Tuple[List["Issue"], List["Issue"]]:
    """
    Prepares Tenable vulnerabilities for synchronization as RegScale issues
    :param Application app: Application object
    :param pd.DataFrame df: Dataframe of Tenable data
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :return: List of issues to insert, list of issues to update
    :rtype: Tuple[List[Issue], List[Issue]]
    """
    default_due_delta = app.config["issues"]["tenable"]["moderate"]
    existing_issues = get_existing_regscale_issues(app, regscale_ssp_id)
    new_issues = []
    update_issues = []
    for index, row in df.iterrows():
        if row["severity"] != "Info":
            issue = create_issue_from_vuln(app, row, default_due_delta)
            if issue.title in {iss.title for iss in new_issues}:
                # Update
                update_issues = update_existing_issue(update_issues, issue)
            elif issue.title not in {iss["title"] for iss in existing_issues}:
                # Add
                new_issues.append(issue)
    return new_issues, update_issues


def sync_issues_to_regscale(
    app: Application, new_issues: List["Issue"], update_issues: List["Issue"]
) -> None:
    """Synchronizes issues to RegScale

    :param Application app: Application object
    :param List[Issue] new_issues: New issues
    :param List[Issue] update_issues: Updated issues
    :return: None
    """
    logger = create_logger()

    if new_issues:
        logger.info(f"Inserting {len(new_issues)} new issue(s)")
        Issue.bulk_insert(app, new_issues)
        logger.info("Done!")
    else:
        logger.info("No new issues to insert")

    if update_issues:
        logger.info(f"Updating {len(update_issues)} existing issue(s)")
        Issue.bulk_update(app, update_issues)
        logger.info("Done!")
    else:
        logger.info("No issues to update")


def create_regscale_issue_from_vuln(
    regscale_ssp_id: int, df: pd.DataFrame = pd.DataFrame()
) -> None:
    """
    Sync Tenable Vulnerabilities to RegScale issues
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :param pd.Dataframe df: Pandas dataframe of Tenable data
    :return: None
    """
    app = Application()
    new_issues, update_issues = prepare_issues_for_sync(app, df, regscale_ssp_id)
    sync_issues_to_regscale(app, new_issues, update_issues)


def log_vulnerabilities(
    data: list, query_id: int, regscale_ssp_id: int
) -> pd.DataFrame:
    """
    Logs Vulnerabilities to a panda's dataframe
    :param list data: Raw data of Tenable vulnerabilities
    :param int query_id: Query ID for Tenable query
    :param int regscale_ssp_id: RegScale System Security Plan ID
    :raises: pd.errors.DataError if unable to convert data to panda's dataframe
    :return: Cleaned up data of Tenable vulnerabilities
    :rtype: pd.DataFrame
    """
    warnings.filterwarnings("ignore", category=FutureWarning)
    try:
        dataframe = pd.DataFrame([x.dict() for x in data])
        if dataframe.empty:
            return dataframe
        dataframe["query_id"] = query_id
        dataframe["regscale_ssp_id"] = regscale_ssp_id
        dataframe["first_scan"] = dataframe["firstSeen"].apply(epoch_to_datetime)
        dataframe["last_scan"] = dataframe["lastSeen"].apply(epoch_to_datetime)
        dataframe["severity"] = [d.get("name") for d in dataframe["severity"]]
        dataframe["family"] = [d.get("name") for d in dataframe["family"]]
        dataframe["repository"] = [d.get("name") for d in dataframe["repository"]]
        dataframe["report_date"] = get_current_datetime(dt_format="%Y-%m-%d")
        filename = "vulnerabilities.pkl"

        dataframe.drop_duplicates()
        if not Path(filename).exists():
            logger.info("Saving vulnerability data to %s.", filename)
        else:
            logger.info(
                "Updating vulnerabilities.pkl with the latest data from Tenable."
            )
            old_df = pd.read_pickle(filename)
            old_df = old_df[
                old_df["report_date"] != get_current_datetime(dt_format="%Y-%m-%d")
            ]
            try:
                dataframe = pd.concat([old_df, dataframe]).drop_duplicates()
            except ValueError as vex:
                logger.error("Pandas ValueError:%s.", vex)
        dataframe.to_pickle(filename)
        severity_arr = dataframe.groupby(["severity", "repository"]).size().to_frame()
        console.rule("[bold red]Vulnerability Overview")
        console.print(severity_arr)
        return dataframe

    except pd.errors.DataError as dex:
        logger.error(dex)


def fetch_assets(ssp_id: int) -> list[TenableIOAsset]:
    """Fetch assets from Tenable IO and sync to RegScale

    :param int ssp_id: RegScale System Security Plan ID
    :return: List of Tenable assets
    :rtype: list[TenableIOAsset]
    """
    app = Application()
    config = app.config
    client = gen_tio(config=config)
    assets = []
    logger.info("Fetching assets from Tenable IO...")
    for asset in client.assets.list():
        try:
            assets.append(TenableIOAsset(**asset))
        except ValidationError as vex:
            logger.error(vex)
            logger.error(asset)

    # Post or Update Assets in RegScale
    TenableIOAsset.sync_to_regscale(app=app, assets=assets, ssp_id=ssp_id)
    return assets


def fetch_vulns(
    query_id: int = 0, regscale_ssp_id: int = 0
) -> Tuple[list, pd.DataFrame]:
    """
    Fetch vulnerabilities from Tenable by query ID
    :param int query_id: Tenable query ID, defaults to 0
    :param int regscale_ssp_id: RegScale System Security Plan ID, defaults to 0
    :return: Tuple[list of vulnerabilities from Tenable, Tenable vulnerabilities as a panda's dataframe]
    :rtype: Tuple[list, pd.DataFrame]
    """
    client = gen_client()
    data = []
    if query_id:
        description = f"Fetching Vulnerabilities for Tenable query id: {query_id}."
        if client._env_base == "TSC":
            vulns = client.analysis.vulns(query_id=query_id)
            data.extend(
                TenableAsset.from_dict(vuln)
                for vuln in track(vulns, description=description, show_speed=False)
            )
            logger.info("Found %i vulnerabilities.", len(data))
    dataframe = log_vulnerabilities(
        data, query_id=query_id, regscale_ssp_id=regscale_ssp_id
    )
    return data, dataframe
    # FIXME - unsure where code should reach
    # if len(data) == 0:
    #     logger.warning("No vulnerabilities found.")
    #     sys.exit(0)
    # df = log_vulnerabilities(data, query_id=query_id, regscale_ssp_id=regscale_ssp_id)
    # return data, df


def sync_vulns(regscale_ssp_id: int = 0) -> None:
    """
    Sync Vulnerabilities
    :param int regscale_ssp_id: _description_, defaults to 0
    :return: None
    """
    app = Application()
    config = app.config
    client = gen_tio(config=config)
    vulns = client.exports.vulns()
    NessusReport.sync_to_regscale(vulns=vulns, parent_id=regscale_ssp_id)


@sc.command(name="list_tags")
def sc_tags():
    """List tags from Tenable."""
    list_tags()


def list_tags():
    """
    Query a list of tags on the server and print to console.
    :return: None
    """
    tag_list = get_tags()
    pprint(tag_list)


def get_tags() -> list:
    """
    List of Tenable query definitions
    :return: List of unique tags for Tenable queries
    :rtype: list
    """
    client = gen_client()
    logger.debug(client._env_base)
    if client._env_base == "TSC":
        return client.queries.tags()
    return list(client.tags.list())


def gen_client() -> Union[TenableIO, TenableSC]:
    """
    Return the appropriate Tenable client based on the URL.
    :return: Client type
    :rtype: Union[TenableIO, TenableSC]
    """
    app = Application()
    config = app.config
    if "cloud.tenable.com" in config["tenableUrl"]:
        return gen_tio(config)
    return gen_tsc(config)


def gen_tsc(config: dict) -> TenableSC:
    """
    Generate Tenable Object
    :return: Tenable client
    :rtype: TenableSC
    """
    if not config:
        app = Application()
        config = app.config
    return TenableSC(
        url=config["tenableUrl"],
        access_key=config["tenableAccessKey"],
        secret_key=config["tenableSecretKey"],
        vendor="RegScale, Inc.",
        product="RegScale CLI",
        build=__version__,
    )


def gen_tio(config: dict) -> TenableIO:
    """
    Generate Tenable Object
    :return: Tenable client
    :rtype: TenableSC
    """
    return TenableIO(
        url=config["tenableUrl"],
        access_key=config["tenableAccessKey"],
        secret_key=config["tenableSecretKey"],
        vendor="RegScale, Inc.",
        product="RegScale CLI",
        build=__version__,
    )


def inner_join(reg_list: list[Asset], tenable_list: list) -> list:
    """
    Function to inner join two lists on the macAddress field and returns the assets existing in RegScale and Tenable
    :param list reg_list: List of RegScale assets
    :param list tenable_list: List of Tenable assets
    :raises: KeyError if macAddress isn't a key within the tenable_list
    :return: Returns list of assets that exists in RegScale and Tenable using the mac address
    :rtype: list
    """
    set1 = {lst["macAddress"].lower() for lst in reg_list if "macAddress" in lst}
    data = []
    try:
        data = [
            list_ten for list_ten in tenable_list if list_ten.macAddress.lower() in set1
        ]
    except KeyError as ex:
        logger.error(ex)
    return data


def get_control_implementations(parent_id: int) -> list:
    """
    Gets all the control implementations.
    :param parent_id: parent control id
    :type parent_id: int
    :return: list of control implementations
    :rtype: list
    """
    app = Application()
    api = Api(app)
    url = urljoin(
        app.config.get("domain"), f"/api/controlImplementation/getAllByPlan/{parent_id}"
    )
    response = api.get(url)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()
    return []


def get_controls(catalog_id: int) -> List[Dict]:
    """
    Gets all the controls.
    :return: list of controls
    :rtype: list
    """
    app = Application()
    api = Api(app)
    url = urljoin(
        app.config.get("domain"), f"/api/SecurityControls/getList/{catalog_id}"
    )
    response = api.get(url)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()
    return []


def create_control_implementations(
    controls: list,
    parent_id: int,
    parent_module: str,
    existing_implementation_dict: Dict,
    passing_controls: Dict,
    failing_controls: Dict,
) -> List[Dict]:
    """
    Creates a list of control implementations.
    :param list controls: list of controls
    :param int parent_id: parent control id
    :param str parent_module: parent module
    :param dict existing_implementation_dict: Dictionary of existing control implementations
    :param dict passing_controls: Dictionary of passing controls
    :param dict failing_controls: Dictionary of failing controls
    :return: list of control implementations
    :rtype: list[Dict]
    """
    app = Application()
    api = Api(app)
    user_id = app.config.get("userId")
    domain = app.config.get("domain")
    control_implementations = []
    to_create = []
    to_update = []
    for control in controls:
        lower_case_control_id = control["controlId"].lower()
        status = check_implementation(
            passing_controls=passing_controls,
            failing_controls=failing_controls,
            control_id=lower_case_control_id,
        )
        if control["controlId"] not in existing_implementation_dict.keys():
            cim = ControlImplementation(
                controlOwnerId=user_id,
                dateLastAssessed=get_current_datetime(),
                status=status,
                controlID=control["id"],
                parentId=parent_id,
                parentModule=parent_module,
                createdById=user_id,
                dateCreated=get_current_datetime(),
                lastUpdatedById=user_id,
                dateLastUpdated=get_current_datetime(),
            ).dict()
            cim["controlSource"] = "Baseline"
            to_create.append(cim)

        else:
            # update existing control implementation data
            existing_imp = existing_implementation_dict.get(control["controlId"])
            existing_imp["status"] = status
            existing_imp["dateLastAssessed"] = get_current_datetime()
            existing_imp["lastUpdatedById"] = user_id
            existing_imp["dateLastUpdated"] = get_current_datetime()
            del existing_imp["createdBy"]
            del existing_imp["systemRole"]
            del existing_imp["controlOwner"]
            del existing_imp["lastUpdatedBy"]
            to_update.append(existing_imp)

    if len(to_create) > 0:
        ci_url = urljoin(domain, "/api/controlImplementation/batchCreate")
        resp = api.post(url=ci_url, json=to_create)
        if resp.ok:
            control_implementations.extend(resp.json())
            logger.info(
                f"Created {len(to_create)} Control Implementations, Successfully!"
            )
        else:
            resp.raise_for_status()
    if len(to_update) > 0:
        # print(json.dumps(to_update))
        ci_url = urljoin(domain, "/api/controlImplementation/batchUpdate")
        resp = api.post(url=ci_url, json=to_update)
        if resp.ok:
            control_implementations.extend(resp.json())
            logger.info(
                f"Updated {len(to_update)} Control Implementations, Successfully!"
            )
        else:
            resp.raise_for_status()
    return control_implementations


def check_implementation(
    passing_controls: Dict, failing_controls: Dict, control_id: str
) -> str:
    """
    Checks the status of a control implementation.
    :param dict passing_controls: Dictionary of passing controls
    :param dict failing_controls: Dictionary of failing controls
    :param str control_id: control id
    :return: status of control implementation
    :rtype: str
    """
    if control_id in passing_controls.keys():
        return "Fully Implemented"
    elif control_id in failing_controls.keys():
        return "In Remediation"
    else:
        return "Not Implemented"


def get_existing_control_implementations(parent_id: int) -> Dict:
    """
    fetch existing control implementations
    :param int parent_id: parent control id
    :return: Dictionary of existing control implementations
    :rtype: dict
    """
    app = Application()
    api = Api(app)
    domain = app.config.get("domain")
    existing_implementation_dict = {}
    get_url = urljoin(domain, f"/api/controlImplementation/getAllByPlan/{parent_id}")
    response = api.get(get_url)
    if response.ok:
        existing_control_implementations_json = response.json()
        for cim in existing_control_implementations_json:
            existing_implementation_dict[cim["controlName"]] = cim
        logger.info(
            f"Found {len(existing_implementation_dict)} existing control implementations"
        )
    elif response.status_code == 404:
        logger.info(f"No existing control implementations found for {parent_id}")
    else:
        logger.warn(f"Unable to get existing control implementations. {response.text}")

    return existing_implementation_dict


def get_matched_controls(
    tenable_controls: List[Dict], catalog_controls: List[Dict]
) -> List[Dict]:
    """
    Get controls that match between Tenable and the catalog
    :param tenable_controls: List of controls from Tenable
    :param catalog_controls: List of controls from the catalog
    :return: List of matched controls
    :rtype: List[Dict]
    """
    matched_controls = []
    for control in tenable_controls:
        formatted_control = convert_control_id(control)
        logger.info(formatted_control)
        for catalog_control in catalog_controls:
            if catalog_control["controlId"].lower() == formatted_control.lower():
                logger.info(f"Catalog Control {formatted_control} matched")
                matched_controls.append(catalog_control)
                break
    return matched_controls


def get_assessment_status_from_implementation_status(status: str) -> str:
    """
    Get the assessment status from the implementation status
    :param str status: Implementation status
    :return: Assessment status
    :rtype: str
    """
    if status == "Fully Implemented":
        return "Pass"
    elif status == "In Remediation":
        return "Fail"
    else:
        return "N/A"


def create_assessments(
    control_implementations: List[Dict],
    catalog_controls_dict: Dict,
    asset_checks: Dict[str, List[AssetCheck]],
) -> None:
    """
    Create assessments based on control implementations
    :param List[Dict] control_implementations: List of control implementations
    :param Dict catalog_controls_dict: Dictionary of catalog controls
    :param Dict[str, List[AssetCheck]] asset_checks: Asset checks data
    :return: None
    """
    app = Application()
    api = Api(app)
    user_id = app.config.get("userId")
    assessment_url = urljoin(app.config.get("domain"), "/api/assessments/batchCreate")
    assessments_to_create = []
    for cim in control_implementations:
        # logger.info(cim)
        control = catalog_controls_dict.get(cim["controlID"])
        check = asset_checks.get(control["controlId"].lower())

        assessment_result = get_assessment_status_from_implementation_status(
            cim.get("status")
        )
        summary_dict = check[0].dict() if check else dict()
        if summary_dict:
            del summary_dict["reference"]
        title = summary_dict.get("check_name") if summary_dict else control.get("title")
        html_summary = format_dict_to_html(summary_dict)
        # logger.info(html_summary)
        document_reviewed = check[0].audit_file if check else None
        check_name = check[0].check_name if check else None
        methodology = check[0].check_info if check else None
        summary_of_results = check[0].description if check else None
        uuid = (
            check[0].asset_uuid if check and check[0].asset_uuid is not None else None
        )
        title_part = f"{title} - {uuid}" if uuid else f"{title}"
        uuid_title = f"{title_part} Automated Assessment test"
        assessment = {
            "leadAssessorId": user_id,
            "title": uuid_title,
            "assessmentType": "Control Testing",
            "plannedStart": get_current_datetime(),
            "plannedFinish": get_current_datetime(),
            "status": "Complete",
            "assessmentResult": assessment_result if assessment_result else "N/A",
            "controlID": cim["id"],
            "actualFinish": get_current_datetime(),
            "assessmentReport": html_summary if html_summary else "Passed",
            "parentId": cim["id"],
            "parentModule": "controls",
            "assessmentPlan": check_name if check_name else None,
            "documentsReviewed": document_reviewed if document_reviewed else None,
            "methodology": methodology if methodology else None,
            "summaryOfResults": summary_of_results if summary_of_results else None,
        }
        assessments_to_create.append(assessment)
    assessment_response = api.post(url=assessment_url, json=assessments_to_create)
    if assessment_response.ok:
        logger.info(f"Created {len(assessment_response.json())} Assessments!")
    else:
        logger.debug(assessment_response.status_code)
        logger.error(f"Failed to insert Assessment.\n{assessment_response.text}")


def get_future_datetime() -> str:
    """
    Get a future date and time of today + 30 days as a string
    :return: Today + 30 days as a string in the format "YYYY-MM-DDTHH:MM:SSZ"
    :rtype: str
    """
    # Get the current date and time
    current_datetime = datetime.now()

    # Add 30 days to the current date and time
    future_datetime = current_datetime + timedelta(days=30)
    # Convert the datetime object to a string in the format "YYYY-MM-DDTHH:MM:SSZ"
    future_datetime_str = future_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    return future_datetime_str


def map_status(status: str) -> str:
    """
    Map the status from Tenable.io to the status in the catalog
    :param str status: The status from Tenable.io
    :return: The status in the catalog
    :rtype: str
    """
    if status == "FAILED":
        return "Fail"
    elif status == "PASSED":
        return "Pass"
    else:
        return "N/A"


def process_compliance_data(
    framework_controls: Dict,
    asset_checks: Dict,
    catalog_id: int,
    ssp_id: int,
    framework: str,
    passing_controls: Dict,
    failing_controls: Dict,
) -> None:
    """
    Processes the compliance data from Tenable.io to create control implementations for controls in frameworks.
    :param list framework_controls: List of tenable.io controls per framework.
    :param Dict asset_checks: Asset checks data.
    :param int catalog_id: The catalog id.
    :param int ssp_id: The ssp id.
    :param str framework: The framework name.
    :param Dict passing_controls: Dictionary of passing controls.
    :param Dict failing_controls: Dictionary of failing controls.
    :return: None
    """
    existing_implementation_dict = get_existing_control_implementations(ssp_id)
    catalog_controls = get_controls(catalog_id)
    matched_controls = []
    for tenable_framework, tenable_controls in framework_controls.items():
        logger.info(
            f"Found {len(tenable_controls)} controls that passed for framework: {tenable_framework}"
        )
        # logger.info(f"tenable_controls: {tenable_controls[0]}") if len(tenable_controls) >0 else None
        if tenable_framework == framework:
            matched_controls = get_matched_controls(tenable_controls, catalog_controls)

    logger.info(f"Found {len(matched_controls)} controls that matched")

    control_implementations = create_control_implementations(
        controls=matched_controls,
        parent_id=ssp_id,
        parent_module="securityplans",
        existing_implementation_dict=existing_implementation_dict,
        passing_controls=passing_controls,
        failing_controls=failing_controls,
    )

    logger.info(f"SSP now has {len(control_implementations)} control implementations")
    catalog_controls_dict = {c["id"]: c for c in catalog_controls}
    create_assessments(control_implementations, catalog_controls_dict, asset_checks)


def convert_control_id(control_id: str) -> str:
    """
    Convert the control id to a format that can be used in Tenable.io
    :param str control_id: The control id to convert
    :return: The converted control id
    :rtype: str
    """
    # Convert to lowercase
    control_id = control_id.lower()

    # Check if there's a parenthesis and replace its content
    if "(" in control_id and ")" in control_id:
        inner_value = control_id.split("(")[1].split(")")[0]
        control_id = control_id.replace(f"({inner_value})", f".{inner_value}")

    return control_id


@io.command(name="sync_compliance_controls")
@click.option(
    "--ssp_id",
    type=click.INT,
    help="The ID number from RegScale of the System Security Plan",
    prompt="Enter RegScale System Security Plan ID",
    required=True,
)
@click.option(
    "--catalog_id",
    type=click.INT,
    help="The ID number from RegScale Catalog that the System Security Plan's controls belong to",
    prompt="Enter RegScale Catalog ID",
    required=True,
)
@click.option(
    "--framework",
    required=True,
    type=click.Choice(["800-53", "800-53r5", "CSF", "800-171"], case_sensitive=True),
    help="The framework to use. from Tenable.io frameworks MUST be the same RegScale Catalog of controls",
)
def sync_compliance_data(ssp_id: int, catalog_id: int, framework: str):
    """
    Sync the compliance data from Tenable.io to create control implementations for controls in frameworks.
    """
    _sync_compliance_data(ssp_id=ssp_id, catalog_id=catalog_id, framework=framework)


def _sync_compliance_data(ssp_id: int, catalog_id: int, framework: str) -> None:
    """
    Sync the compliance data from Tenable.io to create control implementations for controls in frameworks
    :param int ssp_id: The ID number from RegScale of the System Security Plan
    :param int catalog_id: The ID number from RegScale Catalog that the System Security Plan's controls belong to
    :param str framework: The framework to use. from Tenable.io frameworks MUST be the same RegScale Catalog of controls
    :return: None
    """
    logger.info("Note: This command only available for Tenable.io")
    logger.info("Note: This command Requires admin access.")
    app = Application()
    config = app.config
    # we specifically don't gen client here, so we only get the client for Tenable.io as its only supported there
    client = TenableIO(
        url="https://cloud.tenable.com",
        access_key=config["tenableAccessKey"],
        secret_key=config["tenableSecretKey"],
        vendor="RegScale, Inc.",
        product="RegScale CLI",
        build=__version__,
    )

    dict_of_frameworks_and_asset_checks: Dict = dict()
    framework_controls: Dict[str, List[str]] = {}
    asset_checks: Dict[str, List[AssetCheck]] = {}
    passing_controls: Dict = dict()
    # partial_passing_controls: Dict = dict()
    failing_controls: Dict = dict()
    for findings in client.exports.compliance():
        asset_check = AssetCheck(**findings)
        for ref in asset_check.reference:
            if ref.framework not in framework_controls:
                framework_controls[ref.framework] = []
            if (
                ref.control not in framework_controls[ref.framework]
            ):  # Avoid duplicate controls
                framework_controls[ref.framework].append(ref.control)
                formatted_control_id = convert_control_id(ref.control)
                # sort controls by status
                add_control_to_status_dict(
                    control_id=formatted_control_id,
                    status=asset_check.status,
                    dict_obj=failing_controls,
                    desired_status="FAILED",
                )
                add_control_to_status_dict(
                    control_id=formatted_control_id,
                    status=asset_check.status,
                    dict_obj=passing_controls,
                    desired_status="PASSED",
                )
                remove_passing_controls_if_in_failed_status(
                    passing=passing_controls, failing=failing_controls
                )
                if formatted_control_id not in asset_checks:
                    asset_checks[formatted_control_id] = [asset_check]
                else:
                    asset_checks[formatted_control_id].append(asset_check)
        for key in framework_controls.keys():
            dict_of_frameworks_and_asset_checks[key] = {
                "controls": framework_controls,
                "asset_checks": asset_checks,
            }
    logger.info(f"Found {len(dict_of_frameworks_and_asset_checks)} findings to process")
    framework_data = dict_of_frameworks_and_asset_checks[framework]
    if framework_data:
        process_compliance_data(
            framework_controls=framework_data["controls"],
            asset_checks=framework_data["asset_checks"],
            catalog_id=catalog_id,
            ssp_id=ssp_id,
            framework=framework,
            passing_controls=passing_controls,
            failing_controls=failing_controls,
        )


def add_control_to_status_dict(
    control_id: str, status: str, dict_obj: Dict, desired_status: str
) -> None:
    """
    Add a control to a status dictionary.
    :param str control_id: The control id to add to the dictionary.
    :param str status: The status of the control.
    :param dict dict_obj: The dictionary to add the control to.
    :param str desired_status: The desired status of the control.
    :return: None
    """
    friendly_control_id = control_id.lower()
    if status == desired_status:
        if friendly_control_id not in dict_obj:
            dict_obj[friendly_control_id] = desired_status


def remove_passing_controls_if_in_failed_status(passing: Dict, failing: Dict) -> None:
    """
    Remove passing controls if they are in failed status.
    :param passing: Dictionary of passing controls.
    :param failing: Dictionary of failing controls.
    :return: None
    """
    to_remove = []
    for k in passing.keys():
        if k in failing.keys():
            to_remove.append(k)

    for k in to_remove:
        del passing[k]
