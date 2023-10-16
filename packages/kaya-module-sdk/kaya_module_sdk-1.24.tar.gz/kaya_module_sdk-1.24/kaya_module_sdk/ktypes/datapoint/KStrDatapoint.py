from kaya_module_sdk.ktypes.datapoint.KTimeSeries import KTimeSeries
from kaya_module_sdk.ktypes.primitives.KString import KString


class KStrDatapoint(KTimeSeries):

    def __init__(self, data: list[KString, KString]):
        invalid_values = [
            item[1] for item in data if not isinstance(item[1], KString)
        ]
        if invalid_values:
            raise TypeError(
                f'KTSString can only have KString values! Not ({invalid_values})'
            )
        super().__init__(data)
