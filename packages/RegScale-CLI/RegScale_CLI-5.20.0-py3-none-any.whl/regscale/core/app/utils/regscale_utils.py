#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Functions used to interact with RegScale API """

# standard imports
import os
import re
from typing import Optional
from urllib.parse import urljoin

from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    error_and_exit,
    get_file_name,
    get_file_type,
)
from regscale.models.regscale_models.modules import Modules

logger = create_logger()


def send_email(api: Api, domain: str, payload: dict) -> bool:
    """
    Function to use the RegScale email API and send an email, returns bool on whether API call was successful
    :param Api api: API object
    :param str domain: RegScale URL of instance
    :param dict payload: email payload
    :return: Boolean if RegScale api was successful
    :rtype: bool
    """
    # use the api to post the dict payload passed
    response = api.post(url=f"{domain}/api/email", json=payload)
    # see if api call was successful and return boolean
    return response.status_code == 200


def update_regscale_config(str_param: str, val: any, app: Application = None) -> str:
    """
    Update config in init.yaml
    :param str str_param: config parameter to update
    :param any val: config parameter value to update
    :param app: Application object
    :return: Verification message
    :rtype: str
    """
    if not app:
        app = Application()
    config = app.config
    # update config param
    # existing params will be overwritten, new params will be added
    config[str_param] = val
    # write the changes back to file
    app.save_config(config)
    logger.debug(f"Parameter '{str_param}' set to '{val}'.")
    return "Config updated"


def create_regscale_assessment(url: str, new_assessment: dict, api: Api) -> int:
    """
    Function to create a new assessment in RegScale and returns the new assessment's ID
    :param str url: RegScale instance URL to create the assessment
    :param dict new_assessment: API assessment payload
    :param Api api: API object
    :return: New RegScale assessment ID
    :rtype: int
    """
    assessment_res = api.post(url=url, json=new_assessment)
    return assessment_res.json()["id"] if assessment_res.status_code == 200 else None


def get_issues_by_integration_field(api: Api, field: str) -> list:
    """
    Function to get the RegScale issues for the provided integration field that has data populated
    :param Api api: API Object
    :param field: Integration field to filter the RegScale issues
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: List of issues with the provided integration field populated
    :rtype: list
    """
    # set the url with the field provided
    url = f'{api.config["domain"]}/api/issues/getAllByIntegrationField/{field}'
    # get the data via API
    response = api.get(url=url)
    try:
        # try to convert the data to a json
        issues = response.json()
    except JSONDecodeError as ex:
        # unable to convert the data to a json, display error and exit
        error_and_exit(f"Unable to retrieve issues from RegScale.\n{ex}")
    # return the issues
    return issues


def verify_provided_module(module: str) -> None:
    """
    Function to check the provided module is a valid RegScale module and will display the acceptable RegScale modules
    :param str module: desired module
    :raises: General Error if the provided module is not a valid RegScale module
    :return: None
    """
    if module not in Modules().api_names():
        Modules().to_table()
        error_and_exit("Please provide an option from the Accepted Value column.")


def lookup_reg_assets_by_parent(api: Api, parent_id: int, module: str) -> list:
    """
    Function to get assets from RegScale via API with the provided System Security Plan ID
    :param Api api: API object
    :param int parent_id: RegScale System Security Plan ID
    :param str module: RegScale module
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :raises: General Error if API response is not successful
    :return: List of data returned from RegScale API
    :rtype: list
    """
    # verify provided module
    verify_provided_module(module)

    config = api.config
    regscale_assets_url = (
        f"{config['domain']}/api/assets/getAllByParent/{parent_id}/{module}"
    )
    results = []

    response = api.get(url=regscale_assets_url)
    if response.ok:
        try:
            results = response.json()
        except JSONDecodeError:
            logger.warning(
                f"No assets associated with the provided ID and module: {module} #{parent_id}."
            )
    else:
        error_and_exit(
            f"Unable to get assets from RegScale. Received:{response.status_code}\n{response.text}"
        )
    return results


def get_all_from_module(api: Api, module: str, timeout: int = 300) -> list[dict]:
    """
    Function to retrieve all records for the provided Module in RegScale via GraphQl
    :param Api api: API object
    :param str module: RegScale Module, accepts issues, assessments, and risks
    :param int timeout: Timeout for the API call, defaults to 300 seconds
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: list of objects from RegScale API of the provided module
    :rtype: list[dict]
    """
    original_timeout = api.timeout
    # adjust timeout to the provided timeout if it is greater than the default
    api.timeout = timeout if timeout > original_timeout else original_timeout

    regscale_data = []
    if module == "issues":
        from regscale.models.regscale_models.issue import Issue

        all_issues = Issue().fetch_all_issues(api.app)
        regscale_data = [issue.dict() for issue in all_issues]
    elif module == "assessments":
        from regscale.models.regscale_models.assessment import Assessment

        all_assessments = Assessment().fetch_all_assessments(api.app)
        regscale_data = [assessment.dict() for assessment in all_assessments]
    elif module == "risks":
        from regscale.models.regscale_models.risks import Risk

        all_risks = Risk().fetch_all_risks(api.app)
        regscale_data = [risk.dict() for risk in all_risks]
    else:
        logger.warning(
            "%s is not a valid module.\nPlease provide a valid module: issues, assessments, or risks.",
            module,
        )
    return regscale_data


