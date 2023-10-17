"""StakeHolders pydantic BaseModel."""
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseModel, validator

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger

logger = create_logger()


class StakeHolders(BaseModel):
    id: int = 0
    name: str = ""
    shortname: str = ""
    title: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    otherID: str = ""
    notes: str = ""
    parentId: int
    parentModule: str

    @validator("email", pre=True, always=True)
    def convert_email_none_to_empty_str(cls, value):
        """Convert a none email to an empty string"""
        return value if value is not None else ""

    @validator("shortname", pre=True, always=True)
    def convert_shortname_none_to_empty_str(cls, value):
        """Convert a none shortname to an empty string"""
        return value if value is not None else ""

    @validator("notes", pre=True, always=True)
    def convert_notes_none_to_empty_str(cls, value):
        """Convert a none notes to an empty string"""
        return value if value is not None else ""

    @staticmethod
    def from_dict(data: dict) -> "StakeHolders":
        """Convert dict to StakeHolders object
        :param data: dict to create object from
        :return: A StakeHolders object
        """
        return StakeHolders(**data)

    def post(self, app: Application) -> Optional[dict]:
        """Post a StakeHolders to RegScale
        :param app: The application instance
        :return: The response from the API or None
        :rtype: dict or None
        """
        api = Api(app)
        url = urljoin(app.config.get("domain"), "/api/stakeholders")
        data = self.dict()
        response = api.post(url, json=data)
        return response.json() if response.ok else None

    @staticmethod
    def get_all_by_parent(
        app: Application, parentModule: str, parentId: int
    ) -> Optional[list[dict]]:
        """
        Get all stakeholders in parentModule with parentId
        """
        api = Api(app)
        url = urljoin(
            app.config.get("domain"),
            f"/api/stakeholders/getAllByParent/{parentId}/{parentModule}",
        )
        response = api.get(url)
        return [StakeHolders(**_) for _ in response.json()] if response.ok else None
