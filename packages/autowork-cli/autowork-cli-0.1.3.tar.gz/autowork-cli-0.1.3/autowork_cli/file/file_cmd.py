import asyncio
import os
import uuid
import warnings
from pathlib import Path

import typer
from typing_extensions import Annotated

from autowork_cli.file.CosFileManager import CosFileManager, BucketExpireTime
from autowork_cli.util.dateutil import DateUtil

file_app = typer.Typer(name='file', help='Autowork File Tool')
warnings.filterwarnings("ignore")


@file_app.command(help='上传文件')
def upload(file: Annotated[str, typer.Argument(help='上传的文件')],
           target: str = typer.Option(None, '-t', '--target-file', help='目标文件,默认autowork/YYYYmmdd/uuid'),
           expire_type: int = typer.Option(1, '-e', '--expire-type', help='过期类型')):
    if file is None:
        typer.secho('请指定要上传的文件', fg=typer.colors.RED)

    if file.startswith("./"):
        upload_file = Path(__file__).resolve().parent.joinpath(file)
        if not upload_file.exists():
            typer.secho('指定的文件不存在', fg=typer.colors.RED)
            return
    else:
        upload_file = Path(file)
        if not Path(file).exists():
            typer.secho('指定的文件不存在', fg=typer.colors.RED)
            return

    if target is None:
        upload_file_name = str(uuid.uuid4()).replace('-', '') + '.' + upload_file.name.split('.')[-1]
        cloud_file_path = f"autowork/{DateUtil().now().strftime('%Y%m%d')}/{upload_file_name}"
    else:
        cloud_file_path = target if target.startswith('autowork') else f'autowork/${target}'

    try:
        res = asyncio.run(CosFileManager().upload_file(upload_file,
                                                       cloud_file_path,
                                                       BucketExpireTime.get_expire_time(expire_type)))
        if res:
            typer.secho(f"文件上传成功, 上传地址：{res}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"上传文件报错：{e}", fg=typer.colors.RED)


@file_app.command(help="下载文件")
def download(file: Annotated[str, typer.Argument(help='待下载的文件, ')],
             outdir: str = typer.Option(None, '-d', '--out-dir', help='下载保存目录'),
             expire_type: int = typer.Option(1, '-e', '--expire-type', help='过期类型')):
    global download_dir
    if file.startswith('http'):
        file = '/'.join(file.split('/')[3:])

    if outdir is not None:
        if outdir.startswith('./'):
            download_dir = Path(os.getcwd()).parent.joinpath(outdir)
        else:
            download_dir = Path(outdir)
    else:
        download_dir = Path(os.getcwd())

    if not download_dir.exists():
        download_dir.mkdir(parents=True, exist_ok=True)

    download_file = download_dir.joinpath(Path(file).name)

    try:
        asyncio.run(CosFileManager().download_file(download_file,
                                                   file,
                                                   BucketExpireTime.get_expire_time(expire_type)))
        typer.secho(f"下载文件成功，地址：{download_file}", fg=typer.colors.RED)
    except Exception as e:
        typer.secho(f"下载文件报错：{e}", fg=typer.colors.RED)
