import getpass

import jwt
from beni.bfunc import magicSequence, tryRun


def getPypi() -> tuple[str, str]:
    while True:
        with tryRun():
            data = _getData(
                '输入密钥用户（pypi）',
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJlbmltYW5nIiwicGFzc3dvIjoxNjk2OTIxNDg3Ljg2NzY5MTN9.WvtsFXFB0fk7GTj01tfed1BF-gmDv-3U4bVmcN2wT9wcmQiOiJweXBpMDA5OTg4IiwiODVlYmMwMmQtZDg4MS00NWJiLWE3ZjktNTdkZDA1YjJiNjg2'
            )
            return data['username'], data['password']


def getQiniu() -> tuple[str, str]:
    while True:
        with tryRun():
            data = _getData(
                '输入密钥用户（七牛云）',
                'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhayI6Ik8td1lkdzA1Q05fLThoLUFKYmZDWTRqN2VoRkJTcEdiQTlyNlhOUk4iLCJzayI6InQxZWI5ZDI4YzNhZWMiOjE2OTY5MjI0MjAuNTgzMzkzNn0.4pn5edULuUmgo_pTpcoPE1Cxwxq5W81CjSeTCmnaEyEyNjAtck5ZUlJNZ29tSUcwZ0Rtakp2T2o1VmNjdTFWMzJHZHFFY2UiLCIyMzE4NmNlMy01MTI0LTRjMWItYjIzZC0'
            )
            return data['ak'], data['sk']


def _getData(tips: str, content: str):
    content = magicSequence(content)
    while True:
        with tryRun():
            pwd = getpass.getpass(f'{tips}：')
            return jwt.decode(content, pwd, algorithms=['HS256'])
