from functools import partial
from typing import Callable, TypeVar, Any


T = TypeVar('T')


def bind(something: T, function: Callable[[T, ], Any]):
    self_function = partial(function, something)
    setattr(something, function.__name__, self_function)


def bind_all(something: T, functions: list[Callable[[T, ], Any]]):
    for function in functions:
        bind(something, function)
