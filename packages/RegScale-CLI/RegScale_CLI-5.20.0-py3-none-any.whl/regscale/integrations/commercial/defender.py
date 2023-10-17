#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" RegScale Microsoft Defender recommendations integration"""

# standard python imports
from datetime import datetime, timedelta
from json import JSONDecodeError
from typing import Tuple

import click
import requests
from rich.console import Console

from regscale.core.app.api import Api
from regscale.core.app.internal.login import is_valid
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    check_license,
    create_progress_object,
    error_and_exit,
    flatten_dict,
    get_current_datetime,
    reformat_str_date,
    uncamel_case,
)
from regscale.core.app.utils.regscale_utils import get_issues_by_integration_field
from regscale.core.app.utils.threadhandler import create_threads, thread_assignment
from regscale.models.integration_models.recommendations import Recommendations
from regscale.models.regscale_models.issue import Issue

console = Console()
job_progress = create_progress_object()
logger = create_logger()
unique_recs = []
new_issues = []
closed = []
updated = []


######################################################################################################
#
# Adding application to Microsoft Defender API:
#   https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-create-app-webapp
# Microsoft Defender 365 APIs Docs:
#   https://learn.microsoft.com/en-us/microsoft-365/security/defender-endpoint/exposed-apis-list?view=o365-worldwide
# Microsoft Defender for Cloud API Docs:
#   https://learn.microsoft.com/en-us/rest/api/defenderforcloud/
#
######################################################################################################


@click.group()
def defender():
    """Create RegScale issues for each Microsoft Defender 365 Recommendation"""


@defender.command(name="authenticate")
@click.option(
    "--system",
    type=click.Choice(["cloud", "365"], case_sensitive=False),
    help="Pull recommendations from Microsoft Defender 365 or Microsoft Defender for Cloud.",
    prompt="Please choose a system",
    required=True,
)
def authenticate_in_defender(system: str):
    """Obtains an access token using the credentials provided in init.yaml."""
    authenticate(system=system)


@defender.command(name="sync_365_alerts")
def sync_365_alerts():
    """
    Get Microsoft Defender 365 alerts and create RegScale
    issues with the information from Microsoft Defender 365.
    """
    get_365_alerts()


@defender.command(name="sync_365_recommendations")
def sync_365_recommendations():
    """
    Get Microsoft Defender 365 recommendations and create RegScale
    issues with the information from Microsoft Defender 365.
    """
    get_365_recommendations()


@defender.command(name="sync_cloud_alerts")
def sync_cloud_alerts():
    """
    Get Microsoft Defender for Cloud alerts and create RegScale
    issues with the information from Microsoft Defender for Cloud.
    """
    get_cloud_alerts()


def authenticate(system: str) -> None:
    """
    Obtains an access token using the credentials provided in init.yaml
    :param str system:
    :return: None
    """
    app = check_license()
    api = Api(app)
    if system == "365":
        url = "https://api.securitycenter.microsoft.com/api/alerts"
    elif system == "cloud":
        url = (
            f'https://management.azure.com/subscriptions/{app.config["azureCloudSubscriptionId"]}/'
            + "providers/Microsoft.Security/alerts?api-version=2022-01-01"
        )
    else:
        error_and_exit("Please enter 365 or cloud for the system.")
    check_token(api=api, app=app, system=system, url=url)


