#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel
from requests import Response

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import convert_datetime_to_regscale_string


class Scan(BaseModel):
    id: int
    uuid: Optional[str]
    scanningTool: Optional[str]
    tenableId: Optional[str]
    scanDate: Optional[str]
    scannedIPs: Optional[int]
    checks: Optional[int]
    vInfo: Optional[int]
    vLow: Optional[int]
    vMedium: Optional[int]
    vHigh: Optional[int]
    vCritical: Optional[int]
    parentId: Optional[int]
    parentModule: Optional[str]
    createdById: Optional[str]
    lastUpdatedById: Optional[str]
    isPublic: Optional[bool] = True
    dateCreated: Optional[str] = ""
    tenantsId: Optional[int] = 0

    def __hash__(self) -> int:
        """
        Hash items in Scan class
        :return: Hashed Scan
        :rtype: int
        """
        return hash((self.tenableId, self.parentId, self.parentModule))

    def __eq__(self, other) -> bool:
        """
        Update items in TenableAsset class
        :param other:
        :return: Updated Asset
        :rtype: bool
        """
        if isinstance(other, Scan):
            return (
                self.tenableId == other.tenableId
                and self.parentId == other.parentId
                and self.parentModule == other.parentModule
            )

        return (
            self.tenableId == other["tenableId"]
            and self.parentId == other["parentId"]
            and self.parentModule == other["parentModule"]
        )

    @staticmethod
    def post_scan(app: Application, api: Api, scan: "Scan") -> "Scan":
        """Post a Scan to RegScale.

        :param Application app: Application Instance
        :param Api api: Api Instance
        :param Scan scan: Scan Object
        :return: RegScale Scan
        :rtype: Scan
        """
        logger = create_logger()
        res = api.post(url=app.config["domain"] + "/api/scanhistory", json=scan.dict())
        if res.status_code != 200:
            logger.error(res)
        return Scan(**res.json())

    @staticmethod
    def group_vulns_by_severity(associated_vulns: List[dict]) -> Dict[str, List[dict]]:
        """Groups vulnerabilities by severity

        :param List[dict] associated_vulns: A list of associated vulnerabilities
        :return: Dictionary of vulnerabilities grouped by severity
        :rtype: Dict[str, List[dict]]
        """
        return {
            vuln["severity"]: [
                v for v in associated_vulns if v["severity"] == vuln["severity"]
            ]
            for vuln in associated_vulns
        }

    @staticmethod
    def get_existing_scan_history(app: Application, reg_asset: dict) -> List[dict]:
        """Gets existing scan history for a RegScale asset

        :param Application app: Application Instance
        :param dict reg_asset: RegScale Asset
        :return: List of existing scan history
        :rtype: List[dict]
        """
        api = Api(app)
        res = api.get(
            url=app.config["domain"]
            + f"/api/scanhistory/getAllByParent/{reg_asset.id}/assets"
        )
        if not res.raise_for_status():
            return res.json()

    @staticmethod
    def create_scan_from_tenable(
        associated_vulns: List[dict], reg_asset: dict, config: dict, tenant_id: int
    ) -> "Scan":
        """Creates a Scan object from a Tenable scan

        :param associated_vulns: List of associated vulnerabilities
        :param reg_asset: RegScale Asset
        :param config: Application Config
        :param tenant_id: Tenant ID
        :return: Scan object
        :rtype: Scan
        """
        grouped_vulns = Scan.group_vulns_by_severity(associated_vulns)
        return Scan(
            id=0,
            uuid=associated_vulns[0]["scan"]["uuid"],
            scanningTool="NESSUS",
            tenableId=associated_vulns[0]["scan"]["uuid"],
            scanDate=convert_datetime_to_regscale_string(
                associated_vulns[0]["scan"]["started_at"]
            ),
            scannedIPs=1,
            checks=len(associated_vulns),
            vInfo=len(grouped_vulns["info"]) if "info" in grouped_vulns else 0,
            vLow=len(grouped_vulns["low"]) if "low" in grouped_vulns else 0,
            vMedium=len(grouped_vulns["medium"]) if "medium" in grouped_vulns else 0,
            vHigh=len(grouped_vulns["high"]) if "high" in grouped_vulns else 0,
            vCritical=len(grouped_vulns["critical"])
            if "critical" in grouped_vulns
            else 0,
            parentId=reg_asset.id,
            parentModule="assets",
            createdById=config["userId"],
            lastUpdatedById=config["userId"],
            dateCreated=convert_datetime_to_regscale_string(datetime.now()),
            tenantsId=tenant_id,
        )

    @staticmethod
    def prepare_scan_history_for_sync(
        app: Application,
        nessus_list: List[dict],
        existing_assets: List[dict],
        parent_id: int,
        parent_module: str,
    ) -> Tuple[List["Scan"], List["Scan"], List[dict]]:
        """Prepares scan history data for synchronization.

        :param Application app: The Application object to use for database operations.
        :param List[dict] nessus_list: A list of Nessus scan history data.
        :param List[dict] existing_assets: A list of existing Asset objects to compare against.
        :param int parent_id: The ID of the parent object associated with the scan history data.
        :param str parent_module: The name of the parent module associated with the scan history data.
        :return: A tuple containing three lists: new Scan objects, updated Scan objects, and a list of Asset objects.
        :rtype: Tuple[List[Scan], List[Scan], List[Asset]]
        """
        logger = create_logger()
        new_scan_history = []
        update_scan_history = []
        assets = {asset["asset"]["uuid"] for asset in nessus_list}
        asset_count = 0
        api = Api(app)
        config = app.config
        existing_scan_history_list = api.get(
            url=app.config["domain"]
            + f"/api/scanhistory/getAllByParent/{parent_id}/{parent_module}"
        ).json()
        tenant_id = api.get(url=api.config["domain"] + "/api/tenants/config").json()[
            "id"
        ]

        def process_asset(asset):
            nonlocal asset_count
            asset_count += 1
            if asset_count % 100 == 0:
                logger.info(f"Processing asset {asset_count} of {len(assets)}")
            associated_vulns = [
                ness for ness in nessus_list if ness["asset"]["uuid"] == asset
            ]
            reg_assets = [reg for reg in existing_assets if reg["tenableId"] == asset]
            if reg_assets:
                reg_asset = reg_assets[0] if reg_assets else None
                existing_scan_history_list.extend(
                    Scan.get_existing_scan_history(app, reg_asset)
                )
                scan = Scan.create_scan_from_tenable(
                    associated_vulns, reg_asset, config, tenant_id
                )
                if scan in [Scan(**s) for s in existing_scan_history_list]:
                    update_scan_history.append(scan)
                else:
                    new_scan_history.append(scan)
                    existing_scan_history_list.append(scan.dict())

        with ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(process_asset, assets)

        return new_scan_history, update_scan_history, existing_scan_history_list

    @staticmethod
    def sync_scan_history_to_regscale(
        app: Application,
        new_scan_history: List["Scan"],
        update_scan_history: List["Scan"],
    ) -> None:
        """Synchronizes scan history to RegScale

        :param Application app: Application Instance
        :param List[Scan] new_scan_history: List of new scan history items
        :param List[Scan] update_scan_history: List of updated scan history items
        :return: None
        """
        logger = create_logger()

        if new_scan_history:
            logger.info(f"Inserting {len(new_scan_history)} new scan history item(s)")
            Scan.bulk_insert(app, new_scan_history)
            logger.info("Done!")
        else:
            logger.info("No new scan history items to insert")

        if update_scan_history:
            logger.info(
                f"Updating {len(update_scan_history)} existing scan history item(s)"
            )
            Scan.bulk_update(app, update_scan_history)
            logger.info("Done!")
        else:
            logger.info("No scan history items to update")

    @staticmethod
    def convert_from_tenable(
        nessus_list: List[dict],
        existing_assets: List[dict],
        parent_id: int,
        parent_module: str,
    ) -> List[dict]:
        """Converts a TenableScan object to a RegScale Scan object

        :param List[dict] nessus_list: List of Tenable Scans
        :param List[dict] existing_assets: Existing RegScale Assets
        :param int parent_id: RegScale Parent ID
        :param str parent_module: RegScale Parent Module
        :return: List of RegScale Scans
        :rtype: List[dict]
        """
        app = Application()

        (
            new_scan_history,
            update_scan_history,
            existing_scan_history_list,
        ) = Scan.prepare_scan_history_for_sync(
            app, nessus_list, existing_assets, parent_id, parent_module
        )

        Scan.sync_scan_history_to_regscale(app, new_scan_history, update_scan_history)

        return existing_scan_history_list

    @staticmethod
    def bulk_insert(app: Application, scans: List["Scan"], max_workers=10) -> None:
        """Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param Application app: Application Instance
        :param List[Scan] scans: List of Scans
        :param int max_workers: Max Workers, defaults to 10
        :return: None
        """
        api = Api(app)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            [
                executor.submit(
                    Scan.insert_scan,
                    app,
                    api,
                    scan,
                )
                for scan in scans
            ]

    @staticmethod
    def bulk_update(app: Application, scans: List["Scan"], max_workers=10) -> None:
        """Bulk update assets using the RegScale API and ThreadPoolExecutor

        :param Application app: Application Instance
        :param List[Scan] scans: List of Scans
        :param int max_workers: Max Workers, defaults to 10
        :return: None
        """
        api = Api(app)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            [
                executor.submit(
                    Scan.update_scan,
                    app,
                    api,
                    scan,
                )
                for scan in scans
            ]

    @staticmethod
    def update_scan(
        app: Application, api: Api, regscale_scan: "Scan"
    ) -> Tuple[Response, "Scan"]:
        """Api wrapper to update a scan

        :param Application app: Application Instance
        :param Api api: Api Instance
        :param Scan regscale_scan: Regscale Scan
        :return: RegScale Scan and Response
        :rtype: Tuple[Response, Scan]
        """
        scan_res = api.put(
            url=app.config["domain"]
            + "/api/scanHistory",  # no ID needed on this endpoint
            json=regscale_scan.dict(),
        )
        regscale_scan.id = scan_res.json()["id"]
        return scan_res, regscale_scan

    @staticmethod
    def insert_scan(
        app: Application, api: Api, regscale_scan: "Scan"
    ) -> Tuple[Response, "Scan"]:
        """Api wrapper to insert a scan

        :param Application app: Application Instance
        :param Api api: Api Instance
        :param Scan regscale_scan: Regscale Scan
        :return: RegScale Scan and Response
        :rtype: Tuple[Response, Scan]
        """
        scan_res = api.post(
            url=app.config["domain"] + "/api/scanHistory",
            json=regscale_scan.dict(),
        )
        regscale_scan.id = scan_res.json()["id"]
        return scan_res, regscale_scan
