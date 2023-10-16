import os
import pandas as pd
import requests
import json
from typing import List, IO, Union
from salure_helpers.salureconnect import SalureConnect


class SalureConnectFiles(SalureConnect):
    def __init__(self):
        super().__init__()

    def list_files(self) -> json:
        """
        This method is to list the available files from the SalureConnect API
        :return json with credentials
        """
        response = requests.get(url=f"{self.url}file-storage/files", headers=self._get_sc_headers())
        response.raise_for_status()

        return response.json()

    def download_files(self, output_path: os.PathLike, filter_upload_definition_ids: List = None, filter_file_names: List = None, filter_deleted=False):
        """
        This method can be used to download multiple files from salureconnect at once.
        :param output_path: folder in which to save the downloaded files
        :param filter_upload_definition_ids: filter files on specific file definitions
        :param filter_file_names: filter files on specific filenames
        :param filter_deleted: filter boolean if you want to retrieve deleted files as well
        """
        response = requests.get(url=f"{self.url}file-storage/files", headers=self._get_sc_headers())
        response.raise_for_status()
        files = response.json()
        for file_object in files:
            # Only get file(s) that are in filter
            if (filter_upload_definition_ids is None or file_object['fileuploadDefinition']['id'] in filter_upload_definition_ids) and \
                    (filter_file_names is None or file_object['file_name'] in filter_file_names) and pd.isnull(file_object['deleted_at']) is not filter_deleted:
                file_string = requests.get(url=f"{self.url}file-storage/files/{file_object['id']}/download", headers=self._get_sc_headers())
                with open(f"{output_path}{file_object['file_name']}", mode='wb') as file:
                    file.write(file_string.content)

    def download_file(self, file_id: int, file_name_and_path: str):
        """
        This method downloads a specific file to the specified path. The file is identified bij the file_id parameter.
        :param file_id: file id that the file is identified by in SalureConnect
        :param file_name_and_path: file name
        """
        response = requests.get(url=f"{self.url}file-storage/files/{file_id}/download", headers=self._get_sc_headers())
        response.raise_for_status()
        with open(file_name_and_path, mode='wb') as file:
            file.write(response.content)

    def upload_file(self, file_name: str, file_object: IO, definition_id: int = None) -> requests.Response:
        """
        This method uploads a file to SalureConnect
        :param file_name: filename including extension
        :param file_object: fileobject as bytes (open with mode=rb)
        :param definition_id: optional definition ID for categorization in SalureConnect
        :return:
        """

        payload = {'filename': file_name}
        if definition_id is not None:
            payload['definition_id'] = definition_id

        files = [
            ('file', (file_name, file_object, 'application/octet-stream'))
        ]
        response = requests.post(url=f"{self.url}file-storage/files/upload", headers=self._get_sc_headers(), data=payload, files=files)
        response.raise_for_status()

        return response

