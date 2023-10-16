from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.branch_one_default_item_mock import BranchOneDefaultItemMock
    from ..models.branch_one_default_item_retry import BranchOneDefaultItemRetry
    from ..models.branch_one_default_item_sleep_type_0 import BranchOneDefaultItemSleepType0
    from ..models.branch_one_default_item_sleep_type_1 import BranchOneDefaultItemSleepType1
    from ..models.branch_one_default_item_stop_after_if import BranchOneDefaultItemStopAfterIf
    from ..models.branch_one_default_item_suspend import BranchOneDefaultItemSuspend


T = TypeVar("T", bound="BranchOneDefaultItem")


@_attrs_define
class BranchOneDefaultItem:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, BranchOneDefaultItemStopAfterIf]):
        sleep (Union['BranchOneDefaultItemSleepType0', 'BranchOneDefaultItemSleepType1', Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        summary (Union[Unset, str]):
        mock (Union[Unset, BranchOneDefaultItemMock]):
        suspend (Union[Unset, BranchOneDefaultItemSuspend]):
        retry (Union[Unset, BranchOneDefaultItemRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, "BranchOneDefaultItemStopAfterIf"] = UNSET
    sleep: Union["BranchOneDefaultItemSleepType0", "BranchOneDefaultItemSleepType1", Unset] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, "BranchOneDefaultItemMock"] = UNSET
    suspend: Union[Unset, "BranchOneDefaultItemSuspend"] = UNSET
    retry: Union[Unset, "BranchOneDefaultItemRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.branch_one_default_item_sleep_type_0 import BranchOneDefaultItemSleepType0

        id = self.id
        value = self.value
        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, BranchOneDefaultItemSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        cache_ttl = self.cache_ttl
        timeout = self.timeout
        summary = self.summary
        mock: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mock, Unset):
            mock = self.mock.to_dict()

        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if summary is not UNSET:
            field_dict["summary"] = summary
        if mock is not UNSET:
            field_dict["mock"] = mock
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.branch_one_default_item_mock import BranchOneDefaultItemMock
        from ..models.branch_one_default_item_retry import BranchOneDefaultItemRetry
        from ..models.branch_one_default_item_sleep_type_0 import BranchOneDefaultItemSleepType0
        from ..models.branch_one_default_item_sleep_type_1 import BranchOneDefaultItemSleepType1
        from ..models.branch_one_default_item_stop_after_if import BranchOneDefaultItemStopAfterIf
        from ..models.branch_one_default_item_suspend import BranchOneDefaultItemSuspend

        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, BranchOneDefaultItemStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = BranchOneDefaultItemStopAfterIf.from_dict(_stop_after_if)

        def _parse_sleep(
            data: object,
        ) -> Union["BranchOneDefaultItemSleepType0", "BranchOneDefaultItemSleepType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, BranchOneDefaultItemSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = BranchOneDefaultItemSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, BranchOneDefaultItemSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = BranchOneDefaultItemSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, BranchOneDefaultItemMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = BranchOneDefaultItemMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, BranchOneDefaultItemSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = BranchOneDefaultItemSuspend.from_dict(_suspend)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, BranchOneDefaultItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = BranchOneDefaultItemRetry.from_dict(_retry)

        branch_one_default_item = cls(
            id=id,
            value=value,
            stop_after_if=stop_after_if,
            sleep=sleep,
            cache_ttl=cache_ttl,
            timeout=timeout,
            summary=summary,
            mock=mock,
            suspend=suspend,
            retry=retry,
        )

        branch_one_default_item.additional_properties = d
        return branch_one_default_item

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
