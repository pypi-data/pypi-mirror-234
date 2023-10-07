from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class AnalysisStepUpdateWithFailureStatusWithMessageStatus(Enums.KnownString):
    FAILED = "FAILED"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "AnalysisStepUpdateWithFailureStatusWithMessageStatus":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of AnalysisStepUpdateWithFailureStatusWithMessageStatus must be a string (encountered: {val})"
            )
        newcls = Enum("AnalysisStepUpdateWithFailureStatusWithMessageStatus", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(AnalysisStepUpdateWithFailureStatusWithMessageStatus, getattr(newcls, "_UNKNOWN"))