def format_control(control: str):
    """Convert a verbose control id to a regscale friendly control id,
        e.g. AC-2 (1) becomes ac-2.1
             AC-2(1) becomes ac-2.1

    :param control: Verbose Control
    :return: RegScale friendly control
    """
    # Define a regular expression pattern to match the parts of the string
    # pattern = r'^([A-Z]{2})-(\d+)\s\((\d+)\)$'
    pattern = r"^([A-Z]{2})-(\d+)\s?\((\d+)\)$"

    # Use re.sub() to replace the matched parts of the string with the desired format
    new_string = re.sub(pattern, r"\1-\2.\3", control)

    return new_string.lower()  # Output: ac-2.1


def get_user(api: Api, user_id: str) -> list:
    """
    Function to get the provided user_id from RegScale via API
    :param Api api: API Object
    :param str user_id: the RegScale user's GUID
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: list containing the user's information
    :rtype: str
    """
    user_data = []
    try:
        url = urljoin(api.config["domain"], f"/api/accounts/find/{user_id}")
        response = api.get(url)

        if response.ok:
            user_data = response.json()
    except JSONDecodeError:
        logger.error(
            "Unable to retrieve user from RegScale for the provided user id: %s",
            user_id,
        )
    return user_data


def get_threats(api: Api) -> list:
    """
    Function to get all threats from RegScale via GraphQL
    :param Api api: API Object
    :raises: JSONDecodeError if GraphQL cannot retrieve list of threats
    :return: List containing threat descriptions
    :rtype: List
    """

    regscale_data = []
    body = """
            query {
                  threats (skip: 0, take: 50) {
                    items {
                        id
                        description
                        uuid
                        status
                        source
                        threatType
                        threatOwnerId
                        status
                        notes
                        mitigations
                        targetType
                        dateCreated
                        dateLastUpdated
                        isPublic
                        investigated
                        investigationResults
                    }
                    totalCount
                    pageInfo {
                      hasNextPage
                    }
                }
            }"""
    logger.info("Fetching full list of threats from RegScale...")

    try:
        regscale_response = api.graph(query=body)
        if regscale_response["threats"]["totalCount"] > 0:
            regscale_data = regscale_response["threats"]["items"]
    except JSONDecodeError:
        error_and_exit("Unable to retrieve full list of threats from RegScale.")
    logger.info("Retrieved %i threats from RegScale.", len(regscale_data))
    return regscale_data


def create_new_data_submodule(
    api: Api,
    parent_id: int,
    parent_module: str,
    file_path: str,
) -> Optional[dict]:
    """
    Function to create a new data record in the data submodule in RegScale
    :param Api api: API Object to post the data in RegScale
    :param int parent_id: RegScale parent ID to associate the data record
    :param str parent_module: RegScale parent module to associate the data record
    :param str file_path: Path to the file to read and upload
    :raises: General Error if the file does not exist
    :raises: JSONDecodeError if API response cannot be converted to a json object
    :return: dictionary of the posted data or None if the API call was unsuccessful
    """
    posted_data = None
    # check if the file exists
    if not os.path.isfile(file_path):
        error_and_exit(
            f"Unable to upload file because the file does not exist: {file_path}"
        )

    with open(file_path, "r", encoding="utf-8") as in_file:
        raw_xml = in_file.read()

    new_data = {
        "id": 0,
        "isPublic": True,
        "dataSource": get_file_name(file_path),
        "dataType": get_file_type(file_path)[1:].upper(),
        "rawData": raw_xml,
        "parentId": parent_id,
        "parentModule": parent_module,
    }
    # post the data to RegScale
    response = api.post(api.config["domain"] + "/api/data", json=new_data)
    if response.ok:
        try:
            posted_data = response.json()
            logger.info(
                "Successfully created data record for %s #%i in RegScale.",
                parent_module,
                parent_id,
            )
        except JSONDecodeError:
            logger.error(
                "Unable to retrieve data from RegScale for the provided data id: %s",
                parent_id,
            )
    return posted_data
