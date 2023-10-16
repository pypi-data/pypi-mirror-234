from typing import List

import requests

from mediaApiClient.compilation_models import LightWeightCompilation, PageCompilationWithContents, \
    CompilationRequest


class ClientCompilationControllerV2:
    COMPILATION_URL = "/api/v2/compilations"

    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_all_compilations(self):
        url = f"{self.base_url}{self.COMPILATION_URL}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            compilation_data = response.json()
            return [LightWeightCompilation(**compilation) for compilation in compilation_data]
        else:
            raise Exception(f"Request failed with status code: {response.status_code}")

    def get_full_compilation_by_id(self, compilation_id, number=0, size=10):
        url = f"{self.base_url}{self.COMPILATION_URL}/{compilation_id}"
        params = {
            "number": number,
            "size": size
        }

        headers = {
            "Authorization-Client": self.auth_token
        }

        content_response = requests.get(url, params=params, headers=headers)
        if content_response.status_code == 200:
            return PageCompilationWithContents(**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")

    def update_compilation_by_id(self, compilation_id, update_compilation_request: CompilationRequest):
        url = f"{self.base_url}{self.COMPILATION_URL}/{compilation_id}"

        json = update_compilation_request.model_dump_json()

        headers = {
            "Authorization-Client": self.auth_token,
            "Content-Type": "application/json"
        }

        content_response = requests.put(url, headers=headers, data=json)
        if content_response.status_code == 200:
            return LightWeightCompilation(**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")

    def delete_compilation_by_id(self, compilation_id):
        url = f"{self.base_url}{self.COMPILATION_URL}/{compilation_id}"

        headers = {
            "Authorization-Client": self.auth_token
        }

        content_response = requests.delete(url, headers=headers)
        if content_response.status_code != 200:
            raise Exception(f"Request failed with status code: {content_response.status_code}")

    def create_compilation(self, create_compilation_request: CompilationRequest):
        url = f"{self.base_url}{self.COMPILATION_URL}"

        json = create_compilation_request.model_dump_json()

        headers = {
            "Authorization-Client": self.auth_token,
            "Content-Type": "application/json"
        }

        content_response = requests.post(url, headers=headers, data=json)
        if content_response.status_code == 200:
            return LightWeightCompilation(**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")
