#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale User """

# standard python imports
import random
import string
from dataclasses import asdict, dataclass


def generate_password() -> str:
    """
    Generates a random string that is 12-20 characters long
    :return: random string 12-20 characters long
    :rtype: str
    """
    # select a random password length between 12-20 characters
    length = random.randint(12, 20)

    # get all possible strings to create a password
    all_string_chars = (
        string.ascii_lowercase
        + string.ascii_uppercase
        + string.digits
        + string.punctuation
    )

    # randomly select characters matching the random length
    temp = random.sample(all_string_chars, length)
    # return a string from the temp list of samples
    return "".join(temp)


@dataclass
class User:
    """User Model"""

    userName: str  # Required
    email: str  # Required
    firstName: str  # Required
    lastName: str  # Required
    tenantId: int  # Required
    initials: str = None
    id: str = None
    password: str = generate_password()
    name: str = None
    workPhone: str = None
    mobilePhone: str = None
    avatar: str = None
    jobTitle: str = None
    orgId: str = None
    pictureURL: str = None
    activated: bool = False
    emailNotifications: bool = True
    ldapUser: bool = False
    externalId: str = None
    dateCreated: str = None
    lastLogin: str = None
    readOnly: bool = True

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

    def dict(self) -> dict:
        """
        Create a dictionary from the Asset dataclass
        :return: Dictionary of Asset
        :rtype: dict
        """
        return {k: v for k, v in asdict(self).items()}
