#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

from lxml.etree import Element
from pydantic import BaseModel, validator

from regscale.core.app.api import Api
from regscale.core.app.application import Application


class LeveragedAuthorizations(BaseModel):
    """LeveragedAuthorizations model."""

    id: Optional[int] = 0
    isPublic: bool = True
    uuid: Optional[str] = None
    title: str
    fedrampId: Optional[str] = None
    ownerId: str
    securityPlanId: int
    dateAuthorized: str
    description: Optional[str] = None
    servicesUsed: Optional[str] = None
    securityPlanLink: Optional[str] = None
    crmLink: Optional[str] = None
    responsibilityAndInheritanceLink: Optional[str] = None
    createdById: str
    dateCreated: Optional[str] = None
    lastUpdatedById: str
    dateLastUpdated: Optional[str] = None
    tenantsId: Optional[int] = None

    @validator("crmLink", pre=True, always=True)
    def validate_crm_link(cls, value):
        if not value:
            value = ""
        return value

    @validator("responsibilityAndInheritanceLink", pre=True, always=True)
    def validate_responsibility_and_inheritance_link(cls, value):
        if not value:
            value = ""
        return value

    @validator("securityPlanLink", pre=True, always=True)
    def validate_security_plan_link(cls, value):
        if not value:
            value = ""
        return value

    @staticmethod
    def insert_leveraged_authorizations(
        app: Application, leveraged_auth: "LeveragedAuthorizations"
    ):
        """Insert a leveraged authorization into the database.
        :param Application app: The application instance.
        :param LeveragedAuthorizations leveraged_auth: The leveraged authorization to insert.
        :return: LeveragedAuthorizations dictionary.
        :rtype dict: The response from the API or raise an exception.
        """
        api = Api(app)

        # Construct the URL by joining the domain and endpoint
        url = urljoin(app.config.get("domain"), "/api/leveraged-authorization")
        # Convert the Pydantic model to a dictionary
        data = leveraged_auth.dict()
        # Make the POST request to insert the data
        response = api.post(url, json=data)

        # Check for success and handle the response as needed
        return response.json() if response.ok else response.raise_for_status()
