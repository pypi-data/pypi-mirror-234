"""DataCenter model for RegScale."""
from urllib.parse import urljoin

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger


class DataCenter(BaseModel):
    """DataCenter pydantic BaseModel."""

    id: int = 0
    uuid: str = ""
    facilityId: int
    parentId: int
    parentModule: str
    isPublic: bool = True
    facility: str = ""

    @staticmethod
    def from_dict(data: dict) -> "DataCenter":
        """Convert dict to DataCenter object
        :param data: dict to create object from
        :return: A DataCenter object
        """
        return DataCenter(**data)

    def post(self, app: Application) -> dict:
        """Post a DataCenter to RegScale
        :param app: The application instance
        :return: The response from the API
        :rtype: dict
        """
        api = Api(app)
        url = urljoin(app.config.get("domain"), "/api/datacenters")
        data = self.dict()
        response = api.post(url, json=data)
        return response.json()
