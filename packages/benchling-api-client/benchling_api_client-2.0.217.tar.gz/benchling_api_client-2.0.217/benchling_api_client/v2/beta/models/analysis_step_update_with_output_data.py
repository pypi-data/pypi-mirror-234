from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_data import AnalysisStepData
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepUpdateWithOutputData")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepUpdateWithOutputData:
    """  """

    _output_data: Union[Unset, AnalysisStepData] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("output_data={}".format(repr(self._output_data)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepUpdateWithOutputData({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        output_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._output_data, Unset):
            output_data = self._output_data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if output_data is not UNSET:
            field_dict["outputData"] = output_data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_output_data() -> Union[Unset, AnalysisStepData]:
            output_data: Union[Unset, Union[Unset, AnalysisStepData]] = UNSET
            _output_data = d.pop("outputData")

            if not isinstance(_output_data, Unset):
                output_data = AnalysisStepData.from_dict(_output_data)

            return output_data

        try:
            output_data = get_output_data()
        except KeyError:
            if strict:
                raise
            output_data = cast(Union[Unset, AnalysisStepData], UNSET)

        analysis_step_update_with_output_data = cls(
            output_data=output_data,
        )

        analysis_step_update_with_output_data.additional_properties = d
        return analysis_step_update_with_output_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def output_data(self) -> AnalysisStepData:
        if isinstance(self._output_data, Unset):
            raise NotPresentError(self, "output_data")
        return self._output_data

    @output_data.setter
    def output_data(self, value: AnalysisStepData) -> None:
        self._output_data = value

    @output_data.deleter
    def output_data(self) -> None:
        self._output_data = UNSET
