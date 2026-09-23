from __future__ import annotations

# The idea is semigroups come from abstract algebra and so we are encoding this in our code so we can keep the name the same and understand the laws and properties that come with this mathematical structure rather than just making something up on our own.

# Here we know because of the algebra, we can actually concat the inner part first and then the one, two, and we will get the same results. That property is called associativity. We could do the same with strings because that is also a semigroup.


from pyramda import map as map, reduce
from typing import Any, Dict, List
import itertools

# from typing import Callable
# from typing import NewType, Union
# from typing import TypeVar, Generic
# import json

# Empty function makes the semi-group monoids
class Sum():
    def __init__(self, x: Any):
        super(Sum, self).__init__()
        self.x = x

    def concat(self, o: Sum):
        return Sum(self.x + o.x)

    def __str__(self) -> str:
        return f"Sum({self.x})"

    @staticmethod
    def empty():
        return Sum(0)

print(Sum(1).concat(Sum(2)))
print(Sum.empty().concat(Sum(1).concat(Sum(2))))

def foldMap(list: List[Any], empty: Any) -> Any:
    return reduce(lambda acc,x: acc.concat(x), empty, list)


r = foldMap(map(Sum, [1,2,3,4]), Sum.empty())
print(r)

class All():
    def __init__(self, x: bool):
        super(All, self).__init__()
        self.x = x

    def concat(self, o: All):
        return All(self.x and o.x)

    def __str__(self) -> str:
        return f"All({self.x})"

    @staticmethod
    def empty():
        return All(True)

print(All(True).concat(All(True)))
print(All(True).concat(All(False)))
print(All(False).concat(All(True)))
print(All.empty().concat(All(False).concat(All(True))))

class Or():
    def __init__(self, x: bool):
        super(Or, self).__init__()
        self.x = x

    def concat(self, o: Or):
        return Or(self.x or o.x)

    def __str__(self) -> str:
        return f"Or({self.x})"

    @staticmethod
    def empty():
        return Or(True)

print(Or(True).concat(Or(True)))
print(Or(True).concat(Or(False)))
print(Or(False).concat(Or(True)))
print(Or(False).concat(Or(False)))


class First():
    def __init__(self, x: str):
        super(First, self).__init__()
        self.x = x

    def concat(self, _: First):
        return First(self.x)

    def __str__(self) -> str:
        return f"First({self.x})"

    # Can't be promoted to monoid because we have no way to define a neutral element
    # @staticmethod
    # def empty():
    #     return Or(True)

print(First("hi").concat(First("boo")))


class Array():
    def __init__(self, x: List[Any]):
        super(Array, self).__init__()
        self.x = x

    def concat(self, a: Array):
        return Array(list(itertools.chain(self.x, a.x)))

    def __str__(self) -> str:
        return f"First({self.x})"


class BDict():
    def __init__(self, x: Dict[Any, Any]):
        super(BDict, self).__init__()
        self.x = x

    def concat(self, d: BDict):
        newDict = {key: self.x[key].concat(d.x[key]) for key in self.x}
        return BDict(newDict)

    def __str__(self) -> str:
        rep = ""
        for key in self.x:
            rep = f"{rep}{key}={self.x[key]} - "

        return rep

acct1 = { "name": First("Nico"), "isPaid": All(True), "points": Sum(10), "friends": Array(["Franklin"])}
print(BDict(acct1))

acct2 = { "name": First("Nico"), "isPaid": All(False), "points": Sum(2), "friends": Array(["Gatsby"])}
print(BDict(acct2))

print(BDict(acct2).concat(BDict(acct1)))


# Remember, a semigroup is a type with a concat method. If this addition is our concatenation, we have a neutral element here that acts as an identity of sorts that gives us back our element we're trying to concat with. If we have a special element like the zero here under addition, we have what's called a monoid, that is a semigroup with a special element in there that acts like a neutral identity.

# What can we deduce from this? A semigroup, it does not have an element to return so it's not a safe operation, whereas with the monoids we could take as many as we possibly want, even none, and still return us back something. It's a perfectly safe operation here that we can reduce as many of them as we'd like.

# Monoids: Sum, Product, Any, All, Max, Min, Right