#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" standard python imports """

from dataclasses import dataclass


@dataclass
class Objective:
    """RegScale Base Objective"""

    securityControlId: int
    id: int
    uuid: str
