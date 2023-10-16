from kaya_module_sdk.ktypes.datapoint.KTimeSeries import KTimeSeries
from kaya_module_sdk.ktypes.primitives.KString import KString
from kaya_module_sdk.ktypes.primitives.KInt import KInt


class KIntDatapoint(KTimeSeries):

    def __init__(self, data: list[KString, KInt]):
        invalid_values = [
            item[1] for item in data if not isinstance(item[1], KInt)
        ]
        if invalid_values:
            raise TypeError(
                f'KTSInt can only have KInt values! Not ({invalid_values})'
            )
        super().__init__(data)
