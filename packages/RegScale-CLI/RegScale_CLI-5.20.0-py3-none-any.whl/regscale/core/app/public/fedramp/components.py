from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from lxml import etree

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.public.fedramp.fedramp_traversal import FedrampTraversal
from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models.asset import Asset
from regscale.models.regscale_models.components import Component
from regscale.models.regscale_models.interconnects import Interconnects
from regscale.models.regscale_models.link import Link
from regscale.models.regscale_models.ports_protocols import PortsProtocols
from regscale.models.regscale_models.properties import Properties
from regscale.models.regscale_models.references import References

logger = create_logger()

namespaces = {
    "oscal": "http://csrc.nist.gov/ns/oscal/1.0",
    "fedramp": "https://fedramp.gov/ns/oscal",
}

COMP = "Component"


# Use a helper function to safely get the first item in a list or return None
def safe_first_item(lst):
    return lst[0] if lst else None


def parse_common_component_data(component):
    """Parse common data for all component types."""
    component_data = {
        "uuid": component.get("uuid"),
        "type": component.get("type"),
        "title": safe_first_item(
            component.xpath("oscal:title/text()", namespaces=namespaces)
        ),
        "description": safe_first_item(
            component.xpath("oscal:description/oscal:p/text()", namespaces=namespaces)
        ),
        "status": safe_first_item(
            component.xpath("oscal:status/@state", namespaces=namespaces)
        ),
        "remarks": " ".join(
            component.xpath("oscal:remarks/p/text()", namespaces=namespaces)
        ),
    }
    return component_data


def parse_interconnection_data(component):
    """Parse data specific to interconnection components."""
    interconnection_data = {
        "direction": safe_first_item(
            component.xpath(
                'oscal:prop[@name="direction"]/@value', namespaces=namespaces
            )
        ),
        "ipv4_address_local": safe_first_item(
            component.xpath(
                'oscal:prop[@name="ipv4-address"][@class="local"]/@value',
                namespaces=namespaces,
            )
        ),
        "ipv4_address_remote": safe_first_item(
            component.xpath(
                'oscal:prop[@name="ipv4-address"][@class="remote"]/@value',
                namespaces=namespaces,
            )
        ),
        "service_processor": safe_first_item(
            component.xpath(
                'oscal:prop[@name="service-processor"][@ns="https://fedramp.gov/ns/oscal"]/@value',
                namespaces=namespaces,
            )
        ),
        "information": safe_first_item(
            component.xpath(
                'oscal:prop[@name="information"][@ns="https://fedramp.gov/ns/oscal"]/@value',
                namespaces=namespaces,
            )
        ),
        "port_or_circuit_name": safe_first_item(
            component.xpath(
                'oscal:prop[@name="port" or @name="circuit"][@ns="https://fedramp.gov/ns/oscal"]/@name',
                namespaces=namespaces,
            )
        ),
        "port_or_circuit_value": safe_first_item(
            component.xpath(
                'oscal:prop[@name="port" or @name="circuit"][@ns="https://fedramp.gov/ns/oscal"]/@value',
                namespaces=namespaces,
            )
        ),
        "connection_security": safe_first_item(
            component.xpath(
                'oscal:prop[@name="connection-security"][@ns="https://fedramp.gov/ns/oscal"]/@value',
                namespaces=namespaces,
            )
        ),
        "connection_security_remarks": safe_first_item(
            component.xpath(
                'oscal:prop[@name="connection-security"][@ns="https://fedramp.gov/ns/oscal"]/oscal:remarks/oscal:p/text()',
                namespaces=namespaces,
            )
        ),
    }
    return interconnection_data


def parse_roles(component, component_data):
    roles = []
    for role in component.xpath("oscal:responsible-role", namespaces=namespaces):
        role_data = dict()
        role_data["role_id"] = role.get("role-id")
        role_data["party_uuid"] = safe_first_item(
            role.xpath("oscal:party-uuid/text()", namespaces=namespaces)
        )
        if role_data["role_id"] == "asset-owner":
            component_data["asset_owner"] = role_data["party_uuid"]
        role_data["job_title"] = safe_first_item(
            role.xpath('oscal:prop[@name="job-title"]/@value', namespaces=namespaces)
        )
        roles.append(role_data)
    return roles


