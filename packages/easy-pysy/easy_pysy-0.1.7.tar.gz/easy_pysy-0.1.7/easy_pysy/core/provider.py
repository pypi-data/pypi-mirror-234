from dataclasses import dataclass
from typing import TypeVar, Type, Callable, Generic, Any

import easy_pysy.utils.decorators
from easy_pysy.core import logging

T = TypeVar('T')
ProviderFactory = Callable[[], T]


@dataclass
class Provider(Generic[T]):
    type: Type[T]
    factory: ProviderFactory
    singleton: bool


providers: dict[Type, list[Provider]] = {}
singletons: dict[Type, Any] = {}


def provide(type: Type[T], singleton: bool = False):
    # TODO: env and variant
    def decorator(func):
        new_provider = Provider(type, func, singleton)
        if type not in providers:
            providers[type] = [new_provider]
        else:
            providers[type].append(new_provider)
            logging.warning(f'Multiple providers defined for {type}: {providers[type]}')

        return func
    return decorator


def get(type: Type[T]) -> T:  # TODO: other name
    easy_pysy.utils.decorators.require(type in providers and providers[type], f"No provider found for {type}")
    provider = providers[type][-1]

    if not provider.singleton:
        return provider.factory()
    elif type not in singletons:
        instance = provider.factory()
        singletons[type] = instance
        return instance
    else:
        return singletons[type]
