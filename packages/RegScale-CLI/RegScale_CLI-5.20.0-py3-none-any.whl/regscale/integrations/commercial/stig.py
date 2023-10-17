#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

"""STIG CLI"""

import os
import re
import shutil
import tempfile
import zipfile
from json import dump, load
from pathlib import Path
from typing import Dict, List, Tuple

import click
import pandas as pd
from bs4 import BeautifulSoup

from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import check_license, download_file
from regscale.models.integration_models.stig import STIG
from regscale.validation.record import validate_regscale_object

logger = create_logger(propagate=True)
DATA_CCI = Path("assets") / "data_cci.json"


@click.group()
def stig():
    """Performs STIG processing operations"""
    check_license()


@stig.command(name="update_cci_mapping")
def update_cci_mapping():
    """Update the DISA CCI Mapping files (requires internet connection)"""
    cci_control_mapping(force=True)


@stig.command(name="process_stig")
@click.option(
    "--folder_path",
    prompt="Enter the folder path of the STIGs to process",
    help="RegScale will process and load the STIGs",
    type=click.Path(exists=True),
)
@click.option(
    "--regscale_ssp_id",
    prompt="Enter the Security Plan ID to associate result",
    type=click.INT,
    required=True,
    help="The Security Plan ID # in RegScale to associate results.",
)
@click.option(
    "--regscale_dod_catalog_id",
    type=click.INT,
    required=False,
    default=None,
    help="Enter DOD Catalog ID (Optional)",
)
def process_stig(
    folder_path: click.Path,
    regscale_ssp_id: click.INT,
    regscale_dod_catalog_id: click.INT,
):
    """Parse CKL Files from a given folder and Create RegScale Issues"""
    cat = True
    ssp = validate_regscale_object(regscale_ssp_id, "securityplans")
    if regscale_dod_catalog_id:
        cat = validate_regscale_object(regscale_dod_catalog_id, "catalogues")
    if not ssp:
        raise ValueError(f"Invalid SSP ID #{regscale_ssp_id}")
    if not cat:
        raise ValueError(f"Invalid DOD Catalog ID #{regscale_dod_catalog_id}")
    STIG(
        folder_path=folder_path,
        regscale_ssp_id=regscale_ssp_id,
        cci_mapping=cci_control_mapping(),
        regscale_dod_catalog_id=regscale_dod_catalog_id,
    )


