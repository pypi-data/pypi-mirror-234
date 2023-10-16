from __future__ import annotations

from likeinterface.types.base import LikeObject


class Hand(LikeObject):
    """
    Winner hand.
    """

    id: int
    """Winner id. Index for hands from request."""
    hand: str
    """Player combination"""
