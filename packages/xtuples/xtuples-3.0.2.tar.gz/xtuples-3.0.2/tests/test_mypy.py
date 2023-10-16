import typing

import os
import tempfile
import subprocess

import pathlib
XTUPLES = str(pathlib.Path("./src").resolve()).replace("\\", "/")

# ---------------------------------------------------------------

SUCCESS = "Success: "
FAILURE = "error: "

def add_boilerplate(s):
    return """

import os
import sys
sys.path.append("{}")

import typing

from xtuples import iTuple, nTuple, iLazy

import xtuples as xt

""".format(XTUPLES) + s

def run_mypy(s: str, asserting = None):
    try:
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(bytes(add_boilerplate(s), "utf-8"))
        f.close()
        res = subprocess.run(
            [
                "python",
                "-m",
                "mypy",
                f.name,
                "--check-untyped-defs",
                "--soft-error-limit=-1",
            ],
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            text = True,
            env=dict(os.environ, MYPYPATH=XTUPLES)
        ).stdout
    finally:
        os.remove(f.name)

    try:
        if asserting is None:
            assert SUCCESS in res

        elif isinstance(asserting, str):
            assert asserting in res

        else:
            assert asserting(res)

    except Exception as e:

        print(s)
        print(res)

        raise e

    return True
    
# ---------------------------------------------------------------

f_zip = lambda rng_0_type, rng_1_type, v: """
i_rng_0: {}
i_rng_1: {}
i_rng_0, i_rng_1 = {}
""".format(rng_0_type, rng_1_type, v)

def test_zip():
    z = "iTuple.range(3).zip(range(3)).zip()"
    run_mypy(f_zip(
        "typing.Iterable[int]",
        "typing.Iterable[int]",
        z
    ))
    run_mypy(f_zip(
        "typing.Iterable[str]",
        "typing.Iterable[int]",
        z
    ), asserting=FAILURE)
    run_mypy(f_zip(
        "int",
        "typing.Iterable[int]",
        z
    ), asserting=FAILURE)

# ---------------------------------------------------------------

f_map = lambda res_type: """
f: typing.Callable[..., int] = lambda v: v * 2
res: {} = iTuple.range(3).map(f, lazy=False)
""".format(res_type)

f_map_lazy = lambda res_type: """
f: typing.Callable[..., int] = lambda v: v * 2
res: {} = iTuple.range(3).map(f, lazy = True)
""".format(res_type)

f_map_n = lambda f_type, f, res_type, it: """
f: {} = {}
v = {}
res: {} = v.map(f)
""".format(f_type, f, it, res_type)

f_map_n_star = lambda f_type, f, res_type, it: """
f: {} = {}
v = {}
res: {} = v.map(f, star=True)
""".format(f_type, f, it, res_type)

def test_map():
    run_mypy(f_map("iTuple[int]"))
    run_mypy(f_map("int"), asserting=FAILURE)
    run_mypy(f_map("iTuple[str]"), asserting=FAILURE)

    run_mypy(f_map_lazy("iLazy[int]"))
    run_mypy(f_map_lazy("int"), asserting=FAILURE)
    run_mypy(f_map_lazy("iTuple[int]"), asserting=FAILURE)

    run_mypy(
        f_map_n(
            "typing.Callable[[int], int]",
            "lambda v: v * 2",
            "iTuple[int]",
            "iTuple.range(3).zip(range(3))"
        ),
        asserting=FAILURE
    )
    run_mypy(
        f_map_n_star(
            "typing.Callable[[int], int]",
            "lambda v0, v1: v0 * 2",
            "iTuple[int]",
            "iTuple.range(3).zip(range(3))"
        ),
        asserting=FAILURE
    )
    run_mypy(
        f_map_n(
            "typing.Callable[[int, int], int]",
            "lambda v0, v1: v0 * 2",
            "iTuple[int]",
            "iTuple.range(3).zip(range(3))"
        ),
        asserting=FAILURE
    )
    run_mypy(
        f_map_n_star(
            "typing.Callable[..., int]",
            "lambda v0, v1: v0 * 2",
            "iTuple[int]",
            "iTuple.range(3).zip(range(3))"
        )
    )

