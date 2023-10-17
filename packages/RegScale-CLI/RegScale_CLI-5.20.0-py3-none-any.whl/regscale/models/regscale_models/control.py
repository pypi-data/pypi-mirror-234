#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Control Implementation """

# standard python imports
from pydantic import BaseModel
from typing import Any, Optional

# from regscale.core.app.api import Api
# from regscale.core.app.application import Application


class Control(BaseModel):
    """RegScale Control class"""

    id: Optional[int] = None
    isPublic: bool = True
    uuid: Optional[str] = None
    controlId: Optional[str] = None
    sortId: Optional[str] = None
    controlType: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    references: Optional[str] = None
    relatedControls: Optional[str] = None
    subControls: Optional[str] = None
    enhancements: Optional[str] = None
    family: Optional[str] = None
    weight: Optional[int] = None
    catalogueID: Optional[int] = None
    archived: bool = False
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    tenantsId: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Control":
        """
        Create RegScale Control from dictionary
        :param obj: dictionary
        :return: Control class
        :rtype: Control
        """
        if "id" in obj:
            del obj["id"]
        return Control(**obj)
