from __future__ import annotations

from typing import TYPE_CHECKING, List

from likeinterface.methods.base import Method, Request
from likeinterface.types import Action

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetPossibleActions(Method[List[Action]]):
    """
    Use this method to get possible actions for current player.

    Parameters
      Name      | Type   | Required | Description

      1. access | String | Yes      | Game unique ID

    Result
      Array of :class:`Action`
    """

    __name__ = "like/getPossibleActions"
    __returning__ = List[Action]

    access: str

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
