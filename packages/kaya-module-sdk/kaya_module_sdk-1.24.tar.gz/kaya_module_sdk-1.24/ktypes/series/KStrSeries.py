from kaya_module_sdk.ktypes.series.KList import KList
from kaya_module_sdk.ktypes.primitives.KString import KString


class KStrSeries(KList):

    def __init__(self, data: list[KString]):
        invalid_values = [
            item for item in data if not isinstance(item, KString)
        ]
        if invalid_values:
            raise TypeError(
                f'KLString can only have KString values! Not ({invalid_values})'
            )
        super().__init__(data)
