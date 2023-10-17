"""Provide a SystemRoleExternalAssignments model."""
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application


class SystemRoleExternalAssignments(BaseModel):
    id: int = 0
    uuid: str = ""
    stakeholderId: int = 0
    roleId: int = 0

    @staticmethod
    def from_dict(data: dict) -> "SystemRoleExternalAssignments":
        """Convert dict to SystemRoleExternalAssignments object
        :param data: dict to create object from
        :return: A SystemRoleExternalAssignments object
        """
        return SystemRoleExternalAssignments(**data)

    def post(self, app: Application) -> Optional[dict]:
        """Post a SystemRoleExternalAssignments to RegScale
        :param app: The application instance
        :return: The response from the API or None
        :rtype: dict or None
        """
        api = Api(app)
        url = urljoin(app.config.get("domain"), "/api/systemRoleExternalAssignments")
        data = self.dict()
        response = api.post(url, json=data)
        return SystemRoleExternalAssignments(**response.json()) if response.ok else None
