
from __future__ import annotations

import abc
import typing
from typing import TYPE_CHECKING

# ---------------------------------------------------------------

import itertools
import functools

# NOTE: used in doctests
import operator

# ---------------------------------------------------------------

T = typing.TypeVar('T')
V = typing.TypeVar('V')

U = typing.TypeVar('U')
U0 = typing.TypeVar('U0')
U1 = typing.TypeVar('U1')
U2 = typing.TypeVar('U2')
U3 = typing.TypeVar('U3')
U4 = typing.TypeVar('U4')
U5 = typing.TypeVar('U5')

W = typing.TypeVar('W')
W0 = typing.TypeVar('W0')
W1 = typing.TypeVar('W1')
W2 = typing.TypeVar('W2')
W3 = typing.TypeVar('W3')
W4 = typing.TypeVar('W4')
W5 = typing.TypeVar('W5')

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT, SupportsDunderGT

else:
    class SupportsDunderLT(typing.Protocol):
        def __lt__(self, __other: typing.Any) -> bool: ...

    class SupportsDunderGT(typing.Protocol):
        def __gt__(self, __other: typing.Any) -> bool: ...

CT = typing.Union[
    SupportsDunderLT,
    SupportsDunderGT,
]

# ---------------------------------------------------------------

@typing.overload
def lazy_res(
    res: typing.Iterable[V], lazy: typing.Literal[True]
) -> iLazy[V]: ...

@typing.overload
def lazy_res(
    res: typing.Iterable[V], lazy: typing.Literal[False]
) -> iTuple[V]: ...

def lazy_res(res, lazy) -> iUnionV:
    if not lazy:
        return iTuple(res)
    return iLazy(res)

# ---------------------------------------------------------------

class fStarN(typing.Generic[V]):

    @abc.abstractmethod
    def __call__(
        self, 
        u: U, 
        u0: U0, 
        u1: U1, 
        u2: U2, 
        u3: U3, 
        u4: U4, 
        u5: U5, 
        *args: typing.Any
    ) -> V: ...

@typing.overload
def f_star(
    f: typing.Callable[[U], V]
) -> typing.Callable[[tuple[U]], V]: ...

@typing.overload
def f_star(
    f: typing.Callable[[U, U0], V]
) -> typing.Callable[[tuple[U, U0]], V]: ...

@typing.overload
def f_star(
    f: typing.Callable[[U, U0, U1], V]
) -> typing.Callable[[tuple[U, U0, U1]], V]: ...

@typing.overload
def f_star(
    f: typing.Callable[[U, U0, U1, U2], V]
) -> typing.Callable[[tuple[U, U0, U1, U2]], V]: ...

@typing.overload
def f_star(
    f: typing.Callable[[U, U0, U1, U2, U3], V]
) -> typing.Callable[[tuple[U, U0, U1, U2, U3]], V]: ...

@typing.overload
def f_star(
    f: typing.Callable[[U, U0, U1, U2, U3, U4], V]
) -> typing.Callable[[tuple[U, U0, U1, U2, U3, U4]], V]: ...

@typing.overload
def f_star(
    f: fStarN
) -> typing.Callable[[tuple[U, U0, U1, U2, U3, U4, U5]], V]: ...

def f_star(f, **kwargs):
    def f_res(v_tuple):
        try:
            return f(*v_tuple, **kwargs)
        except:
            assert False, (f, v_tuple, kwargs,)
    return f_res
    
# ---------------------------------------------------------------

tuple_getitem = tuple.__getitem__

# ---------------------------------------------------------------

class iLazy(typing.Iterator[T]):

    it: typing.Iterator[T]
    done: bool = False

    def __init__(self, it: typing.Iterator[T]):
        setattr(self, "__iter__", it.__iter__)
        setattr(self, "__next__", it.__next__)
        self.it = it

    def __iter__(self):
        return self.it.__iter__()
    
    def __next__(self):
        return self.it.__next__()

    def eager(self):
        assert not self.done, self
        self.done = True
        return iTuple(self.it)

# ---------------------------------------------------------------

