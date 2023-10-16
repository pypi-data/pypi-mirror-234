from beni import bpath
from beni.bfunc import runThread
from beni.btype import XPath


async def remove(*paths: XPath):
    return await runThread(
        lambda: bpath.remove(*paths)
    )


async def make(*pathList: XPath):
    return await runThread(
        lambda: bpath.make(*pathList)
    )


async def clearDir(*dirList: XPath):
    return await runThread(
        lambda: bpath.clearDir(*dirList)
    )


async def copy(src: XPath, dst: XPath):
    return await runThread(
        lambda: bpath.copy(src, dst)
    )


async def copyMany(dataDict: dict[XPath, XPath]):
    return await runThread(
        lambda: bpath.copyMany(dataDict)
    )


async def movex(src: XPath, dst: XPath, force: bool = False):
    return await runThread(
        lambda: bpath.move(src, dst, force)
    )


async def moveMany(dataDict: dict[XPath, XPath], force: bool = False):
    return await runThread(
        lambda: bpath.moveMany(dataDict, force)
    )


async def listPath(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: bpath.listPath(path, recursive)
    )


async def listFile(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: bpath.listFile(path, recursive)
    )


async def listDir(path: XPath, recursive: bool = False):
    return await runThread(
        lambda: bpath.listDir(path, recursive)
    )
