#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """
from typing import Optional

from pydantic import BaseModel, validator

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import camel_case, snake_case


class Incident(BaseModel):
    """RegScale Incident

    :param BaseModel: Pydantic BaseModel
    :raises ValueError: Validation Error
    :return: RegScale Incident
    """

    category: str  # Required
    detectionMethod: str  # Required
    dateDetected: str  # Required
    phase: str  # Required
    title: str  # Required
    incidentPOCId: str  # Required
    id: Optional[int]
    attackVector: Optional[str]
    compromiseDate: Optional[str]
    cost: Optional[float] = 0
    dateResolved: Optional[str]
    description: Optional[str]
    ioc: Optional[str]
    impact: Optional[str]
    parentId: Optional[int]
    responseActions: Optional[str]
    sourceCause: Optional[str]
    createdById: Optional[str]
    dateCreated: Optional[str]
    dateLastUpdated: Optional[str]
    lastUpdatedById: Optional[str]
    parentModule: Optional[str]
    tenantsId: Optional[int]
    facilityId: Optional[int]
    # post_incident: Optional[str]
    uuid: Optional[str]
    isPublic: bool = True
    orgId: Optional[int]
    containmentSteps: Optional[str]
    eradicationSteps: Optional[str]
    recoverySteps: Optional[str]
    severity: Optional[str]

    @validator("category")
    def check_category(value):
        """Validate Category

        :param value: An incident category
        :raises ValueError: Validation Error for Incident Category
        :return: An incident category
        """
        categories = [
            "CAT 0 - Exercise/Network Defense Testing",
            "CAT 1 - Unauthorized Access",
            "CAT 2 - Denial of Service (DoS)",
            "CAT 3 - Malicious Code",
            "CAT 4 - Improper Usage",
            "CAT 5 - Scans/Probes/Attempted Access",
            "CAT 6 - Investigation",
        ]
        if value not in categories:
            cats = "\n".join(categories)
            raise ValueError(f"Category must be one of the following:\n{cats}")
        return value

    @validator("phase")
    def check_phases(value):
        """Validate Phases

        :param value: An incident phase
        :raises ValueError: Validation Error for Incident Phase
        :return: An incident phase
        """
        phases = [
            "Analysis",
            "Closed",
            "Containment",
            "Detection",
            "Eradication",
            "Recovery",
        ]
        if value not in phases:
            phas = "\n".join(phases)
            raise ValueError(f"Phase must be one of the following:\n{phas}")
        return value

    @staticmethod
    def post_incident(incident: "Incident"):
        """Post Incident

        :param incident: An instance of Incident
        :return: RegScale incident
        """
        app = Application()
        config = app.config
        api = Api(app)
        url = config["domain"] + "/api/incidents"
        incident.id = 0  # ID must be 0 for POST
        incident_d = incident.dict()
        # del incident_d["dateCreated"]
        response = api.post(url=url, json=incident_d)
        return response

    @staticmethod
    def get_incident(incident_id: int):
        """Get Incident

        :param incident_id: A Incident ID
        :return: RegScale incident
        """
        app = Application()
        config = app.config
        api = Api(app)
        url = config["domain"] + "/api/incidents/" + str(incident_id)
        response = api.get(url=url)
        dat = response.json()
        convert = {
            snake_case(camel_case(key)).lower().replace("pocid", "poc_id"): value
            for (key, value) in dat.items()
        }
        return Incident(**convert)

    def to_dict(self):
        """RegScale friendly dict

        :return: RegScale friendly dict for posting to API
        """
        dat = self.dict()
        return {camel_case(key): value for (key, value) in dat.items()}
