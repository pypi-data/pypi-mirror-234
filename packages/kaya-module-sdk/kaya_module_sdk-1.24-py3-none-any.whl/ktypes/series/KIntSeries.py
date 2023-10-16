from kaya_module_sdk.ktypes.series.KList import KList
from kaya_module_sdk.ktypes.primitives.KInt import KInt


class KIntSeries(KList):

    def __init__(self, data: list[KInt]):
        invalid_values = [
            item for item in data if not isinstance(item, KInt)
        ]
        if invalid_values:
            raise TypeError(
                f'KLInt can only have KInt values! Not ({invalid_values})'
            )
        super().__init__(data)
