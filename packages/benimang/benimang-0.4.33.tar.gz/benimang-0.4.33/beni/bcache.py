from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any

from beni.bfunc import crcData, getWrapped, toAny
from beni.btype import AsyncFunc, AsyncFuncType


def cache(func: AsyncFuncType) -> AsyncFuncType:
    @wraps(func)
    async def wraper(*args: Any, **kwargs: Any):
        baseFunc = getWrapped(func)
        cacheData = _caches.get(baseFunc)
        if not cacheData:
            cacheData = _CacheData()
            _caches[baseFunc] = cacheData
        key = (args, kwargs)
        while True:
            result = cacheData.get(key)
            if result is None:
                async with cacheData.lock():
                    result = await func(*args, **kwargs)
                    cacheData.set(key, result)
                    return result
            else:
                return result
    return toAny(wraper)


def clear(func: AsyncFunc):
    baseFunc = getWrapped(func)
    if baseFunc in _caches:
        del _caches[baseFunc]


_caches: dict[AsyncFunc, _CacheData] = {}
_Key = tuple[tuple[Any, ...], dict[str, Any]]


class _CacheData:

    def __init__(self) -> None:
        self._event = asyncio.Event()
        self._running = False
        self._results: dict[str, Any] = {}

    def get(self, key: _Key):
        return self._results.get(crcData(key))

    def set(self, key: _Key, result: Any):
        self._results[crcData(key)] = result

    @asynccontextmanager
    async def lock(self):
        if self._running:
            await self._event.wait()
        self._running = True
        try:
            yield
        finally:
            self._running = False
            self._event.set()
            self._event.clear()
