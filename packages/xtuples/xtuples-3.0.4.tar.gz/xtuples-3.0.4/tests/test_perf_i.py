
from . import utils

import xtuples as xt

# ---------------------------------------------------------------

def create_range_it(l):
    def f():
        return xt.iTuple.range(l)
    f.__name__ = utils.outer_func_name()
    return f

def create_range_list(l):
    def f():
        return list(range(l))
    f.__name__ = utils.outer_func_name()
    return f

# ---------------------------------------------------------------

def test_creation():
    utils.compare(
        create_range_list(10 ** 3),
        create_range_it(10 ** 3),
        fastest=1,
        f_compare=utils.within_multiple(2, fastest=1)
    )
    utils.compare(
        create_range_list(10 ** 4),
        create_range_it(10 ** 4),
        fastest=1,
        f_compare=utils.within_multiple(2, fastest=1)
    )
    utils.compare(
        create_range_list(10 ** 5),
        create_range_it(10 ** 5),
        fastest=1,
        f_compare=utils.within_multiple(2, fastest=1),
        iters=10e3
    )
    utils.compare(
        create_range_list(10 ** 6),
        create_range_it(10 ** 6),
        fastest=1,
        f_compare=utils.within_multiple(2, fastest=1),
        iters=10e2
    )
    
# ---------------------------------------------------------------
