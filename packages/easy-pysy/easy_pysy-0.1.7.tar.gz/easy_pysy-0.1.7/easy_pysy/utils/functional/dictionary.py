from typing import Callable
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')


class Dict(Generic[K, V], dict[K, V]):
    def keep(self, predicate: Callable[[K, V], bool]) -> "Dict[K, V]":
        return Dict({k: v for k, v in self.items() if predicate(k, v)})

    def omit(self, predicate: Callable[[K, V], bool]) -> "Dict[K, V]":
        return Dict({k: v for k, v in self.items() if not predicate(k, v)})
