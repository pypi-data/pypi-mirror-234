from __future__ import annotations

import asyncio
import inspect
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any

from beni import binput, bpath
from beni.bfunc import crcStr, toAny
from beni.btype import AsyncFuncType, Func


@asynccontextmanager
async def useFileLock(*keys: str, timeout: float = 0, quite: bool = False):
    import portalocker
    lock_list: list[portalocker.Lock] = []
    keyfile_list: list[Path] = []
    for key in keys:
        lock, keyfile = await _lock_acquire(key, timeout, quite)
        lock_list.append(lock)
        keyfile_list.append(keyfile)
    try:
        yield
    finally:
        for lock in lock_list:
            lock.release()
        for keyfile in keyfile_list:
            try:
                bpath.remove(keyfile)
            except:
                pass


async def _lock_acquire(key: str, timeout: float = 0, quite: bool = False):
    '''不对外部提供，只提供给 async_keylock 方法使用'''
    keyfile = bpath.workspace(f'.lock/{crcStr(key)}.lock')
    bpath.make(keyfile.parent)
    import portalocker
    while True:
        try:
            lock = portalocker.Lock(keyfile, timeout=timeout, fail_when_locked=timeout == 0)
            f = lock.acquire()
            f.write(key)
            f.flush()
            break
        except:
            if quite:
                raise Exception(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}')
            else:
                async def __retry(_):
                    print('正在重试...')

                async def __exit(_):
                    raise Exception(f'资源被锁定无法继续操作 - {key}')

                await binput.select(
                    ('重试', 'retry', None, __retry),
                    ('退出', 'exit', None, __exit),
                )
    return lock, keyfile


# ------------------------------------------------------------------------------------------------------------------------


def limit(value: int = 1):
    def wraperfun(func: AsyncFuncType) -> AsyncFuncType:
        @wraps(func)
        async def wraper(*args: Any, **kwargs: Any):
            funid = id(inspect.unwrap(func))
            if funid not in _limitDict:
                _limitDict[funid] = _Limit(value)
            try:
                await _limitDict[funid].wait()
                return await func(*args, **kwargs)
            finally:
                await _limitDict[funid].release()
        return toAny(wraper)
    return wraperfun


async def setLimit(func: Func, limit: int):
    funid = id(inspect.unwrap(func))
    if funid not in _limitDict:
        _limitDict[funid] = _Limit(limit)
    await _limitDict[funid].set_limit(limit)


_limitDict: dict[int, _Limit] = {}


class _Limit():

    _queue: asyncio.Queue[Any]
    _running: int

    def __init__(self, limit: int):
        self._limit = limit
        self._queue = asyncio.Queue()
        self._running = 0
        while self._queue.qsize() < self._limit:
            self._queue.put_nowait(True)

    async def wait(self):
        await self._queue.get()
        self._running += 1

    async def release(self):
        if self._queue.qsize() < self._limit:
            await self._queue.put(True)
        self._running -= 1

    async def set_limit(self, limit: int):
        self._limit = limit
        while self._running + self._queue.qsize() < self._limit:
            await self._queue.put(True)
        while self._running + self._queue.qsize() > self._limit:
            if self._queue.empty():
                break
            await self._queue.get()


# ------------------------------------------------------------------------------------------------------------------------


class RWLock():

    def __init__(self, maxNum: int) -> None:
        self._maxNum = maxNum
        self._readNum = 0
        self._writeNum = 0
        self._onReadFinished = asyncio.Event()
        self._onWriteFinished = asyncio.Event()

    def _getNum(self):
        return self._readNum + self._writeNum

    async def getRead(self):
        while True:
            if self._writeNum:
                self._onWriteFinished.clear()
                await self._onWriteFinished.wait()
            elif self._getNum() >= self._maxNum:
                self._onReadFinished.clear()
                await self._onReadFinished.wait()
            else:
                self._readNum += 1
                break

    def releaseRead(self):
        self._readNum -= 1
        if not self._readNum:
            self._onReadFinished.set()

    @asynccontextmanager
    async def useRead(self):
        await self.getRead()
        try:
            yield
        finally:
            self.releaseRead()

    async def getWrite(self):
        while True:
            if self._readNum:
                self._onReadFinished.clear()
                await self._onReadFinished.wait()
            elif self._writeNum:
                self._onWriteFinished.clear()
                await self._onWriteFinished.wait()
            else:
                self._writeNum += 1
                break

    def releaseWrite(self):
        self._writeNum -= 1
        self._onWriteFinished.set()

    @asynccontextmanager
    async def useWrite(self):
        await self.getWrite()
        try:
            yield
        finally:
            self.releaseWrite()
