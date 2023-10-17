
import sys
import doctest

import xtuples as xt

from . import utils

# ---------------------------------------------------------------

def unpack_doctests(module = xt):
    return xt.iTuple(doctest.DocTestFinder().find(module))

def unpack_docstrings(module) -> xt.iTuple[str]:
    return unpack_doctests(module).map(
        lambda dt: dt.__dict__["docstring"]
    )

def parse_docstring(s: str) -> str:
    lines: xt.iTuple[str] = xt.iTuple(s.split("\n"))
    return "\t" + "\n\t".join(
        lines.map(lambda ss: ss.strip())
        .filter(
            lambda ss: ss.startswith(">>>") or ss.startswith("...")
        )
        .map(lambda ss: ss[4:])
    )

def gen_example(i: int, s: str):
    return '''
def example_{}():
{}
'''.format(
    i, s
)

def gen_examples(mod):
    return (
        unpack_docstrings(mod)
        .map(parse_docstring)
        .filter(lambda s: len(s.strip()) > 0)
        .enumerate()
        .mapstar(gen_example)
    )

# ---------------------------------------------------------------

boilerplate = """

import operator
from xtuples.n import _Example

"""

def test_i():
    utils.run_mypy(
        "\n\n".join(gen_examples(xt.i)),
        extra = boilerplate
    )

def test_n():
    utils.run_mypy(
        "\n\n".join(gen_examples(xt.n)),
        extra = boilerplate
    )

def test_f():
    utils.run_mypy(
        "\n\n".join(gen_examples(xt.f)),
        extra = boilerplate
    )

# ---------------------------------------------------------------
