from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, binput, bpath, btask
from beni.bfunc import syncCall
from beni.btype import Null

from . import bin, venv

app: Final = btask.newSubApp('BTask 工具')


_templateFolder: Final = bpath.get(__file__, './../../data/task_template')
_ignoreFolders: Final = {'.git', 'bin', 'venv', '__pycache__', 'node_modules'}
_renameSuffixs: Final = {'.py'}
_renameNames: Final = {'.gitignore'}


@app.command()
@syncCall
async def template_gen(
    source_folder: Path = typer.Argument(None, help="用于生成模板的文件夹路径"),
    output_folder: Path = typer.Argument(None, help="导出文件路径"),
    is_quiet: bool = typer.Option(False, '--quiet', help="是否静默模式"),
):
    '生成模板'
    with bpath.useTempPath() as tempPath:
        print(output_folder)
        if not is_quiet:
            if output_folder.exists():
                await binput.confirm('当前导出文件路径，是否确认覆盖？')
        _copyTemplateFiles(source_folder, tempPath)
        bpath.move(tempPath, output_folder, True)
        bcolor.printGreen('OK')


def _copyTemplateFiles(src: Path, dst: Path):
    files = bpath.listFile(src)
    for file in files:
        toFile = dst / file.name
        if toFile.suffix in _renameSuffixs or toFile.name in _renameNames:
            toFile = toFile.with_name(toFile.name + 'xx')
        bpath.copy(file, toFile)
    folders = bpath.listDir(src)
    for folder in folders:
        if folder.name in _ignoreFolders:
            continue
        _copyTemplateFiles(folder, dst / folder.name)


@app.command()
@syncCall
async def create(
    tempalte_name: str = typer.Argument(..., help="模板名称"),
    project_path: Path = typer.Argument(None, help="项目路径，不填标识在当前目录创建"),
):
    '创建项目'
    if Path(tempalte_name).is_absolute():
        btask.abort(f'模板名称不能为绝对路径：{tempalte_name}')
    templateFolder = bpath.get(_templateFolder, tempalte_name)
    if not templateFolder.is_dir():
        btask.abort(f'模板不存在：{tempalte_name}')
    if not project_path:
        project_path = Path.cwd()
    if project_path.exists():
        await binput.confirm(f'项目路径 {project_path} 已存在，是否覆盖？')
    for item in bpath.listPath(templateFolder):
        toItem = project_path / item.name
        bpath.copy(item, toItem)

    # 将 xx 结尾的文件名去掉 xx
    for file in bpath.listFile(project_path, True):
        if file.name.endswith('xx'):
            bpath.renameName(file, file.name[:-2])

    init(project_path)


@app.command()
@syncCall
async def init(
    project_path: Path = typer.Argument(None, help="项目路径"),
):
    '初始化 BTask 项目，包括 venv 和 bin 操作'
    if not project_path:
        project_path = Path.cwd()
    fileList = bpath.listFile(project_path, True)
    for file in fileList:
        if file.name == 'venv.list':
            targetPath = file.parent
            venv.venv(
                packages=Null,
                path=targetPath,
                disabled_mirror=False,
                quiet=True,
            )
            binListFile = targetPath / 'bin.list'
            if binListFile.is_file():
                bin.download(
                    names=Null,
                    file=binListFile,
                    output=targetPath / 'bin',
                )


@app.command()
@syncCall
async def tidy(
    tasks_path: Path = typer.Argument(None, help="tasks 路径"),
):
    '整理 tasks 文件'
    initFile = tasks_path / '__init__.py'
    btask.check(initFile.is_file(), '文件不存在', initFile)
    files = bpath.listFile(tasks_path)
    files = [x for x in files if not x.name.startswith('_')]
    contents = [f'from . import {x.stem}' for x in files]
    contents.insert(0, '# type: ignore')
    contents.append('')
    content = '\n'.join(contents)
    await bfile.writeText(
        initFile,
        content,
    )
    print(content)
