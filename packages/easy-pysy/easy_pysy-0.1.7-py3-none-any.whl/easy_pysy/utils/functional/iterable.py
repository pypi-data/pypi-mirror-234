from typing import Callable, Optional, Iterable
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')
U = TypeVar('U')


class List(Generic[T], list[T]):
    def map(self, func: Callable[[T], U]) -> "List[U]":
        return List([func(v) for v in self])

    def flat_map(self, func: Callable[[T], Iterable[U]]) -> "List[U]":
        return List([e for v in self for e in func(v)])

    def filter(self, predicate: Callable[[T], bool]) -> "List[T]":
        return List([v for v in self if predicate(v)])

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        for v in self:
            if predicate(v):
                return v
        return None
