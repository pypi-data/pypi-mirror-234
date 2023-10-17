#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Provide References models."""
from typing import List, Union

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import get_current_datetime


class References(BaseModel):
    """References model"""

    id: int = 0
    createdById: str = ""  # this should be userID
    dateCreated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    lastUpdatedById: str = ""  # this should be userID
    isPublic: bool = True
    identificationNumber: str = ""
    title: str = ""
    version: str = ""
    datePublished = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    referenceType: str = ""
    link: str = ""
    parentId: int = 0
    parentModule: str = ""
    dateLastUpdated: str = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def from_dict(data: dict) -> "References":
        """Convert dict to References object
        :param data: dict to create object from
        :return: A References object
        """
        return References(**data)

    @staticmethod
    def create_references_from_list(
        parent_id: Union[str, int],
        references_list: List[dict],
        parent_module: str = "securityplans",
    ) -> List[Union["References", bool]]:
        """Create a list of References objects from a list of dicts
        :param parent_id: ID of the SSP to create the References objects for
        :param references_list: List of dicts to create objects from
        :param parent_module: Parent module of the References objects
        :return: List of References objects or False if unsuccessful
        """
        references = [
            References(parentId=parent_id, parentModule=parent_module, **references)
            for references in references_list
        ]
        response = []
        for reference in references:
            response.append(reference.create_new_references(return_object=True))
        return response

    def create_new_references(
        self, return_object: bool = False
    ) -> Union[bool, "References"]:
        """Create a new References object in RegScale
        :return: True if successful, False otherwise
        """
        app = Application()
        api = Api(app=app)
        data = self.dict()
        data["createdById"] = api.config["userId"]
        data["lastUpdatedById"] = api.config["userId"]
        references_response = api.post(
            f'{api.config["domain"]}/api/references/',
            json=data,
        )
        logger = create_logger()
        if references_response.ok:
            logger.info(f'Created References: {references_response.json()["id"]}')
            if return_object:
                return References.from_dict(references_response.json())
            return True
        logger.error(f"Error creating References: {references_response.text}")
        return False
