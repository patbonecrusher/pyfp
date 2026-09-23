from typing import Callable, Any, Optional, TypedDict
from functools import partial, wraps
from inspect import signature, _empty
#from itertools import map

# def curry(fn: Callable[..., Any]) -> Callable[..., Any]:
#     """
#     Curry a function
#     """
#     #! We use an inner function to be able to type correctly.
#     #! Without the inner, we rely on calling curry with a function
#     #! but in the _ case, it gets called with a partial and the
#     #! getting the arguments count is non possible in such case.
#     def _inner(n: int, fn: Callable[..., Any]) -> Callable[..., Any]:
#         match n:
#             case 1: return fn
#             case 2: return lambda x: partial(fn, x)
#             case _: return lambda x: _inner(n-1, partial(fn,x))
#     return _inner(fn.__code__.co_argcount, fn)

# def curry2(fn: Callable[..., Any]) -> Callable[..., Any]:
#     def _inner(**kwargs: Optional[Any]) -> Callable[..., Any]:
#         for key, value in kwargs.items():
#             print("{0} = {1}".format(key, value))
#         return fn
#     return _inner

# def test(d,b,c):
#     return d+b+c

# print(test(d=1, c=2, b=3))

# def test(*argv, **karg):
#     print(f"{argv=}, {karg=}")

# test(12, a=1, b=2, c='abc')

def varnames_to_kv(fn: Callable[..., Any]) -> list[dict[str, Any]]:
    params = signature(fn).parameters
    def to_kv(key: str) -> dict[str, Any]:
        return {key: params[key].default}

    return list(map(to_kv, fn.__code__.co_varnames))
    #return [{}]



def curry4(fn: Callable[..., Any]) -> Callable[..., Any]:
    # Keep track of the passed in values when count passed in == fn arg count
    # then execute the function in one go using the dictionary.

    # Before executing, do some variable assignments
    #   for each named variable, remove it from the original array
    #   then for remaining unnamed variable, just pop from the remaining array

    class Context(TypedDict):
        fn: Callable[..., Any]
        fn_args: list[dict[str, Any]]
        passed_args: list[dict[str, Any]]

    context: Context = {"fn": fn, "fn_args":varnames_to_kv(fn), "passed_args": []}
    #  def _inner(_context: Context, *argv: str, **kwargs: int) -> Callable[..., Any]:
    @wraps(fn)
    def _inner(passed_args: list[dict[str, Any]], *argv: str, **kwargs: str) -> Callable[..., Any]:
        # If count + so far > total args, abort.
        print(f"{passed_args=}")

        #args_as_list = list(map(lambda v: {"?":v}, argv))
        args = passed_args+ [{"?":v} for v in argv]
        args += [{k:v} for k,v in kwargs.items()]

        if len(args) == len(varnames_to_kv(fn)):
            # Make sure a variable is not defined twice
            print("executing")

        print(args)

        return partial(_inner, args)

    return partial(_inner, [])

def test(d: int,b: int=2,c: int=3) -> int:
    return d+b+c

print(varnames_to_kv(test))

ff = curry4(test)
print(ff(c=1)(2)(d=3))

