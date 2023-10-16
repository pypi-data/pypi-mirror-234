from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request
from likeinterface.types import Game

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetGame(Method[Game]):
    """
    Use this method to get game by access.

    Parameters
      Name      | Type   | Required | Description

      1. access | String | Yes      | Game unique ID

    Result
      :class:`Game`
    """

    __name__ = "like/getGame"
    __returning__ = Game

    access: str

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
