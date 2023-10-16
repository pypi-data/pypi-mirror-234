import tomllib
import orjson
import json
import yaml
import os
import pickle
from pathlib import Path
from typing import Any

import aiofiles

from beni import bcolor, bfile, bfunc, bpath
from beni.btype import Null, XPath


async def writeText(file: XPath, content: str, encoding: str = 'utf8', newline: str = '\n'):
    file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


async def writeBytes(file: XPath, data: bytes):
    file = bpath.get(file)
    bpath.make(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


async def writeYaml(file: XPath, data: Any):
    await writeText(file, yaml.safe_dump(data))


async def writeJson(file: XPath, data: Any, mini: bool = True):
    if mini:
        content = bfunc.jsonDumpsMini(data)
    else:
        content = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    await writeText(file, content)


async def writePickle(file: XPath, data: Any):
    await writeBytes(file, pickle.dumps(data))


async def readText(file: XPath, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


async def readBytes(file: XPath):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


async def readYaml(file: XPath):
    return yaml.safe_load(
        await readText(file)
    )


async def readJson(file: XPath):
    return orjson.loads(await readBytes(file))


async def readPickle(file: XPath):
    return pickle.loads(
        await readBytes(file)
    )


async def readToml(file: XPath):
    return tomllib.loads(
        await readText(file)
    )


async def md5(file: XPath):
    return bfunc.md5Bytes(
        await readBytes(file)
    )


async def crc(file: XPath):
    return bfunc.crcBytes(
        await readBytes(file)
    )


async def makeFiles(content: str, output: Path = Null, key: str = '>>>'):
    if output is Null:
        output = Path(os.curdir).absolute()
    ary = content.split(key)
    ary = [x.strip() for x in ary]
    ary = [x for x in ary if x]
    ary.sort()
    for substr in ary:
        subAry = substr.replace('\r\n', '\n').split('\n')
        fileName = subAry.pop(0)
        file = output / fileName
        bcolor.printYellow(file)
        await bfile.writeText(
            file,
            '\n'.join(subAry).strip(),
        )
