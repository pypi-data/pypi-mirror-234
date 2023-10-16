import time
from datetime import datetime as Datetime
from datetime import timezone
from typing import Final
from zoneinfo import ZoneInfo

import typer
from beni import bcolor, btask
from beni.bfunc import syncCall
from beni.btype import Null

app: Final = btask.app


@app.command('time')
@syncCall
async def showtime(values: list[str] = typer.Argument(None)):
    '''
    格式化时间戳\n
    beni time\n
    beni time 1632412740\n
    beni time 1632412740.1234\n
    beni time 2021-9-23\n
    beni time 2021-9-23 09:47:00\n
    '''
    values = values or []
    btask.check(len(values) <= 2, '参数过多')
    value1: str | None = values[0] if len(values) >= 1 else None
    value2: str | None = values[1] if len(values) >= 2 else None
    timestamp: float = Null
    if not value1:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value1)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value1} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value1}', '%Y-%m-%d').timestamp()
            except:
                pass
    if not timestamp:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msg_ary = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msg_ary = [x.strip() for x in msg_ary]
        typer.secho('\n'.join(msg_ary), fg=color)
        return
    print()
    bcolor.printMagenta(timestamp)
    print()
    # localtime = time.localtime(timestamp)
    # tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    # bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colors=[Fore.YELLOW])
    # print()
    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Shanghai',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        if tzname == 'Asia/Shanghai':
            bcolor.printYellow(f'{datetime_tz} {tzname} {dstStr}')
        else:
            print(f'{datetime_tz} {tzname} {dstStr}')
