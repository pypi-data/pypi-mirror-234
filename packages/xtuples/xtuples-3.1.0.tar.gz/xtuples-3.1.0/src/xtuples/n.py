
from __future__ import annotations

from typing import TYPE_CHECKING

# ---------------------------------------------------------------

import abc
import typing
import functools

from .i import iTuple, pipe

# ---------------------------------------------------------------


class nTuple(abc.ABC):

    @abc.abstractmethod
    def __abstract__(self):
        # NOTE: here to prevent initialise instances of this
        # but rather use the decorator and typing.NamedTuple
        return

    @staticmethod
    def pipe(obj, f, *args, at = None, **kwargs):
        """
        >>> _ex = _Example(1, "a")
        >>> _ex.pipe(lambda a, b: a, None)
        _Example(x=1, s='a', it=iTuple())
        >>> _ex.pipe(lambda a, b: a, None, at = 1)
        >>> _ex.pipe(lambda a, b: a, None, at = 'b')
        >>> _ex.pipe(lambda a, b: a, a=None, at = 'b')
        >>> _ex.pipe(lambda a, b: a, b=None, at = 'a')
        _Example(x=1, s='a', it=iTuple())
        >>> _ex.pipe(lambda a, b: a, None, at = 0)
        _Example(x=1, s='a', it=iTuple())
        """
        return pipe(f, obj, *args, at = at, **kwargs)

    @staticmethod
    def partial(obj, f, *args, **kwargs):
        return functools.partial(f, obj, *args, **kwargs)

    @classmethod
    def is_subclass(cls, t):
        """
        >>> nTuple.is_subclass(tuple)
        False
        >>> nTuple.is_subclass(_Example(1, "a"))
        False
        >>> nTuple.is_subclass(_Example)
        True
        """
        try:
            is_sub = issubclass(t, tuple)
        except:
            is_sub = False
        return (
            is_sub and
            hasattr(t, "cls") and
            hasattr(t, "pipe") and
            hasattr(t, "partial")
        )

    @classmethod
    def is_instance(cls, obj):
        """
        >>> nTuple.is_instance(tuple)
        False
        >>> nTuple.is_instance(_Example)
        False
        >>> nTuple.is_instance(_Example(1, "a"))
        True
        """
        return (
            cls.is_subclass(type(obj)) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
        )


    @staticmethod
    def annotations(obj):
        """
        >>> ex = _Example(1, "a")
        >>> ex.pipe(ex.meta().annotations)
        {'x': ForwardRef('int'), 's': ForwardRef('str'), 'it': ForwardRef('iTuple')}
        """
        return obj.__annotations__

    @classmethod
    def as_dict(cls, obj):
        """
        >>> ex = _Example(1, "a")
        >>> ex.pipe(ex.meta().as_dict)
        {'x': 1, 's': 'a', 'it': iTuple()}
        """
        return obj._asdict()

    @classmethod
    def decorate(meta, **methods):
        def decorator(cls):
            cls.pipe = meta.pipe
            cls.partial = meta.partial
            cls.meta = lambda_meta(meta)
            cls.cls = lambda_cls(cls)
            for k, f in methods.items():
                setattr(cls, k, f)
            return cls
        return decorator

    @classmethod
    def enum(meta, cls):
        cls = meta.decorate()(cls)
        return functools.lru_cache(maxsize=1)(cls)

def lambda_meta(meta):
    def f(self: typing.NamedTuple) -> type[nTuple]:
        return meta
    return f

def lambda_cls(cls):
    def f(self: NT) -> type[NT]:
        return cls
    return f

NT = typing.TypeVar("NT", bound=typing.NamedTuple)
nT = typing.TypeVar("nT", bound=nTuple)

# ---------------------------------------------------------------

@nTuple.decorate()
class _Example(typing.NamedTuple):
    """
    >>> ex = _Example(1, "a")
    >>> ex
    _Example(x=1, s='a', it=iTuple())
    >>> ex.meta()
    <class 'xtuples.n.nTuple'>
    >>> ex.pipe(lambda nt: nt.x)
    1
    >>> f = ex.partial(lambda nt, v: nt.x * v)
    >>> f(2)
    2
    >>> f(3)
    3
    """
    # NOTE: cls, pipe, partial are mandatory boilerplate

    x: int
    s: str
    it: iTuple = iTuple.empty()
    
    def cls( # type: ignore[empty-body]
        self: _Example
    ) -> type[typing.NamedTuple]: ...

    def meta( # type: ignore[empty-body]
        self: _Example
    ) -> type[nTuple]: ...

    def pipe(self, f, *args, at = None, **kwargs): ...

    def partial(self, f, *args, at = None, **kwargs): ...

# ---------------------------------------------------------------
    
# NOTE: from the README

class Has_X(typing.Protocol):
    x: int

def f(self: Has_X) -> int:
    return self.x + 1

@nTuple.decorate(f = f)
class Example_A(typing.NamedTuple):

    x: int

    def f(self: Example_A) -> int: ... # type: ignore[empty-body]

@nTuple.decorate(f = f)
class Example_B(typing.NamedTuple):

    x: int
    y: float

    def f(self: Example_B) -> int: ... # type: ignore[empty-body]

nt: Example_A = Example_A(1)
i: int = nt.f()

# ---------------------------------------------------------------