def curry3(fn: Callable[..., Any]) -> Callable[..., Any]:

    #! We use an inner function to be able to type correctly.
    #! Without the inner, we rely on calling curry with a function
    #! but in the _ case, it gets called with a partial and the
    #! getting the arguments count is non possible in such case.
    # def _inner2(n: int, fn: Callable[..., Any]) -> Callable[..., Any]:
    #     match n:
    #         case 1: return fn
    #         case 2: return lambda x: partial(fn, x)
    #         case _: return lambda x: _inner2(n-1, partial(fn,x))

    # print(f"var={fn.__code__.co_argcount=}")
    # print(f"{signature(fn).parameters=}")

    base=0
    default_count=0
    default = []

    for k in fn.__code__.co_varnames:
        print(f"{k}={signature(fn).parameters[k].default=}")
        if signature(fn).parameters[k].default is _empty:
            base = base+1
        else:
            default_count = default_count+1
        default.append({k: signature(fn).parameters[k].default})

    #c = _inner2(fn.__code__.co_argcount, fn)
    #print(c(2)(3)('abc'))


    class Context(TypedDict):
        n: int
        fn: Callable[..., Any]
        base: int
        default_count: int
        default: Any

 
    context = {"n": fn.__code__.co_argcount, "fn": fn, "base": base, "default": default, "default_count": default_count}
    @wraps(fn)
    def _inner4(_context: Context, *argv: str, **kwargs: int) -> Callable[..., Any]:
        print('-----basdasd')
        print(f'a: {_context=}')
        _totalc = _context["n"]
        _fn = _context["fn"]
        _base = _context["base"]
        _default_count = _context["default_count"]
        _default = _context["default"]
        print(f'{_default=}')
        print(f"{_totalc=}")
        print(f"asa{_base=}")

        if _totalc == 1 and _base == 10:
            print(f"aaaasds{argv[0]=}")
            return _fn(argv[0])
        else:
            argc = len(argv)
            print(f"{argc=}")
            for arg in argv:
                print(f"{arg=}")
                print("c3 another arg through *argv:", arg)
                _default = _default[1:]
                print(f"{_default=}")

                _totalc = _totalc-1
                _base = _base-1
                print(f"b{_totalc=}")
                print(f"b{_base=}")

                if _totalc > 0:
                    _fn = wraps(fn)(partial(_fn, arg))
                    print(f"fn is now {_fn=}")
                else:
                    # # Last argument, we need to apply all the default.
                    # while _default_count != 0:
                    #     print(f"{_default=}")
                    #     _defaultx = _default[:1][0]
                    #     print(f"{_defaultx=}")
                    #     _default = _default[:-1]
                    #     _default_count = _default_count - 1
                    #     _fn = partial(_fn, **_defaultx)

                    print(f"asds_{arg=}")
                    return _fn(arg)


                #print(f"{_fn=}")
            argk = len(kwargs.items())
            print(f"{argk=}")
            for k,v in kwargs.items():
                print(f"{k=}, {v=}")
                kwarg = {k: v}
                print(f"{kwarg=}")
                for x in _default:
                    print(f"{x.get(k,None)=}")
                _default = [x for x in _default if x.get(k, None) is None]
                _default_count = _default_count - 1
                _totalc = _totalc-1
                if _totalc <= 0:
                    return _fn(**kwarg)

                _fn = wraps(fn)(partial(_fn, **kwarg))
                print(f"fn is now {_fn=}")
            #_totalc = _totalc - argc
            print(f"cc {_totalc=}")
            return partial(_inner4, {"n": _totalc, "fn": _fn, "base": _base, "default": _default, "default_count": _default_count})
    print("boo")
    return partial(_inner4, context)

def abcd(d: int, b: int = 3, c: str = 'hi') -> int:
    print(f"aaaa {d=},{b=}, {c=}")
    return d + b #+ int(c)

#? Keep an array of the value passed in.
#? When the array has been filled, call the function with the dictionary
#? If method takes a, b, c, d
#? If user specify b=2, 3, a=1, 4

#print("334", partial(partial(partial(abcd, d=1),5),c="aea")())
# abcd_cur3 = curry3(abcd)
# #print(abcd_cur3)
# print('-----a')
# #    assert fc(x=1)(1, 2) == 4
# print(abcd_cur3(b=1)(c="aaa")(d=3))
# #print(abcd_cur3(b=1)("aaa")(d=3)) // Fails because aaa will be assigned to d since d is the first member
# print('-----0')
# print(abcd_cur3(c="boo")(2, 3))
# print('-----1')
# print(abcd_cur3(2, 3, c="boo"))
# print('-----2')
# print(abcd_cur3(2, 3)(c="boo"))
# print('-----3')
# print(abcd_cur3(2)(3)(c="boo"))
# print('-----4')
# print(abcd_cur3(2)(c="a")(23))

# def abcd(a: int, b: int, c: str) -> int:
#     print(f"aaaa {a=},{b=}, {c=}")
#     return a + b #+ int(c)

#print(abcd.__code__.co_argcount)
#print(partial(abcd, 1))
# print(curry(abcd).__name__)
# print(curry(abcd)(1)(2)('10'))

# print(curry2(abcd).__name__)

# abcd_cur2 = curry2(abcd)
# print(abcd_cur2(a=12))

# abcd_cur3 = curry3(abcd)
# print(abcd_cur3)
# print('-----1')
# print(abcd_cur3(2))
# print('-----2')
# print(abcd_cur3(2,3))
# print('-----3')
# print(abcd_cur3(2, 3)('abd'))
# print('-----4')
# print(abcd_cur3(2)(3)('abd'))

# print('-----5')
# print(abcd_cur3(2)(3, 'abd'))

# print('-----6')
# print(abcd_cur3(2, 3, 'abd'))

# print(abcd_cur3(2,3)(2))

# abcd_cur4 = curry4(abcd)
# print(abcd_cur4(2))
# print(abcd_cur4(a=2))

# print(curry(abcd)(1)(2)('abc'))