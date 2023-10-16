from __future__ import annotations

from typing import Any, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Network:
    """
    Class describing access to different services.
    """

    base: str
    """Example: http://host:port/{method}"""
    file_base: Optional[str] = None
    """Example: http://host:port/file/{file_id}"""

    def url(self, **kwargs: Any) -> str:
        """
        Formats base url for request.

        :param kwargs: format kwargs
        :return: url
        """

        return self.base.format(**kwargs)

    def file(self, **kwargs: Any) -> str:
        """
        Formats base url for file.

        :param kwargs: format kwargs
        :return: url
        """

        if not self.file_base:
            raise RuntimeError("File service not specified")

        return self.file_base.format(**kwargs)