def parse_links(component, component_data):
    links = component.xpath("oscal:link/@href", namespaces=namespaces)
    rels = component.xpath("oscal:link/@rel", namespaces=namespaces)
    component_data["links"] = [
        {"rel": rel, "component_uuid": component_data["uuid"], "href": href}
        for rel, href in zip(rels, links)
    ]


def parse_properties(component, component_data):
    properties = []
    for prop in component.xpath("oscal:prop", namespaces=namespaces):
        name = prop.get("name")
        value = prop.get("value")
        remarks = safe_first_item(
            prop.xpath("oscal:remarks/oscal:p/text()", namespaces=namespaces)
        )
        properties.append({"key": name, "value": value, "remarks": remarks})
    logger.debug(f"Parsed {len(properties)} properties")
    component_data["props"] = properties
    return component_data


def parse_component(component):
    component_data: dict()
    component_data = parse_common_component_data(component)
    parse_links(component, component_data)
    component_data["responsible_roles"] = parse_roles(component, component_data)
    component_data = parse_properties(component, component_data)
    # this is a seperate module interconnections in regscale
    if component_data["type"] == "interconnection":
        # Parse properties using specific XPath queries and the safe_first_item function
        interconnection_data = parse_interconnection_data(component)
        component_data = {**component_data, **interconnection_data}

        properties = [
            {
                "key": "service-processor",
                "value": component_data.get("service_processor"),
            },
            {
                "key": "ipv4_address_local",
                "value": component_data.get("ipv4_address_local"),
            },
            {
                "key": "ipv4_address_remote",
                "value": component_data.get("ipv4_address_remote"),
            },
            {"key": "direction", "value": component_data.get("direction")},
            {"key": "information", "value": component_data.get("information")},
            {
                "key": "connection_security",
                "value": component_data.get("connection_security"),
            },
            {
                "key": "connection_security_remarks",
                "value": component_data.get("connection_security_remarks"),
            },
        ]

        component_data["properties"] = properties
        # Parse responsible roles
        component_data["aoid_remote"] = safe_first_item(
            component.xpath(
                'oscal:responsible-role[@role-id="isa-authorizing-official-remote"]/oscal:party-uuid/text()',
                namespaces=namespaces,
            )
        )
        component_data["aoid_local"] = safe_first_item(
            component.xpath(
                'oscal:responsible-role[@role-id="isa-authorizing-official-local"]/oscal:party-uuid/text()',
                namespaces=namespaces,
            )
        )
        component_data["isa_remote"] = safe_first_item(
            component.xpath(
                'oscal:responsible-role[@role-id="isa-poc-remote"]/oscal:party-uuid/text()',
                namespaces=namespaces,
            )
        )
        component_data["isa_local"] = safe_first_item(
            component.xpath(
                'oscal:responsible-role[@role-id="isa-poc-local"]/oscal:party-uuid/text()',
                namespaces=namespaces,
            )
        )
        roles = []
        for role in component.xpath("oscal:responsible-role", namespaces=namespaces):
            role_data = dict()
            role_data["party_uuid"] = role.text
            role_data["job_title"] = safe_first_item(
                role.xpath(
                    'oscal:prop[@name="job-title"]/@value', namespaces=namespaces
                )
            )
            roles.append(role_data)
        component_data["responsible_roles"] = roles

    elif component_data["type"] == "service":
        # Parsing logic for service type
        component_data["purpose"] = " ".join(
            component.xpath("oscal:purpose/text()", namespaces=namespaces)
        )
        component_data["used_by"] = safe_first_item(
            component.xpath('oscal:prop[@name="used-by"]/@value', namespaces=namespaces)
        )

        protocols = []
        for protocol in component.xpath("oscal:protocol", namespaces=namespaces):
            protocol_data = dict()
            protocol_data["used_by"] = safe_first_item(
                component.xpath(
                    'oscal:prop[@name="used-by"][@ns="https://fedramp.gov/ns/oscal"]/@value',
                    namespaces=namespaces,
                )
            )
            protocol_data["name"] = protocol.get("name")
            protocol_data["port_range_start"] = safe_first_item(
                protocol.xpath("oscal:port-range/@start", namespaces=namespaces)
            )
            protocol_data["port_range_end"] = safe_first_item(
                protocol.xpath("oscal:port-range/@end", namespaces=namespaces)
            )
            protocol_data["transport"] = safe_first_item(
                protocol.xpath("oscal:port-range/@transport", namespaces=namespaces)
            )
            protocols.append(protocol_data)

        component_data["protocols"] = protocols
        component_data["remarks"] = (
            " ".join(component.xpath("oscal:remarks/p/text()", namespaces=namespaces))
            if component.xpath("oscal:remarks/p/text()", namespaces=namespaces)
            else None
        )

    elif component_data["type"] == "subnet":
        # Parsing logic for subnet type
        component_data["asset_id"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="asset-id"]/@value', namespaces=namespaces
            )
        )
        component_data["ipv4_subnet"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="ipv4-subnet"]/@value', namespaces=namespaces
            )
        )
        component_data["is_scanned"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="is-scanned"]/@value', namespaces=namespaces
            )
        )

    elif component_data["type"] == "hardware":
        # Parsing logic for hardware type
        component_data["asset_type"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="asset-type"]/@value', namespaces=namespaces
            )
        )
        component_data["vendor_name"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="vendor-name"]/@value', namespaces=namespaces
            )
        )
        component_data["model"] = safe_first_item(
            component.xpath('oscal:prop[@name="model"]/@value', namespaces=namespaces)
        )
        component_data["version"] = safe_first_item(
            component.xpath('oscal:prop[@name="version"]/@value', namespaces=namespaces)
        )

    elif component_data["type"] == "software":
        # Parsing logic for software type
        component_data["asset_type"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="asset-type"]/@value', namespaces=namespaces
            )
        )
        component_data["baseline_configuration_name"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="baseline-configuration-name"]/@value',
                namespaces=namespaces,
            )
        )
        component_data["allows_authenticated_scan"] = safe_first_item(
            component.xpath(
                'oscal:prop[@name="allows-authenticated-scan"]/@value',
                namespaces=namespaces,
            )
        )

    return component_data


