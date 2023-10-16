from kaya_module_sdk.ktypes.series.KList import KList
from kaya_module_sdk.ktypes.primitives.KBool import KBool


class KBoolSeries(KList):

    def __init__(self, data: list[KBool]):
        invalid_values = [
            item for item in data if not isinstance(item, KBool)
        ]
        if invalid_values:
            raise TypeError(
                f'KLBool can only have KBool values! Not ({invalid_values})'
            )
        super().__init__(data)
