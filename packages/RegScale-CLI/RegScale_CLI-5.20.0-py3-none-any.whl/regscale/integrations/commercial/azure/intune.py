#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale Azure InTune Integration """
import multiprocessing
import re
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Tuple

import click
import inflect
from requests import Response

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    convert_datetime_to_regscale_string,
    create_progress_object,
    error_and_exit,
    get_current_datetime,
    random_hex_color,
)
from regscale.integrations.commercial.azure.common import get_token
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.issue import Issue
from regscale.validation.record import validate_regscale_object

logger = create_logger()
p = inflect.engine()


@click.group()
def intune():
    """Microsoft Azure InTune Integrations"""


@intune.command(name="sync_intune")
@click.option(
    "--regscale_parent_id",
    type=click.INT,
    required=True,
    prompt="Enter RegScale Parent ID",
    help="The ID number from RegScale of the System Security Plan",
)
@click.option(
    "--regscale_module",
    type=click.STRING,
    required=True,
    prompt="Enter RegScale Module",
    help="The module from RegScale. i.e. securityplans, components, etc.",
)
@click.option(
    "--create_issues",
    type=click.BOOL,
    required=False,
    help="Create Issues in RegScale from failed configurations in InTune.",
    default=False,
)
def sync_intune(
    regscale_parent_id: int, regscale_module: str, create_issues: bool = False
):
    """Sync Intune Alerts.
    :param regscale_ssp_id: RegScale System Security Plan ID
    :param create_issue: Create Issue in RegScale from vulnerabilities in AWS Security Hub.
    :return: dict Return AWS Assessment Report
    """
    try:
        assert validate_regscale_object(
            parent_id=regscale_parent_id, parent_module=regscale_module
        )
    except AssertionError:
        error_and_exit(
            "This RegScale object does not exist. Please check your RegScale Parent ID \
                     and Module."
        )
    sync_regscale_assets(
        regscale_parent_id=regscale_parent_id,
        regscale_module=regscale_module,
        create_issues=create_issues,
    )


def page_graph_api(api: Api, headers: dict, response: Response) -> list[dict]:
    """Page through the Graph API.
    :param api: RegScale API instance
    :param headers: A simple dictionary of headers to send
    :rtype: list[dict]
    :return: list of response data.
    """
    data = []
    if response.status_code == 200:
        data.extend(response.json()["value"])
        if "@odata.nextLink" in response.json():
            while "@odata.nextLink" in response.json():
                next_link = response.json()["@odata.nextLink"]
                response = api.get(url=next_link, headers=headers)
                data.extend(response.json()["value"])
    return data


def fetch_intune_assets(
    app: Application,
    headers: dict,
    response: Response,
    regscale_parent_id: int,
    regscale_module: str,
) -> list[Asset]:
    """Pull Azure InTune Assets from the managedDevices API.

    :param response: managedDevices response
    :param regscale_parent_id: RegScale Parent ID
    :param regscale_module: RegScale Module
    :return: A list of RegScale Assets
    """

    def check_if_phone():
        if "iphone" in device["operatingSystem"].lower():
            asset_type = "Phone"
        elif "android" in device["operatingSystem"].lower():
            asset_type = "Phone"
        elif "ipad" in device["operatingSystem"].lower():
            asset_type = "Tablet"
        else:
            asset_type = None
        return asset_type

    api = Api(app)
    asset_type = ""
    intune_assets = []
    config = app.config
    if response.status_code == 200:
        devices = page_graph_api(api=api, headers=headers, response=response)
        logger.debug(response)
        logger.info("Building RegScale Assets from %i InTune Devices...", len(devices))
        for device in devices:
            if device["operatingSystem"]:
                asset_type = check_if_phone()
            if not asset_type:
                if device["operatingSystem"] and device["operatingSystem"].lower() in [
                    "macmdm",
                    "windows",
                    "linux",
                ]:
                    if device["model"] and "vm" in device["model"].lower():
                        asset_type = "Virtual Machine"
                    else:
                        asset_type = "Laptop"
                else:
                    asset_type = "Virtual Machine"
            r_asset = Asset(
                name=device["displayName"],
                otherTrackingNumber=device["deviceId"],
                parentId=regscale_parent_id,
                parentModule=regscale_module,
                macAddress=None,
                ipAddress=None,
                manufacturer=device["manufacturer"],
                model=device["model"],
                operatingSystem=device["operatingSystem"]
                + " "
                + device["operatingSystemVersion"],
                assetOwnerId=config["userId"],
                assetType=asset_type if asset_type else "Other",
                assetCategory="Hardware",
                status="Off-Network",
                notes=f"<p>isCompliant: <strong>{device['isCompliant']}</strong><br>isManaged: "
                + f"<strong>{device['isManaged']}</strong><br>isRooted: <strong>"
                + f"{device['isRooted']}</strong><br>approximateLastSignInDateTime: <strong>"
                + f"{device['approximateLastSignInDateTime']}</strong>",
            )
            intune_assets.append(r_asset)
            logger.debug(device)
    else:
        logger.error(
            "Error fetching Intune Assets: HTTP %s, %s",
            response.status_code,
            response.reason,
        )
    return intune_assets


