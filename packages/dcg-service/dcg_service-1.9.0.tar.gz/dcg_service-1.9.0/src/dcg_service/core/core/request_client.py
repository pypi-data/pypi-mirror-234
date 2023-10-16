"""Repository."""
import requests
import json
import os
from flask import request

INTERNAL_SERVICE_KEY = os.environ['INTERNAL_SERVICE_KEY']


class AbstractRequestClient(object):
    """Custom Abstract Request."""

    HEADER_CONTENT_TYPE = "Content-Type"
    AUTHORIZATION = "Authorization"
    INTERNAL_KEY = 'Internal-Service-Key'
    _default_timeout = (1, 8)
    _max_retries = 5

    def __init__(self, session=None, request_token=None):
        self.request_token = request_token
        self.response = None
        if session is None:
            self.session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(
                max_retries=self._max_retries
            )
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
        else:
            self.session = session

    def __make_request(self, method, *args, **kwargs):
        response = self.session.request(method, *args, **kwargs)
        return response

    def request(self, type, endpoint, data=None, headers=None, params=None):
        """Request."""
        if type.lower() == "post":
            return self.post(endpoint, data, headers, params)
        if type.lower() == "patch":
            return self.patch(endpoint, data, headers, params)

        return self.get(endpoint, data, headers, params)

    def format_headers(self, headers):
        """format headers."""
        if headers:
            return {**self.default_headers, **headers}
        return self.default_headers

    @property
    def auth_token(self):
        """To get auth token."""
        token = self.request_token or request.headers.get('Authorization')
        return token

    @property
    def default_headers(self):
        """default_headers."""
        return {'Accept': 'application/json', self.HEADER_CONTENT_TYPE: "application/json",
                self.AUTHORIZATION: self.auth_token, self.INTERNAL_KEY: INTERNAL_SERVICE_KEY}

    def post(self, endpoint, data=None, headers=None, params=None):
        """Post."""
        headers = self.format_headers(headers)
        response = self.__make_request('POST', endpoint, headers=headers, json=data)
        return self.process_response(response)

    def patch(self, endpoint, data=None, headers=None, params=None):
        """Patch."""
        headers = self.format_headers(headers)
        response = requests.patch(url=endpoint, headers=headers, data=json.dumps(data), params=params)
        return self.process_response(response)

    def get(self, endpoint, data=None, headers=None, params=None):
        """Get."""
        headers = self.format_headers(headers)
        response = self.__make_request('GET', endpoint, headers=headers, data=json.dumps(data), params=params)
        return self.process_response(response)

    def process_response(self, response):
        """Process response."""
        self.response = response
        if response.status_code:
            json_res = response.json()
            return json_res.get('data')
