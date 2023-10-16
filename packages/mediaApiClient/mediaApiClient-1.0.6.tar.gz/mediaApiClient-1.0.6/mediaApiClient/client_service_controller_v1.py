from typing import List

import requests

from mediaApiClient.services_models import LightWeightService


class ClientServiceControllerV1:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_services(self):
        url = f"{self.base_url}/api/v1/services"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            services_data = response.json()
            return [LightWeightService(**service) for service in services_data]
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

