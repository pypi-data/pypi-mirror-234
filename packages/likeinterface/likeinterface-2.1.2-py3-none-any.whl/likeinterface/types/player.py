from __future__ import annotations

from likeinterface.types.base import LikeObject


class Player(LikeObject):
    id: int
    """Some player ID."""
    is_left: bool = False
    """Is player left from game."""
    stack: int
    """Current player stack."""
    behind: int
    """Stacksize in the game."""
    front: int
    """Posted chips in the game."""
    state: int
    """Player state (init, out, alive, allin)."""
