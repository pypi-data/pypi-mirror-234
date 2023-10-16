from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.analysis_step_data import AnalysisStepData
from ..models.analysis_step_status import AnalysisStepStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStep")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStep:
    """  """

    _id: Union[Unset, str] = UNSET
    _input_data: Union[Unset, AnalysisStepData] = UNSET
    _output_data: Union[Unset, AnalysisStepData] = UNSET
    _status: Union[Unset, AnalysisStepStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("input_data={}".format(repr(self._input_data)))
        fields.append("output_data={}".format(repr(self._output_data)))
        fields.append("status={}".format(repr(self._status)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStep({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        input_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._input_data, Unset):
            input_data = self._input_data.to_dict()

        output_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._output_data, Unset):
            output_data = self._output_data.to_dict()

        status: Union[Unset, int] = UNSET
        if not isinstance(self._status, Unset):
            status = self._status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if input_data is not UNSET:
            field_dict["inputData"] = input_data
        if output_data is not UNSET:
            field_dict["outputData"] = output_data
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_input_data() -> Union[Unset, AnalysisStepData]:
            input_data: Union[Unset, Union[Unset, AnalysisStepData]] = UNSET
            _input_data = d.pop("inputData")

            if not isinstance(_input_data, Unset):
                input_data = AnalysisStepData.from_dict(_input_data)

            return input_data

        try:
            input_data = get_input_data()
        except KeyError:
            if strict:
                raise
            input_data = cast(Union[Unset, AnalysisStepData], UNSET)

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

        def get_status() -> Union[Unset, AnalysisStepStatus]:
            status = UNSET
            _status = d.pop("status")
            if _status is not None and _status is not UNSET:
                try:
                    status = AnalysisStepStatus(_status)
                except ValueError:
                    status = AnalysisStepStatus.of_unknown(_status)

            return status

        try:
            status = get_status()
        except KeyError:
            if strict:
                raise
            status = cast(Union[Unset, AnalysisStepStatus], UNSET)

        analysis_step = cls(
            id=id,
            input_data=input_data,
            output_data=output_data,
            status=status,
        )

        analysis_step.additional_properties = d
        return analysis_step

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
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def input_data(self) -> AnalysisStepData:
        if isinstance(self._input_data, Unset):
            raise NotPresentError(self, "input_data")
        return self._input_data

    @input_data.setter
    def input_data(self, value: AnalysisStepData) -> None:
        self._input_data = value

    @input_data.deleter
    def input_data(self) -> None:
        self._input_data = UNSET

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

    @property
    def status(self) -> AnalysisStepStatus:
        if isinstance(self._status, Unset):
            raise NotPresentError(self, "status")
        return self._status

    @status.setter
    def status(self, value: AnalysisStepStatus) -> None:
        self._status = value

    @status.deleter
    def status(self) -> None:
        self._status = UNSET
