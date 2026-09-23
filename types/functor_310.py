# from https://stackoverflow.com/questions/54004428/how-can-i-write-a-function-fmap-that-returns-the-same-type-of-iterable-that-was


import abc
from typing import Generic, TypeVar, Callable, Any, Dict
import pandas as pd 


A = TypeVar('A')
B = TypeVar('B')


class Functor(Generic[A], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fmap(self, f: Callable[[A], B]) -> 'Functor[B]':
        raise NotImplemented

FMappable = list | tuple | set | dict | str | Functor[Any]

def fmap(f: Callable[..., Any], fmappable: FMappable) -> FMappable:
    match fmappable:
        case Functor():
            return fmappable.fmap(f)
        case list() | set() | tuple() | str():
            return type(fmappable)(map(f, fmappable))
        case dict():
            return {key: f(value) for key, value in fmappable.items()}
        case _:
            raise TypeError('argument fmappable is not an instance of FMappable')

F = TypeVar('F', bound=Callable[[Any], Any])

class FSeries(pd.Series, Functor[A]):
    def fmap(self, f: Callable[[A], A]) -> 'FSeries[A]':
        """
        f: Function callback that take a pandas Series and return a panda Series
        """
        return FSeries(self.apply(f))


print(fmap(lambda x: x * 2, [1, 2, 3]) )
print(fmap(lambda x: x * 2, {'one': 1, 'two': 2, 'three': 3}))
print(fmap(lambda x: float(x*3), FSeries([1, 2, 3], index=['one', 'two', 'three'])))

K = TypeVar('K')
V = TypeVar('V')

class FDict(Dict[K,V], Functor[K]):
    def fmap(self, f: Callable[[K], K]) -> 'FDict[K,V]':
        return FDict({f(key): value for key, value in self.items()})

print(fmap(lambda x: x * 2, FDict({'one': 1, 'two': 2, 'three': 3})) )

d = {'one': 1, 'two': 2, 'three': 3}
print(d)

add: Callable[[int], int] = lambda x: x*2
dd = {key: add(value) for key, value in d.items()}
print(dd)