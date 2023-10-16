from __future__ import annotations

import io
import os.path
from abc import ABC, abstractmethod
from pathlib import Path
from typing import AsyncGenerator, Optional, Union

import aiofiles

DEFAULT_CHUNK_SIZE = 64 * 1024  # 64 KB


class _AIterSupport:
    async def __aiter__(self) -> AsyncGenerator[bytes]:
        async for chunk in self.read():  # noqa
            yield chunk


class InputFile(ABC, _AIterSupport):
    def __init__(
        self, filename: Optional[str] = None, chunk_size: int = DEFAULT_CHUNK_SIZE
    ) -> None:
        self.filename = filename
        self.chunk_size = chunk_size

    @abstractmethod
    async def read(self) -> AsyncGenerator[bytes, ...]:
        ...


class FileSystemInputFile(InputFile):
    def __init__(
        self,
        path: Union[str, Path],
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        if filename is None:
            filename = os.path.basename(path)

        super(FileSystemInputFile, self).__init__(filename=filename, chunk_size=chunk_size)

        self.path = path

    async def read(self) -> AsyncGenerator[bytes, ...]:
        async with aiofiles.open(self.path, "rb") as file:
            while chunk := await file.read(self.chunk_size):
                yield chunk


class BufferedInputFile(InputFile):
    def __init__(
        self,
        data: bytes,
        filename: Optional[str] = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> None:
        super(BufferedInputFile, self).__init__(filename=filename, chunk_size=chunk_size)

        self.data = data

    async def read(self) -> AsyncGenerator[bytes, None]:
        buffer = io.BytesIO(self.data)
        while chunk := buffer.read(self.chunk_size):
            yield chunk
