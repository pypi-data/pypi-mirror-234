from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class DeleteGame(Method[bool]):
    """
    Use this method to delete game.

    Parameters
      Name      | Type   | Required | Description

      1. access | String | Yes      | Game unique ID

    Result
      :class:`bool`
    """

    __name__ = "like/deleteGame"
    __returning__ = bool

    access: str

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
