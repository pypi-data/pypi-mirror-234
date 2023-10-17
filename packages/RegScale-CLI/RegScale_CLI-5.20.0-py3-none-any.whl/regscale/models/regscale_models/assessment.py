#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Assessment """
from pydantic import BaseModel
from typing import Optional

from requests import JSONDecodeError

from regscale.core.app.application import Application
from regscale.core.app.api import Api
from regscale.core.app.logz import create_logger


class Assessment(BaseModel):
    leadAssessorId: Optional[str] = None  # Required field
    title: Optional[str] = None  # Required field
    assessmentType: Optional[str] = None  # Required field
    plannedStart: Optional[str] = None  # Required field
    plannedFinish: Optional[str] = None  # Required field
    status: Optional[str] = "Scheduled"  # Required field
    id: Optional[int] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    assessmentResult: Optional[str] = None
    actualFinish: Optional[str] = None
    assessmentReport: Optional[str] = None
    masterId: Optional[int] = None
    complianceScore: Optional[float] = None
    targets: Optional[str] = None
    automationInfo: Optional[str] = None
    automationId: Optional[str] = None
    metadata: Optional[str] = None
    assessmentPlan: Optional[str] = None
    methodology: Optional[str] = None
    rulesOfEngagement: Optional[str] = None
    disclosures: Optional[str] = None
    scopeIncludes: Optional[str] = None
    scopeExcludes: Optional[str] = None
    limitationsOfLiability: Optional[str] = None
    documentsReviewed: Optional[str] = None
    activitiesObserved: Optional[str] = None
    fixedDuringAssessment: Optional[str] = None
    summaryOfResults: Optional[str] = None
    oscalsspId: Optional[int] = None
    oscalComponentId: Optional[int] = None
    controlId: Optional[int] = None
    requirementId: Optional[int] = None
    securityPlanId: Optional[int] = None
    projectId: Optional[int] = None
    supplyChainId: Optional[int] = None
    policyId: Optional[int] = None
    componentId: Optional[int] = None
    incidentId: Optional[int] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    isPublic: bool = True

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

    def insert_assessment(self, app: Application) -> Optional["Assessment"]:
        """
        Function to create a new assessment in RegScale and returns the new assessment's ID
        :param Application app: Application object
        :return: New Assessment object created in RegScale
        :rtype: Optional[Assessment]
        """
        api = Api(app)
        url = f"{app.config['domain']}/api/assessments"
        response = api.post(url=url, json=self.dict())
        if not response.ok:
            logger = create_logger()
            logger.debug(response.status_code)
            logger.error(f"Failed to insert Assessment.\n{response.text}")
        return Assessment(**response.json()) if response.ok else None

    @staticmethod
    def fetch_all_assessments(app: Application) -> list["Assessment"]:
        """
        Function to retrieve all assessments from RegScale
        :param Application app: Application Object
        :return: List of assessments from RegScale
        :rtype: list[Assessment]
        """
        query = """
            query {
              assessments (take: 50, skip: 0) {
                items {
                  id
                  status
                   actualFinish
                   assessmentReport
                   facilityId
                   orgId
                   masterId
                   complianceScore
                   isPublic
                   targets
                   automationInfo
                   automationId
                   metadata
                   assessmentPlan
                   methodology
                   rulesOfEngagement
                   disclosures
                   scopeIncludes
                   scopeExcludes
                   uuid
                   limitationsOfLiability
                   documentsReviewed
                   activitiesObserved
                   fixedDuringAssessment
                   oscalsspId
                   oscalComponentId
                   controlId
                   requirementId
                   securityPlanId
                   policyId
                   supplyChainId
                   leadAssessorId
                   componentId
                   incidentId
                   projectId
                   parentModule
                   parentId
                   createdById
                   dateCreated
                   title
                   lastUpdatedById
                   dateLastUpdated
                   assessmentType
                   assessmentResult
                   plannedStart
                   plannedFinish
                }
                pageInfo {
                  hasNextPage
                }
                totalCount
              }
            }
        """
        api = Api(app)
        try:
            logger = create_logger()
            logger.info("Retrieving all assessments in RegScale...")
            existing_assessments = api.graph(query=query)["assessments"]["items"]
            logger.info(
                "%i assessment(s) retrieved from RegScale.", len(existing_assessments)
            )
        except JSONDecodeError:
            existing_assessments = []
        return [Assessment(**assessment) for assessment in existing_assessments]
