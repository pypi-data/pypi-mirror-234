from __future__ import annotations

import json
from http import HTTPStatus
from typing import cast

from pydantic import ValidationError

from likeinterface.exceptions import DecodeError, LikeAPIError
from likeinterface.methods import LikeType, Method, Response


def response_validator(
    method: Method[LikeType],
    status_code: int,
    content: str,
) -> Response[LikeType]:
    try:
        json_data = json.loads(content)
    except Exception as e:
        raise DecodeError("Failed to decode object", e, content)

    try:
        response = method.response(json_data)
    except ValidationError as e:
        raise DecodeError("Failed to deserialize object", e, json_data)

    if HTTPStatus.OK <= status_code <= HTTPStatus.IM_USED and response.ok:
        return response

    error = cast(str, response.error)

    raise LikeAPIError("Exception %s: %s." % (method, error))
