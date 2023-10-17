from typing import Union

from ..extensions import UnknownType
from ..models.analysis_step_update_with_failure_status_with_message import (
    AnalysisStepUpdateWithFailureStatusWithMessage,
)
from ..models.analysis_step_update_with_output_data import AnalysisStepUpdateWithOutputData
from ..models.analysis_step_update_with_success_status_without_message import (
    AnalysisStepUpdateWithSuccessStatusWithoutMessage,
)

AnalysisStepUpdate = Union[
    AnalysisStepUpdateWithOutputData,
    AnalysisStepUpdateWithSuccessStatusWithoutMessage,
    AnalysisStepUpdateWithFailureStatusWithMessage,
    UnknownType,
]
