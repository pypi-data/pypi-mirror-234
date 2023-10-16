from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from likeinterface.methods.base import Method, Request
from likeinterface.types import Player

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class AddGame(Method[bool]):
    """
    Use this method to add game.

    Parameters
      Name                             | Type                     | Required | Description

      1. access                        | String                   | Yes      | Game unique ID
      2. sb_bet                        | Integer                  | Yes      | Small blind bet
      3. bb_bet                        | Integer                  | Yes      | Big blind bet
      4. bb_mult                       | Integer                  | Yes      | For formula to join: stacksize >= bb_bet * bb_mult
      5. players                       | Array Of :class:`Player` | Yes      | Players in the game
      6. current                       | Integer                  | Yes      | Current player (index of players)
      7. on_start_all_player_are_allin | Boolean                  | Yes      | When blinds posted all players in allin state?
      8. min_raise                     | Integer                  | Yes      | Minimal raise
      9. round                         | Integer                  | Yes      | Round: can be - 0 preflop, 1 flop, 2 turn, 3 river, 4 showdown
      10. flop_dealt                   | Boolean                  | Yes      | Is flop dealt

    Result
      :class:`bool`
    """

    __name__ = "like/addGame"
    __returning__ = bool

    access: str
    sb_bet: int = 500
    bb_bet: int = 1000
    bb_mult: int = 20
    players: List[Player] = Field(default_factory=list)
    current: int = 0
    on_start_all_players_are_allin: bool = False
    min_raise: int = 1000
    round: int = 0
    flop_dealt: bool = False

    def request(self, interface: Interface) -> None:
        return Request(method=self.__name__, data=self.model_dump())
