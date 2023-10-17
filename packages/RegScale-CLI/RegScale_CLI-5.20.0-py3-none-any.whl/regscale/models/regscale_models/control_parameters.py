from pydantic import BaseModel
from typing import Optional
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from urllib.parse import urljoin


class ControlParameter(BaseModel):
    """
    ControlParameter class
    """

    id: int = None
    uuid: str = None
    text: str = None
    parameterId: str = None
    securityControlId: int = None
    archived: bool = False
    createdById: str = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    tenantsId: int = None
    dataType: str = None
    isPublic: bool = True
    default: Optional[str] = None

    def insert_parameter(self, app: Application) -> dict:
        """
        Insert a new control parameter
        :param app: Application object
        :return: JSON response
        :rtype: dict of a control parameter
        """
        # Convert the model to a dictionary
        api = Api(app)
        data = self.dict()
        api_url = urljoin(app.config["domain"], "/api/controlparameters")
        # Make the API call
        response = api.post(api_url, json=data)

        # Check the response
        if not response.ok:
            print(response.text)
            raise Exception(f"API request failed with status {response.status_code}")

        return response.json()

    @staticmethod
    def from_dict(obj: dict) -> "ControlParameter":
        """
        Create ControlParameter object from dict
        :param obj: dictionary
        :return: ControlParameter class
        :rtype: ControlParameter
        """
        return ControlParameter(**obj)
