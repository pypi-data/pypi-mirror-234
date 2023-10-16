from __future__ import annotations

from enum import StrEnum
from typing import Final

import typer
from beni import bcolor, bfile, bpath, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def mirror(
    types: list[_MirrorsType] = typer.Argument(None, help="镜像的类型"),
    disabled: bool = typer.Option(False, '--disabled', '-d', help="是否禁用"),
):
    '设置镜像'
    if not types:
        # types = [_MirrorsType.pip, _MirrorsType.npm]
        types = [_MirrorsType.pip]
    for targetType in types:
        data = _mirrorsFiles[targetType]
        for file, msgAry in data.items():
            if disabled:
                bpath.remove(file)
                bcolor.printRed('删除文件', file)
            else:
                print()
                bcolor.printYellow(file)
                msg = '\n'.join(msgAry)
                await bfile.writeText(file, msg)
                bcolor.printMagenta(msg)


class _MirrorsType(StrEnum):
    pip = 'pip'
    # npm = 'npm'


_mirrorsFiles = {
    _MirrorsType.pip: {
        bpath.user('pip/pip.ini'): [
            '[global]',
            'index-url = https://mirrors.aliyun.com/pypi/simple',
        ],
    },
    # _MirrorsType.npm: {
    #     bpath.user('.bashrc'): [
    #         'registry=https://registry.npm.taobao.org/',
    #         'electron_mirror=https://npm.taobao.org/mirrors/electron/',
    #     ],
    # },
}
