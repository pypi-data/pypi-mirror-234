from typing import Any


def qual_name(obj: Any):
    object_type = type(obj)
    module = object_type.__module__
    if module == 'builtins':
        return object_type.__qualname__
    return module + '.' + object_type.__qualname__
