
from resumer.utils import extract_vars


def test_utils_extract_vars():

    res = extract_vars("a == b")

    assert res == ["a", "b"]

    res = extract_vars("a == 1 and b == 2")

    assert res == ["a", "b"]

    res = extract_vars("'x' in s")

    assert res == ["s"]

    res = extract_vars("a == 1 or b == 2")

    assert res == ["a", "b"]

    res = extract_vars("a == b and c in d")

    assert res == ["a", "b", "c", "d"]