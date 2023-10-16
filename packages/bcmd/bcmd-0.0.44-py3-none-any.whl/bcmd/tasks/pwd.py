import getpass
import json
import time
import uuid
from typing import Final

import jwt
import pyperclip
from beni import bcolor, btask
from beni.bfunc import magicSequence, syncCall
from rich.console import Console

app: Final = btask.newSubApp('lib 工具')


@app.command()
@syncCall
async def encode():
    '生成密文（JSON内容需要先复制到剪贴板）'
    content = pyperclip.paste()
    try:
        data = json.loads(content)
    except:
        return btask.abort('剪贴板内容并非JSON格式', content)
    Console().print_json(data=data, indent=4, ensure_ascii=False, sort_keys=True)
    password = ''
    while not password:
        password = getpass.getpass('输入密码：')
    while password != getpass.getpass('再次密码：'):
        pass
    data[str(uuid.uuid4())] = time.time()
    result = jwt.encode(data, password, algorithm='HS256')
    result = magicSequence(result)
    pyperclip.copy(result)
    print('密文已复制到剪贴板')
    bcolor.printYellow(result)
    bcolor.printGreen('OK')
    # {"uuu": "xxx", "ppp": "xxx"}


@app.command()
@syncCall
async def decode():
    '还原密文内容'
    content = pyperclip.paste()
    bcolor.printYellow(content)
    content = magicSequence(content)
    password = ''
    while not password:
        password = getpass.getpass('输入密码：')
    try:
        data = jwt.decode(content, password, algorithms=['HS256'])
        Console().print_json(data=data, indent=4, ensure_ascii=False, sort_keys=True)
    except:
        return btask.abort('无法解析密文')
