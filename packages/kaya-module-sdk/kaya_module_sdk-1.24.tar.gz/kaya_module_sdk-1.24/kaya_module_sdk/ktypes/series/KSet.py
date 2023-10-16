

class KSet:

    def __init__(self, initial_data: set = None) -> None:
        if initial_data is None:
            initial_data = set()
        if not isinstance(initial_data, set):
            raise TypeError("Initial value must be a set.")
        self._data = set(initial_data)

    def __repr__(self) -> str:
#       return f"KSet(value={self._data})"
        return str(self._data).replace(' ', '')

    def __str__(self) -> str:
        return str(self._data)

    def __contains__(self, item) -> bool:
        return item in self._data

    def add(self, item) -> None:
        self._data.add(item)

    def discard(self, item) -> None:
        self._data.discard(item)

    def pop(self):
        return self._data.pop()

    def clear(self) -> None:
        self._data.clear()

    def copy(self):
        return KSet(self._data)

    def union(self, other_data):
        return KSet(self._data.union(other_data))

    def intersection(self, other_data):
        return KSet(self._data.intersection(other_data))

    def difference(self, other_data):
        return KSet(self._data.difference(other_data))

    def issubset(self, other_data) -> bool:
        return self._data.issubset(other_data)

    def issuperset(self, other_data) -> bool:
        return self._data.issuperset(other_data)

    def symmetric_difference(self, other_data):
        return KSet(self._data.symmetric_difference(other_data))

    def update(self, other_data) -> None:
        self._data.update(other_data)

    def remove(self, item) -> None:
        self._data.remove(item)

    def pop(self):
        return self._data.pop()

