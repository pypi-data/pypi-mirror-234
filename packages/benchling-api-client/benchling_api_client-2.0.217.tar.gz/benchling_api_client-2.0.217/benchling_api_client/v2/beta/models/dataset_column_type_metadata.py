from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.dataset_column_type_metadata_name import DatasetColumnTypeMetadataName
from ..models.dataset_column_type_metadata_target import DatasetColumnTypeMetadataTarget
from ..types import UNSET, Unset

T = TypeVar("T", bound="DatasetColumnTypeMetadata")


@attr.s(auto_attribs=True, repr=False)
class DatasetColumnTypeMetadata:
    """  """

    _is_list: Union[Unset, bool] = UNSET
    _is_nullable: Union[Unset, bool] = UNSET
    _name: Union[Unset, DatasetColumnTypeMetadataName] = UNSET
    _target: Union[Unset, DatasetColumnTypeMetadataTarget] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("is_list={}".format(repr(self._is_list)))
        fields.append("is_nullable={}".format(repr(self._is_nullable)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("target={}".format(repr(self._target)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DatasetColumnTypeMetadata({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        is_list = self._is_list
        is_nullable = self._is_nullable
        name: Union[Unset, int] = UNSET
        if not isinstance(self._name, Unset):
            name = self._name.value

        target: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._target, Unset):
            target = self._target.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if is_list is not UNSET:
            field_dict["isList"] = is_list
        if is_nullable is not UNSET:
            field_dict["isNullable"] = is_nullable
        if name is not UNSET:
            field_dict["name"] = name
        if target is not UNSET:
            field_dict["target"] = target

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_is_list() -> Union[Unset, bool]:
            is_list = d.pop("isList")
            return is_list

        try:
            is_list = get_is_list()
        except KeyError:
            if strict:
                raise
            is_list = cast(Union[Unset, bool], UNSET)

        def get_is_nullable() -> Union[Unset, bool]:
            is_nullable = d.pop("isNullable")
            return is_nullable

        try:
            is_nullable = get_is_nullable()
        except KeyError:
            if strict:
                raise
            is_nullable = cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, DatasetColumnTypeMetadataName]:
            name = UNSET
            _name = d.pop("name")
            if _name is not None and _name is not UNSET:
                try:
                    name = DatasetColumnTypeMetadataName(_name)
                except ValueError:
                    name = DatasetColumnTypeMetadataName.of_unknown(_name)

            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, DatasetColumnTypeMetadataName], UNSET)

        def get_target() -> Union[Unset, DatasetColumnTypeMetadataTarget]:
            target: Union[Unset, Union[Unset, DatasetColumnTypeMetadataTarget]] = UNSET
            _target = d.pop("target")

            if not isinstance(_target, Unset):
                target = DatasetColumnTypeMetadataTarget.from_dict(_target)

            return target

        try:
            target = get_target()
        except KeyError:
            if strict:
                raise
            target = cast(Union[Unset, DatasetColumnTypeMetadataTarget], UNSET)

        dataset_column_type_metadata = cls(
            is_list=is_list,
            is_nullable=is_nullable,
            name=name,
            target=target,
        )

        dataset_column_type_metadata.additional_properties = d
        return dataset_column_type_metadata

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
    def is_list(self) -> bool:
        if isinstance(self._is_list, Unset):
            raise NotPresentError(self, "is_list")
        return self._is_list

    @is_list.setter
    def is_list(self, value: bool) -> None:
        self._is_list = value

    @is_list.deleter
    def is_list(self) -> None:
        self._is_list = UNSET

    @property
    def is_nullable(self) -> bool:
        if isinstance(self._is_nullable, Unset):
            raise NotPresentError(self, "is_nullable")
        return self._is_nullable

    @is_nullable.setter
    def is_nullable(self, value: bool) -> None:
        self._is_nullable = value

    @is_nullable.deleter
    def is_nullable(self) -> None:
        self._is_nullable = UNSET

    @property
    def name(self) -> DatasetColumnTypeMetadataName:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: DatasetColumnTypeMetadataName) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def target(self) -> DatasetColumnTypeMetadataTarget:
        """ Only present if the column type is ObjectLink """
        if isinstance(self._target, Unset):
            raise NotPresentError(self, "target")
        return self._target

    @target.setter
    def target(self, value: DatasetColumnTypeMetadataTarget) -> None:
        self._target = value

    @target.deleter
    def target(self) -> None:
        self._target = UNSET
