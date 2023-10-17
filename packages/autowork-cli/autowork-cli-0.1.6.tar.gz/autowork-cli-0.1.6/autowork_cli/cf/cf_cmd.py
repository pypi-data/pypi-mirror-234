# -*- coding: utf-8 -*-

import shutil
import urllib.request

import requests
import typer
import os

from autowork_cli.common.config.TemplateConfig import SANDBOX_BOOT_URL
from autowork_cli.common.config.template.hello_world_template import HELLO_WORD
from autowork_cli.common.config.template.pyproject_template import PYPROJECT_TEMPLATE
from autowork_cli.common.config.template.sandbox_function_template import SANDBOX_FUNCTION
from autowork_cli.util.fileutil import FileUtil

cf_app = typer.Typer(name='cf', help='Autowork Cloud Function Tool')


@cf_app.command(help='初始沙盒函数工程')
def init(project_id: str = typer.Option(None, '-p', '--project-id', prompt='工程ID', help='工程ID'),
         app_id: str = typer.Option(None, '-a', '--app-id', prompt='所属应用ID', help='所属应用ID')):
    # 初始化函数
    src_dir = project_id.strip().lower()
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)
    if not os.path.exists('tests'):
        os.mkdir('tests')

    # init pyproject.toml
    content = PYPROJECT_TEMPLATE.replace('{project_id}', src_dir, 2)
    FileUtil.genFile('./pyproject.toml', content)

    # init sandbox_function.json
    content = SANDBOX_FUNCTION.replace('{app_id}', app_id, 1).replace('{project_id}', src_dir, 1)
    FileUtil.genFile('./sandbox_function.json', content)

    # init hello world
    FileUtil.genFile(f"./{src_dir}/hello_world.py", HELLO_WORD)

    # add sandbox-boot
    urllib.request.urlretrieve(SANDBOX_BOOT_URL, 'sandbox_boot.zip')
    shutil.unpack_archive('sandbox_boot.zip', './', format='zip')
    os.remove('sandbox_boot.zip')

    typer.echo("project inited")


@cf_app.command()
def run():
    # 初始化函数
    typer.echo("run project...")
