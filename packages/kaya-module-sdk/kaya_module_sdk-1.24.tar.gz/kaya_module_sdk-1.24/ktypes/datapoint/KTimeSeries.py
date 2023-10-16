import pandas as pd

from typing import TypeVar, Generic
from dataclasses import dataclass

from kaya_module_sdk.ktypes.primitives.KBool import KBool
from kaya_module_sdk.ktypes.primitives.KInt import KInt
from kaya_module_sdk.ktypes.primitives.KFloat import KFloat
from kaya_module_sdk.ktypes.primitives.KString import KString
from kaya_module_sdk.ktypes.series.KList import KList

T = TypeVar('T', int, str, bool, float, KBool, KInt, KFloat, KString)


@dataclass
class KTimeSeries(Generic[T]):
    '''
    [ DESCRIPTION ]: Wrapper over pandas.DataFrame that supports four different
        types of indices: integers, floats, booleans and strings. The
        implementation also includes type hints for clarity.

    [ NOTE ]: This implementation makes use of the generic type T to specify
        that the indices of the TimeSeries can be either int or str.

        The __init__ method takes in a dictionary with keys of type T and values
        of type KFloat, which is then used to create a pandas.Series object.

        The __getitem__ and __setitem__ methods allow for getting and setting
        values using the TimeSeries object's keys, while the __repr__, __len__,
        keys, values, and items methods provide some additional convenience
        methods for working with the TimeSeries object.
    '''

    def __init__(self, data: list[T, float]):
        self._data = pd.Series(data)

    def __getitem__(self, key: T) -> KFloat:
        value = [item for item in self._data if item[0] == key]
        return False if not values else value[0]

    def __setitem__(self, key: T, value: KFloat) -> None:
        self._data[key] = value

    def __repr__(self) -> str:
        builder = '['
        for tuple_item in self._data:
            item = f'[{tuple_item[0]},{tuple_item[1]}];'
            builder += item
        builder = builder.rstrip(';')
        builder += ']'
        return builder

    def __len__(self) -> int:
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    @classmethod
    def is_list_of_tuples_with_two_elements(cls, data) -> bool:
        if not isinstance(data, list):
            return False
        for item in data:
            if not isinstance(item, tuple) or len(item) != 2:
                return False
        return True

