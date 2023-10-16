import logging
import time
from functools import wraps
from typing import Type

from easy_pysy.utils.common import require


logger = logging.getLogger(__name__)


def retry(times: int, exception_class: Type = BaseException, sleep=0):
    require(times >= 1, "times should be >= in @retry")

    def decorated(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            last_exception = None
            while attempt <= times:
                try:
                    return func(*args, **kwargs)
                except exception_class as exc:
                    logger.exception(f'Execution of {func} failed (attempt: {attempt}/{times})')
                    attempt += 1
                    last_exception = exc
                    if attempt <= times:
                        logger.debug(f'Will retry in {sleep} seconds')
                        time.sleep(sleep)
                    else:
                        raise exc
            raise last_exception
        return wrapper
    return decorated
