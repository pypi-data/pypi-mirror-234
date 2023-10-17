#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a Microsoft Defender for Cloud alerts """

# standard python imports
from dataclasses import dataclass
from typing import Any
from typing import List


@dataclass
class Location:
    countryCode: str = None
    countryName: str = None
    state: str = None
    city: str = None
    longitude: float = None
    latitude: float = None
    asn: int = None
    carrier: str = None
    organization: str = None
    organizationType: str = None
    cloudProvider: str = None
    systemService: str = None

    @staticmethod
    def from_dict(obj: Any) -> "Location":
        _countryCode = str(obj.get("countryCode"))
        _countryName = str(obj.get("countryName"))
        _state = str(obj.get("state"))
        _city = str(obj.get("city"))
        _longitude = float(obj.get("longitude"))
        _latitude = float(obj.get("latitude"))
        _asn = int(obj.get("asn"))
        _carrier = str(obj.get("carrier"))
        _organization = str(obj.get("organization"))
        _organizationType = str(obj.get("organizationType"))
        _cloudProvider = str(obj.get("cloudProvider"))
        _systemService = str(obj.get("systemService"))
        return Location(
            _countryCode,
            _countryName,
            _state,
            _city,
            _longitude,
            _latitude,
            _asn,
            _carrier,
            _organization,
            _organizationType,
            _cloudProvider,
            _systemService,
        )


@dataclass
class SourceAddress:
    ref: str = None

    @staticmethod
    def from_dict(obj: Any) -> "SourceAddress":
        _ref = str(obj.get("$ref"))
        return SourceAddress(_ref)


@dataclass
class Host:
    ref: str = None

    @staticmethod
    def from_dict(obj: Any) -> "Host":
        _ref = str(obj.get("$ref"))
        return Host(_ref)


@dataclass
class Entity:
    id: str = None
    resourceId: str = None
    type: str = None
    address: str = None
    location: Location = None
    hostName: str = None
    sourceAddress: SourceAddress = None
    name: str = None
    host: Host = None

    @staticmethod
    def from_dict(obj: Any) -> "Entity":
        _id = str(obj.get("$id"))
        _resourceId = str(obj.get("resourceId"))
        _type = str(obj.get("type"))
        _address = str(obj.get("address"))
        _location = Location.from_dict(obj.get("location"))
        _hostName = str(obj.get("hostName"))
        _sourceAddress = SourceAddress.from_dict(obj.get("sourceAddress"))
        _name = str(obj.get("name"))
        _host = Host.from_dict(obj.get("host"))
        return Entity(
            _id,
            _resourceId,
            _type,
            _address,
            _location,
            _hostName,
            _sourceAddress,
            _name,
            _host,
        )


@dataclass
class ExtendedProperties:
    alertId: str = None
    compromisedEntity: str = None
    clientIpAddress: str = None
    clientPrincipalName: str = None
    clientApplication: str = None
    investigationSteps: str = None
    potentialCauses: str = None
    resourceType: str = None
    killChainIntent: str = None

    @staticmethod
    def from_dict(obj: Any) -> "ExtendedProperties":
        _alertId = str(obj.get("alert Id"))
        _compromisedEntity = str(obj.get("compromised entity"))
        _clientIpAddress = str(obj.get("client IP address"))
        _clientPrincipalName = str(obj.get("client principal name"))
        _clientApplication = str(obj.get("client application"))
        _investigationSteps = str(obj.get("investigation steps"))
        _potentialCauses = str(obj.get("potential causes"))
        _resourceType = str(obj.get("resourceType"))
        _killChainIntent = str(obj.get("killChainIntent"))
        return ExtendedProperties(
            _alertId,
            _compromisedEntity,
            _clientIpAddress,
            _clientPrincipalName,
            _clientApplication,
            _investigationSteps,
            _potentialCauses,
            _resourceType,
            _killChainIntent,
        )


@dataclass
class ResourceIdentifier:
    id: str = None
    azureResourceId: str = None
    type: str = None
    azureResourceTenantId: str = None

    @staticmethod
    def from_dict(obj: Any) -> "ResourceIdentifier":
        _id = str(obj.get("$id"))
        _azureResourceId = str(obj.get("azureResourceId"))
        _type = str(obj.get("type"))
        _azureResourceTenantId = str(obj.get("azureResourceTenantId"))
        return ResourceIdentifier(_id, _azureResourceId, _type, _azureResourceTenantId)


@dataclass
class Properties:
    status: str = None
    timeGeneratedUtc: str = None
    processingEndTimeUtc: str = None
    version: str = None
    vendorName: str = None
    productName: str = None
    productComponentName: str = None
    alertType: str = None
    startTimeUtc: str = None
    endTimeUtc: str = None
    severity: str = None
    isIncident: bool = None
    systemAlertId: str = None
    correlationKey: str = None
    intent: str = None
    resourceIdentifiers: List[ResourceIdentifier] = None
    compromisedEntity: str = None
    alertDisplayName: str = None
    description: str = None
    remediationSteps: List[str] = None
    extendedProperties: ExtendedProperties = None
    entities: List[Entity] = None
    alertUri: str = None

    @staticmethod
    def from_dict(obj: Any) -> "Properties":
        _status = str(obj.get("status"))
        _timeGeneratedUtc = str(obj.get("timeGeneratedUtc"))
        _processingEndTimeUtc = str(obj.get("processingEndTimeUtc"))
        _version = str(obj.get("version"))
        _vendorName = str(obj.get("vendorName"))
        _productName = str(obj.get("productName"))
        _productComponentName = str(obj.get("productComponentName"))
        _alertType = str(obj.get("alertType"))
        _startTimeUtc = str(obj.get("startTimeUtc"))
        _endTimeUtc = str(obj.get("endTimeUtc"))
        _severity = str(obj.get("severity"))
        _isIncident = bool(obj.get("isIncident"))
        _systemAlertId = str(obj.get("systemAlertId"))
        _correlationKey = str(obj.get("correlationKey"))
        _intent = str(obj.get("intent"))
        _resourceIdentifiers = [
            ResourceIdentifier.from_dict(y) for y in obj.get("resourceIdentifiers")
        ]
        _compromisedEntity = str(obj.get("compromisedEntity"))
        _alertDisplayName = str(obj.get("alertDisplayName"))
        _description = str(obj.get("description"))
        _remediationSteps = [obj.get("remediationSteps")]
        _extendedProperties = ExtendedProperties.from_dict(
            obj.get("extendedProperties")
        )
        _entities = [Entity.from_dict(y) for y in obj.get("entities")]
        _alertUri = str(obj.get("alertUri"))
        return Properties(
            _status,
            _timeGeneratedUtc,
            _processingEndTimeUtc,
            _version,
            _vendorName,
            _productName,
            _productComponentName,
            _alertType,
            _startTimeUtc,
            _endTimeUtc,
            _severity,
            _isIncident,
            _systemAlertId,
            _correlationKey,
            _intent,
            _resourceIdentifiers,
            _compromisedEntity,
            _alertDisplayName,
            _description,
            _remediationSteps,
            _extendedProperties,
            _entities,
            _alertUri,
        )


@dataclass
class Alert:
    id: str
    name: str
    type: str
    properties: Properties

    @staticmethod
    def from_dict(obj: Any) -> "Alert":
        _id = str(obj.get("id"))
        _name = str(obj.get("name"))
        _type = str(obj.get("type"))
        _properties = Properties.from_dict(obj.get("properties"))
        return Alert(_id, _name, _type, _properties)
