# Functor

"""
! https://typelevel.org/cats/typeclasses/functor.html
^ Functor is a type class that abstracts over type constructors that can be map‘ed over. 
^ Examples of such type constructors are List, Option, and Future.
"""


# Some references: https://notes.asaleh.net/posts/functor-pattern-in-python/

# Functor
#^ In practice, you wouldn't probably use this sort of nesting. But it hints on interesting building blocks that are useful. And for the most part, this is what functors are. A basic building block, that more interesting things are based upon. For example, right now, we can only lift single-param functions. We should be able to solve this somehow.


"""
!So what in practice is a functor?

?In general, anything where you can define a sensible fmap(function, ) operation. The anything in question are mostly containers, but it might be a generic object providing additional context/metadata, for value(s) it could encapsulate, or produce.

*Sensible in this context means, that the interface obeys certain laws, but before we state them explicitly, I need to define two functions, id and compose:

^yellow
&pink
~purple
todo mustard
"""

from typing import Any
from typing import Callable, TypeVar
F = TypeVar('F', bound=Callable[[Any], Any])

T = TypeVar('T')
S = TypeVar('S')

def fmapList(fn: Callable[[Any], S], lst: list[Any]) -> list[S]:
    return [fn(x) for x in lst]

print(fmapList(str,[1,2,3]))


## ! there are more interesting things than containers that could be functors, for example functions:
def fmapFunction(function, fn):
    def wrapper(*arr):
        return fn(function(*arr))
    return wrapper

import random
print(fmapFunction(random.randint, str)(1,10))

"""
? Lift for our functions

^ Lifting is a concept which allows you to transform a function into a corresponding function
^ within another (usually more general) setting.

There is a recuring concept, where we use some bit of information 
about our datatype to convert functions that know nothing about it, 
to work with it.

We call this lifting.

For example, because I know that lists have map function, I could 
lift i.e. str to work on lists of things.
"""

def lift(fn):
    def liftedfn(x):
        return fmapList(fn,x)
    return liftedfn 

lifted_str = lift(str)
print(lifted_str([1,2,3]))

"""
? Making this more usable
Interesting question is, how to make these more pleasan't to use.
One approach might be defining fmap as @singledispatch, as we did
with mconcat previously. Only thing that is a bit awkward is, that
we can't have the function argument first.
"""

from functools import singledispatch, partial

@singledispatch
def fmap(x, fn):
    print(f"{fn} Not implemented for {x}")

def lift(fn):
    def liftedfn(x):
        return fmap(x, fn)
    return liftedfn 

@fmap.register([].__class__)
def _(lst, fn):
    return [fn(x) for x in lst]

@fmap.register(set().__class__)
def _(lst, fn):
    return set(fn(x) for x in lst)


@fmap.register({}.__class__)
def _(d, fn):
    return {x: fn(d[x]) for x in d}


lifted_str2 = lift(str)
lifted_str2 = lift(str)
print(f"A: ${lifted_str2([1,2,3])}")

print(fmap({1,2,3}, str))
print(fmap([1,2,3], str))
print(fmap('abcd', str))

# fmap is open for extension — register it for any new type.
# (This originally demoed a pandas Series; a plain tuple makes the same
#  point with no third-party dependency.)
@fmap.register(tuple)
def _(t, fn):
    return tuple(fn(x) for x in t)

print(fmap((1, 2, 3), str))

"""
? Now we can do nested fmap

Because we know, that functor of a functor is a functor, we can attempt a nested fmap.
"""

def fmapNested(xs, fn):
    def recur(x):
        if x.__class__ in fmap.registry.keys():
            return fmap(x,recur)
        else:
            return fn(x)
    return fmap(xs,recur)

def liftNested(fn):
    return lambda x: fmapNested(x,fn)

print(fmapNested([[1,2],{'a':[3,4]}, 3, 'lll'],str))

"""
? Effect tracking
Now, the interesting thing you can use functors for, is to track various side-effects 
and their meta-data with them. This is what i.e. Haskell does. The fmap then gives you 
the ability to say "I don't care about anything, just let me operate on the inner value(s)". 
These values might not be there, there might be error instead, there might be many, 
you might need to wait for a http request to complete, but with fmap, you can choose 
to ignore it, and just fmap over the values.
"""

class ErrorOrValue:
    def __init__(self,error,value):
        self._error = error
        self._value = value
        
    def map(self,fn):
        if self._error:
            return self
        else:
            return ErrorOrValue(None,fn(self._value))
        
    def __repr__(self):
        if self._error:
            return "Error:" + self._error
        else:
            return "Value:" + repr(self._value)
        
# @fmap.register(ErrorOrValue)
# def _(x,fn):
#     return x.map(fn)

import math
def sqrt(x):
    if x>=0:
        return ErrorOrValue(None,[math.sqrt(x), - math.sqrt(x)])
    else:
        return ErrorOrValue("Can't sqrt "+str(x),None)

print(sqrt(16))
print(sqrt(-16))

#lsqrt = liftNested(sqrt)
#print((lsqrt(lsqrt([256]))))


def curried_window(begin):
    return lambda end: (lambda array: array[begin:end])
curried_window(2)(4)([1,2,3,4,5])

print(fmap([1,2,3,4],curried_window))

@singledispatch
def apply(lx, lfn):
    raise Error("Not implemented for" + lx)

@fmap.register([].__class__)
def apply(lx,lfn):
    return [fn(x) for fn in lfn for x in lx]

a0 = map(curried_window,[1,2])
a1 = apply([5,6],a0)
a2 = apply([
    [1,2,3,4,5,6],
    [1,2,3,4,5,6]
              ],a1)

print(a0)
print(a1)
print(a2)