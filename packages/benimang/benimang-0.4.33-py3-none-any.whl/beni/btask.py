import inspect
import re
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime as Datetime
from pathlib import Path
from types import FrameType
from typing import Any, Final, cast

import nest_asyncio
from colorama import Fore
from typer import Typer

from beni import bcolor, bfunc, block, blog, bpath, btime
from beni.btype import Null

app = Typer()

nest_asyncio.apply()


@dataclass
class _Options:
    lock: str = 'btask'
    logPath: Path = Null
    binPath: Path = Null
    logFilesLimit: int = 100


options: Final = _Options()
isShowSummary: bool = False

_subApps: list[Typer] = []


def newSubApp(help: str):
    frame = (cast(FrameType, inspect.currentframe())).f_back
    assert frame
    fileName = Path(inspect.getframeinfo(frame).filename).stem
    subAppName = re.sub(r'(?<!^)(?=[A-Z])', '-', fileName).lower()
    subApp = Typer(name=subAppName, help=help)
    _subApps.append(subApp)
    return subApp


async def main():
    async with _task():
        try:
            for subApp in _subApps:
                app.add_typer(subApp)
            app()
        except BaseException as ex:
            if type(ex) is SystemExit and ex.code in (0, 2):
                # 0 - 正常结束
                # 2 - Error: Missing command.
                pass
            else:
                raise


@asynccontextmanager
async def _task():
    _checkVscodeVenv()
    # bfunc.sysUtf8() # 由于不是每次都需要用到，界面显示了不美观 Active code page: 65001
    if options.binPath:
        bfunc.addEnvPath(options.binPath)
    async with block.useFileLock(options.lock):
        start_time = Datetime.now()
        bfunc.initErrorFormat()
        if options.logPath:
            logFile = bpath.get(options.logPath, btime.datetimeStr('%Y%m%d_%H%M%S.log'))
            assert logFile.is_file(), f'日志文件创建失败（已存在） {logFile}'
        else:
            logFile = None
        try:
            blog.init(logFile=logFile)
            yield
        except _AbortException as ex:
            bcolor.printRed(ex.msg)
        except BaseException as ex:
            bcolor.set(Fore.LIGHTRED_EX)
            blog.error(str(ex))
            blog.error('执行失败')
            raise
        finally:
            if isShowSummary:
                criticalNum = blog.getCountCritical()
                errorNum = blog.getCountError()
                warningNum = blog.getCountWarning()
                if criticalNum:
                    color = Fore.LIGHTMAGENTA_EX
                elif errorNum:
                    color = Fore.LIGHTRED_EX
                elif warningNum:
                    color = Fore.YELLOW
                else:
                    color = Fore.LIGHTGREEN_EX
                msgAry = ['', '-' * 75]
                if criticalNum:
                    msgAry.append(f'critical：{criticalNum}')
                if errorNum:
                    msgAry.append(f'error：{errorNum}')
                if warningNum:
                    msgAry.append(f'warning：{warningNum}')
                duration = str(Datetime.now() - start_time)
                if duration.startswith('0:'):
                    duration = '0' + duration
                msgAry.append(f'任务结束（{duration}）')
                bcolor.set(color)
                blog.info('\n'.join(msgAry))

            # 删除多余的日志
            try:
                if logFile:
                    logFileAry = list(logFile.parent.glob('*.log'))
                    logFileAry.remove(logFile)
                    logFileAry.sort()
                    logFileAry = logFileAry[options.logFilesLimit:]
                    bpath.remove(*logFileAry)
            except:
                pass


def _checkVscodeVenv():
    par = '--vscode-venv'
    if par in sys.argv:
        sys.argv.remove(par)
        sys.orig_argv.remove(par)
        input('回车后继续（为了兼容vscode venv问题）...')


def abort(*errorMsgs: Any):
    msg = '\n'.join([str(x) for x in errorMsgs])
    if not msg:
        raise Exception('程序中断，未提供错误信息')
    raise _AbortException(msg)


def check(ok: bool, *errorMsgs: Any):
    if not ok:
        msg = '\n'.join([str(x) for x in errorMsgs])
        if not msg:
            raise Exception('发生错误，未提供错误信息')
        abort(msg)


class _AbortException(BaseException):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg
