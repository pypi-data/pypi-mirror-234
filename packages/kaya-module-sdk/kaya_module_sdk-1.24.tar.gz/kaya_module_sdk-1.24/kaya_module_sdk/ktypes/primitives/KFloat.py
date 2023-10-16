from dataclasses import dataclass
from kaya_module_sdk.ktypes.primitives._k_number import KNumber


@dataclass
class KFloat(KNumber):
    _data: float

    def __repr__(self) -> str:
#       return f"KFloat(value={self._data})"
        return str(self._data)



