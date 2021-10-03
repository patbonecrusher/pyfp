from __future__ import annotations
from pyramda import map as map
from typing import Any
from typing import Callable

lfn = Callable[[Any], Any]

class Box():
    """docstring for Box."""
    def __init__(self, x: Any):
        super(Box, self).__init__()
        self.x = x

    def map(self, fn: lfn) -> Box:
        return Box(fn(self.x))

    def fold(self, fn: lfn) -> Any:
        return fn(self.x)

    def __str__(self):
        return f"Box({self.x})"

def nextCharForNumberString(x: str) -> str:
    return Box(x) \
            .map(lambda s: s.strip()) \
            .map(lambda r: int(r)) \
            .map(lambda i: i+1) \
            .map(lambda i: chr(i)) \
            .fold(lambda c: c.lower())

print(nextCharForNumberString('  64 '))