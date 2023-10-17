"""Mappings for System Roles."""
import json
from typing import List, Optional, Union

from lxml import etree

from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.public.fedramp.mappings.values import (
    UUID,
    FunctionPerformed,
    PropName,
    PropValue,
    RoleId,
    Title,
)
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.system_roles import SystemRoles


def create_system_role(element: etree._Element) -> SystemRoles:
    """
    Create a SystemRoles object from an XML Element
    :param element: The XML Element to parse
    :return: A SystemRoles object
    :rtype: SystemRoles
    """
    data = {}
    for field in [UUID, Title, FunctionPerformed]:
        for elem in element:
            results = field.parse_from_element(elem)
            if results:
                data[field.value] = results[1]
    app = Application()
    data["id"] = 0
    data["createdById"] = app.config.get("userId")
    data["lastUpdatedById"] = app.config.get("userId")
    data["dateCreated"] = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    data["dateLastUpdated"] = get_current_datetime(dt_format="%Y-%m-%dT%H:%M:%S.%fZ")
    return SystemRoles(**data)


if __name__ == "__main__":
    xml_string = """
    <user uuid="16ec71e7-025c-43e4-9d3f-3acb485fac2e">
         <title>[SAMPLE]Client Administrator</title>
         <prop ns="https://fedramp.gov/ns/oscal" name="sensitivity" value="moderate"/>
         <prop name="privilege-level" value="non-privileged"/>
         <prop name="type" value="external"/>
         <role-id>external</role-id>
         <authorized-privilege>
            <title>Portal administration</title>
            <function-performed>Add/remove client users</function-performed>
            <function-performed>Create, modify and delete client applications</function-performed>
         </authorized-privilege>
      </user>
    """
    xml = etree.fromstring(xml_string)
    uuid = UUID.parse_from_element(xml)
    title = Title.parse_from_element(xml)
    function_performed = FunctionPerformed.parse_from_element(
        xml.find("authorized-privilege")
    )
    authorized_privilege = Title.parse_from_element(xml.find("authorized-privilege"))
    print(uuid)
    print(title)
    print(function_performed)
    print(authorized_privilege)
    prop_names = PropName.parse_from_element(xml)
    prop_values = PropValue.parse_from_element(xml)
    print(prop_names)
    print(prop_values)
    role_id = RoleId.parse_from_element(xml)
    print(role_id)
    for name, value in zip(prop_names, prop_values):
        print(f"{name[1]}: {value[1]}")
        if name[1] == "sensitivity":
            sensitivity_level = value[1]
        elif name[1] == "privilege-level":
            access_level = value[1]
        elif name[1] == "type":
            role_type = value[1].capitalize()
    print(sensitivity_level)
    print(access_level)
    print(role_type)
