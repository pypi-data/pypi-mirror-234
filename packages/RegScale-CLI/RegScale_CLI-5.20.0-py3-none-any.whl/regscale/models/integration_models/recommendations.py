#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a Microsoft Defender 365 recommendations """

# standard python imports
from dataclasses import dataclass


@dataclass
class Recommendations:
    """Recommendations Model"""

    id: str  # Required
    data: dict  # Required
    analyzed: bool = False
    created: bool = False

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
