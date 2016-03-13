import rettuce
import io


def _incoming(lines):
    return (i for i in lines)


def test_d():
    i = _incoming(
        [
            "SET ex 10",
            "GET ex",
            "UNSET ex",
            "GET ex",
            "END",
        ]
    )

    expected = """
10

nil
"""
    s = io.StringIO()
    rettuce._main(i, s)

    assert expected == s.getvalue()
