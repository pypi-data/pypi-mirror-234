import json
import traceback
from datetime import datetime
from flask import request


class UserObject:
    """
    Custom user class
    Helps to convert dict to class object instance.
    """

    is_authenticated = False
    is_staff = False
    is_superuser = False
    is_agent = False
    permissions = list()

    def __init__(self, dict1):
        self.__dict__.update(dict1)


def get_user_obj(data):
    """
    using 'json.loads' method and passing 'json.dumps'
    method and custom object hook as arguments
    """
    if not isinstance(data, dict):
        raise TypeError("get_user_obj 'data' argument must be a dict.")
    return json.loads(json.dumps(data), object_hook=UserObject)


def save_error_es_db(error=None):
    """
    Save error logs to Elasticsearch.

    This function is responsible for logging error information to an Elasticsearch index named 'error_logs'. It accepts
    an optional 'error' parameter that allows passing an error message or traceback. If the 'error' parameter is not
    provided, the function will automatically capture the traceback using the 'traceback.format_exc()' method.

    Parameters:
        error (str or Exception, optional): An optional parameter that represents the error message or an Exception
                                            object. If provided, this error message will be logged. If not provided,
                                            the function will capture the traceback using 'traceback.format_exc()'
                                            and log it as the error message.

    Note:
        - The function requires Elasticsearch configurations to be set up appropriately and the `EsClient` instance
          to be imported from the module (specified by the '.' in the import statement).
        - The function uses the `datetime.now()` method to record the current timestamp for the log entry.
        - The 'request' and 'APP_NAME' variables are assumed to be globally available or imported from the appropriate
          context for the log entry.

    Returns:
        bool: Returns True if the error log is successfully saved to Elasticsearch; otherwise, returns False.

    Example Usage:
        # Example 1: Save a custom error message
        save_error_es_db("An error occurred during data processing.")

        # Example 2: Capture and log an exception traceback
        try:
            # Code that may raise an exception
            result = 1 / 0
        except Exception as e:
            save_error_es_db(e)
    """
    try:
        from . import EsClient, APP_NAME
        error_string = error
        if not error:
            error_string = traceback.format_exc()
        headers = getattr(request, 'headers', {})
        request_id = headers.get("Request-Id")
        request_user = getattr(request, 'user', None)
        body = {
            "Path": getattr(request, 'full_path', None) or getattr(request, 'path', None),
            "Method": getattr(request, 'method', None),
            "Entity": APP_NAME,
            "Data": str(error_string),
            "StatusCode": 500,
            "Timestamp": datetime.now(),
            "RequestID": request_id,
            "UserID": getattr(request_user, 'id', None),
            "UserType": getattr(request_user, 'user_type', None),
            "UserName": getattr(request_user, 'first_name', None),
            "ApplicationID": getattr(request_user, 'application_id', None),
            "CompanyID": getattr(request_user, 'company_id', None),
        }
        EsClient.index(index='error_logs', body=body)
        return True
    except Exception as error:
        print("Saving LOG Error >>", error)


def save_logs_es_db(**kwargs):
    """
    Save logs to Elasticsearch.

    This function logs relevant information about an API request or operation to an Elasticsearch index. It receives
    keyword arguments (**kwargs) containing various pieces of information, such as request details, response data,
    user-related information, and custom activities.

    Parameters:
        **kwargs: Keyword arguments containing information about the API request and additional data. The supported
                  keyword arguments are as follows:

            - headers (dict): The HTTP headers of the API request.
            - body (dict): The request body data of the API request.
            - status_code (int): The HTTP status code of the API response.
            - request_company_id (int): The ID of the company/organization associated with the API request.
            - response (dict): The response data of the API request.
            - user_id (int): The ID of the user associated with the API request.
            - user_type (str): The type of user (e.g., "admin", "regular user") associated with the API request.
            - first_name (str): The first name of the user associated with the API request.
            - application_id (int): The ID of the application associated with the API request.
            - company_id (int): The ID of the company associated with the API request.
            - login_id (int): The login ID of the user associated with the API request.
            - activities (list): A list of custom activities or events associated with the API request.
            - action (str): A specific action or event description associated with the API request.

    Note:
        - The function requires Elasticsearch configurations to be set up appropriately and the `EsClient` instance
          to be imported from the module (specified by the '.' in the import statement).
        - The function uses the `datetime.now()` method to record the current timestamp for the log entry.

    :param kwargs:
    :return:
    """
    try:
        from . import EsClient, ACTIVITY_INDEX, APP_NAME
        options = kwargs
        request_user = getattr(request, 'user', None)

        request_company_id = None
        if options.get('body') and ('company_id' in options['body'] or 'organisation_id' in options['body']):
            request_company_id = options['body'].get('company_id') or options['body'].get('organisation_id')

        if options.get('response') and type(options.get('response')) == dict:
            options['response']['action'] = options.get('action')
        else:
            options['response'] = {
                'action': options.get('action')
            }

        body = {
            "LogType": "API",
            "Method": getattr(request, 'method', None),
            "Path": getattr(request, 'full_path', None) or getattr(request, 'path', None),
            "URL": getattr(request, 'url', None),
            "RequestID": None,
            "RequestBody": json.dumps(options.get('body', {}) or {}),
            "Headers": dict(getattr(request, 'headers', options.get('headers', {}))),
            "StatusCode": options.get('status_code') or 200,
            "RequestCompanyID": request_company_id or options.get('request_company_id'),
            "Response": json.dumps(options.get('response', {}) or {}),
            "UserID": getattr(request_user, 'id', options.get('user_id')),
            "UserType": getattr(request_user, 'user_type', options.get('user_type')),
            "UserName": getattr(request_user, 'first_name', options.get('user_name')),
            "ApplicationID": getattr(request_user, 'application_id', options.get('application_id')),
            "CompanyID": getattr(request_user, 'company_id', options.get('company_id')),
            "Service": APP_NAME,
            "LoginID":  getattr(request_user, 'login_id', options.get('login_id')),
            "Timestamp": datetime.now(),
            "Activities": options.get('activities') or [],
            "Action": options.get('action')
        }

        EsClient.index(index=ACTIVITY_INDEX, body=body)
        EsClient.indices.refresh(index=ACTIVITY_INDEX)
    except Exception as error:
        print("ES LOG Error >>", error)
