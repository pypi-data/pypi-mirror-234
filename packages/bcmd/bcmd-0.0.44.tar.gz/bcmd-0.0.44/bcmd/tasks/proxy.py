from __future__ import annotations

from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def proxy(
    port: int = typer.Option(15236, help="代理服务器端口"),
):
    '生成终端设置代理服务器的命令'
    msg = '\r\n'.join([
        f'set http_proxy=http://localhost:{port}',
        f'set https_proxy=http://localhost:{port}',
        f'set all_proxy=http://localhost:{port}',
        '',
    ])
    bcolor.printMagenta('\r\n' + msg)
    pyperclip.copy(msg)
    bcolor.printYellow('已复制，可直接粘贴使用')
