from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.methods.base import Method, Request
from likeinterface.types import Collection

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class GetCollection(Method[Collection]):
    """
    Use this method to get card collection.

    Parameters
      Name       | Type    | Required | Description

      1. name    | String  | Yes      | Collection name

    Result
      :class:`Collection`
    """

    __name__ = "collection/getCollection"
    __returning__ = Collection

    name: str

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