def map_asset_status(status) -> str:
    """Map asset status from OSCAL to internal representation."""
    status_mapping = {
        "operational": "Active (On Network)",
        "disposition": "Decommissioned",
        "under-development": "Off-Network",
    }
    return status_mapping.get(status, "Active (On Network)")


# Asset Creation Functions
def create_asset(
    component_data: Dict, user_id: str, spp_id: int, api_handler: APIHandler
) -> Dict:
    """
    Creates an asset record in the database
    :param Dict component_data:
    :param str user_id:
    :param int spp_id:
    :param APIHandler api_handler:
    :return: Dict of the created asset
    :rtype: Dict
    """
    asset = Asset(
        name=component_data["title"],
        description=component_data["description"],
        status=map_asset_status(component_data["status"]),
        assetType="Other",
        assetOwnerId=user_id,
        parentId=spp_id,
        parentModule="securityplans",
        ram=0,
        diskStorage=0,
        cpu=0,
        assetCategory="software"
        if component_data["type"] == "software"
        else "hardware",
        createdById=user_id,
        lastUpdatedById=user_id,
        securityPlanId=spp_id,
    )
    asset_resp = api_handler.insert_record("/api/assets", json=asset.dict())
    return asset_resp


def create_links(links, parent_id, parent_module, comp_uuid, user_id, api_handler):
    link_responses = []
    for link in links:
        if not link["href"].startswith("#"):
            if link["component_uuid"] == comp_uuid:
                obj = Link(
                    title=link["rel"],
                    url=link["href"],
                    parentID=parent_id,
                    parentModule=parent_module,
                    createdById=user_id,
                    lastUpdatedById=user_id,
                )
                resp = api_handler.insert_record("/api/links", json=obj.dict())
                link_responses.append(resp)
        else:
            obj = References(
                title=link["rel"],
                identificationNumber=link["href"],
                link=link["href"],
                referenceType="Other",
                parentId=parent_id,
                parentModule=parent_module,
                createdById=user_id,
            )
            obj.create_new_references(return_object=False)
    return link_responses


