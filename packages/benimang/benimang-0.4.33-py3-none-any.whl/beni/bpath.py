import os
import shutil
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path

from beni.btype import XPath


def get(path: XPath, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def user(expand: str = ''):
    return get(Path('~').expanduser(), expand)


def desktop(expand: str = ''):
    return user(f'Desktop/{expand}')


def workspace(expand: str = ''):
    if sys.platform == 'win32':
        return get(f'C:/beni-workspace/{expand}')
    else:
        return get(f'/data/beni-workspace/{expand}')


def tempFile():
    return workspace(f'temp/{uuid.uuid4()}.tmp')


def tempPath():
    return workspace(f'temp/{uuid.uuid4()}')


def changeRelative(target: XPath, fromRelative: XPath, toRelative: XPath):
    target = get(target)
    fromRelative = get(fromRelative)
    toRelative = get(toRelative)
    assert target.is_relative_to(fromRelative)
    return toRelative.joinpath(target.relative_to(fromRelative))


def openPath(path: XPath):
    os.system(f'start explorer {path}')


def remove(*paths: XPath):
    for path in paths:
        path = get(path)
        if path.is_file():
            path.unlink(True)
        elif path.is_dir():
            shutil.rmtree(path)


def make(*paths: XPath):
    for path in paths:
        path = get(path)
        path.mkdir(parents=True, exist_ok=True)


def clearDir(*dirList: XPath):
    for dir in dirList:
        remove(*[x for x in get(dir).iterdir()])


def copy(src: XPath, dst: XPath):
    src = get(src)
    dst = get(dst)
    make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


def copyMany(dataDict: dict[XPath, XPath]):
    for src, dst in dataDict.items():
        copy(src, dst)


def move(src: XPath, dst: XPath, force: bool = False):
    src = get(src)
    dst = get(dst)
    if dst.exists():
        if force:
            remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    make(dst.parent)
    os.rename(src, dst)


def moveMany(dataDict: dict[XPath, XPath], force: bool = False):
    for src, dst in dataDict.items():
        move(src, dst, force)


def renameName(src: XPath, name: str):
    src = get(src)
    src.rename(src.with_name(name))


def renameStem(src: XPath, stemName: str):
    src = get(src)
    src.rename(src.with_stem(stemName))


def renameSuffix(src: XPath, suffixName: str):
    src = get(src)
    src.rename(src.with_suffix(suffixName))


def listPath(path: XPath, recursive: bool = False):
    '获取指定路径下文件以及目录列表'
    path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


def listFile(path: XPath, recursive: bool = False):
    '获取指定路径下文件列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


def listDir(path: XPath, recursive: bool = False):
    '获取指定路径下目录列表'
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


@contextmanager
def useTempFile():
    file = tempFile()
    try:
        yield file
    finally:
        remove(file)


@contextmanager
def useTempPath(isMakePath: bool = False):
    path = tempPath()
    if isMakePath:
        make(path)
    try:
        yield path
    finally:
        remove(path)


@contextmanager
def changePath(path: XPath):
    path = Path(path)
    currentPath = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(currentPath)
