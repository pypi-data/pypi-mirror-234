import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_by_path_response_200_extra_perms import GetFlowByPathResponse200ExtraPerms
    from ..models.get_flow_by_path_response_200_schema import GetFlowByPathResponse200Schema
    from ..models.get_flow_by_path_response_200_value import GetFlowByPathResponse200Value


T = TypeVar("T", bound="GetFlowByPathResponse200")


@_attrs_define
class GetFlowByPathResponse200:
    """
    Attributes:
        summary (str):
        value (GetFlowByPathResponse200Value):
        path (str):
        edited_by (str):
        edited_at (datetime.datetime):
        archived (bool):
        extra_perms (GetFlowByPathResponse200ExtraPerms):
        description (Union[Unset, str]):
        schema (Union[Unset, GetFlowByPathResponse200Schema]):
        workspace_id (Union[Unset, str]):
        additional_properties (Union[Unset, bool]):
        starred (Union[Unset, bool]):
        draft_only (Union[Unset, bool]):
        tag (Union[Unset, str]):
    """

    summary: str
    value: "GetFlowByPathResponse200Value"
    path: str
    edited_by: str
    edited_at: datetime.datetime
    archived: bool
    extra_perms: "GetFlowByPathResponse200ExtraPerms"
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "GetFlowByPathResponse200Schema"] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    additional_properties: Union[Unset, bool] = UNSET
    starred: Union[Unset, bool] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    tag: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        value = self.value.to_dict()

        path = self.path
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        archived = self.archived
        extra_perms = self.extra_perms.to_dict()

        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        workspace_id = self.workspace_id
        additional_properties = self.additional_properties
        starred = self.starred
        draft_only = self.draft_only
        tag = self.tag

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "value": value,
                "path": path,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "archived": archived,
                "extra_perms": extra_perms,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if additional_properties is not UNSET:
            field_dict["additionalProperties"] = additional_properties
        if starred is not UNSET:
            field_dict["starred"] = starred
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_by_path_response_200_extra_perms import GetFlowByPathResponse200ExtraPerms
        from ..models.get_flow_by_path_response_200_schema import GetFlowByPathResponse200Schema
        from ..models.get_flow_by_path_response_200_value import GetFlowByPathResponse200Value

        d = src_dict.copy()
        summary = d.pop("summary")

        value = GetFlowByPathResponse200Value.from_dict(d.pop("value"))

        path = d.pop("path")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        archived = d.pop("archived")

        extra_perms = GetFlowByPathResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, GetFlowByPathResponse200Schema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = GetFlowByPathResponse200Schema.from_dict(_schema)

        workspace_id = d.pop("workspace_id", UNSET)

        additional_properties = d.pop("additionalProperties", UNSET)

        starred = d.pop("starred", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        tag = d.pop("tag", UNSET)

        get_flow_by_path_response_200 = cls(
            summary=summary,
            value=value,
            path=path,
            edited_by=edited_by,
            edited_at=edited_at,
            archived=archived,
            extra_perms=extra_perms,
            description=description,
            schema=schema,
            workspace_id=workspace_id,
            additional_properties=additional_properties,
            starred=starred,
            draft_only=draft_only,
            tag=tag,
        )

        get_flow_by_path_response_200.additional_properties = d
        return get_flow_by_path_response_200

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