def get_365_alerts() -> None:
    """
    Get Microsoft Defender 365 alerts and create RegScale issues based on the information from Microsoft Defender 365
    :return: None
    """
    # Get Status of Client Application
    app = check_license()
    api = Api(app)
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        error_and_exit("No init.yaml file or permission error when opening file.")
    # check if RegScale token is valid:
    if is_valid(app=app):
        url = "https://api.securitycenter.microsoft.com/api/alerts?$top=10000&$filter=status+ne+'Resolved'"

        # check the azure token, get a new one if needed
        token = check_token(api=api, app=app, system="365", url=url)

        # set headers for the data
        headers = {"Content-Type": "application/json", "Authorization": token}

        # get Microsoft Defender recommendations
        alerts = get_items_from_azure(
            api=api,
            headers=headers,
            url=url,
        )
        defender_alerts = [
            Recommendations(id=alert["id"], data=alert) for alert in alerts
        ]
        logger.info("Found %s Microsoft Defender 365 alert(s).", len(defender_alerts))

        # get all issues from RegScale where the defenderId field is populated
        issues = get_issues_by_integration_field(api=api, field="defenderAlertId")

        regscale_issues = [
            Recommendations(id=issue["id"], data=issue) for issue in issues
        ]
        # create progress bars for each threaded task
        with job_progress:
            # see if there are any issues with defender id populated
            if regscale_issues:
                logger.info(
                    "%s RegScale issue(s) will be analyzed.",
                    len(regscale_issues),
                )
                # create progress bar and analyze the RegScale issues
                analyze_regscale_issues = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(regscale_issues)} RegScale issue(s)...",
                    total=len(regscale_issues),
                )
                # evaluate open issues in RegScale:
                create_threads(
                    process=evaluate_open_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_alerts,
                        "defenderAlertId",
                        "defender365Alert",
                        analyze_regscale_issues,
                    ),
                    thread_count=len(regscale_issues),
                )
            else:
                logger.info("No issues from RegScale need to be analyzed.")
            # compare defender 365 recommendations and RegScale issues
            # while removing duplicates, updating existing RegScale Issues,
            # and adding new unique recommendations to unique_recs global variable
            if defender_alerts and regscale_issues:
                logger.info(
                    "Comparing %s Microsoft Defender 365 alert(s) and %s RegScale issue(s).",
                    len(defender_alerts),
                    len(regscale_issues),
                )
                compare_issues_and_recs = job_progress.add_task(
                    f"[#ef5d23]Comparing {len(defender_alerts)} Microsoft Defender 365 alert(s) and "
                    + f"{len(regscale_issues)} RegScale issue(s)...",
                    total=len(defender_alerts),
                )
                create_threads(
                    process=compare_recs_and_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_alerts,
                        "defenderAlertId",
                        "id",
                        "defender365Alert",
                        compare_issues_and_recs,
                    ),
                    thread_count=len(defender_alerts),
                )
            # start threads and progress bar for # of issues that need to be created
            if len(unique_recs) > 0:
                logger.warning("Creating %s issue(s) in RegScale.", len(unique_recs))
                create_issues = job_progress.add_task(
                    f"[#21a5bb]Creating {len(unique_recs)} alert(s) in RegScale...",
                    total=len(unique_recs),
                )
                create_threads(
                    process=create_issue_from_365_alert,
                    args=(api, unique_recs, config, create_issues),
                    thread_count=len(unique_recs),
                )
                logger.info(
                    "%s/%s issue(s) created in RegScale.",
                    len(unique_recs),
                    len(new_issues),
                )
        # check if issues needed to be created, updated or closed and print the appropriate message
        if (len(unique_recs) + len(updated) + len(closed)) == 0:
            console.print("[green]No changes required for existing RegScale issue(s)!")
        else:
            console.print(
                f"[red]{len(unique_recs)} issue(s) created, {len(updated)} issue(s)"
                + f" updated and {len(closed)} issue(s) were closed in RegScale."
            )
    else:
        error_and_exit(
            "Login Invalid RegScale Credentials, please login for a new token."
        )


