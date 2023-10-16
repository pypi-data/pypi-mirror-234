from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_script_json_body_kind import CreateScriptJsonBodyKind
from ..models.create_script_json_body_language import CreateScriptJsonBodyLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_script_json_body_schema import CreateScriptJsonBodySchema


T = TypeVar("T", bound="CreateScriptJsonBody")


@_attrs_define
class CreateScriptJsonBody:
    """
    Attributes:
        path (str):
        summary (str):
        description (str):
        content (str):
        language (CreateScriptJsonBodyLanguage):
        parent_hash (Union[Unset, str]):
        schema (Union[Unset, CreateScriptJsonBodySchema]):
        is_template (Union[Unset, bool]):
        lock (Union[Unset, List[str]]):
        kind (Union[Unset, CreateScriptJsonBodyKind]):
        tag (Union[Unset, str]):
        draft_only (Union[Unset, bool]):
        envs (Union[Unset, List[str]]):
        concurrent_limit (Union[Unset, List[int]]):
        concurrency_time_window_s (Union[Unset, List[int]]):
        cache_ttl (Union[Unset, float]):
        dedicated_worker (Union[Unset, bool]):
    """

    path: str
    summary: str
    description: str
    content: str
    language: CreateScriptJsonBodyLanguage
    parent_hash: Union[Unset, str] = UNSET
    schema: Union[Unset, "CreateScriptJsonBodySchema"] = UNSET
    is_template: Union[Unset, bool] = UNSET
    lock: Union[Unset, List[str]] = UNSET
    kind: Union[Unset, CreateScriptJsonBodyKind] = UNSET
    tag: Union[Unset, str] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    envs: Union[Unset, List[str]] = UNSET
    concurrent_limit: Union[Unset, List[int]] = UNSET
    concurrency_time_window_s: Union[Unset, List[int]] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        description = self.description
        content = self.content
        language = self.language.value

        parent_hash = self.parent_hash
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        is_template = self.is_template
        lock: Union[Unset, List[str]] = UNSET
        if not isinstance(self.lock, Unset):
            lock = self.lock

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        tag = self.tag
        draft_only = self.draft_only
        envs: Union[Unset, List[str]] = UNSET
        if not isinstance(self.envs, Unset):
            envs = self.envs

        concurrent_limit: Union[Unset, List[int]] = UNSET
        if not isinstance(self.concurrent_limit, Unset):
            concurrent_limit = self.concurrent_limit

        concurrency_time_window_s: Union[Unset, List[int]] = UNSET
        if not isinstance(self.concurrency_time_window_s, Unset):
            concurrency_time_window_s = self.concurrency_time_window_s

        cache_ttl = self.cache_ttl
        dedicated_worker = self.dedicated_worker

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "description": description,
                "content": content,
                "language": language,
            }
        )
        if parent_hash is not UNSET:
            field_dict["parent_hash"] = parent_hash
        if schema is not UNSET:
            field_dict["schema"] = schema
        if is_template is not UNSET:
            field_dict["is_template"] = is_template
        if lock is not UNSET:
            field_dict["lock"] = lock
        if kind is not UNSET:
            field_dict["kind"] = kind
        if tag is not UNSET:
            field_dict["tag"] = tag
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if envs is not UNSET:
            field_dict["envs"] = envs
        if concurrent_limit is not UNSET:
            field_dict["concurrent_limit"] = concurrent_limit
        if concurrency_time_window_s is not UNSET:
            field_dict["concurrency_time_window_s"] = concurrency_time_window_s
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if dedicated_worker is not UNSET:
            field_dict["dedicated_worker"] = dedicated_worker

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_script_json_body_schema import CreateScriptJsonBodySchema

        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        description = d.pop("description")

        content = d.pop("content")

        language = CreateScriptJsonBodyLanguage(d.pop("language"))

        parent_hash = d.pop("parent_hash", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, CreateScriptJsonBodySchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = CreateScriptJsonBodySchema.from_dict(_schema)

        is_template = d.pop("is_template", UNSET)

        lock = cast(List[str], d.pop("lock", UNSET))

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, CreateScriptJsonBodyKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = CreateScriptJsonBodyKind(_kind)

        tag = d.pop("tag", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        envs = cast(List[str], d.pop("envs", UNSET))

        concurrent_limit = cast(List[int], d.pop("concurrent_limit", UNSET))

        concurrency_time_window_s = cast(List[int], d.pop("concurrency_time_window_s", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        create_script_json_body = cls(
            path=path,
            summary=summary,
            description=description,
            content=content,
            language=language,
            parent_hash=parent_hash,
            schema=schema,
            is_template=is_template,
            lock=lock,
            kind=kind,
            tag=tag,
            draft_only=draft_only,
            envs=envs,
            concurrent_limit=concurrent_limit,
            concurrency_time_window_s=concurrency_time_window_s,
            cache_ttl=cache_ttl,
            dedicated_worker=dedicated_worker,
        )

        create_script_json_body.additional_properties = d
        return create_script_json_body

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
