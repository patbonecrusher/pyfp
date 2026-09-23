# from https://stackoverflow.com/questions/54004428/how-can-i-write-a-function-fmap-that-returns-the-same-type-of-iterable-that-was
from __future__ import annotations

import abc
from typing import Generic, TypeVar, Callable, Union
    #Dict, List, Tuple, Set, Text, Any


A = TypeVar('A')
B = TypeVar('B')


class Functor(Generic[A], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        raise NotImplemented

def square(number: Union[int, float]) -> Union[int, float]:
    return number ** 2

FMappable = list | tuple | set | dict | str | Functor

#FMappable = Union[List[Any], Tuple[Any], Tuple[Any], Set[Any], Dict[Any, Any], Text, Functor[Any]]


def fmap(f: Callable[[A], B], fmappable: FMappable) -> FMappable:
    print(type(fmappable))
    match fmappable:
        case Functor():
            return fmappable.fmap(f)
        case list() | set() | tuple() | str():
            return type(fmappable)(map(f, fmappable))
        case dict():
            return type(fmappable)(
                        (key, f(value)) for key, value in fmappable.items())
        case _:
            raise TypeError('argument fmappable is not an instance of FMappable')
    # if isinstance(fmappable, Functor):
    #     return fmappable.fmap(f)
    # if isinstance(fmappable, (List, Tuple, Set, Text)):
    #     return type(fmappable)(map(f, fmappable))
    # if isinstance(fmappable, Dict):
    #     return type(fmappable)(
    #         (key, f(value)) for key, value in fmappable.items()
    #     )
    # raise TypeError('argument fmappable is not an instance of FMappable')

print(fmap(lambda x: x * 2, [1, 2, 3]) )

print(fmap(lambda x: x * 2, {'one': 1, 'two': 2, 'three': 3}))

class FDict(dict, Functor):
    def fmap(self, f):
        return {f(key): value for key, value in self.items()}

print(fmap(lambda x: x * 2, FDict({'one': 1, 'two': 2, 'three': 3})) )