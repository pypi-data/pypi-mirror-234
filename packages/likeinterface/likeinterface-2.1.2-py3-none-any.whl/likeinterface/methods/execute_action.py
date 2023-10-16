from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request
from likeinterface.types import Action

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class ExecuteAction(Method[bool]):
    """
    Use this method to execute player action.

    Parameters
      Name      | Type            | Required | Description

      1. access | String          | Yes      | Game unique ID
      2. action | :class:`Action` | Yes      | Player action to execute

    Result
      :class:`bool`
    """

    __name__ = "like/executeAction"
    __returning__ = bool

    access: str
    action: Action

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
