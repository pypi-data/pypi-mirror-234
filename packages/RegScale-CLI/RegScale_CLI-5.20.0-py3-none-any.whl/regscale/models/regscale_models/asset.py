#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Asset """

# standard python imports
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Optional
from urllib.parse import urljoin

from pydantic import BaseModel
from requests import JSONDecodeError, Response

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import get_current_datetime


class Asset(BaseModel):
    """Asset Model"""

    name: str  # Required
    id: int = 0  # Required
    parentId: int  # Required
    parentModule: str  # Required
    isPublic: bool = True  # Required as Bool
    ram: int = 0  # Required as int
    assetOwnerId: str  # Required as string
    dateCreated: Optional[str] = get_current_datetime()  # Required as string
    dateLastUpdated: Optional[str] = get_current_datetime()  # Required as string
    assetType: Optional[str]
    cpu: Optional[int]
    description: Optional[str]
    diskStorage: Optional[int]
    ipAddress: Optional[str]
    macAddress: Optional[str]
    manufacturer: Optional[str]
    model: Optional[str]
    osVersion: Optional[str]
    operatingSystem: Optional[str]
    otherTrackingNumber: Optional[str]
    uuid: Optional[str]
    serialNumber: Optional[str]
    createdById: Optional[str]
    lastUpdatedById: Optional[str]
    endOfLifeDate: Optional[str]
    purchaseDate: Optional[str]
    status: Optional[str]
    tenantsId: Optional[int]
    facilityId: Optional[int]
    orgId: Optional[int]
    cmmcAssetType: Optional[str]
    wizId: Optional[str]
    wizInfo: Optional[str]
    assetCategory: Optional[str]
    assetTagNumber: Optional[str]
    baselineConfiguration: Optional[str]
    fqdn: Optional[str]
    netBIOS: Optional[str]
    softwareName: Optional[str]
    softwareVendor: Optional[str]
    softwareVersion: Optional[str]
    vlanId: Optional[int]
    bAuthenticatedScan: Optional[bool]
    bPublicFacing: Optional[bool]
    bVirtual: Optional[bool]
    notes: Optional[str]
    patchLevel: Optional[str]
    softwareFunction: Optional[str]
    systemAdministratorId: Optional[str]
    bLatestScan: Optional[bool]
    managementType: Optional[str]
    qualysId: Optional[str]
    tenableId: Optional[str]
    firmwareVersion: Optional[str]
    purpose: Optional[str]
    awsIdentifier: Optional[str]
    azureIdentifier: Optional[str]
    googleIdentifier: Optional[str]
    otherCloudIdentifier: Optional[str]
    ipv6Address: Optional[str]
    scanningTool: Optional[str]
    uri: Optional[str]
    bScanDatabase: Optional[bool]
    bScanInfrastructure: Optional[bool]
    bScanWeb: Optional[bool]

    @staticmethod
    def from_dict(obj: dict) -> "Asset":
        """
        Create Asset object from dict
        :param obj: dictionary
        :return: Asset class
        :rtype: Asset
        """
        if "assetOwnerId" not in obj.keys():
            obj["assetOwnerId"] = "Unknown"
        return Asset(**obj)

    # 'uniqueness': 'ip, macaddress'
    # Enable object to be hashable
    def __hash__(self):
        """
        Enable object to be hashable
        :return: Hashed TenableAsset
        :rtype: int
        """
        return hash(
            (
                self.name,
                self.ipAddress,
                self.macAddress.lower() if self.macAddress else None,
                self.assetCategory,
                self.assetType,
                self.fqdn,
                self.parentId,
                self.parentModule,
                self.description,
                self.notes,
            )
        )

    def __getitem__(self, key: any) -> any:
        """
        Get attribute from Pipeline
        :param any key:
        :return: value of provided key
        :rtype: any
        """
        return getattr(self, key)

    def __setitem__(self, key: any, value: any) -> None:
        """
        Set attribute in Pipeline with provided key
        :param any key: Key to change to provided value
        :param any value: New value for provided Key
        :return: None
        """
        return setattr(self, key, value)

    def __eq__(self, other) -> "Asset":
        """
        Update items in Asset class
        :param other:
        :return: Updated Asset
        :rtype: Asset
        """
        return (
            self.name == other.name
            and self.ipAddress == other.ipAddress
            and self.macAddress == other.macAddress
            and self.wizId == other.wizId
            and self.description == other.description
            and self.notes == other.notes
            and self.status == other.status
            and self.parentId == other.parentId
            and self.otherTrackingNumber == other.otherTrackingNumber
            and self.parentModule == other.parentModule
        )

    @staticmethod
    def insert_asset(
        app: Application,
        obj: Any,
        retry_count: Optional[int] = 3,
    ) -> Response:
        """
        Create an asset in RegScale via API
        :param Application app: Application Instance
        :param Any obj: Asset Object
        :param int retry_count: Number of times to retry if it fails, defaults to 3
        :return: Response from RegScale after inserting the provided asset object
        :rtype: Response
        """
        url = urljoin(app.config["domain"], "/api/assets")
        if isinstance(obj, Asset):
            obj = obj.dict()
        api = Api(app)
        res = api.post(url=url, json=obj)
        if not res.ok:
            if res.status_code == 500:
                app.logger.error(
                    "%i: %s\nError inserting asset: %s", res.status_code, res.text, obj
                )
            # as long as the status code is not 500, retry
            while res.status_code != 500 and retry_count >= 0:
                app.logger.warning(
                    "Retrying to insert asset, attempts remaining: %i", retry_count
                )
                res = api.post(url=url, json=obj)
                retry_count -= 1
                if res.ok:
                    app.logger.info(
                        "[green]Successfully inserted asset: %s", res.json()["id"]
                    )
                    break
            if retry_count < 0:
                app.logger.error(
                    "%i: %s\n[red]Failed to insert asset: %s",
                    res.status_code,
                    res.text,
                    obj,
                )
        return res

    @staticmethod
    def update_asset(
        app: Application,
        obj: Any,
    ) -> Response:
        """
        Create an asset in RegScale via API
        :param app: Application Instance
        :param obj: Asset Object
        :return: Response from RegScale after inserting the provided asset object
        :rtype: Response
        """
        url = urljoin(app.config["domain"], f"/api/assets/{obj['id']}")
        if isinstance(obj, Asset):
            obj = obj.dict()
        api = Api(app)
        res = api.put(url=url, json=obj)
        if res.status_code != 200:
            app.logger.error("Error updating asset: %s", obj)
        return res

    @staticmethod
    def fetch_all(app: Application) -> List["Asset"]:
        """
        Find all assets
        :param app: Application Instance
        :return: List of Assets
        :rtype: List[Asset]
        """
        api = Api(app)
        try:
            res = api.get(url=app.config["domain"] + "/api/assets/getAll")
            existing_assets = res.json()
        except JSONDecodeError:
            existing_assets = []
        existing_assets = [Asset.from_dict(asset) for asset in existing_assets]
        return existing_assets

    @staticmethod
    def bulk_insert(
        app: Application, assets: List["Asset"], max_workers=30
    ) -> List[Response]:
        """Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param app: Application Instance
        :param assets: Asset List
        :param max_workers: Max Workers, defaults to 10
        :return: List of Responses from RegScale
        :rtype: List[Response]
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            [
                executor.submit(
                    Asset.insert_asset,
                    app,
                    asset,
                )
                for asset in assets
            ]

    @staticmethod
    def bulk_update(
        app: Application, assets: List["Asset"], max_workers=30
    ) -> List[Response]:
        """Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param app: Application Instance
        :param assets: Asset List
        :param max_workers: Max Workers, defaults to 10
        :return: List of Responses from RegScale
        :rtype: List[Response]
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            [
                executor.submit(
                    Asset.update_asset,
                    app,
                    asset,
                )
                for asset in assets
            ]

    @staticmethod
    def find_assets_by_parent(
        app: Application,
        parent_id: int,
        parent_module: str,
    ) -> List["Asset"]:
        """
        Find all assets by parent id and parent module
        :param app: Application Instance
        :param parent_id: Parent Id
        :param parent_module: Parent Module
        :return: List of Assets
        :rtype: List[Asset]
        """
        api = Api(app)
        try:
            res = api.get(
                url=app.config["domain"]
                + f"/api/assets/getAllByParent/{parent_id}/{parent_module}"
            )
            existing_assets = res.json()
        except JSONDecodeError:
            existing_assets = []
        existing_assets = [Asset.from_dict(asset) for asset in existing_assets]
        return existing_assets

    @staticmethod
    def fetch_asset_by_id(id: int) -> Optional["Asset"]:
        """
        Find all assets by parent id and parent module
        :param id: Id of the asset
        :return: Asset
        :rtype: Optional[Asset]
        """
        app = Application()
        api = Api(app)
        url = urljoin(app.config["domain"], f"/api/assets/{id}")
        try:
            res = api.get(url=url)
            if res.ok:
                return res.json()
        except JSONDecodeError:
            return None
