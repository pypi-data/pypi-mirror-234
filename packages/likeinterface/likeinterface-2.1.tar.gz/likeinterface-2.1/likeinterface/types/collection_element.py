from __future__ import annotations

from likeinterface.enums import Rank, Suit
from likeinterface.types.base import LikeObject


class CollectionElement(LikeObject):
    file_id: str
    """File ID in the system."""
    rank: Rank
    """Card rank."""
    suit: Suit
    """Card suit."""
