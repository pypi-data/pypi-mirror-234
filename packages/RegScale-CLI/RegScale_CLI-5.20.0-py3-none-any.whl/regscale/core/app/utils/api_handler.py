from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.utils.app_utils import create_logger

logger = create_logger()


class APIHandler:
    def __init__(self):
        self.app = Application()
        self.api = Api(self.app)
        self.domain = self.app.config.get("domain")

    def fetch_record(self, endpoint, headers: Dict = None, params: Any = None) -> Any:
        """
        Fetch data from an API endpoint.

        :param str endpoint: API endpoint to fetch data from, the domain is added automatically
        :param Dict headers: Optional headers
        :param Any params: Optional query parameters
        :return: Fetched data
        """
        try:
            endpoint = urljoin(self.domain, endpoint)
            response = self.api.get(endpoint, headers=headers, params=params)
            if response.ok:
                return response.json()
            else:
                logger.error(
                    f"Failed to fetch data. Status code: {response.status_code}"
                )
                return None
        except Exception as e:
            logger.error(f"An error occurred while fetching data: {e}")
            return None

    def insert_record(
        self,
        endpoint: str,
        headers: Dict = None,
        json: Optional[Union[Dict, str, List]] = None,
        data: Dict = None,
        files: List = None,
        params=None,
    ) -> Any:
        """
        Insert new data into an API endpoint.
        :param str endpoint: API endpoint to insert data into, the domain is added automatically
        :param Dict headers: Optional headers
        :param Dict data: Data to insert
        :param Optional[Union[Dict, str, List]]  json: JSON data to insert
        :param List files: Files to upload
        :param  params: Optional query parameters
        :return: Inserted data
        """
        try:
            endpoint = urljoin(self.domain, endpoint)
            logger.debug(f"Inserting data into {endpoint}")
            response = self.api.post(
                endpoint,
                headers=headers,
                data=data,
                json=json,
                files=files,
                params=params,
            )
            if response.ok:
                return response.json()
            else:
                logger.error(
                    f"Failed to insert data. Status code: {response.status_code} and response text: {response.text}"
                )
                response.raise_for_status()
                return response
        except Exception as e:
            logger.error(f"An error occurred while inserting data: {e}")
            return None

    def update_record(
        self, endpoint: str, headers: Dict = None, json: Dict = None, params: Any = None
    ) -> Any:
        """
        Update existing data at an API endpoint.

        :param str endpoint: API endpoint to update data at the domain is added automatically
        :param Dict headers: Optional headers
        :param Dict json: JSON data to update
        :param Any params: Optional query parameters
        :return: Updated data
        """
        try:
            endpoint = urljoin(self.domain, endpoint)
            response = self.api.put(endpoint, headers=headers, json=json, params=params)
            if response.ok:
                return response.json()
            else:
                logger.error(
                    f"Failed to update data. Status code: {response.status_code}"
                )
                return None
        except Exception as e:
            logger.error(f"An error occurred while updating data: {e}")
            return None
