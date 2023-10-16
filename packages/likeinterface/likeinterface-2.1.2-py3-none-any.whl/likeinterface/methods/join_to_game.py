from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request
from likeinterface.types import Game

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class JoinToGame(Method[Game]):
    """
    Use this method to join to game.

    Parameters
      Name         | Type    | Required | Description

      1. access    | String  | Yes      | Game unique ID
      2. id        | Integer | Yes      | Some player ID
      3. stacksize | Integer | Yes      | Start player stack size, should be greater than X * Big Blind Bet in the game

    Result
      :class:`Game`
    """

    __name__ = "like/joinToGame"
    __returning__ = Game

    access: str
    id: int
    stacksize: int

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
