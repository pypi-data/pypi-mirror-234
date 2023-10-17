#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Risks """

# standard python imports
from typing import Optional

from pydantic import BaseModel
from requests import JSONDecodeError

from regscale.core.app import create_logger
from regscale.core.app.api import Api
from regscale.core.app.application import Application


class Risk(BaseModel):
    """Risks Model"""

    id: Optional[int] = 0
    uuid: Optional[str] = None
    dateIdentified: Optional[str] = None
    riskStatement: Optional[str] = None
    probability: Optional[str] = None
    probabilityReason: Optional[str] = None
    consequence: Optional[str] = None
    consequenceReason: Optional[str] = None
    trigger: Optional[str] = None
    mitigation: Optional[str] = None
    mitigationEffectiveness: Optional[str] = None
    residualProbability: Optional[str] = None
    residualConsequence: Optional[str] = None
    residualRisk: Optional[str] = None
    riskStrategy: Optional[str] = None
    businessRisk: Optional[str] = None
    operationalRisk: Optional[str] = None
    safetyRisk: Optional[str] = None
    securityRisk: Optional[str] = None
    qualityRisk: Optional[str] = None
    environmentalRisk: Optional[str] = None
    reputationRisk: Optional[str] = None
    complianceRisk: Optional[str] = None
    operationalRequirements: Optional[str] = None
    riskSource: Optional[str] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None
    status: Optional[str] = None
    dateClosed: Optional[str] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    comments: Optional[str] = None
    riskTier: Optional[str] = None
    title: Optional[str] = None
    recommendations: Optional[str] = None
    impactDescription: Optional[str] = None
    inherentRiskScore: Optional[int] = None
    residualRiskScore: Optional[int] = None
    targetRiskScore: Optional[int] = None
    difference: Optional[int] = None
    futureCosts: Optional[int] = None
    costToMitigate: Optional[int] = None
    controlId: Optional[int] = None
    assessmentId: Optional[int] = None
    requirementId: Optional[int] = None
    securityPlanId: Optional[int] = None
    projectId: Optional[int] = None
    supplyChainId: Optional[int] = None
    policyId: Optional[int] = None
    componentId: Optional[int] = None
    incidentId: Optional[int] = None
    riskAssessmentFrequency: Optional[str] = None
    dateLastAssessed: Optional[str] = None
    nextAssessmentDueDate: Optional[str] = None
    riskOwnerId: Optional[str] = None
    isPublic: Optional[bool] = True

    @staticmethod
    def fetch_all_risks(app: Application) -> list["Risk"]:
        """
        Fetches all risks from RegScale
        :param Application app: Application object
        :return: List of Risks from RegScale
        :rtype: list[Risk]
        """
        api = Api(app)
        body = """
            query {
              risks(take: 50, skip: 0) {
                items {
                  assessmentId
                  id
                  mitigation
                  mitigationEffectiveness
                  residualProbability
                  residualConsequence
                  residualRisk
                  riskStrategy
                  facilityId
                  orgId
                  isPublic
                  businessRisk
                  operationalRisk
                  safetyRisk
                  securityRisk
                  qualityRisk
                  environmentalRisk
                  reputationRisk
                  complianceRisk
                  riskTier
                  title
                  uuid
                  operationalRequirements
                  riskSource
                  parentId
                  parentModule
                  status
                  dateClosed
                  comments
                  recommendations
                  impactDescription
                  inherentRiskScore
                  dateIdentified
                  residualRiskScore
                  targetRiskScore
                  difference
                  futureCosts
                  costToMitigate
                  controlId
                  assessmentId
                  requirementId
                  riskStatement
                  securityPlanId
                  projectId
                  supplyChainId
                  policyId
                  componentId
                  probability
                  incidentId
                  riskAssessmentFrequency
                  dateLastAssessed
                  nextAssessmentDueDate
                  createdById
                  dateCreated
                  lastUpdatedById
                  probabilityReason
                  dateLastUpdated
                  riskOwnerId
                  consequence
                  consequenceReason
                  trigger
                }
                pageInfo {
                  hasNextPage
                }
                totalCount
              }
            }
        """
        try:
            logger = create_logger()
            logger.info("Retrieving all risks in RegScale...")
            existing_risks = api.graph(query=body)["risks"]["items"]
            logger.info("%i risk(s) retrieved from RegScale.", len(existing_risks))
        except JSONDecodeError:
            existing_risks = []
        return [Risk(**risk) for risk in existing_risks]
