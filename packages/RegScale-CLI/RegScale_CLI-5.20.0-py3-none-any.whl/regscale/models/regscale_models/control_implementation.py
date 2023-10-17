#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Control Implementation """
from enum import Enum
from typing import Any, Optional

from lxml.etree import Element

# standard python imports
from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.models.regscale_models.control import Control
from regscale.models.regscale_models.security_control import SecurityControl


class ControlImplementationStatus(Enum):
    """Control Implementation Status"""

    FullyImplemented = "Fully Implemented"
    NotImplemented = "Not Implemented"
    PartiallyImplemented = "Partially Implemented"
    InRemediation = "In Remediation"
    Inherited = "Inherited"
    NA = "Not Applicable"
    Planned = "Planned"
    Archived = "Archived"
    RiskAccepted = "Risk Accepted"


class ControlImplementation(BaseModel):
    """Control Implementation"""

    parentId: Optional[int]
    parentModule: Optional[str]
    controlOwnerId: str  # Required
    status: str  # Required
    controlID: int  # Required
    control: Optional[Control] = None
    id: Optional[int] = None
    createdById: Optional[str] = None
    uuid: Optional[str] = None
    policy: Optional[str] = None
    implementation: Optional[str] = None
    dateLastAssessed: Optional[str] = None
    lastAssessmentResult: Optional[str] = None
    practiceLevel: Optional[str] = None
    processLevel: Optional[str] = None
    cyberFunction: Optional[str] = None
    implementationType: Optional[str] = None
    implementationMethod: Optional[str] = None
    qdWellDesigned: Optional[str] = None
    qdProcedures: Optional[str] = None
    qdSegregation: Optional[str] = None
    qdFlowdown: Optional[str] = None
    qdAutomated: Optional[str] = None
    qdOverall: Optional[str] = None
    qiResources: Optional[str] = None
    qiMaturity: Optional[str] = None
    qiReporting: Optional[str] = None
    qiVendorCompliance: Optional[str] = None
    qiIssues: Optional[str] = None
    qiOverall: Optional[str] = None
    responsibility: Optional[str] = None
    inheritedControlId: Optional[int] = None
    inheritedRequirementId: Optional[int] = None
    inheritedSecurityPlanId: Optional[int] = None
    inheritedPolicyId: Optional[int] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    weight: Optional[int] = None
    isPublic: bool = True
    inheritable: bool = False
    systemRoleId: Optional[int] = None

    @staticmethod
    def post_implementation(app: Application, implementation: "ControlImplementation"):
        res = None
        api = Api(app)
        headers = {
            "accept": "*/*",
            "Authorization": app.config["token"],
            "Content-Type": "application/json-patch+json",
        }

        res = api.post(
            app.config["domain"] + "/api/controlimplementation",
            headers=headers,
            data=implementation.json(),
        )
        if not res.raise_for_status() and res.status_code == 200:
            return res.json()
        else:
            return res

    @staticmethod
    def fetch_existing_implementations(
        app: Application, regscale_parent_id: int, regscale_module: str
    ):
        """_summary_

        :param app: Application instance
        :param regscale_parent_id: RegScale Parent ID
        :param regscale_module: RegScale Parent Module
        :return: _description_
        """
        api = Api(app)
        existing_implementations = []
        existing_implementations_response = api.get(
            url=app.config["domain"]
            + "/api/controlimplementation"
            + f"/getAllByParent/{regscale_parent_id}/{regscale_module}"
        )
        if existing_implementations_response.ok:
            existing_implementations = existing_implementations_response.json()
        return existing_implementations

    @staticmethod
    def from_oscal_element(
        app: Application, obj: Element, control: dict
    ) -> "ControlImplementation":
        """
        Create RegScale ControlImplementation from XMl element
        :param obj: dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """

        logger = create_logger()
        user = app.config["userId"]
        imp = ControlImplementation(
            controlOwnerId=user, status="notimplemented", controlID=control["id"]
        )

        for element in obj.iter():
            if element.text is not None:
                text = element.text.strip()  # remove unnecessary whitespace
                if text:
                    logger.debug("Text: %s", text)
            logger.debug("Element: %s", element.tag)
            imp.control = control["controlId"]
            for name, value in element.attrib.items():
                logger.debug(f"Property: {name}, Value: {value}")
                if (
                    "name" in element.attrib.keys()
                    and element.attrib["name"] == "implementation-status"
                ):
                    imp.status = (
                        "Fully Implemented"
                        if value == "implemented"
                        else "Not Implemented"
                    )
        return imp

    @staticmethod
    def from_dict(obj: Any) -> "ControlImplementation":
        """
        Create ControlImplementation from dictionary
        :param obj: dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """
        if "id" in obj:
            del obj["id"]
        return ControlImplementation(**obj)

    def __hash__(self):
        return hash(
            (
                self.controlID,
                self.controlOwnerId,
                self.status,
            )
        )

    @staticmethod
    def stringify_children(node):
        from itertools import chain

        from lxml.etree import tostring

        parts = (
            [node.text]
            + list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren())))
            + [node.tail]
        )
        # filter removes possible Nones in texts and tails
        return "".join(filter(None, parts))