def query_intune_devices(api: Api, token: str) -> Tuple[Response, dict]:
    """Query Azure Intune devices.

    :param api: requests.Session instance
    :param token: Azure AD Token
    :return: Tuple containing Requests Response and headers dictionary
    :rtype: Tuple[requests.Response, dict]
    """
    url = "https://graph.microsoft.com/v1.0/devices?$top=10"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = api.get(url=url, headers=headers)
    return response, headers


def find_compliance(notes: str) -> bool:
    """
    Check if the notes field indicates compliance
    :param notes: A string containing the contents of the notes field
    :return: True if the notes field indicates compliance, False otherwise
    """

    match = re.search(r"isCompliant: <strong>(\w+)</strong>", notes)
    if match:
        is_compliant = match.group(1)
        return is_compliant.lower() == "true"
    return False


def create_or_update_issue(
    app: Application, asset: Asset, regscale_parent_id: int, regscale_module: str
) -> None:
    """
    Create or Update Issue in RegScale
    :param app: Application instance
    :param asset: RegScale Asset instance
    :param regscale_parent_id: RegScale Parent ID
    :param regscale_module: RegScale Module
    """

    severity_level = Issue.assign_severity("High")
    due_date = datetime.now() + timedelta(days=30)
    # Extract the isCompliant boolean
    is_compliant = find_compliance(notes=asset.notes)
    issue = Issue(
        title=f"{asset.name} - Intune ID: {asset.otherTrackingNumber}",
        dateCreated=get_current_datetime(),
        status="Open",
        severityLevel=severity_level,
        issueOwnerId=app.config["userId"],
        securityPlanId=regscale_parent_id
        if regscale_module == "securityplans"
        else None,
        componentId=regscale_parent_id if regscale_module == "components" else None,
        identification="Intune Compliance Check",
        dueDate=convert_datetime_to_regscale_string(due_date),
        description="Intune Compliance: Failed",  # TODO: Do we create a new issue or reopen the
        #       existing issue and data appended to the comments?
    )
    if regscale_module == "securityplans":
        existing_issues = Issue.fetch_issues_by_ssp(
            app=app, ssp_id=issue.securityPlanId
        )
    else:
        existing_issues = Issue.fetch_issues_by_parent(
            app=app, regscale_id=issue.parentId, regscale_module=issue.parentModule
        )
    issue.parentId = asset.id
    issue.parentModule = "assets"
    if [iss for iss in existing_issues if iss.title == issue.title]:
        issue_exists = True
    # TODO: Verify with Dale how to handle recurrence of findings,
    #       which would be common with this scenario.
    if is_compliant and not issue_exists:
        return
    if issue_exists:
        try:
            issue.id = [iss for iss in existing_issues if iss.title == issue.title][
                0
            ].id
            if issue.status == "Open" and is_compliant:
                # Update issue
                issue.status = "Closed"
                issue.dateCompleted = (
                    get_current_datetime() if issue.status == "Closed" else ""
                )
            logger.info('Updating issue "%s"', issue.title)
            Issue.update_issue(app=app, issue=issue)
        except ValueError as vex:
            logger.error(vex)
    else:
        logger.info('Inserting issue "%s"', issue.title)
        Issue.insert_issue(app=app, issue=issue)


