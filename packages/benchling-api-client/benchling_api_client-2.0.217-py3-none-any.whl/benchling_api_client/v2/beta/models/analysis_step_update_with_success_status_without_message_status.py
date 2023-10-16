from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AnalysisStepUpdateWithSuccessStatusWithoutMessageStatus(Enums.KnownString):
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AnalysisStepUpdateWithSuccessStatusWithoutMessageStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AnalysisStepUpdateWithSuccessStatusWithoutMessageStatus must be a string (encountered: {val})"
            )
        newcls = Enum("AnalysisStepUpdateWithSuccessStatusWithoutMessageStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AnalysisStepUpdateWithSuccessStatusWithoutMessageStatus, getattr(newcls, "_UNKNOWN"))
