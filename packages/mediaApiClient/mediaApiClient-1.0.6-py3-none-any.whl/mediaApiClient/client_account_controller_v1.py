from typing import List

import requests

from mediaApiClient.account_models import LightWeightAccount, AccountFullInfo, AccountToCreate


class ClientAccountControllerV1:
    ACCOUNT_URL = "/api/v1/accounts"

    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_all_accounts(self):
        url = f"{self.base_url}{self.ACCOUNT_URL}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            account_data = response.json()
            return [LightWeightAccount(**account) for account in account_data]
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def get_account_by_id(self, account_id):
        url = f"{self.base_url}{self.ACCOUNT_URL}/{account_id}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            account_data = response.json()
            return AccountFullInfo(**account_data)
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def create_account_by_request(self, account_to_create: AccountToCreate):
        payload = account_to_create.model_dump_json()
        url = f"{self.base_url}{self.ACCOUNT_URL}"

        headers = {
            "Authorization-Client": self.auth_token,
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 201:
            account_data = response.json()
            return AccountFullInfo(**account_data)
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def delete_account_by_id(self, account_id):
        url = f"{self.base_url}{self.ACCOUNT_URL}/{account_id}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.delete(url, headers=headers)

        if response.status_code != 204:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def add_service_for_account(self, account_id, service_id):
        url = f"{self.base_url}{self.ACCOUNT_URL}/{account_id}/services/{service_id}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.patch(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def disable_service_for_account(self, account_id, service_id):
        url = f"{self.base_url}{self.ACCOUNT_URL}/{account_id}/services/{service_id}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.delete(url, headers=headers)

        if response.status_code != 204:
            raise Exception(f"Request failed with status code: {response.status_code}")

