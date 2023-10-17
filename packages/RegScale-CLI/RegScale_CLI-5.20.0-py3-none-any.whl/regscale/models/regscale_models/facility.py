"""Facility model for RegScale."""
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application


class Facilities(BaseModel):
    """Data Model for Facilities"""

    id: int = 0
    name: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zipCode: str = ""
    status: str = ""
    latitude: Optional[float] = 0
    longitude: Optional[float] = 0
    createdBy: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    lastUpdatedBy: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    isPublic: bool = True
    dateLastUpdated: Optional[str]

    @staticmethod
    def from_dict(data: dict) -> "Facilities":
        """Convert dict to Facilities object
        :param data: dict to create object from
        :return: A Facilities object
        """
        return Facilities(**data)

    def post(self, app: Application) -> Optional[dict]:
        """Post a Facility to RegScale
        :param app: The application instance
        :return: The response from the API or None
        :rtype: dict or None
        """
        api = Api(app)
        url = urljoin(app.config.get("domain"), "/api/facilities")
        data = self.dict()
        response = api.post(url, json=data)
        return response.json() if response.ok else None
