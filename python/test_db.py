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


def test_transaction1():
    i = _incoming(
        [
            "BEGIN",
            "SET a 10",
            "GET a",
            "BEGIN",
            "SET a 20",
            "GET a",
            "ROLLBACK",
            "GET a",
            "ROLLBACK",
            "GET a",
            "END",
        ]
    )

    expected = """


10


20

10

NULL
"""
    s = io.StringIO()
    rettuce._main(i, s)

    assert expected == s.getvalue()


def test_empty_get():
    db = rettuce.DBState()
    assert db.get("a") is rettuce.DELETED


def test_set():
    db = rettuce.DBState()
    db.set("a", 1)
    assert db.get("a") == 1
