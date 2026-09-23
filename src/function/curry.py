from typing import Any, Callable
from functools import wraps
from inspect import signature, Parameter


def curry(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Curry ``fn``, supporting positional args, keyword args, and defaults.

    Arguments accumulate across successive calls and may be grouped and ordered
    freely. ``fn`` is invoked as soon as every *required* parameter (one without
    a default) has been bound; parameters with defaults that were not supplied
    fall back to their defaults.

    Positional arguments fill the left-most parameters not already bound, so
    keyword and positional arguments can be interleaved::

        c = curry(lambda x, y, z: x + y + z)
        c(1)(2)(3) == c(1, 2, 3) == c(1, 2)(3) == c(1)(2, 3) == 6
        c(y=1)(1, 2) == 4          # y bound by name, x and z fill positionally

    Because invocation happens as soon as the required parameters are satisfied,
    supply any optional arguments in the same call as (or before) the final
    required one::

        d = curry(lambda a, b=3, c=10: a + b + c)
        d(b=1)(c=2)(5) == 8        # a is the only required param, bound last
        d(5) == 18                 # fires immediately: a=5, b and c defaulted

    Variadic parameters (``*args`` / ``**kwargs``) are not supported.
    """
    params = list(signature(fn).parameters.values())
    required = [p.name for p in params if p.default is Parameter.empty]

    def collect(bound: dict[str, Any]) -> Callable[..., Any]:
        @wraps(fn)
        def step(*args: Any, **kwargs: Any) -> Any:
            new = dict(bound)

            open_slots = [p.name for p in params if p.name not in new]
            if len(args) > len(open_slots):
                raise TypeError(
                    f"{fn.__name__}() got too many positional arguments")
            for name, value in zip(open_slots, args):
                new[name] = value

            for name, value in kwargs.items():
                if name not in signature(fn).parameters:
                    raise TypeError(
                        f"{fn.__name__}() got an unexpected keyword "
                        f"argument '{name}'")
                if name in new:
                    raise TypeError(
                        f"{fn.__name__}() got multiple values for "
                        f"argument '{name}'")
                new[name] = value

            if all(name in new for name in required):
                return fn(**new)
            return collect(new)

        return step

    return collect({})
