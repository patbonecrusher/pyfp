# Either = Right || Left

from __future__ import annotations
from pyramda import map as map
from typing import Any
from typing import Callable
from typing import NewType, Union
from typing import TypeVar, Generic
import json

lfn = Callable[[Any], Any]
lfe = Callable[[], Any]

class Right():
    """docstring for Box."""
    def __init__(self, x: Any):
        super(Right, self).__init__()
        self.x = x

    def map(self, fn: lfn) -> Right:
        return Right(fn(self.x))

    def chain(self, fn: lfn) -> Right:
        return fn(self.x)

    def fold(self, f: lfn, g: lfn) -> Any:
        return g(self.x)

    def __str__(self):
        return f"Right({self.x})"

class Left():
    """docstring for Box."""
    def __init__(self, x: Any):
        super(Left, self).__init__()
        self.x = x

    def map(self, fn: lfn) -> Left:
        return Left(self.x)

    def chain(self, fn: lfn) -> Left:
        return Left(self.x)

    def fold(self, f: lfn, g: lfn) -> Any:
        return f(self.x)

    def __str__(self):
        return f"Left({self.x})"


result = Right(2).map(lambda x: x+1) \
    .map(lambda x: x/2) \
    .fold(lambda x: 'error', lambda x: x)
print(result)


#  This allows us to do some pure functional error handling, code branching, null checks, and all sorts of concepts that capture disjunction, or the concept of or. That's why we call this either, it's either/or. We can use that all throughout our code.
#region findColor
def findColor(name: str) -> str:
    return ({'red': "#ff4444", 'blue': "#4444ff", 'green': "#44ff44"})[name]

Either = Union[Right, Left]

def fromNone(x: Any): 
    return Left(x) if x is None else Right(x)

def findColorFP(name: str) -> Either:
    return fromNone(({'red': "#ff4444", 'blue': "#4444ff", 'green': "#44ff44"}).get(name, None))

blue = findColorFP('blue') \
    .map(lambda x: x.lstrip("#"))\
    .fold(lambda x: 'no color', lambda x: x.upper())

print(blue)


purple = findColorFP('purple') \
    .map(lambda x: x.lstrip("#"))\
    .fold(lambda x: 'no color', lambda x: x.upper())

print(purple)
#endregion

def tryCatch(f: lfe) -> Either:
    try:
        return Right(f())
    except Exception as e:
        return Left(e)

#region config
def getPort(config_file: str) -> int:
    try:
        config = json.load(open(config_file))
        return config.get("port", 30030)
    except FileNotFoundError:
        return 3

def getPortFP(config_file: str) -> int:
    return tryCatch(lambda: open(config_file)) \
        .chain(lambda c: tryCatch(lambda: json.load(c))) \
        .fold(lambda e: (200, e), lambda cfg: cfg.get("port", 2000))

print(getPortFP('./config.json'))

#endregion

