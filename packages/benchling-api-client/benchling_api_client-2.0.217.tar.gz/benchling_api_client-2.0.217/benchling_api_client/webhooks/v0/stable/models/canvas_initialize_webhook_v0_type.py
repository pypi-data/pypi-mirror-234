from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInitializeWebhookV0Type(Enums.KnownString):
    V0_CANVASINITIALIZED = "v0.canvas.initialized"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInitializeWebhookV0Type":
        if not isinstance(val, str):
            raise ValueError(f"Value of CanvasInitializeWebhookV0Type must be a string (encountered: {val})")
        newcls = Enum("CanvasInitializeWebhookV0Type", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInitializeWebhookV0Type, getattr(newcls, "_UNKNOWN"))
