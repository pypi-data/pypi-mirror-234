

class KDict:

    def __init__(self, initial_data: dict = None) -> None:
        if initial_data is None:
            initial_data = {}
        if not isinstance(initial_data, dict):
            raise TypeError("Initial value must be a dictionary.")
        self._data = dict(initial_data)

    def __repr__(self) -> str:
#       return f"KDict(value={self._data})"
        return str(self._data).replace(' ', '')

    def __str__(self) -> str:
        return str(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

    def __delitem__(self, key) -> None:
        del self._data[key]

    def __contains__(self, key) -> bool:
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def get(self, key, default=None):
        return self._data.get(key, default)

    def clear(self) -> None:
        self._data.clear()

    def copy(self):
        return KDict(self._data)

    def update(self, other_data):
        self._data.update(other_data)

    def setdefault(self, key, default=None):
        return self._data.setdefault(key, default)

    def pop(self, key, default=None):
        return self._data.pop(key, default)

    def popitem(self):
        return self._data.popitem()


