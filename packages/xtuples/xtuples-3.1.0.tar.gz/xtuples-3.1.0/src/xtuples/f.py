
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsDunderLT, SupportsDunderGT

# ---------------------------------------------------------------

import abc
import typing
import dataclasses
import collections

import operator
import itertools
import functools

from .i import iTuple, T, CT

# TODO: these are for use in .map() etc.
# so should return a func that accepts the relevant value, where it takes args / kwargs
# if no args / kwargs, not necessary

# ---------------------------------------------------------------

def empty(cls=iTuple) -> iTuple:
    return cls.empty()

def one(v, cls=iTuple) -> iTuple:
    return cls.one(v)

def none(n, cls = iTuple):
    return cls.none(n)

def from_keys(d, cls = iTuple):
    return cls.from_keys(d)
    
def from_values(d, cls = iTuple):
    return cls.from_values(d)
    
def from_items(d, cls = iTuple):
    return cls.from_items(d)

def from_index(s, cls = iTuple):
    return cls.from_index(s)

def from_index_values(s, cls = iTuple):
    return cls.from_index_values(s)

def from_columns(s, cls = iTuple):
    return cls.from_columns(s)

def n_from(gen, n, cls = iTuple):
    return cls.n_from(gen, n)

def from_while(
    gen, 
    f, 
    n = None, 
    star = False,
    iters=None,
    value=True,
    cls=iTuple,
):
    return cls.from_while(
        gen,
        f,
        n=n,
        star=star,
        iters=iters,
        value=value,
    )

def from_where(
    gen, 
    f, 
    n = None, 
    star = False,
    iters=None,
    value=True,
    cls=iTuple,
):
    return cls.from_where(
        gen,
        f,
        n=n,
        star=star,
        iters=iters,
        value=value,
    )

# -----

def partial(f, *args, **kwargs):
    def res(self, **kws):
        return self.partial(f, *args, **kwargs, **kws)
    return res

# -----

def index_of(v):
    def res(self):
        return self.index_of(v)
    return res

def len_range(self):
    return self.len_range()

def append(value, *values):
    def res(self):
        return self.append(value, *values)
    return res

def prepend(value, *values):
    def res(self):
        return self.prepend(value, *values)
    return res

def zip(*itrs, lazy = False, at = None):
    def res(self):
        return self.zip(*itrs, lazy=lazy, at=at)
    return res

def flatten(self):
    return self.flatten()

def extend(value, *values):
    def res(self):
        return self.extend(value, *values)
    return res

def pretend(value, *values):
    def res(self):
        return self.pretend(value, *values)
    return res

def any(f = None, star = False):
    def res(self):
        return self.any(f=f, star=star)
    return res

def anystar(f):
    def res(self):
        return self.anystar(f)
    return res

def all(f = None, star = False):
    def res(self):
        return self.all(f=f, star=star)
    return res

def allstar(f):
    def res(self):
        return self.allstar(f)
    return res

def assert_all(f, f_error = None):
    def res(self):
        return self.assert_all(f, f_error=f_error)
    return res

def assert_any(f, f_error = None):
    def res(self):
        return self.assert_any(f, f_error=f_error)
    return res

def filter_eq(v, f = None, eq = None, lazy = False):
    def res(self):
        return self.filter_eq(v, f=f, eq=eq, lazy=lazy)
    return res

def filter(f, eq = None, lazy = False, **kws):
    def res(self):
        return self.filter(f, eq=eq, lazy=lazy, **kws)
    return res

def filterstar(f, eq = None, lazy = False, **kws):
    def res(self):
        return self.filterstar(f, eq=eq, lazy=lazy, **kws)
    return res

def is_none(self):
    return self.is_none()

def not_none(self):
    return self.not_none()

def i_min(key = None):
    def res(self):
        return self.i_min(key=key)
    return res

def i_max(key = None):
    def res(self):
        return self.i_max(key=key)
    return res