def parse_ssp_components(trv: FedrampTraversal):
    """
    Parses the OSCAL XML file and extracts the component data.
    :param FedrampTraversal trv: FedRAMP Traversal object
    :return: A list of dictionaries containing the component data
    """
    try:
        ssp_id = trv.ssp_id
        api_handler = APIHandler()
        user_id = trv.api.config.get("userId")
        # Loop through each components node to extract its properties
        components = trv.root.xpath("//oscal:component", namespaces=namespaces)
        logger.info(f"Found {len(components)} components for parsing.")
        trv.log_info(
            {
                "model_layer": "System Implementation",
                "record_type": "Component",
                "event_msg": f"Found {len(components)} components for parsing.",
            }
        )
        components_dict = dict()
        for component in components:
            # logger.info(f"component {component}")
            component_data = parse_component(component)
            # logger.info(f"component_data {component_data}")
            comp_id = 0
            regcomp_module = "components"
            if component_data["type"] == "interconnection":
                regcomp_module = "interconnects"
                inter_comp_resp = create_interconnection(
                    component_data=component_data,
                    user_id=user_id,
                    ssp_id=ssp_id,
                    api_handler=api_handler,
                )
                comp_id = (
                    inter_comp_resp["id"]
                    if inter_comp_resp and "id" in inter_comp_resp
                    else 0
                )

            elif component_data["type"] in ["subnet", "hardware", "software"]:
                asset_response = create_asset(
                    component_data, user_id, ssp_id, api_handler
                )
                comp_id = (
                    asset_response["id"]
                    if asset_response and "id" in asset_response
                    else 0
                )
                regcomp_module = "assets"
            elif component_data["type"] == "validation":
                comp_resp = create_component(
                    component_data, ssp_id, user_id, api_handler
                )
                if comp_resp:
                    comp_id = comp_resp["id"] if comp_resp and "id" in comp_resp else 0
            else:
                comp_resp = create_component(
                    component_data, ssp_id, user_id, api_handler
                )
                comp_id = comp_resp["id"] if comp_resp and "id" in comp_resp else 0
            # logger.info(f"comp_id {comp_id}")
            if comp_id == 0:
                continue

            component_data["id"] = comp_id
            component_data["module"] = regcomp_module
            components_dict[component_data["uuid"]] = component_data
            logger.info(f"Component {component_data['uuid']} created.")
            if "properties" in component_data and len(component_data["properties"]) > 0:
                if new_props := create_properties(
                    properties=component_data["properties"],
                    parent_id=comp_id,
                    parent_module=regcomp_module,
                    api_handler=api_handler,
                    user_id=user_id,
                ):
                    trv.log_info(
                        {
                            "record_type": "Property",
                            "event_msg": f"Created {len(new_props)} properties for component {component_data['uuid']}.",
                            "model_layer": COMP,
                        }
                    )
                else:
                    trv.log_error(
                        {
                            "record_type": "Property",
                            "event_msg": f"Failed to create know properties for component {component_data['uuid']}.",
                            "missing_element": "Properties",
                            "model_layer": COMP,
                        }
                    )
            if "props" in component_data and len(component_data["props"]) > 0:
                if props := create_properties(
                    properties=component_data["props"],
                    user_id=user_id,
                    parent_id=comp_id,
                    parent_module=regcomp_module,
                    api_handler=api_handler,
                ):
                    trv.log_info(
                        {
                            "record_type": "Property",
                            "event_msg": f"Created {len(props)} property(s) for component {component_data['uuid']}.",
                            "model_layer": COMP,
                        }
                    )
                else:
                    trv.log_error(
                        {
                            "record_type": "Property",
                            "event_msg": f"Failed to create properties for component {component_data['uuid']}.",
                            "missing_element": "Properties",
                            "model_layer": COMP,
                        }
                    )

            if "protocols" in component_data and len(component_data["protocols"]) > 0:
                if protocols := create_protocols(
                    protocols=component_data["protocols"],
                    parent_id=comp_id,
                    parent_module=regcomp_module,
                    api_handler=api_handler,
                    user_id=user_id,
                ):
                    trv.log_info(
                        {
                            "record_type": "Protocol",
                            "event_msg": f"Created {len(protocols)} protocol(s) for component {component_data['uuid']}.",
                            "model_layer": COMP,
                        }
                    )
                else:
                    trv.log_error(
                        {
                            "record_type": "Protocol",
                            "event_msg": f"Failed to create protocol(s) for component {component_data['uuid']}.",
                            "missing_element": "Protocols",
                            "model_layer": COMP,
                        }
                    )
            if "links" in component_data and len(component_data["links"]) > 0:
                if links := create_links(
                    links=component_data["links"],
                    parent_id=comp_id,
                    parent_module=regcomp_module,
                    comp_uuid=component_data["uuid"],
                    user_id=user_id,
                    api_handler=api_handler,
                ):
                    trv.log_info(
                        {
                            "record_type": "Link",
                            "event_msg": f"Created {len(links)} link(s) for component {component_data['uuid']}.",
                            "model_layer": COMP,
                        }
                    )
                else:
                    trv.log_error(
                        {
                            "record_type": "Link",
                            "event_msg": f"Unable to create link(s) for component {component_data['uuid']}.",
                            "missing_element": "Link",
                            "model_layer": COMP,
                        }
                    )
        return components_dict
    except Exception as e:
        trv.log_error(
            {
                "record_type": "Component",
                "event_msg": f"Unable to create component {component_data['uuid']}.",
                "missing_element": "Component",
                "model_layer": COMP,
            }
        )
        logger.error(f"Error parsing components item: {str(e)}")


