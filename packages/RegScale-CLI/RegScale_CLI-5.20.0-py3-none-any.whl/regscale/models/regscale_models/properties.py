#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Properties model."""
from typing import List, Union

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime

logger = create_logger()


class Properties(BaseModel):
    """Properties plan model"""

    id: int = 0
    createdById: str = ""  # this should be userID
    dateCreated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    lastUpdatedById: str = ""  # this should be userID
    isPublic: bool = True
    key: str = ""
    value: str = ""
    label: str = ""
    otherAttributes: str = ""
    parentId: int = 0
    parentModule: str = ""
    dateLastUpdated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def from_dict(data: dict) -> "Properties":
        """Convert dict to Properties object
        :param data: dict to create object from
        :return: A Properties object
        """
        return Properties(**data)

    @staticmethod
    def create_properties_from_list(
        parent_id: Union[str, int],
        parent_module: str,
        properties_list: List[dict],
    ) -> List["Properties"]:
        """Create a list of Properties objects from a list of dicts
        :param parent_id: ID of the SSP to create the Properties objects for
        :param properties_list: List of dicts to create objects from
        :param parent_module: Parent module of the Properties objects
        :return: List of Properties objects
        """
        properties = [
            Properties(parentId=parent_id, parentModule=parent_module, **properties)
            for properties in properties_list
        ]
        return [
            property_.create_new_properties(return_object=True)
            for property_ in properties
        ]

    def create_new_properties(
        self, return_object: bool = False
    ) -> Union[bool, "Properties"]:
        """Create a new Properties object in RegScale
        :param return_object: Return the object if successful
        :return: True or the Properties created if successful, False otherwise
        """
        app = Application()
        api = Api(app=app)
        data = self.dict()
        data["id"] = None
        data["createdById"] = api.config["userId"]
        data["lastUpdatedById"] = api.config["userId"]
        properties_response = api.post(
            f'{api.config["domain"]}/api/properties/',
            json=data,
        )
        if properties_response.ok:
            logger.info(f'Created Properties: {properties_response.json()["id"]}')
            if return_object:
                return Properties.from_dict(properties_response.json())
            return True
        logger.error(f"Error creating Properties: {properties_response.text}")
        return False
