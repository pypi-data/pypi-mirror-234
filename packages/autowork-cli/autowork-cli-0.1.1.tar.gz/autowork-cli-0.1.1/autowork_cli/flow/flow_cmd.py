import typer

from autowork_cli.common.config.BusinessURLConfig import BusinessURLConfig
from autowork_cli.common.request.CybotronSyncClient import CybotronSyncClient
from autowork_cli.repository.cybotron.model.flowobj import FlowWebRequest
from autowork_cli.util.jsonobjutil import parse_to_obj

flow_app = typer.Typer(name='flow', help='Autowork Flow Tool')


@flow_app.command(help='基于CODE的流程编排')
def service(app_code: str = typer.Option(None, '-a', '--app-code', prompt='APP CODE', help='应用编码'),
            flow_code: str = typer.Option(None, '-f', '--flow-code', prompt='FLOW CODE', help='流程编码'),
            data: str = typer.Option(None, '-d', '--data', help='详细参数')):
    url = f"{BusinessURLConfig.get_flow_url()}/{app_code}/{flow_code}"
    process(url, data)


@flow_app.command(help='基于ID的流程编排')
def service_call(app_id: str = typer.Option(None, '-a', '--app-id', prompt='APP ID', help='应用编号'),
                 flow_id: str = typer.Option(None, '-f', '--flow-id', prompt='FLOW ID', help='流程编号'),
                 data: str = typer.Option(None, '-d', '--data', help='详细参数')):
    url = f"{BusinessURLConfig.get_flow_url()}/{app_id}/{flow_id}/call"
    process(url, data)


def process(url: str, data: str):
    client = CybotronSyncClient()
    if data is None:
        data = FlowWebRequest()
    else:
        data = parse_to_obj(data, FlowWebRequest)

    try:
        res = client.send(url, 'POST', data.model_dump())
        if not res.get('success'):
            typer.secho(res.get('message'), fg=typer.colors.RED)
        else:
            typer.secho(f"调用成功, traceId: {res.get('traceId')}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"调用报错：{e}", fg=typer.colors.RED)