def create_properties(
    properties: List[Dict],
    parent_id,
    parent_module,
    api_handler: APIHandler,
    user_id: str,
) -> list:
    """
    Creates a new property in the Regscale.
    :param List[Dict] properties: The properties to create
    :param int parent_id: The ID of the parent object
    :param str parent_module: The module of the parent object
    :param APIHandler api_handler: The API handler
    :param str user_id: The ID of the user creating the property
    :return: list of created properties
    :rtype: list
    """
    created_properties = []
    for prop in properties:
        prop_obj = Properties(
            parentId=parent_id,
            parentModule=parent_module,
            key=prop["key"],
            value=prop["value"],
            createdById=user_id,
        )
        new_prop = api_handler.insert_record("/api/properties", json=prop_obj.dict())
        logger.info(f"Created property {new_prop['key']} with ID of {new_prop['id']}")
        if new_prop:
            created_properties.append(new_prop)
        else:
            continue
    return created_properties


def create_component(
    component_data: Dict, ssp_id: int, user_id: str, api_handler: APIHandler
) -> Optional[Any]:
    """
    Creates a new component in the OSCAL database.
    :param Dict component_data: The component data
    :param int ssp_id: The ID of the SSP
    :param str user_id: The ID of the user creating the component
    :param APIHandler api_handler: The API handler
    :return: The response object of the newly created component
    :rtype: Any or None
    """
    comp = Component(
        id=0,
        isPublic="true",
        uuid=component_data["uuid"],
        title=component_data["title"],
        description=component_data["description"],
        purpose=component_data["purpose"] if "purpose" in component_data else "",
        componentType=component_data["type"],
        componentOwnerId=component_data["asset_owner"]
        if "asset_owner" in component_data and component_data["asset_owner"] is not None
        else user_id,
        securityPlansId=ssp_id,
        status="Active"
        if "status" in component_data and component_data["status"] == "operational"
        else "Draft/Pending",
        cmmcAssetType=component_data["asset_type"]
        if "asset_type" in component_data
        else None,
        cmmcExclusion="false",
        lastUpdatedById=user_id,
        createdById=user_id,
        dateCreated=get_current_datetime(),
        dateLastUpdated=get_current_datetime(),
    )
    # insert component
    # logger.info(f"creating component {json.dumps(comp.dict(), indent=4)}")
    resp_json = api_handler.insert_record("/api/components", json=comp.dict())
    if resp_json:
        create_component_mapping(
            resp_json, ssp_id=ssp_id, user_id=user_id, api_handler=api_handler
        )
        return resp_json
    else:
        logger.error(f"failed to insert comp {comp.dict()}")
        return None