def get_365_recommendations() -> None:
    """
    Get Microsoft Defender 365 recommendations and create RegScale issues with
    the information from Microsoft Defender 365
    :return: None
    """
    # Get Status of Client Application
    app = check_license()
    api = Api(app)
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        error_and_exit("No init.yaml file or permission error when opening file.")
    # check if RegScale token is valid:
    if is_valid(app=app):
        url = "https://api.securitycenter.microsoft.com/api/recommendations?$top=10000"

        # check the azure token, get a new one if needed
        token = check_token(api=api, app=app, system="365", url=url)

        # set headers for the data
        headers = {"Content-Type": "application/json", "Authorization": token}

        # get Microsoft Defender recommendations
        recommendations = get_items_from_azure(
            api=api,
            headers=headers,
            url=url,
        )
        defender_recs = [
            Recommendations(id=rec["id"], data=rec) for rec in recommendations
        ]
        logger.info(
            "Found %s Microsoft Defender 365 recommendation(s).", len(defender_recs)
        )

        # get all issues from RegScale where the defenderId field is populated
        issues = get_issues_by_integration_field(api=api, field="defenderId")

        regscale_issues = [
            Recommendations(id=issue["id"], data=issue) for issue in issues
        ]
        # create progress bars for each threaded task
        with job_progress:
            # see if there are any issues with defender id populated
            if regscale_issues:
                logger.info(
                    "%s RegScale issue(s) will be analyzed.",
                    len(regscale_issues),
                )
                # create progress bar and analyze the RegScale issues
                analyze_regscale_issues = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(regscale_issues)} RegScale issue(s)...",
                    total=len(regscale_issues),
                )
                # evaluate open issues in RegScale:
                create_threads(
                    process=evaluate_open_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_recs,
                        "defenderId",
                        "defender365Rec",
                        analyze_regscale_issues,
                    ),
                    thread_count=len(regscale_issues),
                )
            else:
                logger.info("No issues from RegScale need to be analyzed.")
            # compare defender 365 recommendations and RegScale issues
            # while removing duplicates, updating existing RegScale Issues,
            # and adding new unique recommendations to unique_recs global variable
            if defender_recs:
                logger.info(
                    "Comparing %s Microsoft Defender 365 recommendation(s) and %s RegScale issue(s).",
                    len(defender_recs),
                    len(regscale_issues),
                )
                compare_issues_and_recs = job_progress.add_task(
                    f"[#ef5d23]Comparing {len(defender_recs)} Microsoft Defender 365 recommendation(s) and "
                    + f"{len(regscale_issues)} RegScale issue(s)...",
                    total=len(defender_recs),
                )
                create_threads(
                    process=compare_recs_and_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_recs,
                        "defenderId",
                        "id",
                        "defender365",
                        compare_issues_and_recs,
                    ),
                    thread_count=len(defender_recs),
                )
            # start threads and progress bar for # of issues that need to be created
            if len(unique_recs) > 0:
                logger.warning("Creating %s issue(s) in RegScale.", len(unique_recs))
                create_issues = job_progress.add_task(
                    f"[#21a5bb]Creating {len(unique_recs)} issue(s) in RegScale...",
                    total=len(unique_recs),
                )
                create_threads(
                    process=create_issue_from_recommendation,
                    args=(api, unique_recs, config, create_issues),
                    thread_count=len(unique_recs),
                )
                logger.info(
                    "%s/%s issue(s) created in RegScale.",
                    len(unique_recs),
                    len(new_issues),
                )
        # check if issues needed to be created, updated or closed and print the appropriate message
        if (len(unique_recs) + len(updated) + len(closed)) == 0:
            console.print("[green]No changes required for existing RegScale issue(s)!")
        else:
            console.print(
                f"[red]{len(unique_recs)} issue(s) created, {len(updated)} issue(s)"
                + f" updated and {len(closed)} issue(s) were closed in RegScale."
            )
    else:
        error_and_exit(
            "Login Invalid RegScale Credentials, please login for a new token."
        )


