from math import nan
from typing import Final

import typer
from beni import bcolor, btask
from beni.bfunc import Counter, syncCall, toFloat
from prettytable import PrettyTable

app: Final = btask.newSubApp('math 工具集')


@app.command()
@syncCall
async def scale(
    a: float = typer.Argument(..., help='原始数值'),
    b: float = typer.Argument(..., help='原始数值'),
    c: str = typer.Argument(..., help='数值 或 ?'),
    d: str = typer.Argument(..., help='数值 或 ?'),
):
    '按比例计算数值，例子：beni math scale 1 2 3 ?'
    if not ((c == '?') != (d == '?')):
        return bcolor.printRed('参数C和参数D必须有且仅有一个为?')
    print()
    table = PrettyTable(
        title=bcolor.yellow('按比例计算数值'),
    )
    if c == '?':
        dd = toFloat(d)
        cc = a * dd / b
        table.add_rows([
            ['A', a, bcolor.magenta(str(cc)), bcolor.magenta('C')],
            ['B', b, dd, 'D'],
        ])
    elif d == '?':
        cc = toFloat(c)
        dd = b * cc / a
        table.add_rows([
            ['A', a, cc, 'C'],
            ['B', b, bcolor.magenta(str(dd)), bcolor.magenta('D')],
        ])
    print(table.get_string(header=False))


@app.command()
@syncCall
async def increase(
    old: float = typer.Argument(nan, help='原始数值'),
    new: float = typer.Argument(nan, help='新数值'),
):
    '''
    计算增长率

    例子：beni math increase 123 456

    例子（连续对话）：beni math increase
    '''
    if old is not nan and new is not nan:
        value = (new - old) / old
        if value > 0:
            valueStr = bcolor.red(f'{value*100:+,.3f}%')
        else:
            valueStr = bcolor.green(f'{value*100:+,.3f}%')
        table = PrettyTable(
            title=bcolor.yellow('计算增长率'),
        )
        table.add_rows([
            ['旧数值', f'{old:,}'],
            ['新数值', f'{new:,}'],
            ['增长率', valueStr],
        ])
        print()
        print(table.get_string(header=False))
    elif old is nan and new is nan:
        while True:
            print()
            value = input('输入2个数值，空格分隔，退出输入 [exit] ：').strip()
            if value == 'exit':
                break
            try:
                ary = value.split(' ')
                ary = [float(x) for x in ary if x]
                assert len(ary) == 2, '参数必须要2个数值'
                increase(ary[0], ary[1])
            except Exception as e:
                bcolor.printRed(e)
    else:
        btask.abort('参数错误，不传参数，或者传入2个数值参数')


@app.command()
@syncCall
async def discount(
    values: list[str] = typer.Argument(..., help='每组数据使用#作为分隔符，注意后面的数据不能为0，例：123#500'),
):
    '计算折扣，例子：beni math discount 123#500 130#550'
    btask.check(len(values) >= 2, '至少需要提供2组数据用作比较')

    class Data:
        def __init__(self, value: str):
            try:
                ary = [x.strip() for x in value.strip().split('#')]
                self.a = float(ary[0])
                self.b = float(ary[1])
                self.v = self.a / self.b
                self.discount = 0.0
            except:
                btask.abort(f'数据格式错误', value)

    datas = [Data(x) for x in values]
    table = PrettyTable(
        title=bcolor.yellow('计算折扣'),
    )
    vAry = [x.v for x in datas]
    minV = min(vAry)
    maxV = max(vAry)
    for data in datas:
        data.discount = -(maxV - data.v) / maxV
    table.add_column(
        '',
        [
            '前数据',
            '后数据',
            '单价',
            '折扣',
        ],
    )
    counter = Counter(-1)
    for data in datas:
        colorFunc = bcolor.white
        if data.v == minV:
            colorFunc = bcolor.green
        elif data.v == maxV:
            colorFunc = bcolor.red
        columns = [
            f'{data.a:,}',
            f'{data.b:,}',
            f'{data.v:,.3f}',
            f'{data.discount*100:+,.3f}%' if data.discount else '',
        ]
        table.add_column(
            chr(65 + counter()),
            [colorFunc(x) for x in columns],
        )
    print(table.get_string())
