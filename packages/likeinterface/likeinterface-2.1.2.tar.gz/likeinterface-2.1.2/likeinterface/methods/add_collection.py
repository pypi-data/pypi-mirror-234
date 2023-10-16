from __future__ import annotations

from typing import TYPE_CHECKING, List

from likeinterface.methods.base import Method
from likeinterface.types import Collection, CollectionElement

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class AddCollection(Method[Collection]):
    """
    Use this method to add new card collection.

    Parameters
      Name                   | Type                                | Required | Description

      1. access_token        | String                              | Yes      | Auth access token
      2. name                | String                              | Yes      | Collection name
      3. collection_elements | Array Of :class:`CollectionElement` | Yes      | Collection set, requires all cards from Two Clubs to Ace Spades

    Result
      :class:`Collection`
    """

    __is_form__ = True
    __name__ = "collection/addCollection"
    __returning__ = Collection

    access_token: str
    name: str
    collection_elements: List[CollectionElement]

    def request(self, interface: Interface) -> None:
        return None
