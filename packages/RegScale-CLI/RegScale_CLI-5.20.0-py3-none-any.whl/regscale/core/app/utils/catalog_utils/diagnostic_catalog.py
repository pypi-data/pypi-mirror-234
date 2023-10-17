#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Add functionality to diagnose catalog via API."""

# Standard Imports
import json
import operator
import sys

import click  # type: ignore
import requests  # type: ignore

from pathlib import Path
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import save_data_to
from regscale.models.app_models.catalog_compare import CatalogCompare

# pylint: disable=line-too-long


def display_menu() -> None:
    """
    Display menu for catalog diagnostic and start the diagnostic process
    :return: None
    """
    # set environment and application configuration
    app = Application()
    api = Api(app)
    api.timeout = 180

    # create logger function to log to the console
    logger = create_logger()
    menu_counter: list = []
    download_url: str = ""
    new_catalog: dict = {}
    # import master catalog list
    data = CatalogCompare.get_master_catalogs(api=api)
    # sort master catalogue list
    catalogues = data["catalogues"]
    catalogues.sort(key=operator.itemgetter("id"))
    for i, catalog in enumerate(catalogues):
        # print each catalog in the master catalog list
        print(f'{catalog["id"]}: {catalog["value"]}')
        menu_counter.append(i)
    # set status to False to run loop
    status: bool = False
    while status is False:
        # select catalog to run diagnostic
        value = click.prompt(
            "Please enter the number of the catalog you would like to run diagnostics on",
            type=int,
        )
        # check if value exist that is selected
        if value < min(menu_counter) or value > max(menu_counter):
            print("That is not a valid selection, please try again")
        else:
            status = True
    # choose catalog to run diagnostics on
    for i, catalog in enumerate(catalogues):
        if catalog["id"] == value:
            if catalog["download"] is True and catalog["paid"] is False:
                download_url = catalog["link"]
            if catalog["download"] is True and catalog["paid"] is True:
                logger.warning(
                    "This is a paid catalog, please contact RegScale customer support."
                )
                sys.exit()
            break
    # retrieve new catalog to run diagnostics on
    new_catalog = get_new_catalog(url=download_url)
    # run the diagnostic output for the selected catalog
    save_data_to(
        file=Path("diagnostics.json"),
        data=run_diagnostics(diagnose_cat=new_catalog, logger=logger).dict(),
    )


def get_new_catalog(url: str) -> dict:
    """
    Function to download a catalog
    :param str url: URL to download the catalog from
    :return: Dictionary of the catalog downloaded
    :rtype: dict
    """
    # call curl command to download the catalog
    response = requests.get(url, timeout=60)
    # parse into a dictionary
    new_catalog = response.json()
    # return from the function
    return new_catalog


def run_diagnostics(diagnose_cat: dict, logger) -> CatalogCompare:
    """
    Function to run diagnostics on a catalog
    :param dict diagnose_cat: dictionary of a catalog to run diagnostics on
    :param logger: Logger to log to the console
    :return: CatalogCompare object
    :rtype: CatalogCompare
    """
    diagnostic_results = CatalogCompare().run_new_diagnostics(diagnose_cat)

    # print information to the terminal
    logger.info("The catalog you have selected for diagnostics is:")
    logger.info(diagnostic_results.title)
    logger.info("The uuid for this catalog is:")
    logger.info(diagnostic_results.uuid)
    logger.info("The list of contained keywords in this catalog is:")
    logger.info(diagnostic_results.keywords)
    logger.info(
        f"The number of CCIs in this catalog is: {diagnostic_results.cci_count}"
    )
    logger.info(
        f"The number of Objectives in this catalog is: {diagnostic_results.objective_count}"
    )
    logger.info(
        f"The number of Parameters in this catalog is: {diagnostic_results.parameter_count}"
    )
    logger.info(
        f"The number of Security Controls in this catalog is: {diagnostic_results.security_control_count}"
    )
    logger.info(
        f"The number of Tests in this catalog is: {diagnostic_results.test_count}"
    )
    return diagnostic_results
