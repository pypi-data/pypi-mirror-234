import pytest
from storedict import create_store

DATASTORE_PROXY_URL = "http://localhost:8200"


@pytest.fixture(params=[None, DATASTORE_PROXY_URL])
def store(request):
    """
    Test both LocalStore() and ProductionStore().
    """
    return create_store(request.param)


@pytest.fixture
def only_prod_store():
    """
    Transactions don't work on LocalStore() so this fixture is used to test only
    ProductionStore().
    """
    return create_store(DATASTORE_PROXY_URL)


@pytest.fixture(autouse=True)
def clear_store(store):
    """
    Clear the store before and after each test.
    """
    store.clear()
    yield
    store.clear()


def test_getitem(store):
    with pytest.raises(KeyError):
        store["foo"]

    store["foo"] = "bar"
    assert store["foo"] == "bar"


def test_setitem(store):
    store["foo"] = "bar"
    assert store["foo"] == "bar"


def test_delitem(store):
    with pytest.raises(KeyError):
        del store["foo"]

    store["foo"] = "bar"
    del store["foo"]
    with pytest.raises(KeyError):
        store["foo"]


def test_iter(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(iter(store)) == ["foo", "baz"]


def test_len(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert len(store) == 2


def test_contains(store):
    assert "foo" not in store
    store["foo"] = "bar"
    assert "foo" in store
    del store["foo"]
    assert "foo" not in store


def test_get(store):
    assert store.get("foo") is None
    assert store.get("foo", "bar") == "bar"

    store["foo"] = "bar"
    assert store.get("foo") == "bar"
    assert store.get("foo", "baz") == "bar"


def test_items(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.items()) == [("foo", "bar"), ("baz", "qux")]


def test_keys(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.keys()) == ["foo", "baz"]


def test_values(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    assert list(store.values()) == ["bar", "qux"]


def test_clear(store):
    store["foo"] = "bar"
    store["baz"] = "qux"
    store.clear()
    assert len(store) == 0
    assert list(store.items()) == []


def test_validate_key(store):
    """Keys must always be strings"""
    with pytest.raises(TypeError):
        store[1]  # __getitem__
    with pytest.raises(TypeError):
        store[1] = 2  # __setitem__
    with pytest.raises(TypeError):
        del store[1]  # __delitem__
    with pytest.raises(TypeError):
        1 in store  # __contains__
    with pytest.raises(TypeError):
        store.get(1)  # get


def test_validate_value(store):
    # Allowed types
    store["foo"] = "bar"
    store["foo"] = 1
    store["foo"] = 1.1
    store["foo"] = False
    store["foo"] = {"bar": 1}
    store["foo"] = [1, 2, 3]

    with pytest.raises(TypeError):
        store["foo"] = (1, 2, 3)
    with pytest.raises(TypeError):
        store["foo"] = {"bar": (1, 2, 3)}

    # Dict key must be a string
    with pytest.raises(TypeError):
        store["foo"] = {1: 2}
    with pytest.raises(TypeError):
        store["foo"] = {"bar": {1: 2}}


def test_nested_transaction(only_prod_store):
    store = only_prod_store
    with pytest.raises(RuntimeError, match="Nested transactions are not supported."):
        with store.transaction(lock=True):
            with store.transaction(lock=True):
                pass


def test_transaction_commit(only_prod_store):
    store = only_prod_store

    store["name"] = "tom"
    store["surname"] = "sawyer"

    assert store["name"] == "tom"
    assert store["surname"] == "sawyer"

    with store.transaction(lock=True):
        store["name"] = "huck"
        store["surname"] = "finn"

    assert store["name"] == "huck"
    assert store["surname"] == "finn"


def test_transaction_rollback(only_prod_store):
    store = only_prod_store

    store["name"] = "tom"
    store["surname"] = "sawyer"

    assert store["name"] == "tom"
    assert store["surname"] == "sawyer"

    with pytest.raises(RuntimeError):  # using this to continue the test
        with store.transaction(lock=True):
            store["name"] = "huck"
            raise RuntimeError
            store["surname"] = "finn"

    assert store["name"] == "tom"  # rolled back from huck to tom
    assert store["surname"] == "sawyer"


def test_iadd(store):
    """
    Out of allowed types (string, int, bool, dict, list), only dict does not
    support __iadd__. So, we can do the following:

    store["foo"] = 1
    store["foo"] += 2

    store["foo"] = "one"
    store["foo"] += "two"

    store["foo"] = True
    store["foo"] += False

    store["foo"] = [1, 2, 3]
    store["foo"] += [4, 5, 6]

    But we cannot do this:

    store["foo"] = {"bar": 1}
    store["foo"] += {"baz": 2}
    """

    store["foo"] = 1

    # This is what happens:
    # __getitem__ gets called with key "foo" and returns 1
    # __setitem__ gets called with key "foo" and value 3 (1 + 2)
    # So, in production, this will make two requests to the database
    # but will work as expected.
    store["foo"] += 2

    assert store["foo"] == 3
