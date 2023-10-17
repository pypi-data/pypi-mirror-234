#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Module to allow sorting nist catalog controls into RegScale """

# standard python imports
import re
from pathlib import Path
from typing import Tuple

import click
from requests import JSONDecodeError, Response

from regscale.core.app.api import Api, normalize_url
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import (
    create_logger,
    error_and_exit,
    check_file_path,
    save_data_to,
    create_progress_object,
)
from regscale.core.app.utils.threadhandler import create_threads, thread_assignment

# initialize Application and Api objects

logger = create_logger()
job_progress = create_progress_object()

# create global variables for threads to store successful
# and failed control updates
updated_controls, failed_controls, retry_failed, retry_success = [], [], [], []


@click.group()
def nist():
    """Sort the controls of a catalog in RegScale."""


@nist.command(name="sort_control_ids")
@click.option(
    "--catalog_id",
    type=click.INT,
    help="The RegScale catalog ID number.",
    prompt="RegScale catalog ID#",
    required=True,
)
def sort_control_ids(catalog_id: int) -> None:
    """Sort the provided catalog's controls in RegScale with the provided ID #."""
    sort_controls_by_id(catalog_id)


def sort_controls_by_id(catalog_id: int) -> None:
    """
    Sort the provided catalog's controls in RegScale with the provided ID #
    :param int catalog_id: ID # of the catalog in RegScale to sort controls for
    :return: None
    """
    app = Application()
    api = Api(app)
    config = app.config
    # update api limits depending on maxThreads
    api.pool_connections = (
        config["maxThreads"]
        if api.pool_connections < config["maxThreads"]
        else api.pool_connections
    )
    api.pool_maxsize = (
        config["maxThreads"]
        if api.pool_maxsize < config["maxThreads"]
        else api.pool_maxsize
    )
    security_control_count: int = 0

    # get all controls by catalog
    url_controls_get_all = (
        f"{app.config['domain']}/api/SecurityControls/getAllByCatalog/{catalog_id}"
    )

    # get all existing control implementations
    security_control_res = api.get(url_controls_get_all)

    try:
        # try to convert the response to a JSON object
        security_control_data = security_control_res.json()
        security_control_count = len(security_control_data)
    except JSONDecodeError:
        error_and_exit(
            "Unable to retrieve control implementations for this SSP in RegScale."
        )

    # output the RegScale controls, if there are any, else exit
    if security_control_count == 0:
        # generate URL to the provided catalog id
        catalog_url = normalize_url(
            f'{app.config["domain"]}/catalogues/form/{catalog_id}'
        )
        error_and_exit(
            f"No controls were received for catalog #{catalog_id}.\nPlease verify: {catalog_url}"
        )
    # verify artifacts directory exists before saving the received security controls
    check_file_path("artifacts")
    save_data_to(
        file=Path(f"./artifacts/regscale-catalog-{catalog_id}-controls.json"),
        data=security_control_data,
    )

    # loop over the controls and add a sortId to each control
    sorted_controls: list = []
    for control in security_control_data:
        control["sortId"] = parse_control_id(control)
        sorted_controls.append(control["sortId"])

    # output the RegScale controls
    save_data_to(
        file=Path(f"artifacts/catalog-{catalog_id}-sorted-control-ids.json"),
        data=sorted_controls,
    )

    # create threads to process all controls
    with job_progress:
        logger.info(
            "%s security control(s) will be updated.",
            security_control_count,
        )
        # create progress bar and update the controls in RegScale
        updating_controls = job_progress.add_task(
            f"[#f8b737]Updating {security_control_count} security control(s)...",
            total=security_control_count,
        )
        create_threads(
            process=update_security_controls,
            args=(security_control_data, api, updating_controls, False),
            thread_count=security_control_count,
        )
    # output the result
    logger.info(
        "Updated %s/%s control(s) successfully with %s failure(s).",
        security_control_count,
        len(updated_controls),
        len(failed_controls),
    )
    # check if any controls need to be retried
    if failed_controls:
        save_data_to(
            file=Path("./artifacts/failed-controls.json"), data=failed_controls
        )
        with job_progress:
            logger.info(
                "%s security control(s) will be updated.",
                security_control_count,
            )
            # create progress bar and retry the failed controls
            retrying_controls = job_progress.add_task(
                f"[#ffff00]Retrying {len(failed_controls)} failed security control(s)...",
                total=len(failed_controls),
            )
            create_threads(
                process=update_security_controls,
                args=(failed_controls, api, retrying_controls, True),
                thread_count=len(failed_controls),
            )
        logger.info(
            "%i/%i retrie(s) were successful.", len(retry_success), len(failed_controls)
        )
        save_data_to(
            file=Path("./artifacts/retry-successful-controls.json"),
            data=retry_success,
        )
        if retry_failed:
            logger.info("%i failed retrie(s)", len(retry_failed))
            save_data_to(
                file=Path("./artifacts/retry-failed-controls.json"), data=retry_failed
            )