def map(
    f,
    *iterables,
    lazy = False,
    star=False,
    **kwargs,
):
    def res(self):
        return self.map(
            f, 
            *iterables, 
            lazy=lazy,
            star=star, 
            **kwargs
        )
    return res

# TODO: args, kwargs
def mapstar(f):
    def res(self):
        return self.mapstar(f)
    return res

def enumerate(self):
    return self.enumerate()

def chunkby(
    f, 
    lazy = False, 
    keys = False,
    pipe= None,
):
    def res(self):
        return self.chunkby(f, lazy=lazy, keys=keys, pipe=pipe)
    return res

def groupby(
    f, lazy = False, keys = False, pipe = None
):
    def res(self):
        return self.groupby(f, lazy=lazy, keys=keys, pipe=pipe)
    return res

def first(self):
    return self.first()

def last(self):
    return self.last()

def insert(i, v):
    def res(self):
        return self.insert(i, v)
    return res

def instend(i, v):
    def res(self):
        return self.instend(i, v)
    return res

def pop_first(self):
    return self.pop_first()

def pop_last(self):
    return self.pop_last()

def pop(self, i):
    return self.pop(i)

def first_where(f, default = None, star = False):
    def res(self):
        return self.first_where(f, default=default, star=star)
    return res

def last_where(f, default = None, star = False):
    def res(self):
        return self.last_where(f, default=default, star=star)
    return res

def clear(self):
    return self.clear()

def take(n):
    def res(self):
        return self.take(n)
    return res

def tail(n):
    def res(self):
        return self.tail(n)
    return res

def reverse(lazy = False):
    def res(self):
        return self.reverse(lazy=lazy)
    return res

def take_while(f, n = None, lazy = False):
    def res(self):
        return self.take_while(f, n=n, lazy=lazy)
    return res

def tail_while(f, n = None):
    def res(self):
        return self.tail_while(f, n=n)
    return res

# NOTE: from as in, starting from first true
# versus above, which is until first false
def take_after(f, n = None, lazy = False):
    def res(self):
        return self.take_after(f, n=n, lazy=lazy)
    return res

def tail_after(f, n = None):
    def res(self):
        return self.tail_after(f, n=n)
    return res

def islice(left = None, right = None):
    def res(self):
        return self.islice(left=left, right=right)
    return res

def unique(self):
    return self.unique()

def argsort(f = lambda v: v, star = False, reverse = False):
    def res(self):
        return self.argsort(f=f, star=star, reverse=reverse)
    return res

def sort(f = lambda v: v, reverse = False, star = False):
    def res(self):
        return self.sort(f=f, reverse=reverse, star=star)
    return res

# TODO: sortby etc.

def sortstar(f = lambda v: v, reverse = False):
    def res(self):
        return self.sortstar(f=f, reverse=reverse)
    return res

# NOTE: ie. for sorting back after some other transformation
def sort_with_indices(
    f = lambda v: v, reverse=False
):
    def res(self):
        return self.sort_with_indices(f=f, reverse=reverse)
    return res

def sortstar_with_indices(
    f = lambda v: v, reverse=False
):
    def res(self):
        return self.sortstar_with_indices(f=f, reverse=reverse)
    return res

def accumulate(f, initial = None, lazy = False):
    def res(self):
        return self.accumulate(f, initial=initial, lazy=lazy)
    return res

def foldcum(*args, initial=None, **kwargs):
    def res(self):
        return self.foldcum(*args, initial=initial, **kwargs)
    return res

def fold(f, initial=None):
    def res(self):
        return self.fold(f,initial =initial )
    return res

def foldstar(f, initial=None):
    def res(self):
        return self.foldstar(f,initial =initial )
    return res

# -----

def product(self):
    return self.product()

def product_with(*iters):
    def res(self):
        return self.product_with(*iters)
    return res

# TODO: other combinatorics

# TODO: auto gen the tests by inspecting methods on ituple?
# to ensure all have de-bound versions

# ---------------------------------------------------------------
