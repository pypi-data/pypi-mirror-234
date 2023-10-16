from typing import TypeVar, Generic, List as TypingList
from dataclasses import dataclass

from kaya_module_sdk.ktypes.primitives.KBool import KBool
from kaya_module_sdk.ktypes.primitives.KInt import KInt
from kaya_module_sdk.ktypes.primitives.KFloat import KFloat
from kaya_module_sdk.ktypes.primitives.KString import KString

T = TypeVar('T', int, str, bool, float)


@dataclass
class KList(Generic[T]):
    '''
    [ DESCRIPTION ]: Wrapper over a regular Python list and supports elements of
        five different types: integers, strings, booleans, floats and TimeSeries.
        It also uses a generic type T to allow for different types of elements.

    [ NOTE ]: This implementation uses a generic type T that can be any of the
        four types plus the TimeSeries class. The __init__ method takes in a
        regular Python list with elements of type T, which is then used to create
        the List object.

        The __getitem__ and __setitem__ methods allow for getting and setting
        values using the List object's indices, while the __repr__, __len__,
        append, extend, insert, remove, pop, index, and count methods provide
        some additional convenience methods for working with the List object.
    '''

    _data = []

    def __init__(self, data: TypingList[T]) -> None:
        if not isinstance(data, list):
            raise TypeError(f"Argument must be a list, not {type(data).__name__}")
        self._data = data

    def __str__(self) -> None:
        return str(self._data)

    def __getitem__(self, index: int) -> T:
        return self._data[index]

    def __setitem__(self, index: int, value: T) -> None:
        if not isinstance(value, (int, str, bool, float)):
            raise TypeError(
                "List elements must be of type KInt, KFloat, KString or KBool "
                f"not {type(value).__name__}"
            )
        self._data[index] = value

    def __repr__(self) -> str:
        return str(self._data).replace(' ', '')

    def __len__(self) -> int:
        return len(self._data)

    def append(self, value: T) -> None:
        self._data.append(value)
        if not isinstance(value, (int, str, bool, float, KTimeSeries)):
            raise TypeError(
                f"List elements must be of type int, str, bool, float, or "
                "KTimeSeries, not {type(value).__name__}"
            )

    def extend(self, values: list[T]) -> None:
        for value in values:
            if not isinstance(value, (int, str, bool, float, KTimeSeries)):
                raise TypeError(
                    f"List elements must be of type int, str, bool, float, or "
                    "KTimeSeries, not {type(value).__name__}"
                )
        self._data.extend(values)

    def insert(self, index: int, value: T) -> None:
        if not isinstance(value, (int, str, bool, float, KTimeSeries)):
            raise TypeError(
                f"List elements must be of type int, str, bool, float, or "
                "KTimeSeries, not {type(value).__name__}"
            )
        self._data.insert(index, value)

    def remove(self, value: T) -> None:
        self._data.remove(value)

    def pop(self, index: int = -1) -> T:
        return self._data.pop(index)

    def index(self, value: T, start: int = 0, end: int = -1) -> int:
        return self._data.index(value, start, end)

    def count(self, value: T) -> int:
        return self._data.count(value)

# CODE DUMP

#       for value in data:
#           if not isinstance(value, (
#                   int, float, bool, str, list, dict, tuple, set,
#                   KList, KInt, KString, KBool, KFloat, KDict, KSet, KTuple, KTimeSeries
#               )):
#               raise TypeError(
#                   f"Argument must contain elements of type KInt, KString, KBool, "
#                   "KFloat, or KTimeSeries, not {type(value).__name__}"
#               )

