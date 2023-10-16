from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class LeftFromGame(Method[bool]):
    """
    Use this method to left from game. Sets available actions to: fold, check only

    Parameters
      Name        | Type    | Required | Description

      1. access   | String  | Yes      | Game unique ID
      2. position | Integer | Yes      | Player position in the game (index of game players)

    Result
      :class:`bool`
    """

    __name__ = "like/leftFromGame"
    __returning__ = bool

    access: str
    position: int

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
