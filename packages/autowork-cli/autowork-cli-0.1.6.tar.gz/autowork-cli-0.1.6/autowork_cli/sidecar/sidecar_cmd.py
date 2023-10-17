from time import sleep
from typing import Annotated

import rich
import typer

from autowork_cli.sidecar.sidecar_mgr import SidecarManager

sc_app = typer.Typer(name='sidecar', help='Autowork边车服务')

sidecar_mgr = SidecarManager()


@sc_app.command(help="启动边车服务")
def start(port: Annotated[int, typer.Option(help="边车端口号")] = 9080,
          app_port: Annotated[int, typer.Option(help="应用端口号")] = 9000):
    if port == app_port:
        rich.print("[red]边车端口号和应用端口号不能相同")
        return
    rich.print(f"[blue]启动边车服务，监听本地端口号{app_port}")
    sidecar_mgr.port = port
    sidecar_mgr.app_port = app_port
    sidecar_mgr.start()


@sc_app.command(help="查看边车服务状态")
def status():
    st = sidecar_mgr.status()
    if st["pid"] is not None:
        rich.print(f"[green]边车运行中: {st['pid']}")
    else:
        rich.print("[green]边车未运行")


@sc_app.command(help="停止边车服务")
def stop():
    rich.print("[blue]停止边车服务")
    sidecar_mgr.stop()
    while True:
        sleep(0.5)
        st = sidecar_mgr.status()
        if st["pid"] is None:
            rich.print("[green]边车已停止")
            break
