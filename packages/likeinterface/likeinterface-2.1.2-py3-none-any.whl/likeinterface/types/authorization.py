from __future__ import annotations

from likeinterface.types.base import LikeObject


class Authorization(LikeObject):
    access_token: str
    """Token used in the system for authorization."""
