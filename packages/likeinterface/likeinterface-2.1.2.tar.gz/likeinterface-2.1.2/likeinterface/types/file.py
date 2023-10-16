from __future__ import annotations

from typing import Optional

from pydantic import Field

from likeinterface.types.base import LikeObject


class File(LikeObject):
    file_id: str
    """File ID in the system."""
    file_name: Optional[str] = Field(max_length=256)
    """Specified file name."""
    file_size: int
    """File size in bytes."""
    mime_type: Optional[str] = None
    """File type."""
