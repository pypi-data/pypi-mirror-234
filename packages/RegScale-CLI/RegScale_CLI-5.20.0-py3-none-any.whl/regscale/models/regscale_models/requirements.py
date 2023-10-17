#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Python Standard Imports """
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Requirement:
    title: str  # Required
    status: str  # Required
    lastUpdatedById: str  # Required
    controlID: int  # Required
    requirementOwnerId: str  # Required
    parentId: int  # Required

    assessmentPlan: str = ""
    dateLastAssessed: str = ""
    lastAssessmentResult: str = ""
    parentRequirementId: int = None
    parentModule: str = "implementations"
    createdById: str = ""
    dateCreated: str = ""
    dateLastUpdated: str = ""
    isPublic: bool = True
    description: str = ""
    implementation: str = ""
    id: int = None
    uuid: str = ""

    @staticmethod
    def from_dict(obj: Any) -> "Requirement":
        _id = int(obj.get("id"))
        _uuid = str(obj.get("uuid"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _implementation = str(obj.get("implementation"))
        _status = str(obj.get("status"))
        _assessmentPlan = str(obj.get("assessmentPlan"))
        _dateLastAssessed = str(obj.get("dateLastAssessed"))
        _lastAssessmentResult = str(obj.get("lastAssessmentResult"))
        _controlID = int(obj.get("controlID"))
        _parentRequirementId = int(obj.get("parentRequirementId"))
        _requirementOwnerId = str(obj.get("requirementOwnerId"))
        _parentId = int(obj.get("parentId"))
        _parentModule = str(obj.get("parentModule"))
        _createdById = str(obj.get("createdById"))
        _dateCreated = str(obj.get("dateCreated"))
        _lastUpdatedById = str(obj.get("lastUpdatedById"))
        _dateLastUpdated = str(obj.get("dateLastUpdated"))
        _isPublic = True
        return Requirement(
            _id,
            _uuid,
            _title,
            _description,
            _implementation,
            _status,
            _assessmentPlan,
            _dateLastAssessed,
            _lastAssessmentResult,
            _controlID,
            _parentRequirementId,
            _requirementOwnerId,
            _parentId,
            _parentModule,
            _createdById,
            _dateCreated,
            _lastUpdatedById,
            _dateLastUpdated,
            _isPublic,
        )


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
