from pydantic import BaseModel
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from urllib.parse import urljoin


class ControlTestPlan(BaseModel):
    """
    ControlTestPlan class
    """

    id: int = None
    uuid: str = None
    test: str = None
    testId: str = None
    securityControlId: int = None
    archived: bool = False
    createdById: str = None
    dateCreated: str = None
    lastUpdatedById: str = None
    dateLastUpdated: str = None
    tenantsId: int = None
    isPublic: bool = True

    def insert_controltestplan(self, app: Application) -> dict:
        """
        Insert a ControlTestPlan into the database
        :param app: Application
        :type app: Application
        :return: JSON response
        :rtype: dict
        """
        # Convert the model to a dictionary
        api = Api(app)
        data = self.dict()
        api_url = urljoin(app.config["domain"], "/api/controltestplans")
        # Make the API call
        response = api.post(api_url, json=data)

        # Check the response
        if not response.ok:
            print(response.text)
            raise Exception(f"API request failed with status {response.status_code}")

        return response.json()

    @staticmethod
    def from_dict(obj: dict) -> "ControlTestPlan":
        """
        Create ControlTestPlan object from dict
        :param obj: dictionary
        :return: ControlTestPlan class
        :rtype: ControlTestPlan
        """
        return ControlTestPlan(**obj)
