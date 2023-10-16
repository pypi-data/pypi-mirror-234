from __future__ import annotations

from typing import List

from likeinterface.types import LikeObject


class Cards(LikeObject):
    board: List[str]
    """Board in the game: ["3h", "4h", "5h", "6h", "7h"]"""
    hands: List[str]
    """Players hands: ["AcAh", "2h7d"]"""
