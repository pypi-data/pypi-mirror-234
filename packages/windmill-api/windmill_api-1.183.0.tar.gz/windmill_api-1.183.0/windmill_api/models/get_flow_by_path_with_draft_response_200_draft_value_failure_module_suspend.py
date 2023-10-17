from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend_resume_form import (
        GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm,
    )


T = TypeVar("T", bound="GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend")


@_attrs_define
class GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspend:
    """
    Attributes:
        required_events (Union[Unset, int]):
        timeout (Union[Unset, int]):
        resume_form (Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm]):
    """

    required_events: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    resume_form: Union[Unset, "GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_events = self.required_events
        timeout = self.timeout
        resume_form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resume_form, Unset):
            resume_form = self.resume_form.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_events is not UNSET:
            field_dict["required_events"] = required_events
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if resume_form is not UNSET:
            field_dict["resume_form"] = resume_form

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend_resume_form import (
            GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm,
        )

        d = src_dict.copy()
        required_events = d.pop("required_events", UNSET)

        timeout = d.pop("timeout", UNSET)

        _resume_form = d.pop("resume_form", UNSET)
        resume_form: Union[Unset, GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm]
        if isinstance(_resume_form, Unset):
            resume_form = UNSET
        else:
            resume_form = GetFlowByPathWithDraftResponse200DraftValueFailureModuleSuspendResumeForm.from_dict(
                _resume_form
            )

        get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend = cls(
            required_events=required_events,
            timeout=timeout,
            resume_form=resume_form,
        )

        get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend.additional_properties = d
        return get_flow_by_path_with_draft_response_200_draft_value_failure_module_suspend

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
