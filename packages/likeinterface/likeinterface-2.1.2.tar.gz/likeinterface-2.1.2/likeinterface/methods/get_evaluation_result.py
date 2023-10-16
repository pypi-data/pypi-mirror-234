from __future__ import annotations

from typing import TYPE_CHECKING, List

from likeinterface.methods.base import Method, Request
from likeinterface.types import Cards, Hand

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetEvaluationResult(Method[List[Hand]]):
    """
    Use this method to evaluate hands.

    Parameters
      Name     | Type           | Required | Description

      1. cards | :class:`Cards` | Yes      | Cards in the game

    Result
      Array of :class:`Hand`
    """

    __name__ = "like/getEvaluationResult"
    __returning__ = List[Hand]

    cards: Cards

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
