import pytest
from beni import bcache

_num = 0


@pytest.mark.asyncio
async def test():
    assert await _myfunc(1, 2) == 3
    assert await _myfunc(1, 2) == 3
    assert _num == 1
    assert await _myfunc(3, 4) == 7
    assert _num == 2
    bcache.clear(_myfunc)
    assert await _myfunc(3, 4) == 7
    assert _num == 3


@bcache.cache
async def _myfunc(a: int, b: int):
    global _num
    _num += 1
    return a + b