def get_cloud_alerts() -> None:
    """
    Get Microsoft Defender for Cloud alerts and create RegScale issues with
    the information from Microsoft Defender for Cloud
    :return: None
    """
    # Get Status of Client Application
    app = check_license()
    api = Api(app)
    try:
        # load the config from YAML
        config = app.load_config()
    except FileNotFoundError:
        error_and_exit("No init.yaml file or permission error when opening file.")
    # check if RegScale token is valid:
    if is_valid(app=app):
        url = f'https://management.azure.com/subscriptions/{api.config["azureCloudSubscriptionId"]}/providers/Microsoft.Security/alerts?api-version=2022-01-01'

        # check the azure token, get a new one if needed
        token = check_token(api=api, app=app, system="cloud", url=url)

        # set headers for the data
        headers = {"Content-Type": "application/json", "Authorization": token}

        # get Microsoft Defender recommendations
        alerts = get_items_from_azure(
            api=api,
            headers=headers,
            url=url,
        )
        defender_alerts = [
            Recommendations(id=alert["name"], data=alert)
            for alert in alerts
            if alert["properties"]["status"] in ["Active", "In Progress"]
        ]
        logger.info(
            "Found %s Microsoft Defender for Cloud alert(s).", len(defender_alerts)
        )

        # get all issues from RegScale where the defenderCloudId field is populated
        issues = get_issues_by_integration_field(api=api, field="defenderCloudId")

        regscale_issues = [
            Recommendations(id=issue["id"], data=issue) for issue in issues
        ]
        # create progress bars for each threaded task
        with job_progress:
            # see if there are any issues with defender id populated
            if regscale_issues:
                logger.info(
                    "%s RegScale issue(s) will be analyzed.",
                    len(regscale_issues),
                )
                # create progress bar and analyze the RegScale issues
                analyze_regscale_issues = job_progress.add_task(
                    f"[#f8b737]Analyzing {len(regscale_issues)} RegScale issue(s)...",
                    total=len(regscale_issues),
                )
                # evaluate open issues in RegScale:
                create_threads(
                    process=evaluate_open_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_alerts,
                        "defenderCloudId",
                        "defenderCloud",
                        analyze_regscale_issues,
                    ),
                    thread_count=len(regscale_issues),
                )
            else:
                logger.info("No issues from RegScale need to be analyzed.")
            # compare defender for cloud alerts and RegScale issues
            # while removing duplicates, updating existing RegScale Issues,
            # and adding new unique recommendations to unique_recs global variable
            if defender_alerts and regscale_issues:
                logger.info(
                    "Comparing %s Microsoft Defender for Cloud alert(s) and %s RegScale issue(s).",
                    len(defender_alerts),
                    len(regscale_issues),
                )
                compare_issues_and_recs = job_progress.add_task(
                    f"[#ef5d23]Comparing {len(defender_alerts)} Microsoft Defender for Cloud alert(s) and "
                    + f"{len(regscale_issues)} RegScale issue(s)...",
                    total=len(defender_alerts),
                )
                create_threads(
                    process=compare_recs_and_issues,
                    args=(
                        api,
                        config,
                        regscale_issues,
                        defender_alerts,
                        "defenderCloudId",
                        "name",
                        "defenderCloud",
                        compare_issues_and_recs,
                    ),
                    thread_count=len(defender_alerts),
                )
            # start threads and progress bar for # of issues that need to be created
            if len(unique_recs) > 0:
                logger.warning("Creating %s issue(s) in RegScale.", len(unique_recs))
                create_issues = job_progress.add_task(
                    f"[#21a5bb]Creating {len(unique_recs)} issue(s) in RegScale...",
                    total=len(unique_recs),
                )
                create_threads(
                    process=create_issue_from_cloud_alert,
                    args=(api, unique_recs, config, create_issues),
                    thread_count=len(unique_recs),
                )
                logger.info(
                    "%s/%s issue(s) created in RegScale.",
                    len(unique_recs),
                    len(new_issues),
                )
        # check if issues needed to be created, updated or closed and print the appropriate message
        if (len(unique_recs) + len(updated) + len(closed)) == 0:
            console.print("[green]No changes required for existing RegScale issue(s)!")
        else:
            console.print(
                f"[red]{len(unique_recs)} issue(s) created, {len(updated)} issue(s)"
                + f" updated and {len(closed)} issue(s) were closed in RegScale."
            )
    else:
        error_and_exit(
            "Login Invalid RegScale Credentials, please login for a new token."
        )


def check_token(api, app, system: str, url: str) -> str:
    """
    Function to check if current Azure token from init.yaml is valid, if not replace it
    :param api: API object
    :param app: Application Object
    :param str system: Which system to check JWT for, either Defender 365 or Defender for Cloud
    :param str url: The URL to use for authentication
    :raises: General error if provided system is not 365 or Cloud
    :return: returns JWT for Microsoft 365 Defender or Microsoft Defender for Cloud depending on system provided
    :rtype: str
    """
    # set up variables for the provided system
    if system == "cloud":
        key = "azureCloudAccessToken"
        params = {"api-version": "2022-01-01"}
    elif system.lower() == "365":
        key = "azure365AccessToken"
        params = None
    else:
        error_and_exit(
            f"{system.title()} is not supported, only Microsoft 365 Defender and Microsoft Defender for Cloud."
        )
    current_token = app.config[key]
    # check the token if it isn't blank
    if current_token is not None:
        # set the headers
        header = {"Content-Type": "application/json", "Authorization": current_token}
        # test current token by getting recommendations
        token_pass = api.get(url=url, headers=header, params=params).status_code
        # check the status code
        if token_pass == 200:
            # token still valid, return it
            token = app.config[key]
            logger.info(
                "Current token for %s is still valid and will be used for future requests.",
                system.title(),
            )
        elif token_pass in [403]:
            # token doesn't have permissions, notify user and exit
            error_and_exit(
                "Incorrect permissions set for application. Cannot retrieve recommendations."
            )
        else:
            # token is no longer valid, get a new one
            token = get_token(api=api, app=app, system=system)
    # token is empty, get a new token
    else:
        token = get_token(api=api, app=app, system=system)
    return token


