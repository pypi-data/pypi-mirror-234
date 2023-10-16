from datetime import date
from typing import Union

import requests

from mediaApiClient.content_meta_models import ContentMeta, PageWithElements, FilmFullMeta, SerialFullMeta
from mediaApiClient.content_reuest_models import ContentFilter


class ClientContentControllerV2:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token

    def get_content_by_id(self, content_id):
        url = f"{self.base_url}/api/v2/contents/{content_id}"
        params = {
            "contentId": content_id
        }

        headers = {
            "Authorization-Client": self.auth_token
        }

        content_response = requests.get(url, params=params, headers=headers)

        if content_response.status_code == 200:
            content_instance = None
            content_response_json = content_response.json()
            if content_response_json['type'] == 'serial':
                content_instance = SerialFullMeta(**content_response_json)
            elif content_response_json['type'] == 'film':
                content_instance = FilmFullMeta(**content_response_json)
            return content_instance
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")

    def get_content_by_filter(self, filter_request: ContentFilter, number=0, size=10):
        payload = filter_request.model_dump_json()
        url = f"{self.base_url}/api/v2/contents"

        params = {
            "number": number,
            "size": size
        }

        headers = {
            "Authorization-Client": self.auth_token,
            "Content-Type": "application/json"
        }

        content_response = requests.post(url, data=payload, headers=headers, params=params)

        if content_response.status_code == 200:
            return PageWithElements[Union[SerialFullMeta, FilmFullMeta]](**content_response.json())
        else:
            raise Exception(f"Request failed with status code: {content_response.status_code}")
