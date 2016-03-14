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


def test_numvals():
    i = _incoming(
        [
            "SET a 10",
            "SET b 10",
            "NUMEQUALTO 10",
            "NUMEQUALTO 20",
            "SET b 30",
            "NUMEQUALTO 10",
            "END",
        ]
    )

    expected = """

2
0

1
"""
    s = io.StringIO()
    rettuce._main(i, s)

    assert expected == s.getvalue()
