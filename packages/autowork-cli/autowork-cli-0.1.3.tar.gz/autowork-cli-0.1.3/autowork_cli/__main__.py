import typer
from rich import print

from autowork_cli.cf.cf_cmd import cf_app
from autowork_cli.log.log_cmd import log_app
from autowork_cli.login.login_cmd import LoginCommand
from autowork_cli.sidecar.sidecar_cmd import sc_app
from autowork_cli.file.file_cmd import file_app
from autowork_cli.flow.flow_cmd import flow_app

# 备份字体：🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉
# 备份字体：🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩

app = typer.Typer(name='autowork', help='Autowork Command-line Tool')
app.add_typer(cf_app, name="cf")
app.add_typer(sc_app, name="sidecar")
app.add_typer(file_app, name="file")
app.add_typer(flow_app, name='flow')
app.add_typer(log_app, name='log')
# app.add_typer(sc_app, name="sc", help="边车服务sidecar缩写命令")


@app.command(help="登录Autowork系统")
def login():
    cmd = LoginCommand()
    cmd.run_login()


@app.command(help="显示Autowork版本号")
def version():
    typer.echo("Autowork 1.0.0")


@app.callback()
def main():
    print("[blue]🅰🆄🆃🅾🆆🅾🆁🅺")


def run():
    app()


if __name__ == "__main__":
    app()
