import signal
from typing import Callable, Optional

from easy_pysy.utils.common import require
from easy_pysy.core import logging

exiting = False
_sigint_callback: Optional[Callable[[int], None]] = None


def sigint_callback(func):
    global _sigint_callback
    require(_sigint_callback is None, "There's already a sigint callback")
    _sigint_callback = func
    return func


def set_sigint_callback(callback: Callable[[int], None]):
    global _sigint_callback
    _sigint_callback = callback


def _sigint_handler(signum, frame):
    logging.info(f'Received sigint: {signum}')

    global exiting
    if exiting:
        logging.warning('Double sigint received, forcing exit')
        exit(1)

    exiting = True
    if _sigint_callback is not None:
        _sigint_callback(signum)


signal.signal(signal.SIGINT, _sigint_handler)