class iTuple(tuple, typing.Generic[T]):

    # -----

    @staticmethod
    def __new__(cls, *args):
        if len(args) == 1:
            v = args[0]
            if isinstance(v, cls):
                return v
            elif not isinstance(v, typing.Iterable):
                return ().__new__(cls, (v,))
        return super().__new__(cls, *args)

    def __repr__(self):
        """
        >>> iTuple()
        iTuple()
        >>> iTuple(iTuple((3, 2,)))
        iTuple(3, 2)
        """
        s = tuple.__repr__(self)
        return "{}({})".format(
            type(self).__name__,
            s[1:-2 if s[-2] == "," else -1],
        )

    def __str__(self):
        return self.__repr__()

    # -----

    @classmethod
    def empty(cls):
        return cls(tuple())

    @classmethod
    def one(cls: typing.Type[iTuple], v: T) -> iTuple[T]:
        return cls((v,))

    @classmethod
    def none(cls, n):
        """
        >>> iTuple.none(3)
        iTuple(None, None, None)
        """
        return cls((None for _ in range(n)))

    @classmethod
    def range(cls, *args, **kwargs) -> iTuple[int]:
        """
        >>> iTuple.range(3)
        iTuple(0, 1, 2)
        """
        return iTuple(range(*args, **kwargs))

    @classmethod
    def from_keys(cls, d):
        """
        >>> iTuple.from_keys({i: i + 1 for i in range(2)})
        iTuple(0, 1)
        """
        return cls(d.keys())
        
    @classmethod
    def from_values(cls, d):
        """
        >>> iTuple.from_values({i: i + 1 for i in range(2)})
        iTuple(1, 2)
        """
        return cls(d.values())
        
    @classmethod
    def from_items(cls, d):
        """
        >>> iTuple.from_items({i: i + 1 for i in range(2)})
        iTuple((0, 1), (1, 2))
        """
        return cls(d.items())
    
    @classmethod
    def from_index(cls, s):
        return cls(s.index)

    @classmethod
    def from_index_values(cls, s):
        return cls(s.index.values)

    @classmethod
    def from_columns(cls, s):
        return cls(s.columns)

    # -----

    def pipe(self, f, *args, at = None, **kwargs):
        """
        >>> iTuple.range(2).pipe(lambda it: it)
        iTuple(0, 1)
        >>> iTuple.range(2).pipe(
        ...     lambda it, v: it.map(lambda x: x * v), 2
        ... )
        iTuple(0, 2)
        """
        return pipe(f, self, *args, at = at, **kwargs)

    def partial(self, f, *args, **kwargs):
        """
        >>> f = iTuple.range(2).partial(
        ...     lambda it, v: it.map(lambda x: x * v)
        ... )
        >>> f(2)
        iTuple(0, 2)
        >>> f(3)
        iTuple(0, 3)
        """
        return functools.partial(f, self, *args, **kwargs)

    # -----

    # def __len__(self):
    #     return len(self)

    # def __contains__(self, v):
    #     return v in self

    def index_of(self, v):
        return self.index(v)

    def len(self):
        """
        >>> iTuple.range(3).len()
        3
        """
        return len(self)

    def len_range(self):
        """
        >>> iTuple.range(3).len()
        3
        """
        return iTuple.range(self.len())

    def append(
        self: iTuple[T], value: V, *values: V
    ) -> iTuple[typing.Union[T, V]]:
        """
        >>> iTuple().append(1)
        iTuple(1)
        >>> iTuple.range(1).append(1)
        iTuple(0, 1)
        >>> iTuple.range(1).append(1, 2)
        iTuple(0, 1, 2)
        >>> iTuple.range(1).append(1, 2, 3)
        iTuple(0, 1, 2, 3)
        >>> iTuple.range(1).append(1, (2,))
        iTuple(0, 1, (2,))
        """
        return iTuple((*self, value, *values,))

    def prepend(
        self: iTuple[T], value: V, *values: V
    ) -> iTuple[typing.Union[T, V]]:
        """
        >>> iTuple().prepend(1)
        iTuple(1)
        >>> iTuple.range(1).prepend(1)
        iTuple(1, 0)
        >>> iTuple.range(1).prepend(1, 2)
        iTuple(1, 2, 0)
        >>> iTuple.range(1).prepend(1, 2, 3)
        iTuple(1, 2, 3, 0)
        >>> iTuple.range(1).prepend(1, (2,))
        iTuple(1, (2,), 0)
        """
        return iTuple((value, *values, *self,))

    # no iterables (so star doesn't matter)

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0]
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0],
        typing.Iterable[U1],
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0],
        typing.Iterable[U1],
        typing.Iterable[U2],
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0],
        typing.Iterable[U1],
        typing.Iterable[U2],
        typing.Iterable[U3],
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0],
        typing.Iterable[U1],
        typing.Iterable[U2],
        typing.Iterable[U3],
        typing.Iterable[U4],
    ]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        *,
        star: typing.Literal[False] = False,
    ) -> tuple[
        typing.Iterable[U],
        typing.Iterable[U0],
        typing.Iterable[U1],
        typing.Iterable[U2],
        typing.Iterable[U3],
        typing.Iterable[U4],
        typing.Iterable[U5],
    ]: ...

    # star - one iter

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, U1, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, U1, U2, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, U1, U2, U3, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, U1, U2, U3, U4, W]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        itr_0: typing.Iterable[W],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[U, U0, U1, U2, U3, U4, U5, W]]: ...

    # star - two iter

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, W, W0
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, U5, W, W0
        #
    ]]: ...

    # star - three iter

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, W, W0, W1
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, U5, W, W0, W1
        #
    ]]: ...

    # star - four iter

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, W, W0, W1, W2
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, U5, W, W0, W1, W2
        #
    ]]: ...

    # star - five iter

    # TODO: check
    @typing.overload
    def zip(
        self: iTuple[tuple[U]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, W, W0, W1, W2, W3
        #
    ]]: ...

    @typing.overload
    def zip(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        itr_0: typing.Iterable[W],
        itr_1: typing.Iterable[W0],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W2],
        itr_4: typing.Iterable[W3],
        *,
        star: typing.Literal[True],
    ) -> iTuple[tuple[
        U, U0, U1, U2, U3, U4, U5, W, W0, W1, W2, W3
        #
    ]]: ...

    # star - fall through

    @typing.overload
    def zip(
        self: iTuple[tuple],
        itr_0: typing.Iterable[W0],
        itr_1: typing.Iterable[W1],
        itr_2: typing.Iterable[W1],
        itr_3: typing.Iterable[W1],
        itr_4: typing.Iterable[W1],
        itr_5: typing.Iterable[W1],
        *iterables: typing.Iterable,
        star: typing.Literal[True],
    ) -> iTuple[tuple]: ...

    # no star

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0]]: ...
    
    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0, U1]]: ...

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        itr_2: typing.Iterable[U2],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0, U1, U2]]: ...

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        itr_2: typing.Iterable[U2],
        itr_3: typing.Iterable[U3],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0, U1, U2, U3]]: ...

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        itr_2: typing.Iterable[U2],
        itr_3: typing.Iterable[U3],
        itr_4: typing.Iterable[U4],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0, U1, U2, U3, U4]]: ...

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        itr_2: typing.Iterable[U2],
        itr_3: typing.Iterable[U3],
        itr_4: typing.Iterable[U4],
        itr_5: typing.Iterable[U5],
        *,
        star: typing.Literal[False] = False,
    ) -> iTuple[tuple[T, U0, U1, U2, U3, U4, U5]]: ...

    # no star - fall through

    @typing.overload
    def zip(
        self: iTuple[T],
        itr_0: typing.Iterable[U0],
        itr_1: typing.Iterable[U1],
        itr_2: typing.Iterable[U2],
        itr_3: typing.Iterable[U3],
        itr_4: typing.Iterable[U4],
        itr_5: typing.Iterable[U5],
        *iters: typing.Iterator,
        star: typing.Literal[False] = False,
    ) -> iTuple: ...

    # implementation

    def zip(
        self,
        *itrs,
        star=False,
    ):
        """
        >>> iTuple([[1, 1], [2, 2], [3, 3]]).zip()
        iTuple((1, 2, 3), (1, 2, 3))
        >>> iTuple([iTuple.range(3), iTuple.range(1, 4)]).zip()
        iTuple((0, 1), (1, 2), (2, 3))
        >>> v0 = iTuple.range(3).zip(iTuple.range(1, 4))
        >>> v0
        iTuple((0, 1), (1, 2), (2, 3))
        >>> v0.zip(v0)
        iTuple(((0, 1), (0, 1)), ((1, 2), (1, 2)), ((2, 3), (2, 3)))
        >>> v0.zip(v0, star=True)
        iTuple((0, 1, (0, 1)), (1, 2, (1, 2)), (2, 3, (2, 3)))
        """
        if star:
            res = zip(*zip(*self), *itrs)
        elif len(itrs) == 0:
            res = zip(*self)
        else:
            res = zip(self, *itrs)
        return iTuple(res)

    def flatten(self):
        """
        >>> iTuple.range(3).map(lambda x: [x]).flatten()
        iTuple(0, 1, 2)
        """
        return iTuple(itertools.chain(*self))

    def extend(self, value, *values):
        """
        >>> iTuple.range(1).extend((1,))
        iTuple(0, 1)
        >>> iTuple.range(1).extend([1])
        iTuple(0, 1)
        >>> iTuple.range(1).extend([1], [2])
        iTuple(0, 1, 2)
        >>> iTuple.range(1).extend([1], [[2]])
        iTuple(0, 1, [2])
        >>> iTuple.range(1).extend([1], [[2]], [2])
        iTuple(0, 1, [2], 2)
        """
        return iTuple(itertools.chain.from_iterable(
            (self, value, *values)
        ))

    def pretend(self, value, *values):
        """
        >>> iTuple.range(1).pretend((1,))
        iTuple(1, 0)
        >>> iTuple.range(1).pretend([1])
        iTuple(1, 0)
        >>> iTuple.range(1).pretend([1], [2])
        iTuple(1, 2, 0)
        >>> iTuple.range(1).pretend([1], [[2]])
        iTuple(1, [2], 0)
        >>> iTuple.range(1).pretend([1], [[2]], [2])
        iTuple(1, [2], 2, 0)
        """
        return iTuple(itertools.chain.from_iterable(
            (value, *values, self)
        ))

    def any_f(
        self, f: typing.Callable[..., bool], *, star = False
    ):
        return any(self.map(f, lazy = True, star=star))

    def any(
        self, 
        f: typing.Optional[
            typing.Callable[..., bool]
        ] = None, 
        *,
        star = False
    ):
        if f is not None:
            return self.any_f(f, star=star)
        return any(self)

    def anystar(self, f):
        return any(self.mapstar(f))
    
    def all_f(
        self, f: typing.Callable[..., bool], *, star = False
    ):
        return all(self.map(f, lazy = True, star=star))

    def all(
        self, 
        f: typing.Optional[
            typing.Callable[..., bool]
        ] = None,
        star: bool = False
    ):
        if f is not None:
            return self.all_f(f, star=star)
        return all(self)

    def allstar(self, f: typing.Callable[..., bool]):
        return all(self.mapstar(f))

    def assert_all(self, f: typing.Callable[..., bool], f_error = None, star: bool = False):
        if f_error:
            assert self.all(f, star = star), f_error(self)
        else:
            assert self.all(f, star = star)
        return self

    def assert_any(self, f: typing.Callable[..., bool], f_error = None, star: bool = False):
        if f_error:
            assert self.any(f, star = star), f_error(self)
        else:
            assert self.any(f, star = star)
        return self

    @typing.overload
    def filter(
        self: iTuple[T], 
        f: typing.Callable[..., bool], 
        *iterables: typing.Iterable,
        lazy: typing.Literal[True],
        star: bool = False,
        **kwargs,
    ) -> iLazy[T]: ...

    @typing.overload
    def filter(
        self: iTuple[T], 
        f: typing.Callable[..., bool], 
        *iterables: typing.Iterable,
        lazy: typing.Literal[False] = False,
        star: bool = False,
        **kwargs,
    ) -> iTuple[T]: ...

    def filter(
        self: iTuple[T], 
        f, 
        *iterables: typing.Iterable,
        lazy = False,
        star =False,
        **kwargs,
    ):
    
        res: typing.Iterator[T]

        func: typing.Callable[..., bool] = (
            functools.partial(f, **kwargs)
            if len(kwargs)
            else f
        )

        if star:
            res = itertools.compress(
                self, self.map(func, star=star)
            )
        elif len(iterables):
            narrow = typing.cast(iTuple[typing.Iterable], self)
            res_wide = narrow.star_filter(f, *iterables, **kwargs)
            res = typing.cast(typing.Iterator[T], res_wide)
        else:
            res = filter(func, self)

        return lazy_res(res, lazy)

    def star_filter(
        self: iTuple[typing.Iterable], 
        f: typing.Callable[..., bool],
        *iterables: typing.Iterable,
        **kwargs,
    ) -> typing.Iterator[typing.Iterable]:
        return itertools.compress(
            self, 
            self.map(f, *iterables, star=True, **kwargs)
        )

    def filter_eq(
        self, eq, **kwargs
    ):
        """
        >>> iTuple.range(3).filter_eq(1)
        iTuple(1)
        """
        f = functools.partial(operator.eq, eq)
        return self.filter(f, **kwargs)

    @typing.overload
    def filterstar(
        self,
        f: typing.Callable[..., bool],
        *,
        lazy: typing.Literal[True],
        **kwargs,
    ) -> iLazy[T]: ...

    @typing.overload
    def filterstar(
        self,
        f: typing.Callable[..., bool],
        *,
        lazy: typing.Literal[False] = False,
        **kwargs
    ) -> iTuple[T]: ...

    def filterstar(
        self,
        f: typing.Callable[..., bool],
        *,
        lazy = False,
        **kwargs
    ):
        """
        >>> iTuple.range(3).filter(lambda x: x > 1)
        iTuple(2)
        """
        return self.filter(f, lazy=lazy, star=True, **kwargs)

    def is_none(self):
        return self.filter(lambda v: v is None)

    def not_none(self):
        return self.filter(lambda v: v is not None)

    # TODO: can probably use overloads?

    def i_min(
        self: iTuple[T], 
        f: typing.Optional[typing.Callable[[T], CT]] = None
    ) -> int:
        if f is not None:
            key = lambda _, v: f(v)
        else:
            key = lambda _, v: v
        return self.enumerate().sortby(key).first()[0]

    def i_max(
        self: iTuple[T], 
        f: typing.Optional[typing.Callable[[T], CT]] = None
    ) -> int:
        if f is not None:
            key = lambda _, v: f(v)
        else:
            key = lambda _, v: v
        return self.enumerate().sortby(key).last()[0]

    #

    @typing.overload
    def map(
        self: iTuple[T],
        f: typing.Callable[[T], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[False] = False,
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[T],
        f: typing.Callable[[T], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[False] = False,
        **kwargs,
    ) -> iTuple[V]: ...

    #

    @typing.overload
    def map(
        self: iTuple[tuple[U]],
        f: typing.Callable[[U], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U]],
        f: typing.Callable[[U], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0]],
        f: typing.Callable[[U, U0], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0]],
        f: typing.Callable[[U, U0], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1]],
        f: typing.Callable[[U, U0, U1], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1]],
        f: typing.Callable[[U, U0, U1], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2]],
        f: typing.Callable[[U, U0, U1, U2], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2]],
        f: typing.Callable[[U, U0, U1, U2], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        f: typing.Callable[[U, U0, U1, U2, U3], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3]],
        f: typing.Callable[[U, U0, U1, U2, U3], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        f: typing.Callable[[U, U0, U1, U2, U3, U4], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4]],
        f: typing.Callable[[U, U0, U1, U2, U3, U4], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        f: typing.Callable[[U, U0, U1], V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[tuple[U, U0, U1, U2, U3, U4, U5]],
        f: typing.Callable[[U, U0, U1], V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    #

    @typing.overload
    def map(
        self: iTuple[typing.Iterable],
        f: typing.Callable[..., V],
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[typing.Iterable],
        f: typing.Callable[..., V],
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def map(
        self: iTuple[typing.Iterable],
        f: typing.Callable[..., V],
        *iterables: typing.Iterable,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple[typing.Iterable],
        f: typing.Callable[..., V],
        *iterables: typing.Iterable,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    #

    @typing.overload
    def map(
        self: iTuple,
        f: typing.Callable[..., V],
        *iterables: typing.Iterable,
        lazy: typing.Literal[True],
        star: typing.Literal[False],
        **kwargs,
    ) -> iLazy[V]: ...

    @typing.overload
    def map(
        self: iTuple,
        f: typing.Callable[..., V],
        *iterables: typing.Iterable,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[False],
        **kwargs,
    ) -> iTuple[V]: ...

    def map(
        self,
        f,
        *iterables: typing.Iterable,
        lazy = False,
        star = False,
        **kwargs,
    ):
        """
        >>> iTuple.range(3).map(lambda x: x * 2)
        iTuple(0, 2, 4)
        """
        z: iTuple[tuple]
        # TODO: comprehensively benchmark all the star cases

        if len(kwargs):
            f = functools.partial(f, **kwargs)

        if not star:
            return lazy_res(map(f, self, *iterables), lazy)
    
        # func: typing.Callable[..., V] = f_star(f)

        if not len(iterables):
            return lazy_res(map(f_star(f), self), lazy)

        z = self.zip(*iterables, star=star)
        return lazy_res(map(f_star(f), z), lazy)

    # args, kwargs
    def mapstar(self, f, *args, star = True, **kwargs):
        return self.map(f, *args, star=star, **kwargs)

    def get(self, i):
        if isinstance(i, slice):
            return type(self)(self[i])
        return self[i]

    def __getitem__(self, i):
        if isinstance(i, slice):
            return type(self)(tuple_getitem(self, i))
        return tuple_getitem(self, i)

    def __add__(self, v):
        if isinstance(v, typing.Iterable):
            return self.extend(v)
        assert False, type(v)

    # def __iter__(self):
    #     return iter(self)

    def iter(self):
        """
        >>> for x in iTuple.range(3).iter(): print(x)
        0
        1
        2
        """
        return iter(self)

    def enumerate(self: iTuple[T]) -> iTuple[tuple[int, T]]:
        """
        >>> iTuple.range(3).enumerate()
        iTuple((0, 0), (1, 1), (2, 2))
        """
        # TODO: allow lazy
        return iTuple(enumerate(self))

    def chunkby(
        self, 
        f, 
        lazy: bool = False, 
        keys = False,
        pipe= None,
        throw=False,
    ):
        """
        >>> iTuple.range(3).chunkby(lambda x: x < 2)
        iTuple(iTuple(0, 1), iTuple(2))
        >>> iTuple.range(3).chunkby(
        ...    lambda x: x < 2, keys=True, pipe=dict
        ... )
        {True: iTuple(0, 1), False: iTuple(2)}
        """
        # TODO: lazy no keys
        res = itertools.groupby(self, key=f)
        if lazy and keys and pipe is None:
            return res
        if pipe is None:
            pipe = iTuple
        if keys:
            return pipe((k, iTuple(g),) for k, g in res)
        else:
            return pipe(iTuple(g) for k, g in res)

    def rechunk(self, keys = False):
        f = lambda kg: kg[0]
        res = itertools.groupby(self, key=f)
        if keys:
            return iTuple(
                (k, iTuple(g for k, g in kgs).flatten(),)
                for k, kgs in res
            )
        return iTuple(
            iTuple(g for k, g in kgs).flatten()
            for k, kgs in res
        )

    def groupby(
        self, f, lazy: bool = False, keys = False, pipe = None
    ):
        """
        >>> iTuple.range(3).groupby(lambda x: x < 2)
        iTuple(iTuple(2), iTuple(0, 1))
        >>> iTuple.range(3).groupby(
        ...    lambda x: x < 2, keys=True, pipe=dict
        ... )
        {False: iTuple(2), True: iTuple(0, 1)}
        """
        res = (
            self.chunkby(f, keys=True)
            .sortby(lambda kg: kg[0])
            .rechunk(keys = keys)
        )
        if pipe is None:
            pipe = iTuple
        return pipe(res)

    def first(self):
        """
        >>> iTuple.range(3).first()
        0
        """
        return self[0]
    
    def last(self):
        """
        >>> iTuple.range(3).last()
        2
        """
        return self[-1]

    def insert(self, i, v):
        """
        >>> iTuple.range(3).insert(2, 4)
        iTuple(0, 1, 4, 2)
        """
        return self[:i].append(v).extend(self[i:])

    def instend(self, i, v):
        return self[:i].extend(v).extend(self[i:])

    def pop_first(self):
        return self[1:]

    def pop_last(self):
        return self[:-1]

    def pop(self, i):
        return self[:i] + self[i + 1:]

    def first_where(self, f, default = None, star: bool = False):
        """
        >>> iTuple.range(3).first_where(lambda v: v > 0)
        1
        """
        if star:
            for v in self:
                if f(*v):
                    return v
        else:
            for v in self:
                if f(v):
                    return v
        return default

    def last_where(self, f, default = None, star: bool = False):
        """
        >>> iTuple.range(3).last_where(lambda v: v < 2)
        1
        """
        if star:
            for v in reversed(self):
                if f(*v):
                    return v
        for v in reversed(self):
            if f(v):
                return v
        return default

    @classmethod
    def n_from(cls, gen, n):
        return cls.range(n).zip(gen).mapstar(
            lambda i, v: v
        )

    @classmethod
    def from_while(
        cls, 
        gen, 
        f, 
        n = None, 
        star: bool = False,
        iters=None,
        value=True,
    ):
        def _gen():
            _n = 0
            for i, v in enumerate(gen):
                if iters is not None and i == iters:
                    return
                if n == _n:
                    return
                if star:
                    if not f(*v) == value:
                        return
                else:
                    if not f(v) == value:
                        return
                yield v
                _n += 1
        return cls(_gen())

    @classmethod
    def from_where(
        cls, 
        gen, 
        f, 
        n = None, 
        star: bool = False,
        iters=None,
        value=True,
    ):
        def _gen():
            _n = 0
            for i, v in enumerate(gen):
                if iters is not None and i == iters:
                    return
                if n == _n:
                    return
                if star:
                    if not f(*v) == value:
                        continue
                else:
                    if not f(v) == value:
                        continue
                yield v
                _n += 1
        return cls(_gen())

    def clear(self):
        return type(self)()

    def take(self, n):
        """
        >>> iTuple.range(3).take(2)
        iTuple(0, 1)
        """
        return self[:n]

    def tail(self, n):
        """
        >>> iTuple.range(3).tail(2)
        iTuple(1, 2)
        """
        return self[-n:]

    def reverse(self, lazy: bool = False):
        """
        >>> iTuple.range(3).reverse()
        iTuple(2, 1, 0)
        """
        if lazy:
            return reversed(self)
        return type(self)(reversed(self))

    def take_while(self, f, n = None, lazy: bool = False):
        """
        >>> iTuple.range(3).take_while(lambda v: v < 1)
        iTuple(0)
        """
        def iter():
            i = 0
            for v in self:
                if f(v) and (n is None or i < n):
                    yield v
                    i += 1
                else:
                    return
        res = iter()
        return res if lazy else type(self)(res)

    def tail_while(self, f, n = None):
        """
        >>> iTuple.range(3).tail_while(lambda v: v > 1)
        iTuple(2)
        """
        i = 0
        for v in reversed(self):
            if f(v) and (n is None or i < n):
                i += 1
            else:
                break
        return self.tail(i)

    # NOTE: from as in, starting from first true
    # versus above, which is until first false
    def take_after(self, f, n = None, lazy: bool = False):
        """
        >>> iTuple.range(3).take_after(lambda v: v < 1)
        iTuple(1, 2)
        >>> iTuple.range(3).take_after(lambda v: v < 1, n = 1)
        iTuple(1)
        """
        def iter():
            i = 0
            for v in self:
                if f(v):
                    pass
                elif n is None or i < n:
                    yield v
                    i += 1
                else:
                    return
        res = iter()
        return res if lazy else type(self)(res)

    def tail_after(self, f, n = None):
        """
        >>> iTuple.range(3).tail_after(lambda v: v < 2)
        iTuple(0, 1)
        >>> iTuple.range(3).tail_after(lambda v: v < 2, 1)
        iTuple(1)
        """
        l = 0
        r = 0
        for v in reversed(self):
            if not f(v):
                l += 1
            elif n is None or r < n:
                r += 1
            else:
                break
        return self.tail(l + r).take(r)

    def islice(self, left = None, right = None):
        """
        >>> iTuple.range(5).islice(1, 3)
        iTuple(1, 2)
        """
        return self[left:right]

    def unique(self):
        """
        >>> iTuple([1, 1, 3, 2, 4, 2, 3]).unique()
        iTuple(1, 3, 2, 4)
        """
        def iter():
            seen: typing.Set = set()
            seen_add = seen.add
            seen_contains = seen.__contains__
            for v in itertools.filterfalse(seen_contains, self):
                seen_add(v)
                yield v
        return type(self)(iter())

    def argsort(self, f = lambda v: v, star: bool = False, reverse = False):
        if star:
            f_sort = lambda i, v: f(*v)
        else:
            f_sort = lambda i, v: f(v)
        return self.enumerate().sortstar(
            f=f_sort, reverse=reverse,
        ).mapstar(lambda i, v: i)

    def sort(self: iTuple[CT], reverse=False) -> iTuple[CT]:
        return type(self)(sorted(self, reverse=reverse))
    
    def sortby(
        self: iTuple[T], 
        f: typing.Union[
            typing.Callable[[T], CT],
            typing.Callable[..., CT],
        ],
        reverse = False,
        star: bool = False,
    ):
        """
        >>> iTuple.range(3).reverse().sort()
        iTuple(0, 1, 2)
        >>> iTuple.range(3).sort()
        iTuple(0, 1, 2)
        """
        if star:
            return self.sortstar(f=f, reverse=reverse)
        return type(self)(
            sorted(self, key = f, reverse=reverse)
            #
        )
    
    def sortstar(
        self: iTuple[T], 
        f: typing.Callable[..., CT],
        reverse = False
    ):
        """
        >>> iTuple.range(3).reverse().sort()
        iTuple(0, 1, 2)
        >>> iTuple.range(3).sort()
        iTuple(0, 1, 2)
        """
        return type(self)(
            sorted(self, key = lambda v: f(*v), reverse=reverse)
            #
        )

    # NOTE: ie. for sorting back after some other transformation
    def sort_with_indices(
        self, f = lambda v: v, reverse=False
    ):
        return self.enumerate().sortstar(
            lambda i, v: f(v), reverse=reverse
        )

    def sortstar_with_indices(
        self, f = lambda v: v, reverse=False
    ):
        return self.enumerate().sortstar(
            lambda i, v: f(*v), reverse=reverse
        )

    @typing.overload
    def foldcum(
        self: iTuple[T], 
        f: typing.Callable[[V, T], V], 
        initial: typing.Optional[V] = None, 
        *,
        lazy: typing.Literal[True],
        star: bool = False,
        **kwargs,
    ) -> iLazy[V]: ...
    
    @typing.overload
    def foldcum(
        self: iTuple[T], 
        f: typing.Callable[[V, T], V], 
        initial: typing.Optional[V] = None, 
        *,
        lazy: typing.Literal[False] = False,
        star: bool = False,
        **kwargs,
    ) -> iTuple[V]: ...

    @typing.overload
    def foldcum(
        self: iTuple, 
        f: typing.Callable[..., V], 
        initial: typing.Optional[V] = None, 
        *,
        lazy: typing.Literal[True],
        star: typing.Literal[True],
        **kwargs,
    ) -> iLazy[V]: ...
    
    @typing.overload
    def foldcum(
        self: iTuple, 
        f: typing.Callable[..., V], 
        initial: typing.Optional[V] = None, 
        *,
        lazy: typing.Literal[False] = False,
        star: typing.Literal[True],
        **kwargs,
    ) -> iTuple[V]: ...

    def foldcum(
        self,
        f,
        initial: typing.Optional[V] = None, 
        *,
        lazy: bool = False,
        star: bool = False,
        **kwargs,
    ) -> iUnionV:
        """
        >>> iTuple.range(3).foldcum(lambda acc, v: v)
        iTuple(0, 1, 2)
        >>> iTuple.range(3).foldcum(lambda acc, v: v, initial=0)
        iTuple(0, 0, 1, 2)
        >>> iTuple.range(3).foldcum(operator.add)
        iTuple(0, 1, 3)
        """
        func: typing.Callable[[V, T], V]
        res: typing.Iterator[V]
        if len(kwargs):
            f = functools.partial(f, **kwargs)
        func = f if not star else lambda acc, v: f(acc, *v)
        res = itertools.accumulate(
            self, func=func, initial=initial
        )
        return iLazy(res) if lazy else iTuple(res)

    @typing.overload
    def fold(
        self: iTuple[T], 
        f: typing.Callable[[V, T], V],
        initial: typing.Optional[V] = None, 
        *,
        star: bool = False,
        **kwargs,
    ) -> V: ...

    @typing.overload
    def fold(
        self: iTuple, 
        f: typing.Callable[..., V],
        initial: typing.Optional[V] = None, 
        *,
        star: typing.Literal[True],
        **kwargs,
    ) -> V: ...

    def fold(
        self,
        f,
        initial: typing.Optional[V] = None, 
        *,
        star: bool = False,
        **kwargs,
    ) -> V:
        """
        >>> iTuple.range(3).fold(lambda acc, v: v)
        2
        >>> iTuple.range(3).fold(lambda acc, v: v, initial=0)
        2
        >>> iTuple.range(3).fold(operator.add)
        3
        >>> (
        ...     iTuple.range(10)
        ...     .filter(lambda v: v > 1)
        ...     .fold(lambda primes, v: (
        ...         primes.append(v)
        ...         if not primes.any(lambda prime: v % prime == 0)
        ...         else primes
        ...     ), initial=iTuple())
        ...     .map(lambda v: v ** 2)
        ... )
        iTuple(4, 9, 25, 49)
        """
        func: typing.Callable[[V, T], V]
        if len(kwargs):
            f = functools.partial(f, **kwargs)
        func = f if not star else lambda acc, v: f(acc, *v)
        if initial is not None:
            return functools.reduce(func, self, initial)
        return functools.reduce(func, self)

    def foldstar(
        self: iTuple[T], 
        f: typing.Callable[..., V], 
        initial: typing.Optional[V] = None, 
        **kwargs,
    ) -> V:
        """
        >>> iTuple.range(3).fold(lambda acc, v: v)
        2
        >>> iTuple.range(3).fold(lambda acc, v: v, initial=0)
        2
        >>> iTuple.range(3).fold(operator.add)
        3
        """
        return self.fold(f, initial=initial, star=True, **kwargs)

    # -----

    def product(self):
        return iTuple(itertools.product(*self))

    def product_with(self, *iters):
        return iTuple(itertools.product(self, *iters))

    # combinatorics

    # -----

iUnionV = typing.Union[iLazy[V], iTuple[V]]
iUnionT = typing.Union[iLazy[T], iTuple[T]]

ituple = iTuple

# ---------------------------------------------------------------

def pipe(f, obj, *args, at = None, discard=False, **kwargs):
    if at is None:
        res = f(obj, *args, **kwargs)
    elif isinstance(at, int):
        res = f(*args[:at], obj, *args[at:], **kwargs)
    elif isinstance(at, str):
        res = f(*args, **{at: obj}, **kwargs)
    else:
        assert False, at
    if not discard:
        return res
    return obj

# ---------------------------------------------------------------

if TYPE_CHECKING:
    it: iTuple[int] = iTuple.range(3)

    f: typing.Callable[[int], int] = lambda v: v * 2
    it = it.map(f)

    filt = lambda v: v < 3
    it = it.filter(filt)

    z = iTuple.range(3).zip(range(3))
    # z.map(f) # should fail

    it_n: iTuple[tuple[int, int, int]] = (
        iTuple.range(3)
        .zip(range(3))
        .zip(range(3), star=True)
    )
    it_n_: iTuple[tuple[tuple[int, int], int]] = (
        iTuple.range(3)
        .zip(range(3))
        .zip(range(3))
    )
    
    # i_rng_0: typing.Iterable[str] # should error
    i_rng_0: typing.Iterable[int]
    i_rng_1: typing.Iterable[int]

    i_rngs = iTuple.range(3).zip(range(3)).zip()
    i_rng_0, i_rng_1 = i_rngs

# ---------------------------------------------------------------
