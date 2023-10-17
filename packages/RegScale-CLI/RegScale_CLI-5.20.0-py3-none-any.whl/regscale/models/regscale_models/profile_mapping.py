from pydantic import BaseModel
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from urllib.parse import urljoin
from typing import List


class ProfileMapping(BaseModel):
    """
    Profile Mapping Model
    """

    id: int = 0
    profileID: int = None
    controlID: int = None
    tenantsId: int = 0
    createdById: str = None
    dateCreated: str = None
    dateLastUpdated: str = None
    isPublic: bool = True
    lastUpdatedById: str = None

    def insert_profile_mapping(self, app: Application) -> dict:
        """
        Insert a new profile mapping
        :param Application app: Application
        :return:dict of profile mapping
        :rtype: dict
        """
        api = Api(app)
        # Convert the model to a dictionary
        data = self.dict()
        api_url = urljoin(app.config["domain"], "/api/profileMapping")

        # Make the API call
        response = api.post(url=api_url, json=data)

        # Check the response
        if not response.ok:
            print(response.text)
            raise Exception(f"API request failed with status {response.status_code}")

        return response.json()

    def insert_batch(
        self, app: Application, mappings: List["ProfileMapping"]
    ) -> list[dict]:
        """
        Insert a new list of profile mappings as a batch
        :param Application app: Application
        :param List[ProfileMapping] mappings: List of profile mappings
        :return: list(dict) of profile mappings
        :rtype: list(dict)
        """
        api = Api(app)
        # Convert the model to a dictionary

        data = [item.dict() for item in mappings]
        for d in data:
            d["isPublic"] = "true"
        api_url = urljoin(app.config["domain"], "/api/profileMapping/batchCreate")

        # Make the API call
        response = api.post(url=api_url, json=data)

        # Check the response
        return response.json() if response.ok else response.raise_for_status()