def get_token(api, app, system: str) -> str:
    """
    Function to get a token from Microsoft Azure and saves it to init.yaml
    :param api: API object
    :param app: Application object
    :param str system: Which platform to authenticate for Microsoft Defender, cloud or 365
    :raises: General error if provided system is not 365 or Cloud
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :raises: KeyError if API response doesn't contain "access_token" as a key
    :return: JWT from Azure
    :rtype: str
    """
    # set the url and body for request
    if system.lower() == "365":
        url = f'https://login.windows.net/{app.config["azure365TenantId"]}/oauth2/token'
        client_id = app.config["azure365ClientId"]
        client_secret = app.config["azure365Secret"]
        resource = "https://api.securitycenter.windows.com"
        key = "azure365AccessToken"
    elif system.lower() == "cloud":
        url = f'https://login.microsoftonline.com/{app.config["azureCloudTenantId"]}/oauth2/token'
        client_id = app.config["azureCloudClientId"]
        client_secret = app.config["azureCloudSecret"]
        resource = "https://management.azure.com"
        key = "azureCloudAccessToken"
    else:
        error_and_exit(
            f"{system.title()} is not supported, only Microsoft 365 Defender and Microsoft Defender for Cloud."
        )
    data = {
        "resource": resource,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    # get the data
    response = api.post(
        url=url,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )
    try:
        return parse_and_save_token(response, app, key, system)
    except KeyError as ex:
        # notify user we weren't able to get a token and exit
        error_and_exit(f"Didn't receive token from Azure.\n{ex}\n{response.text}")
    except JSONDecodeError as ex:
        # notify user we weren't able to get a token and exit
        error_and_exit(f"Unable to authenticate with Azure.\n{ex}\n{response.text}")


def parse_and_save_token(
    response: requests.Response, app, key: str, system: str
) -> str:
    """
    Function to parse the token from the response and save it to init.yaml
    :param requests.Response response: Response from API call
    :param app: Application object
    :param str key: Key to use for init.yaml token update
    :param str system: Which system to check JWT for, either Defender 365 or Defender for Cloud
    :return: JWT from Azure for the provided system
    :rtype: str
    """
    # try to read the response and parse the token
    res = response.json()
    token = res["access_token"]

    # add the token to init.yaml
    app.config[key] = f"Bearer {token}"

    # write the changes back to file
    app.save_config(app.config)

    # notify the user we were successful
    logger.info(
        f"Azure {system.title()} Login Successful! Init.yaml file was updated with the new access token."
    )
    # return the token string
    return app.config[key]


def get_items_from_azure(api, headers: dict, url: str) -> list:
    """
    Function to get data from Microsoft Defender returns the data as a list while handling pagination
    :param api: API object
    :param dict headers: Headers used for API call
    :param url: URL to use for the API call
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :raises: KeyError if value key is not in the API response
    :return: list of recommendations
    :rtype: list
    """
    # get the data via api call
    response = api.get(url=url, headers=headers)
    try:
        response_data = response.json()
        # try to get the values from the api response
        defender_data = response_data["value"]
    except JSONDecodeError:
        # notify user if there was a json decode error from API response and exit
        error_and_exit("JSON Decode error")
    except KeyError:
        # notify user there was no data from API response and exit
        error_and_exit(
            f"Received unexpected response from Microsoft Defender.\n{response.status_code}: {response.text}"
        )
    # check if pagination is required to fetch all data from Microsoft Defender
    next_link = response_data.get("nextLink")
    if response.status_code == 200 and next_link:
        # get the rest of the data
        defender_data.extend(
            get_items_from_azure(api=api, headers=headers, url=next_link)
        )
    # return the defender recommendations
    return defender_data


def get_due_date(score, config: dict, key: str) -> str:
    """
    Function to return due date based on the severity score of
    the Microsoft Defender recommendation; the values are in the init.yaml
    and if not, use the industry standards
    :param score: Severity score from Microsoft Defender
    :param dict config: Application config
    :param str key: The key to use for init.yaml
    :return: Due date for the issue
    :rtype: str
    """
    # check severity score and assign it to the appropriate due date
    # using the init.yaml specified days
    today = datetime.now().strftime("%m/%d/%y")

    # check if the score is a string, if so convert it to an int & determine due date
    if isinstance(score, str):
        if score.lower() == "low":
            score = 3
        elif score.lower() == "medium":
            score = 5
        elif score.lower() == "high":
            score = 9
        else:
            score = 0
    if score >= 7:
        days = config["issues"][key]["high"]
    elif 4 <= score < 7:
        days = config["issues"][key]["moderate"]
    else:
        days = config["issues"][key]["low"]
    due_date = datetime.strptime(today, "%m/%d/%y") + timedelta(days=days)
    return due_date.strftime("%Y-%m-%dT%H:%M:%S")


def format_description(rec: dict, tenant_id: str) -> str:
    """
    Function to format the provided dictionary into an HTML table
    :param dict rec: Recommendation from Microsoft Defender
    :param str tenant_id: Microsoft Azure tenant ID
    :return: HTML formatted string of the rec dictionary
    :rtype: str
    """
    # create empty dictionary to store formatted recommendation headers
    payload = {}

    try:
        # see if the item is a Microsoft Defender for Cloud alert
        url = rec["properties"]["alertUri"]
        # add the <a href> element to the url
        url = f'<a href="{url}">{url}</a>'
    except KeyError:
        # means we are formatting a Microsoft Defender 365 recommendation
        # create url to Microsoft Defender 365 recommendations, will be added to description
        url = f"https://security.microsoft.com/security-recommendations?tid={tenant_id}"
        url = f'<a href="{url}">{url}</a>'
    # remove nested dict from the provided rec
    rec = flatten_dict(data=rec)

    # keys that should be skipped during iteration
    skip_keys = ["associatedthreats", "alerturi", "investigation steps"]
    # iterate through recommendation keys and uncamel_case() them
    for key, value in rec.items():
        # remove long key prefix from flattened dictionary
        key = key.replace("propertiesExtendedProperties", "").replace("properties", "")
        # skip the keys in skip keys and anything with entities in the key
        if isinstance(value, list) and len(value) > 0 and key.lower() not in skip_keys:
            # see if the list contains dictionaries or text
            if isinstance(value[0], dict):
                data = ""
                for item in value:
                    for key, value in item.items():
                        data += f"</br>{key}: {value}"
                payload[uncamel_case(key)] = data
            elif isinstance(value[0], list):
                data = "".join("</br>".join(item) for item in value)
                payload[uncamel_case(key)] = data
            else:
                payload[uncamel_case(key)] = "</br>".join(value)
        elif key.lower() not in skip_keys and "entities" not in key.lower():
            # make sure it isn't a list with no values
            if not isinstance(value, list):
                # uncamel_case the key
                new_key = uncamel_case(key)

                # store it into our payload dictionary
                payload[new_key] = value
    # store the html data into description as an unordered html list
    description = '<table style="border: 1px solid;">'

    # iterate through payload to create a html table for description
    for key, value in payload.items():
        if value is not None and value != "":
            # see if the key is a time, reformat it to something readable
            if "time" in key.lower():
                value = reformat_str_date(value, dt_format="%b %d, %Y")
            # add the item as a html data table
            description += (
                f'<tr><td style="border: 1px solid;"><b>{key}</b></td>'
                f'<td style="border: 1px solid;">{value}</td></tr>'
            )
    # add url to recommendations
    description += (
        '<tr><td style="border: 1px solid;"><b>View in Defender</b></td>'
        f'<td style="border: 1px solid;">{url}</td></tr>'
    )
    # end the html table
    description += "</table>"

    # return the html table as a string
    return description


def compare_recs_and_issues(args: Tuple, thread: int) -> None:
    """
    Function to check for duplicates between issues in RegScale
    and recommendations/alerts from Microsoft Defender while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set local variables with the args that were passed
    api, config, issues, recommendations, key, compare_key, config_key, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(recommendations))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        rec = recommendations[threads[i]]

        # see if recommendation has been analyzed already
        if not rec.analyzed:
            # change analyzed flag
            rec.analyzed = True

            # set duplication flag to false
            dupe_check = False

            # iterate through the RegScale issues with defenderId populated
            for issue in issues:
                # check if the RegScale key == Windows Defender ID
                if issue.data[key] == rec.data[compare_key]:
                    # change the duplication flag to True
                    dupe_check = True
                    # check if the RegScale issue is closed or cancelled
                    if issue.data["status"].lower() in ["closed", "cancelled"]:
                        # reopen RegScale issue because Microsoft Defender has
                        # recommended it again
                        change_issue_status(
                            api=api,
                            config=config,
                            status=config["issues"][config_key]["status"],
                            issue=issue.data,
                            rec=rec.data,
                            rec_type=config_key,
                        )
            # check if the recommendation is a duplicate
            if dupe_check is False:
                # append unique recommendation to global unique_reqs
                unique_recs.append(rec)
        job_progress.update(task, advance=1)


def evaluate_open_issues(args: Tuple, thread: int) -> None:
    """
    function to check for Open RegScale issues against Windows
    Defender recommendations and will close the issues that are
    no longer recommended by Microsoft Defender while using threads
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up local variables from the passed args
    api, config, issues, recs, key, config_key, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(issues))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the issue for the thread for later use in the function
        issue = issues[threads[i]]

        # check if the issue has already been analyzed
        if not issue.analyzed:
            # set analyzed to true
            issue.analyzed = True

            # convert recommendations list to a dictionary
            recs_dct = {recs[i]["id"]: recs[i] for i in range(len(recs))}

            # get all the ids of the Defender Recommendations and make it a list
            vals = list(recs_dct.keys())

            # check if the RegScale defenderId was recommended by Microsoft Defender
            if issue.data[key] not in vals and issue.data["status"] not in [
                "Closed",
                "Cancelled",
            ]:
                # the RegScale issue is no longer being recommended and the issue
                # status is not closed or cancelled, we need to close the issue
                change_issue_status(
                    api=api,
                    config=config,
                    status="Closed",
                    issue=issue.data,
                    rec_type=config_key,
                )
        job_progress.update(task, advance=1)


