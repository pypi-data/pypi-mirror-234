import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExceptionInfo")


@attr.s(auto_attribs=True)
class ExceptionInfo:
    """Contains information for unexpected errors"""

    message_type: Union[Unset, None, str] = UNSET
    message: Union[Unset, None, str] = UNSET
    stack_trace: Union[Unset, None, str] = UNSET
    date: Union[Unset, datetime.datetime] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message_type = self.message_type
        message = self.message
        stack_trace = self.stack_trace
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if message_type is not UNSET:
            field_dict["messageType"] = message_type
        if message is not UNSET:
            field_dict["message"] = message
        if stack_trace is not UNSET:
            field_dict["stackTrace"] = stack_trace
        if date is not UNSET:
            field_dict["date"] = date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message_type = d.pop("messageType", UNSET)

        message = d.pop("message", UNSET)

        stack_trace = d.pop("stackTrace", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.datetime]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date)

        exception_info = cls(
            message_type=message_type,
            message=message,
            stack_trace=stack_trace,
            date=date,
        )

        return exception_info