def update_security_controls(args: Tuple, thread: int) -> None:
    """
    Function to utilize threading and update security controls in RegScale
    :param Tuple args: Tuple of args to use during the process
    :param int thread: Thread number of current thread
    :return: None
    """
    # set up local variables from args passed
    security_control_data, api, task, retry = args

    # find which records should be executed by the current thread
    threads = thread_assignment(thread=thread, total_items=len(security_control_data))

    # iterate through the thread assignment items and process them
    for i in range(len(threads)):
        # set the control for the thread & update it in RegScale
        control = security_control_data[threads[i]]

        control_url = f'{api.config["domain"]}/api/SecurityControls/{control["id"]}'

        # check if the description is populated
        try:
            control_desc = control["description"]
        except KeyError:
            control["description"] = control["title"]
        if not control_desc:
            control["description"] = control["title"]

        # update control in RegScale
        response = api.put(control_url, json=control)

        # verify update was successful
        append_to_list(response, retry, control)
        # update progress bar
        job_progress.update(task, advance=1)


def append_to_list(response: Response, retry: bool, control: dict) -> None:
    """
    Function to append the control to the correct list based if it passed and if it was a retry
    :param Response response: The response from the update API call to RegScale
    :param bool retry: Whether this was an attempted retry for a control update in RegScale
    :param dict control: The control data to append to the correct list
    :return: None
    """
    if response.ok:
        logger.debug(
            "Success: control #%s was updated successfully.", control["sortId"]
        )
        if retry:
            retry_success.append(control)
        else:
            updated_controls.append(control)
    else:
        logger.debug(
            "Error: unable to update control #%s\n%s: %s",
            control["sortId"],
            response.status_code,
            response.text,
        )
        if retry:
            retry_failed.append(control)
        else:
            failed_controls.append(control)


def parse_control_id(control: dict) -> str:
    """
    Function to parse the provided control dictionary from RegScale and returns a sortId as a string
    :param dict control: A control from RegScale
    :return: string to use as a sortId
    :rtype: str
    """

    def _pad_zeros(match) -> str:
        """
        Function to pad zeros to the control's sortId if needed
        :param match: Match object from the regex
        :return: string to use as a sortId
        :rtype: str
        """
        prefix = match.group(1)
        digits = match.group(2)

        # Only pad with a zero if digits has a single character
        if len(digits) == 1:
            return prefix + digits.zfill(2)
        else:
            return prefix + digits

    try:
        original_id = control["sortId"]
        # remove zeros after - and before a number in the control's title
        expected_control = re.sub(
            r"(?<=-)(0+)(?=\d)", "", control["title"].split(" ")[0]
        )
        # remove zeros after - and before a number from the sortId
        formatted_original_control = re.sub(r"(?<=-)(0+)(?=\d)", "", original_id)
        # remove zeros after . and before a number from the previous formatted string
        formatted_original_control = re.sub(
            r"(?<=\.)(0+)(?=\d)", "", formatted_original_control
        )
        original_id = formatted_original_control
        # make sure the controlId is similar to the sortId
        if expected_control not in formatted_original_control:
            original_id = control["title"].split(" ")[0]
    except KeyError as err:
        # doesn't have a sortId so try to get the unique controlId
        try:
            original_id = control["controlId"]
            # verify original_id isn't blank
            if original_id == "":
                # raise a KeyError to parse title of the control name
                raise KeyError from err
        except KeyError:
            # no controlId either so parse it from the title
            original_id = control["title"].split(" ")[0]
    # return the parsed sortId
    return re.sub(r"(-|\.)0*(\d+)", _pad_zeros, original_id)
