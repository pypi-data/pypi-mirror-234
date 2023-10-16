from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class AddGame(Method[bool]):
    """
    Use this method to start/restart game.

    Parameters
      Name                             | Type                     | Required | Description

      1. access                        | String                   | Yes      | Game unique ID
      2. is_new_game | Boolean | Yes | Is need to rotate players positions?

    Result
      :class:`bool`
    """

    __name__ = "like/adjustGame"
    __returning__ = bool

    access: str
    is_new_game: bool = False

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
