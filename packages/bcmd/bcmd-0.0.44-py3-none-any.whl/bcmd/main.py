import asyncio

from beni import btask

from .tasks import *


def run():
    btask.options.lock = 'bcmd'
    asyncio.run(btask.main())
