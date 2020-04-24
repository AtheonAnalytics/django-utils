import json
import logging
import requests

from django.conf import settings
from requests.exceptions import ReadTimeout, SSLError, ConnectionError
from typing import Tuple, Dict, Any


def check_response(code: int) -> bool:
    """
    Check response code
    
    :param code:  response status code
    :return:
        - ``True`` if success
        - ``False`` if failure
    """
    logging_level = resolve_logging_level(code)
    if logging_level in ['info']:
        return True
    elif logging_level in ['warning', 'error']:
        return False


def resolve_logging_level(code: int) -> str:
    """
    Resolve request status code to logging level

    :param code: response status_code
    :return:
        - corresponding logging level
    """
    if (100 <= code <= 199) or (200 <= code <= 299) or (300 <= code <= 399):
        return 'info'
    elif 400 <= code <= 499:
        return 'warning'
    elif 500 <= code <= 599:
        return 'error'


def connection_handler(function):
    """ Handle requests error if connection fail. """

    def _wrapped_view(*args, **kwargs):

        response = None

        try:
            response = function(*args, **kwargs)
            status_code = response.status_code
            response_text = response.text
        except ReadTimeout as e:
            status_code, response_text = 408, e
        except SSLError as e:
            status_code, response_text = 503, e
        except ConnectionError as e:
            status_code, response_text = 510, e

        try:
            response_json = response.json()
        except (ValueError, AttributeError):
            response_json = {}

        try:
            json_data = json.loads(kwargs['json_data'])
        except KeyError:
            json_data = {}

        try:
            data = kwargs['data']
        except KeyError:
            data = {}

        payload = json_data or data

        try:
            url = response.url
        except (NameError, AttributeError):
            url = kwargs['url']

        level = resolve_logging_level(status_code)

        extra = {
            'response_type': 'outbound',
            'response_code': status_code,
            'response_text': response_json or response_text,
            'http_method': function.__name__,
            'url': url,
            'payload': payload,
        }
        logger = logging.getLogger(__name__)
        getattr(logger, level)('API Logger', extra=extra)

        return status_code, response_json, response_text

    return _wrapped_view


class RequestsLogger(object):
    """ Helper for api connections """

    def __init__(self, username: str = None, password: str = None, timeout: int = 60,
                 verify: bool = True, token: str = None) -> None:
        """
        :param username: auth username
        :param password: auth password
        :param timeout: request timeout
        :param verify: ssl verification
        """
        if (username is None) ^ (password is None):
            raise ValueError('Please supply both username and password or neither')

        self.auth_kwargs = {}

        if username is not None:
            self.auth_kwargs['auth'] = (username, password)

        if token is not None:
            self.auth_kwargs['headers'] = {'Authorization': token}

        self.verify = verify
        self.timeout = 1 if settings.TESTING else timeout


def add_http_method(cls, i):
    """ Dynamically add http method """

    def http_method(self, **kwargs):
        headers = kwargs.pop('headers', {})
        auth_headers = self.auth_kwargs.pop('headers', {})
        headers.update(auth_headers)
        kwargs['headers'] = headers

        kwargs.update(self.auth_kwargs)

        return connection_handler(getattr(requests, i))(
            timeout=self.timeout, verify=self.verify, **kwargs)
    http_method.__name__ = i
    setattr(cls, http_method.__name__, http_method)


for method in ['get', 'post', 'put', 'patch', 'delete']:
    add_http_method(RequestsLogger, method)
