from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from likeinterface.types.base import LikeObject

if TYPE_CHECKING:
    from .collection_element import CollectionElement
    from .user import User


class Collection(LikeObject):
    id: int
    """Collection ID in the system."""
    name: str
    """Unique collection name."""
    user: Optional[User] = None
    """Collection creator."""
    collection_elements: List[CollectionElement]
    """Collection elements."""
