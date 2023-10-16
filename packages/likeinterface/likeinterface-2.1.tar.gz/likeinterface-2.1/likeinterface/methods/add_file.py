from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from likeinterface.methods.base import Method
from likeinterface.types import File, InputFile

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class AddFile(Method[File]):
    """
    Use this method to add file.

    Parameters
      Name            | Type   | Required | Description

      1. access_token | String | Yes      | Auth access token
      2. file_name    | String | No       | File name in the system
      3. mime_type    | String | No       | File type in the system

    Result
      :class:`File`
    """

    __is_form__ = True
    __name__ = "file/addFile"
    __returning__ = File

    access_token: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file: InputFile

    def request(self, interface: Interface) -> None:
        return None