def extract_data_from_html(
    html_doc: str, revision: str
) -> Tuple[Dict[str, List[Dict[str, str]]], Dict[str, List[Dict[str, str]]]]:
    """Extracts CCI mappings from an HTML file and returns them as two dictionaries"""
    data_ctl = {}
    data_cci = {}
    with open(Path("./assets") / html_doc, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    for resultset in [tag.select("tr") for tag in soup.select("table")[1:]]:  # tbody
        dat = {
            tag.select("td")[1].get_text().split(":")[2].strip()
            for tag in resultset
            if revision in tag.select("td")[1].get_text()
        }
        try:
            if dat:
                ctl_id = dat.pop()
                cci_id = resultset[0].select("td")[1].get_text()
                ctl_id_parse = re.match(r"^([A-Z][A-Z]-[0-9])(.*)", ctl_id)
                ctl_id_main = ctl_id_parse.group(1)
                ctl_id_parts = ctl_id_parse.group(2).lstrip(" ").replace(" ", ".")
                ctl_id_v1 = f"{ctl_id_main}{ctl_id_parts}"
                ctl_id_oscal = f"{ctl_id_main.lower()}{ctl_id_parts.lower()}"
                cci_text = resultset[2].select("td")[1].get_text()
                # Build custom dicts
                data_dict = {
                    "ctl_id": ctl_id,
                    "ctl_id_main": ctl_id_main,
                    "ctl_id_parts": ctl_id_parts,
                    "ctl_id_v1": ctl_id_v1,
                    "ctl_id_oscal": ctl_id_oscal,
                    "cci_id": cci_id,
                    "cci_text": cci_text,
                }
                if ctl_id in data_ctl:
                    data_ctl[ctl_id].append(data_dict)
                else:
                    data_ctl[ctl_id] = [data_dict]
                if cci_id in data_cci:
                    data_cci[cci_id].append(data_dict)
                else:
                    data_cci[cci_id] = [data_dict]
        except Exception as ex:
            logger.error(ex)
    return data_ctl, data_cci


def extract_data_from_spreadsheet(
    spreadsheet_file: str,
) -> Dict[str, List[Dict[str, str]]]:
    """Extracts CCI mappings from an Excel spreadsheet and returns them as a dictionary"""
    nist_cci_to_ctl_map = {}
    file_name = os.path.join("assets", spreadsheet_file)
    df_dict = pd.read_excel(file_name, header=1)
    for _, row in df_dict.iterrows():
        if isinstance(row.get("index"), float):
            continue
        cci_id = row.get("CCI", "")
        ctl_id = row.get("index", "")
        try:
            ctl_id_parse = re.match(r"^([A-Z][A-Z]-[0-9])(.*)", ctl_id)
            ctl_id_main = ctl_id_parse.group(1)
            ctl_id_parts = ctl_id_parse.group(2).lstrip(" ").replace(" ", ".")
            ctl_id_v1 = f"{ctl_id_main}{ctl_id_parts}"
            ctl_id_oscal = f"{ctl_id_main.lower()}{ctl_id_parts.lower()}"
        except AttributeError:
            ctl_id_parse = "missing"
            ctl_id_main = "missing"
            ctl_id_parts = "missing"
            ctl_id_v1 = "missing"
            ctl_id_oscal = "missing"
        cci_text = row.get("/cci_items/cci_item/definition", "")
        contributor = row.get("contributor", "")
        item = row.get("Item", "")
        row_dict = {
            "ctl_id": ctl_id,
            "ctl_id_main": ctl_id_main,
            "ctl_id_parts": ctl_id_parts,
            "ctl_id_v1": ctl_id_v1,
            "ctl_id_oscal": ctl_id_oscal,
            "cci_id": cci_id,
            "cci_text": cci_text,
            "contributor": contributor,
            "item": item,
        }
        if cci_id in nist_cci_to_ctl_map:
            nist_cci_to_ctl_map[cci_id].append(row_dict)
        else:
            nist_cci_to_ctl_map[cci_id] = [row_dict]
    return nist_cci_to_ctl_map


def add_missing_ccis(
    data_cci: Dict[str, List[Dict[str, str]]],
    nist_cci_to_ctl_map: Dict[str, List[Dict[str, str]]],
) -> None:
    """Adds missing CCIs to the data_cci dictionary"""
    auth_cci_list = nist_cci_to_ctl_map.keys()
    missing_cci = []
    for cci_id in auth_cci_list:
        if cci_id in data_cci:
            pass
        else:
            logger.debug("cci_id %s not found in data_cci", cci_id)
            missing_cci.append(cci_id)
            data_cci[cci_id] = nist_cci_to_ctl_map[cci_id]


def update_mapping() -> dict:
    """Convert CCI source mapping to friendly dictionary format

    :return: A dictionary of CCI mappings
    """
    _, data_cci = extract_data_from_html(
        "U_CCI_List.html", "NIST SP 800-53 Revision 4 (v4)"
    )
    nist_cci_to_ctl_map = extract_data_from_spreadsheet(
        "stig-mapping-to-nist-800-53.xlsx"
    )
    add_missing_ccis(data_cci, nist_cci_to_ctl_map)
    with open(DATA_CCI, "w+", encoding="utf-8") as file:
        logger.info("Updating %s...", DATA_CCI.resolve())
        dump(data_cci, file)
    return data_cci


def cci_control_mapping(
    save_path="./assets/U_CCI_List.html", force: bool = False
) -> dict:
    """Pull CCI Controls from DOD source, saved to assets.

    :param str save_path: The save path of the file, defaults to "./assets/U_CCI_List.html"
    :param bool force: Force a rebuild, even if file exists, defaults to False
    :return: A dictionary of the CCI to Control mapping.
    :rtype: dict
    """
    # https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_CCI_List.zip
    if not Path(save_path).parent.exists():
        os.mkdir(Path(save_path).parent)
    dl_path = tempfile.gettempdir() + os.sep + "U_CCI_List.html"
    xl_path = Path(save_path).parent / "stig-mapping-to-nist-800-53.xlsx"
    if not xl_path.exists() or force:
        # download cci html file
        mapping_url = "https://csrc.nist.gov/csrc/media/projects/forum/documents/stig-mapping-to-nist-800-53.xlsx"
        xl_path.touch()
        download_file(url=mapping_url, download_path=str(Path(save_path).parent))
    if not Path(save_path).exists() or force:
        url = "https://dl.dod.cyber.mil/wp-content/uploads/stigs/zip/U_CCI_List.zip"
        # download cci html file
        file = download_file(url=url, download_path=tempfile.gettempdir(), verify=False)
        with zipfile.ZipFile(file, "r") as zip_ref:
            zip_ref.extractall(tempfile.gettempdir())
            shutil.copy(dl_path, save_path)
    if not DATA_CCI.exists() or force:
        mapping = update_mapping()
    else:
        with open(DATA_CCI, encoding="utf-8") as json_file:
            mapping = load(json_file)
    return mapping
