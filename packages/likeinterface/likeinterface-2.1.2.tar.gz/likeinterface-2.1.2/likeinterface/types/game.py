from __future__ import annotations

from typing import TYPE_CHECKING, List

from likeinterface.types.base import LikeObject

if TYPE_CHECKING:
    from .player import Player


class Game(LikeObject):
    sb_bet: int
    """Small blind bet."""
    bb_bet: int
    """Big blind bet."""
    bb_mult: int
    """Formula to join: stacksize >= bb_bet * bb_mult."""
    players: List[Player]
    """Players in the game."""
    current: int
    """Current player (index of players)."""
    on_start_all_players_are_allin: bool
    """Players posted blinds and they in the allin state."""
    min_raise: int
    """Minimal raise."""
    round: int
    """Round: can be - 0 preflop, 1 flop, 2 turn, 3 river, 4 showdown."""
    flop_dealt: bool
    """Is flop dealt."""
