import typer

from autowork_cli.common.config.LoginConfig import DefaultLoginConfig

log_app = typer.Typer(name='log_app', help='日志管理')


@log_app.command(help="启动DEBUG模式")
def enable_debug():
    DefaultLoginConfig.set_debug(True)
    DefaultLoginConfig.save()
    typer.echo('DEBUG模式已开启')


@log_app.command(help="关闭DEBUG模式")
def disable_debug():
    DefaultLoginConfig.set_debug(False)
    DefaultLoginConfig.save()
    typer.echo('DEBUG模式已关闭')


@log_app.command(help="确认是否DEBUG模式")
def is_debug() -> bool:
    if DefaultLoginConfig.get_debug():
        typer.secho('DEBUG模式已开启')
        return True
    else:
        typer.echo('DEBUG模式已关闭')
        return False
