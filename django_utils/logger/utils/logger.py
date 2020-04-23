import time

from contextlib import contextmanager
from typing import Dict


class LoggingExpectationExecutor(object):
    """ Helper to run code, and check the expected result. """

    def __init__(self, expectation):
        self.expectation = expectation
        self.result = None
        self._ran = False

    def execute(self, result):
        self._ran = True
        self.result = result
        return self.result

    def is_expected_result(self):
        return self.result == self.expectation or not self._ran


@contextmanager
def log_with_time(logger, extra_context: Dict, message: str, expectation=None,
                  failure_message: str = ''):
    """
    Context manager to log time taken to run code.

    Args:
        logger: logger object to user.
        extra_context(dict): extra context to use in logging
        message(str):
        expectation: expected result
        failure_message(str): message if fail

        Examples:
            >>> with log_with_time(logger, {'a': 'b'}, 'Message', expectation=True) as l:
            >>>     status = l.execute((lambda : True)())

    """
    start_time = time.time()
    extra_context = extra_context.copy()

    try:
        executor = LoggingExpectationExecutor(expectation)
        yield executor

        end_time = time.time()
        time_taken = end_time - start_time

        if executor.is_expected_result():
            extra_context.update({'time_taken': time_taken, 'success': True})
            logger.info(message, extra=extra_context)
        else:
            extra_context.update(
                {'time_taken': time_taken, 'success': False, 'failure_message': failure_message})
            logger.warning(message, extra=extra_context)

    except Exception as e:
        end_time = time.time()
        time_taken = end_time - start_time
        extra_context.update({'time_taken': time_taken, 'success': False})
        logger.exception(message, extra=extra_context)
        raise e
