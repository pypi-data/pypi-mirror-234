from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInteractionWebhookV0Type(Enums.KnownString):
    V0_CANVASUSERINTERACTED = "v0.canvas.userInteracted"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInteractionWebhookV0Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasInteractionWebhookV0Type must be a string (encountered: {val})")
        newcls = Enum("CanvasInteractionWebhookV0Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInteractionWebhookV0Type, getattr(newcls, "_UNKNOWN"))
