#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional, Union

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger


class SecurityPlan(BaseModel):
    """Security Plan Model"""

    systemName: str
    planInformationSystemSecurityOfficerId: Optional[str] = None
    planAuthorizingOfficialId: Optional[str] = None
    systemOwnerId: Optional[str] = None  # this could be userID
    otherIdentifier: Optional[str] = ""
    confidentiality: str
    integrity: str
    availability: str
    status: str = ""
    description: Optional[str] = ""
    dateSubmitted: Optional[str] = ""
    approvalDate: Optional[str] = ""
    expirationDate: Optional[str] = ""
    systemType: str
    purpose: Optional[str] = ""
    conditionsOfApproval: Optional[str] = ""
    environment: Optional[str] = ""
    lawsAndRegulations: Optional[str] = ""
    authorizationBoundary: Optional[str] = ""
    networkArchitecture: Optional[str] = ""
    dataFlow: Optional[str] = ""
    overallCategorization: str
    maturityTier: Optional[str] = ""
    wizProjectId: Optional[str] = ""
    serviceNowAssignmentGroup: Optional[str] = ""
    jiraProject: Optional[str] = ""
    tenableGroup: Optional[str] = ""
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    parentId: int = 0
    parentModule: Optional[str] = ""
    createdById: Optional[str] = ""
    dateCreated: Optional[str] = ""
    lastUpdatedById: Optional[str] = ""
    dateLastUpdated: Optional[str] = ""
    users: int = 0
    privilegedUsers: int = 0
    usersMFA: int = 0
    privilegedUsersMFA: int = 0
    hva: bool = False
    practiceLevel: Optional[str] = ""
    processLevel: Optional[str] = ""
    cmmcLevel: Optional[str] = ""
    cmmcStatus: Optional[str] = ""
    isPublic: bool = True
    executiveSummary: Optional[str] = ""
    recommendations: Optional[str] = ""
    id: Optional[int] = 0
    uuid: Optional[str] = ""
    bDeployGov: bool = False
    bDeployHybrid: bool = False
    bDeployPrivate: bool = False
    bDeployPublic: bool = False
    bDeployOther: bool = False
    deployOtherRemarks: Optional[str] = ""
    bModelIaaS: bool = False
    bModelOther: bool = False
    bModelPaaS: bool = False
    bModelSaaS: bool = False
    otherModelRemarks: Optional[str] = ""
    explanationForNonOperational: Optional[str] = ""
    version: Optional[str] = ""
    categorizationJustification: Optional[str] = ""
    internalUsers: int = 0
    externalUsers: int = 0
    externalUsersFuture: int = 0
    internalUsersFuture: int = 0
    prepOrgName: Optional[str] = ""
    prepAddress: Optional[str] = ""
    prepOffice: Optional[str] = ""
    prepCityState: Optional[str] = ""
    cspOrgName: Optional[str] = ""
    cspAddress: Optional[str] = ""
    cspOffice: Optional[str] = ""
    cspCityState: Optional[str] = ""
    authenticationLevel: Optional[str] = ""
    identityAssuranceLevel: Optional[str] = ""
    authenticatorAssuranceLevel: Optional[str] = ""
    federationAssuranceLevel: Optional[str] = ""
    fedrampAuthorizationType: Optional[str] = ""
    fedrampAuthorizationLevel: Optional[str] = ""
    fedrampAuthorizationStatus: Optional[str] = ""
    fedrampDateSubmitted: Optional[str] = ""
    fedrampDateAuthorized: Optional[str] = ""
    fedrampId: Optional[str] = ""

    @staticmethod
    def from_dict(data: dict) -> "SecurityPlan":
        """
        Create a SecurityPlan object from a dictionary.
        :param data: The dictionary to create the object from.
        :return: A SecurityPlan object.
        """
        return SecurityPlan(**data)

    def create_new_ssp(
        self, api: Api, return_id: bool = False
    ) -> Union[int, None, "SecurityPlan"]:
        """
        Create a new SSP in RegScale
        :param Api api: The API object to use to create the SSP in RegScale
        :param bool return_id: Return the SSP ID only
        :return: The SSP or the SSP ID upon success, None otherwise.
        :rtype: Union[int, None, SecurityPlan]
        """
        # create the ssp in RegScale
        data = self.dict()
        ssp_response = api.post(
            f'{api.config["domain"]}/api/securityplans',
            json=data,
        )
        if ssp_response.ok:
            if return_id:
                return ssp_response.json()["id"]
            return SecurityPlan.from_dict(ssp_response.json())
        logger = create_logger()
        logger.error(
            f"Failed to upload SSP: {ssp_response.status_code} - {ssp_response.text}"
        )
        return None

    def update_ssp(
        self, api: Api, return_id: bool = False
    ) -> Union[int, None, "SecurityPlan"]:
        """
        Update an SSP in RegScale
        :param Api api: The API object to use to create the SSP in RegScale
        :param bool return_id: Return the SSP ID only
        :return: The SSP or the SSP ID upon success, None otherwise.
        :rtype: Union[int, None, SecurityPlan]
        """
        # create the ssp in RegScale
        data = self.dict()
        assert self.id is not None or self.id != 0
        ssp_response = api.put(
            f'{api.config["domain"]}/api/securityplans/{self.id}',
            json=data,
        )
        if ssp_response.ok:
            if return_id:
                return ssp_response.json()["id"]
            return SecurityPlan.from_dict(ssp_response.json())
        logger = create_logger()
        logger.error(
            f"Failed to update SSP: {ssp_response.status_code} - {ssp_response.text}"
        )
        return None
