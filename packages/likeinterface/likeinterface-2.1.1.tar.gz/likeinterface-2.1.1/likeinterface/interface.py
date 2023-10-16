from __future__ import annotations

from collections import defaultdict
from typing import Any, AsyncGenerator, Dict, Optional

from aiohttp.client import ClientSession

from likeinterface.methods import LikeType, Method
from likeinterface.network import Network
from likeinterface.session import Session


class Interface:
    def __init__(
        self,
        network: Network,
        *,
        session: Optional[ClientSession] = None,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.network = network
        self.session = Session(session=session, connect_kwargs=connect_kwargs)

    async def request(self, method: Method[LikeType], timeout: int = 60) -> LikeType:
        return await self.session.request(interface=self, method=method, timeout=timeout)

    async def stream(
        self,
        file_id: str,
        timeout: int = 60,
        chunk_size: int = 65536,
    ) -> AsyncGenerator[bytes, None]:
        return self.session.stream(
            interface=self,
            file_id=file_id,
            timeout=timeout,
            chunk_size=chunk_size,
        )
