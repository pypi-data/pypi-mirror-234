from kaya_module_sdk.ktypes.series.KList import KList
from kaya_module_sdk.ktypes.primitives.KFloat import KFloat


class KFloatSeries(KList):

    def __init__(self, data: list[KFloat]):
        invalid_values = [
            item for item in data if not isinstance(item, KFloat)
        ]
        if invalid_values:
            raise TypeError(
                f'KLFloat can only have KFloat values! Not ({invalid_values})'
            )
        super().__init__(data)
