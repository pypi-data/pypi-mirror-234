from datetime import datetime

import requests
from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.models.regscale_models.objective import Objective


class ImplementationOption(BaseModel, Objective):
    """RegScale Implementation Option"""

    id: int = 0
    name: str  # Required
    description: str  # Required
    acceptability: str
    otherId: str
    securityControlId: int
    objectiveId: int
    createdById: str = None
    lastUpdatedById: str = None
    dateCreated: str = datetime.now().isoformat()
    dateLastUpdated: str = datetime.now().isoformat()
    archived: bool = False

    def __eq__(self, other):
        """
        Check if two ImplementationOption objects are equal
        :param other: ImplementationOption object to compare
        :return: True if equal, False if not
        :rtype: bool
        """
        return (
            self.name == other.name
            and self.description == other.description
            and self.objectiveId == other.objectiveId
            and self.securityControlId == other.securityControlId
        )

    def __hash__(self):
        """
        Hash a ImplementationOption object
        :return: Hashed ImplementationOption object
        :rtype: int
        """
        return hash(
            (self.name, self.description, self.objectiveId, self.securityControlId)
        )

    @staticmethod
    def fetch_implementation_options(
        app: Application, control_id: int
    ) -> list["ImplementationOption"]:
        """
        Fetch list of implementation objectives by control id
        :param Application app: Application Instance
        :param int control_id: Security Control ID
        :return: A list of Implementation Objectives as a dictionary from RegScale via API
        :rtype: list[dict]
        """
        results = []
        logger = create_logger()
        api = Api(app)
        res = api.get(
            url=app.config["domain"]
            + f"/api/implementationoptions/getByControl/{control_id}"
        )
        if res.ok:
            try:
                results = [ImplementationOption(**opt) for opt in res.json()]
            except requests.RequestException.JSONDecodeError:
                logger.warning("Unable to find control implementation objectives.")
        return results
