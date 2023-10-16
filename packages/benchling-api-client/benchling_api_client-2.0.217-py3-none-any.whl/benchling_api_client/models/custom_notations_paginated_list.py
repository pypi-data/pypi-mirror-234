from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_notations_paginated_list_custom_notations_item import (
    CustomNotationsPaginatedListCustomNotationsItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationsPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationsPaginatedList:
    """  """

    _custom_notations: Union[Unset, List[CustomNotationsPaginatedListCustomNotationsItem]] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("custom_notations={}".format(repr(self._custom_notations)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "CustomNotationsPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        custom_notations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._custom_notations, Unset):
            custom_notations = []
            for custom_notations_item_data in self._custom_notations:
                custom_notations_item = custom_notations_item_data.to_dict()

                custom_notations.append(custom_notations_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if custom_notations is not UNSET:
            field_dict["customNotations"] = custom_notations
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_custom_notations() -> Union[Unset, List[CustomNotationsPaginatedListCustomNotationsItem]]:
            custom_notations = []
            _custom_notations = d.pop("customNotations")
            for custom_notations_item_data in _custom_notations or []:
                custom_notations_item = CustomNotationsPaginatedListCustomNotationsItem.from_dict(
                    custom_notations_item_data, strict=False
                )

                custom_notations.append(custom_notations_item)

            return custom_notations

        try:
            custom_notations = get_custom_notations()
        except KeyError:
            if strict:
                raise
            custom_notations = cast(
                Union[Unset, List[CustomNotationsPaginatedListCustomNotationsItem]], UNSET
            )

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        custom_notations_paginated_list = cls(
            custom_notations=custom_notations,
            next_token=next_token,
        )

        return custom_notations_paginated_list

    @property
    def custom_notations(self) -> List[CustomNotationsPaginatedListCustomNotationsItem]:
        if isinstance(self._custom_notations, Unset):
            raise NotPresentError(self, "custom_notations")
        return self._custom_notations

    @custom_notations.setter
    def custom_notations(self, value: List[CustomNotationsPaginatedListCustomNotationsItem]) -> None:
        self._custom_notations = value

    @custom_notations.deleter
    def custom_notations(self) -> None:
        self._custom_notations = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
