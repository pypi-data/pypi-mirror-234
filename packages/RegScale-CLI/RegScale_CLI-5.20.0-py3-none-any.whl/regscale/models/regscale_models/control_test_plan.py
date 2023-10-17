#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ControlTestPlan(BaseModel):
    """A RegScale ControlTestPlan model

    :param BaseModel: Pydantic BaseModel class
    """

    test: str  # Required
    securityControlId: int  # Required
    id: int = 0
    archived: bool = False
    testId: Optional[str] = None
    uuid: Optional[str] = None
    createdBy: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[datetime] = None
    lastUpdatedBy: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[datetime] = None