def create_component_mapping(
    component_data: Dict, ssp_id: int, user_id: str, api_handler: APIHandler
) -> None:
    mapping = {
        "componentId": component_data["id"],
        "securityPlanId": ssp_id,
        "createdById": user_id,
        "isPublic": "true",
    }
    api_handler.insert_record("/api/componentmapping", json=mapping)


def create_protocols(
    protocols: List[Dict],
    parent_id: int,
    parent_module: str,
    user_id: str,
    api_handler: APIHandler,
) -> Optional[List[Any]]:
    """
    Creates a new ports and protocol record.
    :param List[Dict] protocols: The protocol to create
    :param int parent_id: The ID of the parent module
    :param str parent_module: The module of the parent module
    :param str user_id: The ID of the user creating the component
    :param APIHandler api_handler: The API handler
    :return: The response object of the newly created component or None
    :rtype: Any or None
    """
    responses = []
    for protocol in protocols:
        protocol_obj = PortsProtocols(
            parentId=parent_id,
            parentModule=parent_module,
            startPort=protocol["port_range_start"],
            endPort=protocol["port_range_end"],
            protocol=protocol["transport"],
            service=protocol["name"],
            purpose=None,
            usedBy=protocol["used_by"],
            createdById=user_id,
            lastUpdatedById=user_id,
            dateCreated=get_current_datetime(),
            dateLastUpdated=get_current_datetime(),
        )
        response = api_handler.insert_record(
            "/api/portsProtocols", json=protocol_obj.dict()
        )
        responses.append(response)
    return responses


def create_interconnection(
    component_data: Dict, user_id: str, ssp_id: int, api_handler
) -> Optional[Any]:
    """
    Creates a new interconnection record.
    :param Dict component_data: The component data
    :param str user_id: The ID of the user creating the component
    :param int ssp_id: The ID of the SSP
    :param APIHandler api_handler: The API handler
    :return: The ID of the newly created component
    :rtype: Any or None
    """
    intercon = Interconnects(
        uuid=component_data["uuid"],
        description=component_data["description"],
        purpose=component_data["purpose"] if "purpose" in component_data else None,
        name=component_data["title"],
        dataDirection=component_data["direction"],
        status="Approved",
        authorizationType="Interconnect Security Agreement (ISA)",
        createdById=user_id,
        dateCreated=get_current_datetime(),
        dateLastUpdated=get_current_datetime(),
        lastUpdatedById=user_id,
        tenantsId=0,
        parentId=ssp_id,
        parentModule="securityplans",
        externalIpAddress=component_data["ipv4_address_remote"],
        sourceIpAddress=component_data["ipv4_address_local"],
        categorization="Moderate",
        connectionType="Internet or Firewall Rule",
        organization=component_data["aoid_local"]
        if "aoid_local" in component_data
        else component_data["aoid_remote"],
        # component_data['aoid_local'] if 'aoid_local' in component_data else component_data['aoid_remote']
        aOId=user_id,
        # component_data['isa_local'] if 'isa_local' in component_data else component_data['isa_remote']
        interconnectOwnerId=user_id,
        expirationDate=get_expiration_date(),
        agreementDate=get_current_datetime(),
    )

    response = api_handler.insert_record("/api/interconnections", json=intercon.dict())
    return response


def get_expiration_date():
    # Get the current date and time in UTC + 30 days
    now = datetime.utcnow()

    # Add 30 days to the current date and time
    expiration_date = now + timedelta(days=30)

    # Convert to Zulu time format (ISO 8601)
    expiration_date_str = expiration_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return expiration_date_str
