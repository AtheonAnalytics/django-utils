import os
import copy

from pythonjsonlogger.jsonlogger import JsonFormatter
from typing import Union


class CleanedJsonFormatter(JsonFormatter):

    LOGGING_KEYS = [
        'levelname',
        'name',
        'asctime',
        'module',
        'message',
    ]

    SENSITIVE_FIELDS = [
        "username",
        "password",
        "password1",
        "password2",
        "user_id"
    ]

    def __init__(self, *args, **kwargs):
        """
        Extended json formatter with "sensitive data cleaning" functionality.

        Args:
            sensitive_fields(list of str): Additional keys which are sensitive.

        """
        sensitive_fields = kwargs.pop('sensitive_fields', [])

        super(CleanedJsonFormatter, self).__init__(*args, **kwargs)

        self._required_fields = self.LOGGING_KEYS
        self.SENSITIVE_FIELDS += sensitive_fields

    def process_log_record(self, log_record: Union[dict, list]) -> Union[dict, list]:
        try:
            data = copy.deepcopy(log_record)
        except TypeError:
            return log_record

        if isinstance(data, dict):
            data = self._apply_env_logging_variables(data)
            for k in data.keys():
                if k in self.SENSITIVE_FIELDS:
                    data[k] = "****"
                else:
                    data[k] = self.process_log_record(data[k])
        elif isinstance(data, list):
            for i, v in enumerate(data):
                data[i] = self.process_log_record(v)
        return data

    def _apply_env_logging_variables(self, data: dict):
        """
        Apply environment variables to logging (with LOGGING_* prefix)
        :return:
        """
        for var in os.environ.keys():
            if var.startswith('LOGGING_'):
                data[var.replace('LOGGING_', '').lower()] = os.environ[var]
        return data
