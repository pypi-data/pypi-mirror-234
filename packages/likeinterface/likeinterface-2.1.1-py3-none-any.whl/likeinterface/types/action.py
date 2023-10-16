from __future__ import annotations

from likeinterface.types.base import LikeObject


class Action(LikeObject):
    """
    Player action.
    """

    amount: int
    """Action amount chips."""
    action: int
    """Selected action."""
    position: int
    """Player position (equals to game players index)."""
