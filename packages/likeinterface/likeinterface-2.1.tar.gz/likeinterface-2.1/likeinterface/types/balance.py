from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.types.base import LikeObject

if TYPE_CHECKING:
    from .user import User


class Balance(LikeObject):
    id: int
    """Balance ID in the system."""
    balance: int
    """Current balance for user."""
    user: User
    """Balance owner."""
