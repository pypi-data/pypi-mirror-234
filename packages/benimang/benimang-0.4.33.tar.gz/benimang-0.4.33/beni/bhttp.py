import asyncio
from http.cookiejar import CookieJar
from typing import Any, Final
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener, install_opener

import aiofiles
import aiohttp
import orjson

from beni import block, bpath
from beni.btype import Null, XPath

_limit: Final = 5
_retry = 3
_headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}


def _makeHttpHeaders(headers: dict[str, Any] | None = None):
    if headers:
        return _headers | headers
    else:
        return dict(_headers)


@block.limit(_limit)
async def get(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    retry = retry or _retry
    while True:
        retry -= 1
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=_makeHttpHeaders(headers), timeout=timeout) as response:
                    result = await response.read()
                    if not result:
                        await asyncio.sleep(0.5)
                        raise Exception('http get result is empty')
                    return result, response
        except:
            if retry <= 0:
                raise


async def getBytes(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    resultBytes, _ = await get(
        url,
        headers=headers,
        timeout=timeout,
        retry=retry,
    )
    return resultBytes


async def getStr(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    result = await getBytes(url, headers=headers, timeout=timeout, retry=retry)
    return result.decode()


async def getJson(
    url: str,
    *,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    result = await getBytes(url, headers=headers, timeout=timeout, retry=retry)
    return orjson.loads(result)


@block.limit(_limit)
async def post(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    retry = retry or _retry
    while True:
        retry -= 1
        try:
            postData = data
            if type(data) is dict:
                postData = urlencode(data).encode()
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=postData, headers=_makeHttpHeaders(headers), timeout=timeout) as response:
                    result = await response.read()
                    if not result:
                        await asyncio.sleep(0.5)
                        raise Exception('http get result is empty')
                    return result, response
        except:
            if retry <= 0:
                raise


async def postBytes(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    resultBytes, _ = await post(
        url,
        data=data,
        headers=headers,
        timeout=timeout,
        retry=retry,
    )
    return resultBytes


async def postStr(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    return (await postBytes(
        url,
        data=data,
        headers=headers,
        timeout=timeout,
        retry=retry,
    )).decode()


async def postJson(
    url: str,
    *,
    data: bytes | dict[str, Any] = Null,
    headers: dict[str, Any] = Null,
    timeout: int = 10,
    retry: int = Null,
):
    return orjson.loads(
        await postBytes(
            url,
            data=data,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )
    )


@block.limit(_limit)
async def download(url: str, file: XPath, timeout: int = 300):
    # total_size: int = 0
    # download_size: int = 0
    try:
        file = bpath.get(file)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=_headers, timeout=timeout) as response:
                bpath.make(file.parent)
                assert response.content_length, '下载内容为空'
                # total_size = response.content_length
                async with aiofiles.open(file, 'wb') as f:
                    while True:
                        data = await response.content.read(1024 * 1024)
                        if data:
                            await f.write(data)
                            # download_size += len(data)
                        else:
                            break
        # 注意：因为gzip在内部解压，所以导致对不上
        # assert total_size and total_size == download_size, '下载为文件不完整'
    except:
        bpath.remove(file)
        raise


def setDefaultRetry(value: int):
    global _retry
    _retry = value


def setDefaultHeaders(value: dict[str, Any]):
    global _headers
    _headers = value


# Cookie
_cookie = CookieJar()
_cookieProc = HTTPCookieProcessor(_cookie)
_opener = build_opener(_cookieProc)
install_opener(_opener)
