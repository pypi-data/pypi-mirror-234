import os
import requests
import json
from typing import Union


class SalureConnect:
    def __init__(self, customer: str = None, api_token: str = None, staging: str = 'prod'):
        if customer is not None and api_token is not None:
            self.customer = customer
            self.api_token = api_token
            self.environment = staging
        elif os.getenv("SALURECONNECT_CUSTOMER_NAME") is not None and os.getenv("SALURECONNECT_API_TOKEN") is not None and os.getenv("SALURECONNECT_ENVIRONMENT") is not None:
            self.customer = os.getenv("SALURECONNECT_CUSTOMER_NAME")
            self.api_token = os.getenv("SALURECONNECT_API_TOKEN")
            self.environment = os.getenv("SALURECONNECT_ENVIRONMENT")
        else:
            raise ValueError("Set the environment variables SALURECONNECT_CUSTOMER_NAME, SALURECONNECT_ENVIRONMENT and SALURECONNECT_API_TOKEN or provide the customer and api_token parameters")
        possible_environments = ['dev', 'prod']
        if self.environment not in possible_environments:
            raise ValueError(f"Environment should be in {','.join(possible_environments)}")
        self.url = 'https://salureconnect-staging.com/api/v1/' if self.environment == 'dev' else 'https://salureconnect.com/api/v1/'

    def _get_sc_headers(self):
        return {
            'Authorization': f'SalureToken {self.api_token}',
            'salure-customer': self.customer
        }

    def get_system_credential(self, system: str, label: Union[str, list], test_environment: bool = False) -> json:
        """
        This method retrieves authentication credentials from salureconnect.
        It returns the json data if the request does not return an error code
        :param system: specifies which token is used. (lowercase)
        :param label: reference to the used label
        :param test_environment: boolean if the test environment is used
        :return json response from salureconnect
        """
        response = requests.get(url=f'{self.url}connector/{system}', headers=self._get_sc_headers())
        response.raise_for_status()
        credentials = response.json()
        # rename parameter for readability
        if isinstance(label, str):
            labels = [label]
        else:
            labels = label
        # filter credentials based on label. All labels specified in label parameter should be present in the credential object
        credentials = [credential for credential in credentials if all(label in credential['labels'] for label in labels)]
        if system == 'profit':
            credentials = [credential for credential in credentials if credential['isTestEnvironment'] is test_environment]

        if len(credentials) == 0:
            raise ValueError(f'No credentials found for {system}')
        if len(credentials) != 1:
            raise ValueError(f'Multiple credentials found for {system} with the specified labels')

        return credentials[0]

    def refresh_system_credential(self, system: str, system_id: int) -> json:
        """
        This method refreshes Oauth authentication credentials in salureconnect.
        It returns the json data if the request does not return an error code
        :param system: specifies which token is used. (lowercase)
        :param system_id: system id in salureconnect
        :return json response from salureconnect
        """
        response = requests.post(url=f'{self.url}connector/{system}/{system_id}/refresh', headers=self._get_sc_headers())
        response.raise_for_status()
        credentials = response.json()

        return credentials

    def get_mappings(self, task_id: int) -> dict:
        """
        Get the mappings from the task in salureconnect
        :param task_id: The id of the task in salureconnect. this does not have to be the task id of the current task
        :return: A dictionary with the following structure: {mapping_title: {tuple(input): output}}
        """
        response = requests.get(url=f'{self.url}connectors/{task_id}/data-mapping', headers=self._get_sc_headers())

        data = response.json()

        # transform the data to a dictionary where the key is the title of the mapping and the value is the mapping as a dict
        mappings = {
            item['title']: {tuple(mapping['input']) if len(mapping['input']) > 1 else mapping['input'][0]: mapping['output'] for mapping in item['mapping']} for item in data
        }

        return mappings
