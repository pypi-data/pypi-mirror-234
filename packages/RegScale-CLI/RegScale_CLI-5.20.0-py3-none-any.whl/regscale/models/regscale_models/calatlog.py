from pydantic import BaseModel
from regscale.core.app.api import Api
from regscale.core.app.application import Application
from urllib.parse import urljoin
from typing import Optional


class Catalog(BaseModel):
    """Catalog class"""

    id: Optional[int] = None
    abstract: Optional[str] = None
    datePublished: Optional[str] = None
    description: Optional[str] = None
    keywords: Optional[str] = None
    lastRevisionDate: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    tenantsId: Optional[int] = None
    uuid: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    master: bool = False
    sourceOscalURL: Optional[str] = None
    archived: bool = False
    isPublic: bool = True

    def insert_catalog(self, app: Application) -> "Catalog":
        """
        Insert catalog into database
        :param app: Application
        :return: Catalog
        :rtype: Catalog
        """
        # Convert the model to a dictionary
        api = Api(app)
        data = self.dict()
        api_url = urljoin(app.config["domain"], "/api/catalogues")
        # Make the API call
        response = api.post(api_url, json=data)

        # Check the response
        if not response.ok:
            print(f"API request failed with status {response.text}")
            raise Exception(f"API request failed with status {response.status_code}")

        return self.from_dict(response.json())

    @staticmethod
    def get_catalogs(app: Application) -> list:
        """
        Get all catalogs from database
        :param app: Application
        :return: list of catalogs
        :rtype: list
        """
        api = Api(app)
        api_url = urljoin(app.config["domain"], "/api/catalogues")
        response = api.get(api_url)
        if not response.ok:
            print(f"API request failed with status {response.text}")
            raise Exception(f"API request failed with status {response.status_code}")
        return response.json()

    @staticmethod
    def from_dict(obj: dict) -> "Catalog":
        """
        Create Catalog object from dict
        :param obj: dictionary
        :return: Catalog class
        :rtype: Catalog
        """
        return Catalog(**obj)
