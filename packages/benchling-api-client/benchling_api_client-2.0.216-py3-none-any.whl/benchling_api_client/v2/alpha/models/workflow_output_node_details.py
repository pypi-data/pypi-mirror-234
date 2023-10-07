from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.schema_summary import SchemaSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowOutputNodeDetails")


@attr.s(auto_attribs=True, repr=False)
class WorkflowOutputNodeDetails:
    """  """

    _id: Union[Unset, str] = UNSET
    _output_schema: Union[Unset, SchemaSummary] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("output_schema={}".format(repr(self._output_schema)))
        return "WorkflowOutputNodeDetails({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        output_schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._output_schema, Unset):
            output_schema = self._output_schema.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if output_schema is not UNSET:
            field_dict["outputSchema"] = output_schema

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

        def get_output_schema() -> Union[Unset, SchemaSummary]:
            output_schema: Union[Unset, Union[Unset, SchemaSummary]] = UNSET
            _output_schema = d.pop("outputSchema")

            if not isinstance(_output_schema, Unset):
                output_schema = SchemaSummary.from_dict(_output_schema)

            return output_schema

        try:
            output_schema = get_output_schema()
        except KeyError:
            if strict:
                raise
            output_schema = cast(Union[Unset, SchemaSummary], UNSET)

        workflow_output_node_details = cls(
            id=id,
            output_schema=output_schema,
        )

        return workflow_output_node_details

    @property
    def id(self) -> str:
        """ The ID of the workflow output node config details """
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
    def output_schema(self) -> SchemaSummary:
        if isinstance(self._output_schema, Unset):
            raise NotPresentError(self, "output_schema")
        return self._output_schema

    @output_schema.setter
    def output_schema(self, value: SchemaSummary) -> None:
        self._output_schema = value

    @output_schema.deleter
    def output_schema(self) -> None:
        self._output_schema = UNSET
