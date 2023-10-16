from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Extra

if TYPE_CHECKING:
    from likeinterface.interface import Interface

LikeType = TypeVar("LikeType")


class Request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    method: str
    data: Dict[str, Any]
    files: Optional[Dict[str, Any]] = None


class Response(BaseModel, Generic[LikeType]):
    ok: bool
    result: Optional[LikeType] = None
    error: Optional[str] = None
    error_code: Optional[int] = None


class Method(abc.ABC, BaseModel, Generic[LikeType]):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra=Extra.allow,
        populate_by_name=True,
    )

    @property
    def __is_form__(self) -> bool:
        return False

    @property
    @abc.abstractmethod
    def __name__(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def __returning__(self) -> Any:
        ...

    @abc.abstractmethod
    def request(self, interface: Interface) -> Request:
        ...

    def response(self, data: Dict[str, Any]) -> Response[LikeType]:
        return Response[self.__returning__].model_validate(data)  # type: ignore[name-defined]
