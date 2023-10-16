from __future__ import annotations

from typing import TYPE_CHECKING

from likeinterface.enums import Services
from likeinterface.methods.base import Method, Request
from likeinterface.types import Balance

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class SetBalance(Method[Balance]):
    """
    Use this method to set new balance for user.

    Parameters
      Name       | Type    | Required | Description

      1. user_id | Integer | Yes      | User ID in the system.
      2. balance | Integer | Yes      | New user balance

    Result
      :class:`Balance`
    """

    __service_name__ = Services.BALANCE
    __name__ = "balance/setBalance"
    __returning__ = Balance

    user_id: int
    balance: int

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
