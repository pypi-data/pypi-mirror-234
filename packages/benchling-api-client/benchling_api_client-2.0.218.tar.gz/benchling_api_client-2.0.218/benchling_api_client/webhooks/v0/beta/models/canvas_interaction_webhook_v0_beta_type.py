from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class CanvasInteractionWebhookV0BetaType(Enums.KnownString):
    V0_BETACANVASUSERINTERACTED = "v0-beta.canvas.userInteracted"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "CanvasInteractionWebhookV0BetaType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of CanvasInteractionWebhookV0BetaType must be a string (encountered: {val})"
            )
        newcls = Enum("CanvasInteractionWebhookV0BetaType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(CanvasInteractionWebhookV0BetaType, getattr(newcls, "_UNKNOWN"))