def change_issue_status(
    api, config: dict, status: str, issue: dict, rec: dict = None, rec_type: str = None
) -> None:
    """
    Function to change a RegScale issue to the provided status
    :param api: API object
    :param dict config: Application config
    :param str status: Status to change the provided issue to
    :param dict issue: RegScale issue
    :param dict rec: Microsoft Defender recommendation, defaults to None
    :param str rec_type: The platform of Microsoft Defender (cloud or 365), defaults to None
    :return: None
    """
    # update issue last updated time, set user to current user and change status
    # to the status that was passed
    issue["lastUpdatedById"] = config["userId"]
    issue["dateLastUpdated"] = get_current_datetime("%Y-%m-%dT%H:%M:%S")
    issue["status"] = status

    # check if rec dictionary was passed, if not create it
    if rec is not None and rec_type == "defender365":
        issue["title"] = rec["recommendationName"]
        issue["description"] = format_description(
            rec=rec, tenant_id=config["azure365TenantId"]
        )
        issue["severityLevel"] = Issue.assign_severity(rec["severityScore"])
        issue["issueOwnerId"] = config["userId"]
        issue["dueDate"] = get_due_date(
            score=rec["severityScore"], config=config, key="defender365"
        )
    elif rec is not None and rec_type == "defenderCloud":
        issue["title"] = (
            f'{rec["properties"]["productName"]} Alert - {rec["properties"]["compromisedEntity"]}',
        )
        issue["description"] = format_description(
            rec=rec, tenant_id=config["azureCloudTenantId"]
        )
        issue["severityLevel"] = (Issue.assign_severity(rec["properties"]["severity"]),)
        issue["issueOwnerId"] = config["userId"]
        issue["dueDate"] = get_due_date(
            score=rec["properties"]["severity"],
            config=config,
            key="defenderCloud",
        )

    # if we are closing the issue, update the date completed
    if status.lower() == "closed":
        if rec_type in ["defender365Rec", "defender365Alert"]:
            message = "via Microsoft 365 Defender"
        elif rec_type == "defenderCloud":
            message = "via Microsoft Defender for Cloud"
        else:
            message = "via Microsoft Defender"
        issue["dateCompleted"] = get_current_datetime("%Y-%m-%dT%H:%M:%S")
        issue[
            "description"
        ] += f'<p>No longer recommended {message} as of {get_current_datetime("%b %d,%Y")}</p>'
        closed.append(issue)
    else:
        issue["dateCompleted"] = ""
        updated.append(issue)

    # use the api to change the status of the given issue
    api.put(url=f'{config["domain"]}/api/issues/{issue["id"]}', json=issue)


