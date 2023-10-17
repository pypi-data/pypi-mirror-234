import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.script_kind import ScriptKind
from ..models.script_language import ScriptLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.script_extra_perms import ScriptExtraPerms
    from ..models.script_schema import ScriptSchema


T = TypeVar("T", bound="Script")


@_attrs_define
class Script:
    """
    Attributes:
        hash_ (str):
        path (str):
        summary (str):
        description (str):
        content (str):
        created_by (str):
        created_at (datetime.datetime):
        archived (bool):
        deleted (bool):
        is_template (bool):
        extra_perms (ScriptExtraPerms):
        language (ScriptLanguage):
        kind (ScriptKind):
        starred (bool):
        workspace_id (Union[Unset, str]):
        parent_hashes (Union[Unset, List[str]]): The first element is the direct parent of the script, the second is the
            parent of the first, etc
        schema (Union[Unset, ScriptSchema]):
        lock (Union[Unset, str]):
        lock_error_logs (Union[Unset, str]):
        tag (Union[Unset, str]):
        has_draft (Union[Unset, bool]):
        draft_only (Union[Unset, bool]):
        envs (Union[Unset, List[str]]):
        concurrent_limit (Union[Unset, List[int]]):
        concurrency_time_window_s (Union[Unset, List[int]]):
        cache_ttl (Union[Unset, float]):
        dedicated_worker (Union[Unset, bool]):
    """

    hash_: str
    path: str
    summary: str
    description: str
    content: str
    created_by: str
    created_at: datetime.datetime
    archived: bool
    deleted: bool
    is_template: bool
    extra_perms: "ScriptExtraPerms"
    language: ScriptLanguage
    kind: ScriptKind
    starred: bool
    workspace_id: Union[Unset, str] = UNSET
    parent_hashes: Union[Unset, List[str]] = UNSET
    schema: Union[Unset, "ScriptSchema"] = UNSET
    lock: Union[Unset, str] = UNSET
    lock_error_logs: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    has_draft: Union[Unset, bool] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    envs: Union[Unset, List[str]] = UNSET
    concurrent_limit: Union[Unset, List[int]] = UNSET
    concurrency_time_window_s: Union[Unset, List[int]] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    dedicated_worker: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        hash_ = self.hash_
        path = self.path
        summary = self.summary
        description = self.description
        content = self.content
        created_by = self.created_by
        created_at = self.created_at.isoformat()

        archived = self.archived
        deleted = self.deleted
        is_template = self.is_template
        extra_perms = self.extra_perms.to_dict()

        language = self.language.value

        kind = self.kind.value

        starred = self.starred
        workspace_id = self.workspace_id
        parent_hashes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.parent_hashes, Unset):
            parent_hashes = self.parent_hashes

        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        lock = self.lock
        lock_error_logs = self.lock_error_logs
        tag = self.tag
        has_draft = self.has_draft
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
                "hash": hash_,
                "path": path,
                "summary": summary,
                "description": description,
                "content": content,
                "created_by": created_by,
                "created_at": created_at,
                "archived": archived,
                "deleted": deleted,
                "is_template": is_template,
                "extra_perms": extra_perms,
                "language": language,
                "kind": kind,
                "starred": starred,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if parent_hashes is not UNSET:
            field_dict["parent_hashes"] = parent_hashes
        if schema is not UNSET:
            field_dict["schema"] = schema
        if lock is not UNSET:
            field_dict["lock"] = lock
        if lock_error_logs is not UNSET:
            field_dict["lock_error_logs"] = lock_error_logs
        if tag is not UNSET:
            field_dict["tag"] = tag
        if has_draft is not UNSET:
            field_dict["has_draft"] = has_draft
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
        from ..models.script_extra_perms import ScriptExtraPerms
        from ..models.script_schema import ScriptSchema

        d = src_dict.copy()
        hash_ = d.pop("hash")

        path = d.pop("path")

        summary = d.pop("summary")

        description = d.pop("description")

        content = d.pop("content")

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        archived = d.pop("archived")

        deleted = d.pop("deleted")

        is_template = d.pop("is_template")

        extra_perms = ScriptExtraPerms.from_dict(d.pop("extra_perms"))

        language = ScriptLanguage(d.pop("language"))

        kind = ScriptKind(d.pop("kind"))

        starred = d.pop("starred")

        workspace_id = d.pop("workspace_id", UNSET)

        parent_hashes = cast(List[str], d.pop("parent_hashes", UNSET))

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, ScriptSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = ScriptSchema.from_dict(_schema)

        lock = d.pop("lock", UNSET)

        lock_error_logs = d.pop("lock_error_logs", UNSET)

        tag = d.pop("tag", UNSET)

        has_draft = d.pop("has_draft", UNSET)

        draft_only = d.pop("draft_only", UNSET)

        envs = cast(List[str], d.pop("envs", UNSET))

        concurrent_limit = cast(List[int], d.pop("concurrent_limit", UNSET))

        concurrency_time_window_s = cast(List[int], d.pop("concurrency_time_window_s", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        dedicated_worker = d.pop("dedicated_worker", UNSET)

        script = cls(
            hash_=hash_,
            path=path,
            summary=summary,
            description=description,
            content=content,
            created_by=created_by,
            created_at=created_at,
            archived=archived,
            deleted=deleted,
            is_template=is_template,
            extra_perms=extra_perms,
            language=language,
            kind=kind,
            starred=starred,
            workspace_id=workspace_id,
            parent_hashes=parent_hashes,
            schema=schema,
            lock=lock,
            lock_error_logs=lock_error_logs,
            tag=tag,
            has_draft=has_draft,
            draft_only=draft_only,
            envs=envs,
            concurrent_limit=concurrent_limit,
            concurrency_time_window_s=concurrency_time_window_s,
            cache_ttl=cache_ttl,
            dedicated_worker=dedicated_worker,
        )

        script.additional_properties = d
        return script

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
