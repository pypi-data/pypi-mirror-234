# !/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale File """
# flake8: noqa
# standard python imports
import mimetypes
import os
import sys
from io import BytesIO
from typing import Optional, Union

from pydantic import BaseModel
from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.utils.app_utils import (
    compute_hash,
    error_and_exit,
    get_current_datetime,
    get_file_name,
    get_file_type,
)


class File(BaseModel):
    """File Model"""

    # fileHash and shaHash are not required because this is due
    # fileHash is the old method and shaHash is the new method in RegScale
    # We are not sure which one will be used/returned
    id: str
    trustedDisplayName: str
    trustedStorageName: str
    size: int
    fullPath: str
    uploadedById: str
    uploadedDate: str = get_current_datetime()
    fileHash: Optional[str] = None
    shaHash: Optional[str] = None
    parentId: Optional[int] = 0
    parentModule: Optional[str] = ""
    tags: Optional[str] = ""

    @staticmethod
    def download_file_from_regscale_to_memory(
        api: Api, record_id: int, module: str, stored_name: str, file_hash: str
    ) -> bytes:
        """
        Download a file from RegScale
        :param Api api: API object
        :param int record_id: RegScale record ID
        :param str module: RegScale module
        :param str stored_name: RegScale stored name
        :param str file_hash: RegScale file hash
        :return: Bytes of file as BytesIO object
        :rtype: BytesIO
        """
        response = api.get(
            url=f'{api.config["domain"]}/api/files/downloadFile/{record_id}/{module}/{stored_name}/{file_hash}'
        )
        response.raise_for_status()
        return response.content

    @staticmethod
    def get_files_for_parent_from_regscale(
        api: Api, parent_id: int, parent_module: str
    ) -> list["File"]:
        """
        Function to download all files from RegScale for the provided parent ID and module
        :param Api api: API object
        :param int parent_id: RegScale parent ID
        :param str parent_module: RegScale module
        :raises: JSONDecodeError if API response cannot be converted to a json object
        :return: List of file objects from RegScale
        :rtype: list[File]
        """
        # get the files from RegScale
        files = []
        try:
            file_response = api.get(
                url=f"{api.config['domain']}/api/files/{parent_id}/{parent_module}"
            ).json()
            files = [File(**file) for file in file_response]
        except JSONDecodeError:
            logger = create_logger()
            logger.error(
                "Unable to retrieve files from RegScale for the provided ID & module."
            )
        except Exception as ex:
            error_and_exit(f"Unable to retrieve files from RegScale.\n{ex}")
        return files

    @staticmethod
    def delete_file(app: Application, file: "File") -> bool:
        """
        Delete a file from RegScale
        :param Application app: Application Instance
        :param File file: File to delete in RegScale
        :return: Whether the file was deleted
        :rtype: bool
        """
        api = Api(app)

        response = api.delete(app.config["domain"] + f"/api/files/{file.id}")
        return response.ok

    @staticmethod
    def upload_file_to_regscale(
        file_name: str,
        parent_id: int,
        parent_module: str,
        api: Api,
        file_data: Optional[Union[bytes, dict, bool]] = None,
        return_object: bool = False,
        tags: Optional[str] = None,
    ) -> Optional[Union[bytes, dict, bool]]:
        """
        Function that will create and upload a file to RegScale to the provided parent_module and parent_id
        returns whether the file upload was successful or not
        :param str file_name: Path to the file to upload
        :param int parent_id: RegScale parent ID
        :param str parent_module: RegScale module
        :param Api api: API object
        :param bytes file_data: File data to upload, defaults to None
        :param bool return_object: Whether to return the file object from RegScale, defaults to False
        :param str tags: Tags to add to the file, defaults to None
        :return: Boolean indicating whether the file upload was successful or not
        :rtype: Optional[bytes, dict, bool]
        """

        def _create_regscale_file(
            file_path: str,
            parent_id: int,
            parent_module: str,
            api: Api,
            file_data: Optional[bytes] = None,
        ) -> Optional[dict]:
            """
            Function to create a file within RegScale via API
            :param str file_path: Path to the file
            :param int parent_id: RegScale parent ID
            :param str parent_module: RegScale module
            :param Api api: API object
            :param bytes file_data: File data to upload, defaults to None
            :raises: General error if unacceptable file type was provided
            :return: Dictionary of the file object from RegScale or None
            :rtype: Optional[dict]
            """
            # get the file type of the provided file_path
            file_type = get_file_type(file_path)

            # get the file name from the provided file_path
            file_name = get_file_name(file_path)

            # set up file headers
            file_headers = {
                "Authorization": api.config["token"],
                "Accept": "application/json",
            }

            # see file_type is an acceptable format and set the file_type_header accordingly
            try:
                file_type_header = mimetypes.types_map[file_type]
            except KeyError:
                if file_type == ".xlsx":
                    file_type_header = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                else:
                    logger = create_logger()
                    logger.warning(f"Unacceptable file type for upload: {file_type}")
                    return None

            # set the files up for the RegScale API Call
            files = [
                (
                    "file",
                    (
                        file_name,
                        file_data or open(file_path, "rb").read(),
                        file_type_header,
                    ),
                )
            ]

            file_like_object = (
                BytesIO(file_data) if file_data else open(file_path, "rb")
            )

            with file_like_object:
                data = {
                    "id": parent_id,
                    "module": parent_module,
                    "shaHash": compute_hash(file_like_object),
                }

            # make the api call
            file_response = api.post(
                url=f"{api.config['domain']}/api/files/file",
                headers=file_headers,
                data=data,
                files=files,
            )
            if not file_response.ok:
                logger = create_logger()
                logger.warning(f"{file_response.status_code} - {file_response.text}")
            return file_response.json() if file_response.ok else None

        if regscale_file := _create_regscale_file(
            file_path=file_name,
            parent_id=parent_id,
            parent_module=parent_module,
            api=api,
            file_data=file_data,
        ):
            # set up headers for file upload
            file_headers = {
                "Authorization": api.config["token"],
                "accept": "application/json, text/plain, */*",
            }

            # set up file_data payload with the regscale_file dictionary
            new_file = File(
                uploadedBy="",
                parentId=parent_id,
                tags=tags,
                parentModule=parent_module,
                uploadedById=api.config["userId"],
                id=regscale_file["id"],
                fullPath=regscale_file["fullPath"],
                trustedDisplayName=regscale_file["trustedDisplayName"],
                trustedStorageName=regscale_file["trustedStorageName"],
                uploadDate=regscale_file["uploadDate"],
                fileHash=regscale_file["fileHash"],
                shaHash=regscale_file["shaHash"],
                size=sys.getsizeof(file_data)
                if file_data
                else os.path.getsize(file_name),
            )
            # post the regscale_file data via RegScale API
            file_res = api.post(
                url=f"{api.config['domain']}/api/files",
                headers=file_headers,
                json=new_file.dict(),
            )
        else:
            return False
        # return whether the api call was successful or not
        # right now there is a bug in the main application where it returns a 204 error code
        # which means there is no content on the file, but the file does upload successfully and has data
        return regscale_file if return_object else file_res.status_code == 204
