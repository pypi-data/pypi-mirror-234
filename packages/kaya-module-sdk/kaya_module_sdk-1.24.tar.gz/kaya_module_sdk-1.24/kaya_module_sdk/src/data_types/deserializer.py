import ast
#import pysnooper

from kaya_module_sdk.ktypes.primitives.KBool import KBool
from kaya_module_sdk.ktypes.primitives.KInt import KInt
from kaya_module_sdk.ktypes.primitives.KFloat import KFloat
from kaya_module_sdk.ktypes.primitives.KString import KString
from kaya_module_sdk.ktypes.datapoint.KTimeSeries import KTimeSeries
from kaya_module_sdk.ktypes.series.KList import KList
from kaya_module_sdk.ktypes.series.KDict import KDict
from kaya_module_sdk.ktypes.series.KSet import KSet
from kaya_module_sdk.ktypes.series.KTuple import KTuple


def data_type_map() -> dict:
    p_map = {
        KInt: int,
        KFloat: float,
        KString: str,
        KBool: bool,
        KList: list,
        KSet: set,
        KTuple: tuple,
        KDict: dict,
    }
    return p_map

#@pysnooper.snoop()
def deserialize_time_series(data_str):
    '''
    [ NOTE ]: Deserialize special edge case data type from string
    [ INPUT ]: '[[item1,item2];[item3,item4]]'
    [ RETURN ]: [('item1', 'item2'), ('item3', 'item4')]
    '''
    list_of_strings = data_str.replace('[[', '[').replace(']]', ']').split(';')
    time_series_data_types, deserialized_data = [], [
        tuple(item.strip('[]').split(',')) for item in list_of_strings
    ]
    for tuple_item in deserialized_data:
        try:
            deserialized_timestamp = ast.literal_eval(tuple_item[0])
            deserialized_value = ast.literal_eval(tuple_item[1])
            time_series_data_types.append(
                (deserialized_timestamp, deserialized_value,)
            )
        except (SyntaxError, ValueError, IndexError):
            time_series_data_types.append(tuple_item)
    kaya_time_series_dt = KTimeSeries(time_series_data_types)
    return kaya_time_series_dt

#@pysnooper.snoop()
def deserialize_string(data_str, supported_types=None):
    try:
        deserialized_data = ast.literal_eval(data_str)
        if not supported_types:
            return deserialized_data
        inverse_supported_data_types = {v: k for k, v in supported_types.items()}
        current_type = type(deserialized_data)
        if current_type in inverse_supported_data_types:
            kaya_data_type = inverse_supported_data_types[current_type](
                deserialized_data
            )
            return kaya_data_type
        kstr = KString(data_str)
        return kstr
    except (SyntaxError, ValueError):
        return KString(data_str) if data_str[0:2] != '[[' \
            else deserialize_time_series(data_str)

#@pysnooper.snoop()
def deserializer(*args, **kwargs) -> (list, dict):
    '''
    [ NOTE ]: Deserializes given positional and keyword serialized string
    arguments used for inter-component communication into python3 native types.
    '''
    deserialized_args, deserialized_kwargs, = [], {},
    supported_types = data_type_map()
    for arg in args:
        if arg in supported_types:
            type_casted_value = supported_types[arg]
            serialized_args.append(type_casted_value)
            continue
        arg_type = type(arg)
        if arg_type not in supported_types:
            if arg_type is str:
                type_casted_value = deserialize_string(
                    arg, supported_types=supported_types
                )
                deserialized_args.append(type_casted_value)
            continue
        type_casted_value = supported_types[arg_type](arg._data)
        deserialized_args.append(type_casted_value)
    for kwarg in kwargs:
        if kwarg in supported_types:
            type_casted_value = supported_types[kwarg]
            serialized_kwargs.append(type_casted_value)
            continue
        kwarg_type = type(kwargs[kwarg])
        if kwarg_type not in supported_types:
            if kwarg_type is str:
                type_casted_value = deserialize_string(
                    kwarg, supported_types=supported_types
                )
                deserialized_args.append(type_casted_value)
            continue
        type_casted_value = {kwarg: supported_types[arg_type](arg._data)}
        deserialized_kwargs.update(type_casted_value)
    return deserialized_args, deserialized_kwargs


# CODE DUMP

#   from kaya_module_sdk.types.datapoint.KBoolDatapoint import KBoolDatapoint
#   from kaya_module_sdk.types.datapoint.KFloatDatapoint import KFloatDatapoint
#   from kaya_module_sdk.types.datapoint.KIntDatapoint import KIntDatapoint
#   from kaya_module_sdk.types.datapoint.KStrDatapoint import KStrDatapoint

#   from kaya_module_sdk.types.series.KBoolSeries import KBoolSeries
#   from kaya_module_sdk.types.series.KFloatSeries import KFloatSeries
#   from kaya_module_sdk.types.series.KIntSeries import KIntSeries
#   from kaya_module_sdk.types.series.KStrSeries import KStrSeries

#   from kaya_module_sdk.sdk import (
#       KInt, KFloat, KString, KList, KDict, KSet, KTuple, KBool, KTimeSeries,
#   )

