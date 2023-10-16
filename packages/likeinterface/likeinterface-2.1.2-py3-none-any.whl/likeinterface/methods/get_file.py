from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request
from likeinterface.types import File

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetFile(Method[File]):
    """
    Use this method to get file.

    Parameters
      Name            | Type   | Required | Description

      1. file_id      | String | Yes      | File ID in the system

    Result
      :class:`File`
    """

    __name__ = "file/getFile"
    __returning__ = File

    file_id: str

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
