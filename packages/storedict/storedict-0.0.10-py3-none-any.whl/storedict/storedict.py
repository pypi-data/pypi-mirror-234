from collections.abc import MutableMapping
from typing import Optional

import requests


class ProxyError(Exception):
    pass


class BaseStore(MutableMapping):
    is_in_transaction = False

    def transaction(self, lock: bool = False):
        return self.Transaction(self, lock)

    class Transaction:
        def __init__(self, store, lock: bool):
            ...

        def __enter__(self):
            ...

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...

    def __getitem__(self, key):
        ...

    def __setitem__(self, key, value):
        ...

    def __delitem__(self, key):
        ...

    def __iter__(self):
        ...

    def __len__(self):
        ...

    def __contains__(self, key):
        ...

    def get(self, key, default=None):
        ...

    def items(self):
        ...

    def keys(self):
        ...

    def values(self):
        ...

    def clear(self):
        ...

    def validate_key(self, key):
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

    def validate_value(self, value):
        """
        Values must be strings, ints, floats, bools, dicts, or lists. Nested
        objects should follow the same rule. All dict keys must be strings.
        """
        if isinstance(value, (str, int, float, bool)):
            return
        elif isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, str):
                    raise TypeError("Dictionary keys must be strings")
                self.validate_value(v)
        elif isinstance(value, list):
            for item in value:
                self.validate_value(item)
        else:
            raise TypeError("Value must be a string, int, float, bool, dict, or list")


class LocalStore(BaseStore):
    def __init__(self):
        super().__init__()
        self._data = {}

    def __getitem__(self, key):
        self.validate_key(key)
        return self._data[key]

    def __setitem__(self, key, value):
        self.validate_key(key)
        self.validate_value(value)
        self._data[key] = value

    def __delitem__(self, key):
        self.validate_key(key)
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        self.validate_key(key)
        return key in self._data

    def get(self, key, default=None):
        self.validate_key(key)
        return self._data.get(key, default)

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def clear(self):
        self._data.clear()


class ProductionStore(BaseStore):
    def __init__(self, datastore_proxy_url: str):
        super().__init__()
        self.datastore_proxy_url = datastore_proxy_url
        self.urls = {
            "get-value": self.datastore_proxy_url + "/get-value",
            "set-value": self.datastore_proxy_url + "/set-value",
            "delete-key": self.datastore_proxy_url + "/delete-key",
            "key-exists": self.datastore_proxy_url + "/key-exists",
            "get-data": self.datastore_proxy_url + "/get-data",
            "get-data-size": self.datastore_proxy_url + "/get-data-size",
            "delete-data": self.datastore_proxy_url + "/delete-data",
            "begin-transaction": self.datastore_proxy_url + "/begin-transaction",
            "commit-transaction": self.datastore_proxy_url + "/commit-transaction",
            "rollback-transaction": self.datastore_proxy_url + "/rollback-transaction",
            "lock-table": self.datastore_proxy_url + "/lock-table",
        }

    def __getitem__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def __setitem__(self, key, value):
        self.validate_key(key)
        self.validate_value(value)
        r = requests.post(self.urls["set-value"], json={"key": key, "value": value})
        if r.status_code != 200:
            raise ProxyError()

    def __delitem__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["delete-key"], json={"key": key})
        if r.status_code == 404:
            raise KeyError()
        if r.status_code != 200:
            raise ProxyError()

    def __iter__(self):
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return iter(r.json())

    def __len__(self):
        r = requests.post(self.urls["get-data-size"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def __contains__(self, key):
        self.validate_key(key)
        r = requests.post(self.urls["key-exists"], json={"key": key})
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def get(self, key, default=None):
        self.validate_key(key)
        r = requests.post(self.urls["get-value"], json={"key": key})
        if r.status_code == 404:
            return default
        if r.status_code != 200:
            raise ProxyError()
        return r.json()

    def items(self):
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().items()

    def keys(self):
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().keys()

    def values(self):
        r = requests.post(self.urls["get-data"])
        if r.status_code != 200:
            raise ProxyError()
        return r.json().values()

    def clear(self):
        r = requests.post(self.urls["delete-data"])
        if r.status_code != 200:
            raise ProxyError()

    def _begin_transaction(self):
        r = requests.post(self.urls["begin-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _commit_transaction(self):
        r = requests.post(self.urls["commit-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _rollback_transaction(self):
        r = requests.post(self.urls["rollback-transaction"])
        if r.status_code != 200:
            raise ProxyError()

    def _lock_table(self):
        r = requests.post(self.urls["lock-table"])
        if r.status_code != 200:
            raise ProxyError()

    class Transaction:
        def __init__(self, store, lock: bool):
            if store.is_in_transaction:
                raise RuntimeError("Nested transactions are not supported.")
            self.store = store
            self.lock = lock

        def __enter__(self):
            self.store.is_in_transaction = True
            self.store._begin_transaction()
            if self.lock:
                self.store._lock_table()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.store._rollback_transaction()
            else:
                self.store._commit_transaction()

            self.store.is_in_transaction = False


def create_store(datastore_proxy_url: Optional[str] = None) -> BaseStore:
    if datastore_proxy_url is None:
        return LocalStore()
    else:
        return ProductionStore(datastore_proxy_url)
