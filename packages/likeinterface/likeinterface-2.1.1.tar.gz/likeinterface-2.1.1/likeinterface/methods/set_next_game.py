from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from likeinterface.methods.base import Method, Request
from likeinterface.types import Cards

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class SetNextGame(Method[bool]):
    """
    Use this method to set next game.

    Parameters
      Name            | Type           | Required | Description

      1. access       | String         | Yes      | Game unique ID
      2. find_winners | Boolean        | No       | If players joined to game or left then just start new game
      3. cards        | :class:`Cards` | No       | Required :ref:`SetNextGame.find_winners` on true

    Result
      :class:`bool`
    """

    __name__ = "like/setNextGame"
    __returning__ = bool

    access: str
    find_winners: bool = False
    cards: Optional[Cards] = None

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
