import json
from flask import request

from .constants import STATUS_CODE_MESSAGE
from .exceptions import logger


class CustomResponse(object):
    def __init__(self, response):
        self.response = response

    @classmethod
    def error_formatter(cls, message, status_code):
        sub_errors = list()
        error_dict = dict()
        if isinstance(message, dict):
            for key, value in message.items():
                sub_errors.append(
                    {
                        'field': key,
                        'message': value[0] if type(value) == list and len(value) > 0 else value
                    }
                )
            error_dict['message'] = sub_errors[0].get('message')
            error_dict['code'] = status_code
            error_dict['sub_errors'] = sub_errors
        else:
            error_dict['message'] = message
            error_dict['code'] = status_code

        return error_dict

    @property
    def render(self):
        message = None
        data = dict()
        error = dict()
        status_code = self.response.status_code
        response_data = json.loads(self.response.data)

        if type(response_data) == dict:
            message = response_data.pop('message', None)
            data = response_data.pop('data', None) if response_data.get('data') else response_data

        if 400 <= status_code <= 499:
            message = response_data.copy() if not message else message
            response_data.clear()
            error = self.error_formatter(
                message=message, status_code=status_code)
            message = error.get('message') or STATUS_CODE_MESSAGE.get(status_code)
        else:
            message = message or STATUS_CODE_MESSAGE.get(status_code)

        response_json = {
            "code": status_code,
            "message": message
        }
        if 200 <= status_code <= 300:
            response_json['data'] = data
        else:
            response_json['error'] = error

        if type(response_data) == dict:
            response_json.update(response_data)

        self.response.data = json.dumps(response_json)
        self.log(response_json)
        return self.response

    def log(self, data):
        if self.response.status_code == 400:
            log = '[{} {} {}]--{}'.format(
                self.response.status_code, request.method,
                request.full_path, data.get('message'))
            logger.error(log)
