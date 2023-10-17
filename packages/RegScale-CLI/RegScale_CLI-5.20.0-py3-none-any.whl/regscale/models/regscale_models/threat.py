#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Threat """

# standard python imports
from dataclasses import dataclass


@dataclass
class Threat:
    """Threat Model"""

    title: str
    threatType: str
    threatOwnerId: str
    dateIdentified: str
    targetType: str
    description: str
    vulnerabilityAnalysis: str
    mitigations: str
    dateCreated: str
    uuid: str = None
    id: int = None
    investigationResults: str = ""
    notes: str = ""
    organization: str = ""
    status: str = "Under Investigation"
    source: str = "Open Source"

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

    @staticmethod
    def xstr(str_eval: str) -> str:
        """
        Replaces string with None value to ""
        :param str str_eval: key to replace None value to ""
        :return: Updates provided str field to ""
        :rtype: str
        """
        return "" if str_eval is None else str_eval
