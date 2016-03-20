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

NULL
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
    assert db.get("a") is rettuce.NIL


def test_set():
    db = rettuce.DBState()
    db.set("a", 1)
    assert db.get("a") == 1


def test_in_transaction():
    db = rettuce.DBState()
    db.begin_transaction()
    db.set("a", 1)
    a = db.get("a")
    assert a == 1


def test_rollback():
    db = rettuce.DBState()
    db.set("a", 1)
    db.begin_transaction()
    db.set("a", 2)
    during = db.get("a")
    db.rollback_transaction()
    after = db.get("a")
    assert during == 2
    assert after == 1


def test_rollback2():
    db = rettuce.DBState()
    # |
    db.set("a", 1)
    first = db.get("a")

    db.begin_transaction()
    # | |
    db.set("a", 2)
    second = db.get("a")

    db.begin_transaction()
    # | | |
    db.set("a", 3)
    third = db.get("a")

    db.rollback_transaction()
    # | |
    rolled_second = db.get("a")

    db.rollback_transaction()
    # |
    rolled_first = db.get("a")

    assert first == 1
    assert second == 2
    assert third == 3
    assert rolled_second == 2
    assert rolled_first == 1


def test_commit():
    db = rettuce.DBState()
    db.set("a", 1)
    db.begin_transaction()
    db.set("a", 2)
    during = db.get("a")
    db.commit_transaction()
    after = db.get("a")
    assert during == 2
    assert after == 2


def test_rolled_not_set():
    db = rettuce.DBState()
    first = db.get("a")
    db.begin_transaction()
    db.set("a", 1)
    second = db.get("a")
    db.rollback_transaction()
    after = db.get("a")
    assert first is rettuce.NIL
    assert second == 1
    assert after is rettuce.NIL
