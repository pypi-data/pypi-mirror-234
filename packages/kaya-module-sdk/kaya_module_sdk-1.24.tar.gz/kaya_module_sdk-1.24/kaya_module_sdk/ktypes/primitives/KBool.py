

class KBool:

    def __init__(self, value: bool = False) -> None:
        self._data = bool(value)

    def __repr__(self) -> str:
        return str(self._data)

    def __str__(self) -> str:
        return str(self._data)

    def __bool__(self) -> bool:
        return self._data

    def __eq__(self, other) -> bool:
        if isinstance(other, BoolWrapper):
            return self._data == other._data
        elif isinstance(other, bool):
            return self._data == other
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def set_data(self, value) -> None:
        self._data = bool(value)

    def get_data(self) -> bool:
        return self._data

    def toggle(self) -> None:
        self._data = not self._data