def sync_regscale_assets(
    regscale_parent_id: int, regscale_module: str, create_issues: bool
) -> None:
    """
    Fetch assets from InTune and sync with RegScale
    :param regscale_parent_id: RegScale Parent ID
    :param regscale_module: RegScale Module
    :param create_issues: Create Issues in RegScale from failed configurations in InTune.
    """
    app = Application()
    api = Api(app=app)
    job_progress = create_progress_object()

    def process_futures(future_list: list[Future], task_name: str) -> None:
        """Process a list of concurrent.futures

        :param future_list: _description_
        :param task_name: _description_
        """
        for asset_future in future_list:
            # extract the asset from the future
            asset = Asset(**asset_future.result().json())
            job_progress.update(task_name, advance=1)
            if create_issues:
                existing_assets = Asset.find_assets_by_parent(
                    app=app, parent_id=regscale_parent_id, parent_module=regscale_module
                )
                asset.id = [
                    asset
                    for asset in existing_assets
                    if asset.otherTrackingNumber == asset.otherTrackingNumber
                ][0].id
                issue_futures.append(
                    executor.submit(
                        create_or_update_issue,
                        app=app,
                        asset=asset,
                        regscale_parent_id=regscale_parent_id,
                        regscale_module=regscale_module,
                    )
                )

    token = get_token(app)
    response, headers = query_intune_devices(api=api, token=token)
    assets = fetch_intune_assets(
        app=app,
        headers=headers,
        response=response,
        regscale_parent_id=regscale_parent_id,
        regscale_module=regscale_module,
    )
    existing_assets = Asset.find_assets_by_parent(
        app=app, parent_id=regscale_parent_id, parent_module=regscale_module
    )
    if not assets:
        logger.warning("No InTune Devices Found")

    with job_progress, ThreadPoolExecutor(
        max_workers=multiprocessing.cpu_count()
    ) as executor:
        insert_futures = []
        update_futures = []
        issue_futures = []
        for asset in assets:
            if asset.otherTrackingNumber not in {
                ast.otherTrackingNumber for ast in existing_assets
            }:
                logger.debug("Inserting new asset: %s", asset.otherTrackingNumber)
                insert_futures.append(
                    executor.submit(Asset.insert_asset, app=app, obj=asset)
                )
            else:
                # update id
                try:
                    asset.id = [
                        asset
                        for asset in existing_assets
                        if asset.otherTrackingNumber == asset.otherTrackingNumber
                    ][0].id
                    logger.debug(
                        "Updating existing asset: %s", asset.otherTrackingNumber
                    )
                    update_futures.append(
                        executor.submit(Asset.update_asset, app=app, obj=asset)
                    )
                except IndexError as vex:
                    logger.error(vex)

        if insert_futures:
            insert_asset_task = job_progress.add_task(
                f"[{random_hex_color()}] Inserting {len(insert_futures)} assets at the "
                + f"{p.singular_noun(regscale_module)} level...",
                total=len(insert_futures),
            )
            process_futures(future_list=insert_futures, task_name=insert_asset_task)
        if update_futures:
            update_asset_task = job_progress.add_task(
                f"[{random_hex_color()}] Updating {len(update_futures)} assets at the"
                + f" {p.singular_noun(regscale_module)} level...",
                total=len(update_futures),
            )
            process_futures(future_list=update_futures, task_name=update_asset_task)
