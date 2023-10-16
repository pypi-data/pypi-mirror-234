import logging

from typing import Optional
from uuid import uuid4


logger = logging.getLogger(__name__)


def uuid() -> str:
    return str(uuid4())


def require(condition: bool, message: Optional[str] = None, exception: Optional[BaseException] = None):
    if not condition:
        exception = exception or RequirementError(message)
        raise exception


class RequirementError(Exception):
    pass


class IntSequence:
    _last_id = 0

    def create_new_id(self) -> int:
        self._last_id += 1
        return self._last_id
