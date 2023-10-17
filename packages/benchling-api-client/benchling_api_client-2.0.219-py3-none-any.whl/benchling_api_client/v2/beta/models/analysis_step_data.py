from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AnalysisStepData")


@attr.s(auto_attribs=True, repr=False)
class AnalysisStepData:
    """  """

    _dataset_ids: Union[Unset, List[str]] = UNSET
    _file_ids: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("dataset_ids={}".format(repr(self._dataset_ids)))
        fields.append("file_ids={}".format(repr(self._file_ids)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AnalysisStepData({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        dataset_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._dataset_ids, Unset):
            dataset_ids = self._dataset_ids

        file_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._file_ids, Unset):
            file_ids = self._file_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if dataset_ids is not UNSET:
            field_dict["datasetIds"] = dataset_ids
        if file_ids is not UNSET:
            field_dict["fileIds"] = file_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_dataset_ids() -> Union[Unset, List[str]]:
            dataset_ids = cast(List[str], d.pop("datasetIds"))

            return dataset_ids

        try:
            dataset_ids = get_dataset_ids()
        except KeyError:
            if strict:
                raise
            dataset_ids = cast(Union[Unset, List[str]], UNSET)

        def get_file_ids() -> Union[Unset, List[str]]:
            file_ids = cast(List[str], d.pop("fileIds"))

            return file_ids

        try:
            file_ids = get_file_ids()
        except KeyError:
            if strict:
                raise
            file_ids = cast(Union[Unset, List[str]], UNSET)

        analysis_step_data = cls(
            dataset_ids=dataset_ids,
            file_ids=file_ids,
        )

        analysis_step_data.additional_properties = d
        return analysis_step_data

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
    def dataset_ids(self) -> List[str]:
        if isinstance(self._dataset_ids, Unset):
            raise NotPresentError(self, "dataset_ids")
        return self._dataset_ids

    @dataset_ids.setter
    def dataset_ids(self, value: List[str]) -> None:
        self._dataset_ids = value

    @dataset_ids.deleter
    def dataset_ids(self) -> None:
        self._dataset_ids = UNSET

    @property
    def file_ids(self) -> List[str]:
        if isinstance(self._file_ids, Unset):
            raise NotPresentError(self, "file_ids")
        return self._file_ids

    @file_ids.setter
    def file_ids(self, value: List[str]) -> None:
        self._file_ids = value

    @file_ids.deleter
    def file_ids(self) -> None:
        self._file_ids = UNSET
