from kaya_module_sdk.ktypes.datapoint.KTimeSeries import KTimeSeries
from kaya_module_sdk.ktypes.primitives.KString import KString
from kaya_module_sdk.ktypes.primitives.KBool import KBool


class KBoolDatapoint(KTimeSeries):

    def __init__(self, data: list[KString, KBool]):
        invalid_values = [
            item[1] for item in data if not isinstance(item[1], KBool)
        ]
        if invalid_values:
            raise TypeError(
                f'KTSBool can only have KBool values! Not ({invalid_values})'
            )
        super().__init__(data)