def create_issue_from_recommendation(args: Tuple, thread: int) -> None:
    """
    Function to utilize threading and create an issues in RegScale for the assigned thread
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up local variables from args passed
    api, recommendations, config, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(recommendations))

    # update api pool limits to max_thread count from init.yaml
    api.pool_connections = config["maxThreads"]
    api.pool_maxsize = config["maxThreads"]

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        rec = recommendations[threads[i]]

        # check if the recommendation was already created as a RegScale issue
        if not rec.created:
            # set created flag to true
            rec.created = True

            # format the description as a html table
            description = format_description(
                rec=rec.data, tenant_id=config["azure365TenantId"]
            )

            # set up the data payload for RegScale API
            issue = Issue(
                title=f'{rec.data["recommendationName"]}',
                dateCreated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
                description=description,
                severityLevel=Issue.assign_severity(rec.data["severityScore"]),
                issueOwnerId=config["userId"],
                dueDate=get_due_date(
                    score=rec.data["severityScore"], config=config, key="defender365"
                ),
                identification="Vulnerability Assessment",
                status=config["issues"]["defender365"]["status"],
                defenderId=rec.data["id"],
                vendorName=rec.data["vendor"],
                parentId=0,
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateLastUpdated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
            )
            # create issue in RegScale via api
            response = api.post(url=f'{config["domain"]}/api/issues', json=issue.dict())

            if response.status_code == 200:
                # add new issue to global list of new_issues
                new_issues.append(issue)
        job_progress.update(task, advance=1)


def create_issue_from_365_alert(args: Tuple, thread: int) -> None:
    """
    Function to utilize threading and create an issues in RegScale for the assigned thread
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up local variables from args passed
    api, recommendations, config, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(recommendations))

    # update api pool limits to max_thread count from init.yaml
    api.pool_connections = config["maxThreads"]
    api.pool_maxsize = config["maxThreads"]

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        rec = recommendations[threads[i]]

        # check if the recommendation was already created as a RegScale issue
        if not rec.created:
            # set created flag to true
            rec.created = True

            # format the description as a html table
            description = format_description(
                rec=rec.data, tenant_id=config["azure365TenantId"]
            )

            # set up the data payload for RegScale API
            issue = Issue(
                title=f'{rec.data["title"]}',
                dateCreated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
                description=description,
                severityLevel=Issue.assign_severity(rec.data["severity"]),
                issueOwnerId=config["userId"],
                dueDate=get_due_date(
                    score=rec.data["severity"], config=config, key="defender365"
                ),
                identification="Vulnerability Assessment",
                status=config["issues"]["defender365"]["status"],
                defenderAlertId=rec.data["id"],
                parentId=0,
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateLastUpdated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
            )
            # create issue in RegScale via api
            response = api.post(url=f'{config["domain"]}/api/issues', json=issue.dict())

            if response.status_code == 200:
                # add new issue to global list of new_issues
                new_issues.append(issue)
        job_progress.update(task, advance=1)


