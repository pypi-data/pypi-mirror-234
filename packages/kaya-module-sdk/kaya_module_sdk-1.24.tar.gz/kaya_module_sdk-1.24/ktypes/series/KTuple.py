

class KTuple:

    def __init__(self, elements) -> None:
        self._data = elements if isinstance(elements, tuple) \
            else tuple(elements)

    def __repr__(self) -> str:
#       return f"KTuple(value={self._data})"
        return str(self._data).replace(' ', '')

    def __str__(self) -> str:
        return str(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def index(self, element, start=0, end=None):
        return self._data.index(element, start, end)

    def count(self, element):
        return self._data.count(element)

    def as_list(self) -> list:
        return list(self._data)

    def update(self, *elements) -> None:
        self._data = tuple(elements)

    def append(self, element) -> None:
        self._data += (element,)

    def extend(self, iterable) -> None:
        self._data += tuple(iterable)

    def remove(self, element) -> None:
        index = self.index(element)
        self._data = self._data[:index] + self._data[index + 1:]

    def pop(self, index=-1) -> None:
        self._data = self._data[:index] + self._data[index + 1:]
