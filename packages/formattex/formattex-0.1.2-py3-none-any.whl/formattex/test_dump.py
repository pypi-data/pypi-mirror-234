import shutil
from pathlib import Path

import pytest

from .intermediate_repr import create_internal_repr_texfile


def _unidiff_output(expected, actual):
    """
    Returns a string containing the unified diff of two multiline strings.

    Taken from https://stackoverflow.com/a/845432
    """
    import difflib

    expected = expected.splitlines(keepends=True)
    actual = actual.splitlines(keepends=True)
    diff = difflib.unified_diff(expected, actual)
    return "".join(diff)


path_package = Path(__file__).absolute().parent
path_cases_test = path_package.parent.parent / "cases_test"
path_invariant = path_cases_test / "invariant"

print(path_cases_test)

cases_invariant = sorted(path_invariant.glob("case*.tex"))
cases_transform = sorted(path_cases_test.glob("input*.tex"))

for path_input in cases_transform:
    path_output = path_input.with_name("output" + path_input.name[len("input") :])
    if not path_output.exists():
        shutil.copyfile(path_input, path_output)


@pytest.mark.parametrize("index_case", range(len(cases_invariant)))
def test_dump_invariant(index_case):
    path_input = path_invariant / f"case{index_case}.tex"
    if index_case in (2, 7):
        pytest.xfail("Bugs texsoup!")

    repr = create_internal_repr_texfile(path_input, verbose=3)
    code_should_be = repr.full_code
    code_out = repr.dump()

    if code_out != code_should_be:
        with open("tmp_input.tex", "w") as file:
            file.write(code_should_be)

        with open("tmp_dumped.tex", "w") as file:
            file.write(code_out)

        raise RuntimeError(
            "Output is wrong:\n" + _unidiff_output(code_should_be, code_out)
        )


@pytest.mark.parametrize("index_case", range(len(cases_transform)))
def test_format(index_case):
    if index_case in (11,):
        pytest.xfail("Not implemented!")

    path_input = path_cases_test / f"input{index_case}.tex"
    path_should_be = path_cases_test / f"output{index_case}.tex"

    repr = create_internal_repr_texfile(path_input, verbose=3)
    code_out = repr.get_formatted()

    with open(path_should_be, "r") as file:
        code_should_be = file.read()

    if code_out != code_should_be:
        with open(f"tmp_dumped{index_case}.tex", "w") as file:
            file.write(code_out)

        raise RuntimeError(
            "Output is wrong:\n" + _unidiff_output(code_should_be, code_out)
        )