def create_issue_from_cloud_alert(args: Tuple, thread: int) -> None:
    """
    Function to utilize threading and create an issues in RegScale for the assigned thread
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up local variables from args passed
    api, alerts, config, task = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(alerts))

    # update api pool limits to max_thread count from init.yaml
    api.pool_connections = config["maxThreads"]
    api.pool_maxsize = config["maxThreads"]

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the recommendation for the thread for later use in the function
        alert = alerts[threads[i]]

        # check if the recommendation was already created as a RegScale issue
        if not alert.created:
            # set created flag to true
            alert.created = True

            # format the description as a html table
            description = format_description(
                rec=alert.data, tenant_id=config["azureCloudTenantId"]
            )
            # set up the data payload for RegScale API
            issue = Issue(
                title=f'{alert.data["properties"]["productName"]} Alert - {alert.data["properties"]["compromisedEntity"]}',
                dateCreated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
                description=description,
                severityLevel=Issue.assign_severity(
                    alert.data["properties"]["severity"]
                ),
                issueOwnerId=config["userId"],
                dueDate=get_due_date(
                    score=alert.data["properties"]["severity"],
                    config=config,
                    key="defenderCloud",
                ),
                identification="Vulnerability Assessment",
                status=config["issues"]["defenderCloud"]["status"],
                defenderCloudId=alert.data["name"],
                vendorName=alert.data["properties"]["vendorName"],
                parentId=0,
                createdById=config["userId"],
                lastUpdatedById=config["userId"],
                dateLastUpdated=get_current_datetime("%Y-%m-%dT%H:%M:%S"),
            )
            # create issue in RegScale via api
            response = api.post(url=f'{config["domain"]}/api/issues', json=issue.dict())

            if response.status_code == 200:
                # add new issue to global list of new_issues
                new_issues.append(issue)
        job_progress.update(task, advance=1)