f_filter = lambda res_type: """
it: iTuple[int] = iTuple.range(3)
filt = lambda v: v < 3
res: {} = it.filter(filt, lazy=False)
""".format(res_type)

f_filter_lazy = lambda res_type: """
it: iTuple[int] = iTuple.range(3)
filt = lambda v: v < 3
res: {} = it.filter(filt, lazy = True)
""".format(res_type)

def test_filter():
    run_mypy(f_filter("iTuple[int]"))
    run_mypy(f_filter("int"), asserting=FAILURE)
    run_mypy(f_filter("iTuple[str]"), asserting=FAILURE)

    run_mypy(f_filter_lazy("iLazy[int]"))
    run_mypy(f_filter_lazy("int"), asserting=FAILURE)
    run_mypy(f_filter_lazy("iTuple[int]"), asserting=FAILURE)

f_fold = lambda res_type: """
it: iTuple[int] = iTuple.range(3)
acc = lambda v_acc, v: v_acc + v
i: {} = it.fold(acc, initial=0)
""".format(res_type)

f_fold_cum = lambda res_type: """
it: iTuple[int] = iTuple.range(3)
acc = lambda v_acc, v: v_acc + v
i: {} = it.foldcum(acc, initial=0)
""".format(res_type)

f_fold_star = lambda res_type: """
it = iTuple.range(3).zip(range(3))
acc = lambda v_acc, v, y: v_acc + v + y
i: {} = it.fold(acc, initial=0, star = True)
""".format(res_type)

f_fold_cum_star = lambda res_type: """
it = iTuple.range(3).zip(range(3))
acc = lambda v_acc, v, y: v_acc + v + y
i: {} = it.foldcum(acc, initial=0, star = True)
""".format(res_type)

f_fold_cum_star_lazy = lambda res_type: """
it = iTuple.range(3).zip(range(3))
acc = lambda v_acc, v, y: v_acc + v + y
i: {} = it.foldcum(acc, initial=0, star = True,lazy= True)
""".format(res_type)

def test_fold():
    run_mypy(f_fold("int"))
    run_mypy(f_fold("iTuple"), asserting=FAILURE)
    run_mypy(f_fold("str"), asserting=FAILURE)

    run_mypy(f_fold_star("int"))
    run_mypy(f_fold_star("iTuple"), asserting=FAILURE)
    run_mypy(f_fold_star("str"), asserting=FAILURE)

def test_fold_cum():
    run_mypy(
        f_fold_cum("iTuple[int]")
    )
    run_mypy(
        f_fold_cum("int"), asserting=FAILURE
    )
    run_mypy(
        f_fold_cum("iTuple[str]"), asserting=FAILURE
    )

    run_mypy(
        f_fold_cum_star("iTuple[int]")
    )
    run_mypy(
        f_fold_cum_star("int"), asserting=FAILURE
    )
    run_mypy(
        f_fold_cum_star("iTuple[str]"), asserting=FAILURE
    )

    run_mypy(
        f_fold_cum_star_lazy("iLazy[int]")
    )
    run_mypy(
        f_fold_cum_star_lazy("iTuple[int]"), asserting=FAILURE
    )

f_append = lambda v_type, v_val, res_type: """
it: iTuple[int] = iTuple.range(3)
v: {} = {}
res: {} = it.append(v)
""".format(v_type, v_val, res_type)

def test_append():
    run_mypy(
        f_append("int", 1, "iTuple[int]")
    )
    run_mypy(
        f_append("str", '"s"', "iTuple[int]"), asserting=FAILURE
    )
    run_mypy(
        f_append("str", '"s"', "iTuple[typing.Union[int, str]]")
    )

# ---------------------------------------------------------------
