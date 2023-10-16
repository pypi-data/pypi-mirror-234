import os
import re
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, bpath, btask
from beni.bfunc import syncCall

from bcmd.common import password

app: Final = btask.newSubApp('lib 工具')


@app.command()
@syncCall
async def tidy(
    workspace_path: Path = typer.Argument(None, help='workspace 路径'),
):
    '整理 pyproject.toml 里面的 dependencies'
    pyprojectTomlFile = workspace_path / 'pyproject.toml'
    venvLockFile = bpath.get(workspace_path, './../venv.lock')
    btask.check(pyprojectTomlFile.is_file(), 'pyproject.toml 不存在', pyprojectTomlFile)
    btask.check(venvLockFile.is_file(), 'venv.lock 不存在', venvLockFile)
    ary = (await bfile.readText(venvLockFile)).strip().replace('\r\n', '\n').split('\n')
    replaceContent = '\n'.join([f"  '{x}'," for x in ary])
    content = await bfile.readText(pyprojectTomlFile)
    content = re.sub(r'dependencies = \[(.*?)\]', f"dependencies = [\n{replaceContent}\n]", content, 0, re.DOTALL)
    await bfile.writeText(pyprojectTomlFile, content)
    bcolor.printYellow(pyprojectTomlFile)
    bcolor.printMagenta(content)


@app.command()
@syncCall
async def version(
    workspace_path: Path = typer.Argument(None, help='workspace 路径'),
    disabled_commit: bool = typer.Option(False, '--disabled-commit', '-d', help='是否提交git'),
):
    '修改 pyproject.toml 版本号'
    if not workspace_path:
        workspace_path = Path.cwd()
    file = workspace_path / 'pyproject.toml'
    btask.check(file.is_file(), '文件不存在', file)
    data = await bfile.readToml(file)
    version = data['project']['version']
    versionList = [int(x) for x in version.split('.')]
    versionList[-1] += 1
    newVersion = '.'.join([str(x) for x in versionList])
    content = await bfile.readText(file)
    if f"version = '{version}'" in content:
        content = content.replace(f"version = '{version}'", f"version = '{newVersion}'")
    elif f'version = "{version}"' in content:
        content = content.replace(f'version = "{version}"', f'version = "{newVersion}"')
    else:
        raise Exception('版本号修改失败，先检查文件中定义的版本号格式是否正常')
    await bfile.writeText(file, content)
    if not disabled_commit:
        os.system(
            rf'TortoiseGitProc.exe /command:commit /path:{file} /logmsg:"更新版本号 {newVersion}"'
        )


@app.command()
@syncCall
async def publish(
    src_path: Path = typer.Argument(None, help='src 路径'),
    keep_build_files: bool = typer.Option(False, '--keep-build-files', '-k', help='是否保留构建文件'),
):
    '发布项目'

    # 获取用户名和密码
    u, p = password.getPypi()

    if not src_path:
        src_path = Path.cwd()
    src_path = src_path.resolve()

    def removeUnusedPath():
        bpath.remove(src_path / 'dist')
        paths = bpath.listDir(src_path)
        for x in paths:
            if x.name.endswith('.egg-info'):
                bpath.remove(x)

    try:
        with bpath.changePath(src_path):
            removeUnusedPath()
            scriptPath = (src_path / './../venv/Scripts').resolve()
            os.system(f'{scriptPath / "pip.exe"} install setuptools -U -i https://mirrors.aliyun.com/pypi/simple')
            os.system(f'{scriptPath / "python.exe"} -m build')
            os.system(f'{scriptPath / "twine.exe"} upload dist/* -u {u} -p {p}')
    finally:
        if not keep_build_files:
            removeUnusedPath()
