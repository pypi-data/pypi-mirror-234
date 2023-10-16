from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from likeinterface.methods.base import Method, Request
from likeinterface.types import Authorization

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class SignIn(Method[Authorization]):
    """
    Use this method to sign in a user with a validated email address

    Parameters
      Name           | Type    | Required | Description

      1. telegram_id | Integer | Yes      | User ID
      2. first_name  | String  | Yes      | User first name
      3. second_name | String  | No       | User second name
      4. username    | String  | No       | Username
      5. photo_url   | String  | No       | User photo url
      6. auth_date   | Integer | Yes      | User authorization date
      7. hash        | String  | Yes      | Hash of all fields

    Result
      :class:`Authorization`
    """

    __name__ = "auth/signIn"
    __returning__ = Authorization

    telegram_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str

    def request(self, interface: Interface) -> Request:
        return Request(method=self.__name__, data=self.model_dump())
