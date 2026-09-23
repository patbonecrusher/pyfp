from __future__ import annotations
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


def moneyToFloat(m: str) -> Box:
    return Box(m) \
        .map(lambda s: s.replace('$', '', 1)) \
        .map(lambda s: float(s))

def percentToFloat(m: str) -> Box:
    return Box(m.replace('%', '')) \
        .map(lambda s: float(s)) \
        .map(lambda number: number*0.01)

def applyDiscount(price: str, discount: str) -> float:
    return moneyToFloat(price) \
        .fold(lambda cost: percentToFloat(discount) \
            .fold(lambda saving: cost - cost * saving))


print(moneyToFloat('$1.23'))
print(percentToFloat('72%'))
print(applyDiscount('$1.24', '10%'))
