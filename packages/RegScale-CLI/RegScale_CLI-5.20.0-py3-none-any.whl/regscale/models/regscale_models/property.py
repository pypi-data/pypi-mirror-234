#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Python Standard Imports """
import json
from typing import Any, Optional

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime, recursive_items


class Property(BaseModel):
    id: int = 0
    createdById: Optional[str]
    dateCreated: Optional[str]
    lastUpdatedById: Optional[str]
    isPublic: bool = True
    alt_id: Optional[str]
    key: str
    value: str
    parentId: int
    parentModule: str
    dateLastUpdated: Optional[str]

    def __eq__(self, other) -> bool:
        """Test equality of two Property objects

        :param other: Other Property object to compare to
        :return: Equality of two Property objects
        :rtype: bool
        """
        return (
            self.key == other.key
            and self.value == other.value
            and self.parentId == other.parentId
            and self.parentModule == other.parentModule
        )

    @staticmethod
    def generate_property_list_from_dict(dat: dict) -> list["Property"]:
        """Generate Property List from Dict

        :param dat: Data to generate Property list from
        :return: List of Properties
        :rtype: list["Property"]
        """
        kvs = recursive_items(dat)
        return [
            Property(key=k, value=v, createdById="", parentId="", parentModule="")
            for k, v in kvs
        ]

    @staticmethod
    def update_properties(app: Application, prop_list: list["Property"]) -> None:
        """
        Post a list of properties to RegScale
        :param Application app: Application object
        :param list prop_list: List of properties to post to RegScale
        :return: None
        """
        api = Api(app)
        logger = create_logger()
        props = [prop.dict() for prop in prop_list]
        res = api.put(
            url=app.config["domain"] + "/api/properties/batchupdate",
            json=props,
        )
        if res.status_code == 200:
            if len(prop_list) > 0:
                logger.info(
                    "Successfully updated %i properties to RegScale", len(prop_list)
                )
        else:
            logger.error("Failed to update properties to RegScale\n%s", res.text)

    @staticmethod
    def existing_properties(
        app: Application, existing_assets: list[dict]
    ) -> list["Property"]:
        """
        Return a list of existing properties in RegScale
        :param Application app: Application object
        :param list existing_assets: List of assets from RegScale
        :return: List of properties for the provided assets
        :rtype: list["Property"]
        """
        properties = []
        api = Api(app)
        for asset in existing_assets:
            res = api.get(
                url=app.config["domain"]
                + f"/api/properties/getAllByParent/{asset['id']}/assets"
            )
            if res.status_code == 200:
                for prop in res.json():
                    prop["alt_id"] = asset["wizId"]
                    properties.append(Property(**prop))
        return properties

    @staticmethod
    def insert_properties(
        app: Application, prop_list: list["Property"]
    ) -> list["Property"]:
        """
        Post a list of properties to RegScale
        :param Application app: Application instance
        :param list prop_list: List of properties to post
        :return: List of created properties in RegScale
        :rtype: list["Property"]
        """
        properties = []
        api = Api(app)
        logger = create_logger()
        res = api.post(
            url=app.config["domain"] + "/api/properties/batchcreate",
            json=[prop.dict() for prop in prop_list],
        )
        if res.status_code == 200:
            if len(prop_list) > 0:
                logger.info(
                    "Successfully posted %i properties to RegScale", len(prop_list)
                )
            properties = [Property(**prop) for prop in res.json()]
        else:
            logger.error("Failed to post properties to RegScale\n%s", res.text)
        return properties

    @staticmethod
    def get_properties(
        app: Application, wiz_data: str, wiz_id: str
    ) -> list["Property"]:
        """
        Convert Wiz properties data into a list of dictionaries
        :param Application app: Application instance
        :param str wiz_data: Wiz information
        :param str wiz_id: Wiz ID for an issue
        :return: Properties from Wiz
        :rtype: list["Property"]
        """

        # FIXME: remove this nested function, there are 2 flatten dict methods in app_utils
        def flatten_dict(d, prefix="", result=None):
            """Simple recursive function to flatten a dictionary

            :param d: The dictionary to flatten
            :param prefix: Prefix, defaults to ""
            :param result: Result, defaults to None
            :return: List of flattened dictionaries
            :rtype: list
            """
            if result is None:
                result = []
            if isinstance(d, dict):
                for key, value in d.items():
                    if isinstance(value, dict):
                        flatten_dict(value, f"{prefix}{key}.", result)
                    elif isinstance(value, list):
                        for dat in value:
                            flatten_dict(dat, f"{prefix}{key}.", result)
                    else:
                        if value:
                            result.append((f"{prefix}{key}", value))
            return result

        props = []
        wiz_data = json.loads(wiz_data)
        result = flatten_dict(wiz_data)
        for k, v in result:
            if v:
                if isinstance(v, list):
                    v = v.pop()
                if isinstance(v, dict):
                    v = flatten_dict(v).pop()[1]
                prop = {
                    "createdById": app.config["userId"],
                    "dateCreated": get_current_datetime(),
                    "lastUpdatedById": app.config["userId"],
                    "isPublic": True,
                    "alt_id": wiz_id,
                    "key": k,
                    "value": v,
                    "parentId": 0,
                    "parentModule": "assets",
                    "dateLastUpdated": get_current_datetime(),
                }
                props.append(Property(**prop))

        return [prop for prop in props if prop.value != "{}"]
