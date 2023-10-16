from dataclasses import dataclass


@dataclass
class KString(str):

    _data: str = ''

    def __init__(self, data: str) -> None:
        self._data = str(data)

    def __repr__(self) -> str:
#       return f"KString(value={self._data})"
        return str(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __lt__(self, other):
        return len(self._data) < len(other._data)

    def __gt__(self, other):
        return len(self._data) > len(other._data)

    def __le__(self, other):
        return len(self._data) <= len(other._data)

    def __ge__(self, other):
        return len(self._data) >= len(other._data)

    def __eq__(self, other):
        return len(self._data) == len(other._data)

