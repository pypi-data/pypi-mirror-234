#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclasses for a Tenable integration """
from concurrent.futures import Future, ThreadPoolExecutor, as_completed

# standard python imports
from datetime import datetime
from logging import Logger
from typing import Iterable, List, Optional, Tuple

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import convert_datetime_to_regscale_string
from regscale.models.integration_models.tenable import (
    Plugin,
    TenableBasicAsset,
    TenablePort,
    TenableScan,
)
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.scan import Scan
from regscale.models.regscale_models.vulnerability import Vulnerability


class NessusReport(BaseModel):
    """Tenable Nessus Report (maps to regscale vuln)


    :param BaseModel: Pydantic Base Class
    """

    asset: TenableBasicAsset
    output: Optional[str]
    plugin: Plugin
    port: TenablePort
    scan: TenableScan
    severity: Optional[str]
    severity_id: int
    severity_default_id: int
    severity_modification_type: str
    first_found: Optional[datetime]
    last_fixed: Optional[datetime]
    last_found: Optional[datetime]
    state: Optional[str]
    indexed: Optional[datetime]

    @staticmethod
    def prepare_tenable_data(
        existing_assets: List[dict],
        vulns: Iterable["NessusReport"],
        logger: Logger,
        parent_id: int,
        parent_module: str,
    ) -> Tuple[List["NessusReport"], List[Scan]]:
        """Prepares Tenable data for download

        :param existing_assets: A list of existing Asset objects to compare against.
        :param vulns: An iterable of NessusReport objects to prepare for download.
        :param logger: The logger object to use for logging.
        :param parent_id: The ID of the parent object associated with the data.
        :param parent_module: The name of the parent module associated with the data.
        :return: A tuple containing two lists: NessusReport objects and Scan objects.
        :rtype: Tuple[List[NessusReport], List[Scan]]
        """
        all_vulns = []
        logger.info("Preparing Tenable data for download...")
        for ix, tenable_data in enumerate(vulns):
            if ix % 50 == 0:
                logger.info(
                    "Downloading %i of %i records in current page",
                    vulns.page_count,
                    len(vulns.page),
                )
            report = NessusReport(**tenable_data)
            all_vulns.append(report)
        logger.info("Processing scan data from Tenable...")
        existing_scans = Scan.convert_from_tenable(
            nessus_list=[vuln.dict() for vuln in all_vulns],
            existing_assets=existing_assets,
            parent_id=parent_id,
            parent_module=parent_module,
        )
        return all_vulns, existing_scans

    @staticmethod
    def create_regscale_vuln(**kwargs) -> Optional[Vulnerability]:
        """Prepares Tenable data for download

        :param existing_assets: A list of existing Asset objects to compare against.
        :param vulns: An iterable of NessusReport objects to prepare for download.
        :param logger: The logger object to use for logging.
        :param parent_id: The ID of the parent object associated with the data.
        :param parent_module: The name of the parent module associated with the data.
        :return: A tuple containing two lists: NessusReport objects and Scan objects.
        :rtype: Tuple[List[NessusReport], List[Scan]]
        """
        app = kwargs.get("app")
        parent_id = kwargs.get("parent_id")
        parent_module = kwargs.get("parent_module")
        existing_assets = kwargs.get("existing_assets")
        report = kwargs.get("report")
        existing_scans = kwargs.get("existing_scans")
        existing_vulns = kwargs.get("existing_vulns")
        asset = None
        res = [
            asset
            for asset in existing_assets
            if asset["otherTrackingNumber"] == report.asset.uuid
        ]

        if res:
            asset = res[0]

        # refresh existing scans
        scans = [
            scan for scan in existing_scans if scan["tenableId"] == report.scan.uuid
        ]
        if scans:
            regscale_vuln = Vulnerability(
                id=0,
                uuid=report.scan.uuid,
                scanId=scans[0]["id"],
                parentId=asset["id"] if asset else parent_id,
                parentModule="assets" if asset else parent_module,
                lastSeen=convert_datetime_to_regscale_string(report.last_found),
                firstSeen=convert_datetime_to_regscale_string(report.first_found),
                daysOpen=None,
                dns=report.asset.hostname,
                ipAddress=report.asset.ipv4,
                mitigated=None,
                operatingSystem=report.asset.operating_system[0]
                if report.asset.operating_system
                else None,
                port=report.port.port,
                protocol=report.port.protocol,
                severity=report.severity,
                plugInName=report.plugin.name,
                plugInId=report.plugin.id,
                cve=None,
                vprScore=None,
                tenantsId=0,
                exploitAvailable=report.plugin.exploit_available,
                cvss3BaseScore=report.plugin.cvss3_base_score,
                title=f"{report.output} on asset {report.asset.hostname}",
                description=report.output,
                plugInText=report.plugin.description,
                createdById=app.config["userId"],
                lastUpdatedById=app.config["userId"],
                dateCreated=convert_datetime_to_regscale_string(datetime.now()),
            )
            if regscale_vuln not in existing_vulns:
                return regscale_vuln
            else:
                if existing_vulns:
                    regscale_vuln.id = [
                        vuln for vuln in existing_vulns if vuln == regscale_vuln
                    ][0].id
                    return regscale_vuln

        return None

    @staticmethod
    def sync_to_regscale(
        vulns: Iterable["NessusReport"], parent_id: int, parent_module="securityplans"
    ) -> None:
        # Create sphinx notypes docstring
        """Synchronizes Tenable assets to RegScale

        :param app: The Application object to use for database operations.
        :param assets: A list of TenableIOAsset objects to synchronize.
        :param ssp_id: The ID of the SSP associated with the assets.
        :return: None
        """
        logger = create_logger()
        app = Application()
        existing_assets = Asset.find_assets_by_parent(
            app=app, parent_id=parent_id, parent_module="securityplans"
        )
        all_vulns, existing_scans = NessusReport.prepare_tenable_data(
            existing_assets, vulns, logger, parent_id, parent_module=parent_module
        )
        existing_vulns = NessusReport.existing_vulns(
            existing_scans=existing_scans, app=app
        )
        logger.info("Saving Tenable Vulnerabilities to RegScale...")
        threads = 100

        with ThreadPoolExecutor(max_workers=threads) as executor:
            new_vulns = []
            futures = [
                executor.submit(
                    NessusReport.create_regscale_vuln,
                    parent_id=parent_id,
                    parent_module=parent_module,
                    report=report,
                    existing_assets=existing_assets,
                    existing_scans=existing_scans,
                    existing_vulns=existing_vulns,
                    app=app,
                )
                for report in all_vulns
            ]
            NessusReport.process_vuln_results(
                futures, all_vulns, existing_vulns, logger
            )

        logger.debug(f"Found {len(new_vulns)} new vulnerabilities")
        Vulnerability.process_vulns(
            app=app,
            new_vulns=new_vulns,
        )

    @staticmethod
    def process_vuln_results(
        futures: List[Future],
        all_vulns: List["NessusReport"],
        existing_vulns: List[Vulnerability],
        logger: Logger,
    ) -> None:
        """Processes the results of the vulnerability futures

        :param futures: A list of Future objects representing the vulnerability futures.
        :param all_vulns: A list of NessusReport objects representing all vulnerabilities.
        :param existing_vulns: A list of existing Vulnerability objects to compare against.
        :param logger: The logger object to use for logging.
        :return: None
        """
        new_vulns = []
        count = 0
        for future in as_completed(futures):
            count += 1
            if count % 5000 == 0:
                logger.info(f"Processed {count} of {len(all_vulns)} vulnerabilities")
            regscale_vuln = future.result()
            if regscale_vuln is not None and (
                regscale_vuln.severity != "info" and regscale_vuln not in existing_vulns
            ):
                new_vulns.append(regscale_vuln)

        logger.info(f"Found {len(new_vulns)} new vulnerabilities")

    @staticmethod
    def existing_vulns(existing_scans, app) -> List[Vulnerability]:
        """Existing Vulns

        :param app: Application Instance
        :param api: Api Instance
        :return: List of Vulns
        :rtype: List[Vulnerability]
        """
        results = []
        api = Api(app)
        for scan_id in {scan["id"] for scan in existing_scans}:
            results.extend(
                api.get(
                    url=app.config["domain"]
                    + f"/api/vulnerability/getAllByParent/{scan_id}"
                ).json()
            )
        return [Vulnerability(**vuln) for vuln in results]

    @staticmethod
    def existing_scans(app, parent_id, parent_module) -> List[dict]:
        """Existing Scans

        :param app: Application Instance
        :param parent_id: RegScale Parent Id
        :param parent_module: RegScale Parent Module
        :return: List of Scans
        :rtype: List[dict]
        """
        api = Api(app)
        return api.get(
            url=app.config["domain"]
            + f"/api/scanHistory/getAllByParent/{parent_id}/{parent_module}"
        ).json()
