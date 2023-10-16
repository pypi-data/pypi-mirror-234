"""Repository."""
import requests
import json
import os
from flask import request

INTERNAL_SERVICE_KEY = os.environ.get('INTERNAL_SERVICE_KEY', '')


class AbstractRequestClient(object):
    """Custom Abstract Request."""

    HEADER_CONTENT_TYPE = "Content-Type"
    AUTHORIZATION = "Authorization"
    INTERNAL_KEY = 'Internal-Service-Key'
    APPLICATION_ID_KEY = 'Application-Id'
    COMPANY_ID_KEY = 'Company-Id'
    APP_NAME_KEY = 'Application-Name'

    _default_timeout = (1, 8)
    _max_retries = 5

    def __init__(self, session=None, request_token=None, **kwargs):
        """
        Override if you need.
        :param session: request session
        :param request_token: request_token
        :param kwargs: application_id, company_id, application_name
        """
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

        self.application_id = kwargs.get('application_id') or "0"
        self.company_id = kwargs.get('company_id') or "0"
        self.application_name = kwargs.get('application_name') or ""

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
        try:
            auth_token = request.headers.get('Authorization')
            token = self.request_token or auth_token
        except Exception:
            token = self.request_token
        return token

    @property
    def default_headers(self):
        """default_headers."""
        return {
            'Accept': 'application/json', self.HEADER_CONTENT_TYPE: "application/json",
            self.AUTHORIZATION: self.auth_token, self.INTERNAL_KEY: INTERNAL_SERVICE_KEY,
            self.APPLICATION_ID_KEY: str(self.application_id), self.COMPANY_ID_KEY: str(self.company_id),
            self.APP_NAME_KEY: self.application_name
        }

    def post(self, endpoint, data=None, headers=None, params=None):
        """Post."""
        headers = self.format_headers(headers)
        response = self.__make_request('POST', endpoint, headers=headers, json=data, params=params)
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
