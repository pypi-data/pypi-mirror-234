from __future__ import annotations

from typing import Optional

from likeinterface.types.base import LikeObject


class User(LikeObject):
    id: int
    """User ID in the system."""
    telegram_id: int
    """User Telegram ID."""
    username: Optional[str]
    """Optional. Username in the system."""
    photo_url: Optional[str]
    """Optional. User photo."""
    first_name: str
    """User first name."""
    last_name: Optional[str] = None
    """Optional. User second name."""
    full_name: str
    """User first and second names."""
