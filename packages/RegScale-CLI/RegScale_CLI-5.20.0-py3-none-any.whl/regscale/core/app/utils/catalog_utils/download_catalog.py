#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Add functionality to download a catalog via API."""

# Standard Imports
import operator
import sys
from pathlib import Path

import click  # type: ignore
import requests  # type: ignore

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import save_data_to
from regscale.models.app_models.catalog_compare import CatalogCompare


def display_menu() -> None:
    """
    Function to display the menu for the catalog export and handle exporting the selected catalog
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
    catalog_name: str = ""
    # import master catalog list
    data = CatalogCompare.get_master_catalogs(api=api)
    # sort master catalog list
    catalogues = data["catalogues"]
    catalogues.sort(key=operator.itemgetter("id"))
    for i, catalog in enumerate(catalogues):
        print(f'{catalog["id"]}: {catalog["value"]}')
        menu_counter.append(i)
    status: bool = False
    while status is False:
        value = click.prompt(
            "Please enter the number of the catalog you would like to download",
            type=int,
        )
        if value < min(menu_counter) or value > max(menu_counter):
            print("That is not a valid selection, please try again")
        else:
            status = True
    # Choose catalog to export
    for catalog in catalogues:
        if catalog["id"] == value:
            if catalog["download"] is True and catalog["paid"] is False:
                download_url = catalog["link"]
                catalog_name = catalog["value"].replace(" ", "_")
            if catalog["download"] is True and catalog["paid"] is True:
                logger.warning(
                    "This is a paid catalog, please contact RegScale customer support."
                )
                sys.exit()
            break
    new_catalog = get_new_catalog(url=download_url)
    save_data_to(
        file=Path(f"{catalog_name}.json"),
        data=new_catalog,
    )


def get_new_catalog(url: str) -> dict:
    """
    Function to download a catalog via API call
    :param str url:
    :return: Catalog API response as a dictionary
    :rtype: dict
    """
    # call curl command to download the catalog
    response = requests.get(url, timeout=60)
    # parse into a dictionary
    new_catalog = response.json()
    # return from the function
    return new_catalog
