import logging
import os
import time

from fastapi import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from autowork_cli.common.lang import logger_setting
from autowork_cli.common.lang.async_requests import AsyncRequests
from autowork_cli.sidecar.dev_register import DevRouterRegister
from autowork_cli.sidecar.sidecar_mgr import SidecarManager

logger_setting.init()
logger = logging.getLogger(__name__)

sidecar_mgr = SidecarManager()
app = FastAPI(title="Autowork CLI Sidecar")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def dev_router_startup():
    DevRouterRegister.start()


@app.on_event("shutdown")
async def dev_router_shutdown():
    await DevRouterRegister.stop()


@app.get("/health")
async def health():
    return {
        "pid": os.getpid()
    }


@app.post("/sandbox/call/{app_id}/{func_id}")
async def call_sandbox_func(app_id: str, func_id: str, req: Request, debug: bool = False):
    try:
        app_port = sidecar_mgr.app_port
        client = AsyncRequests(f"http://localhost:{str(app_port)}")
        data = await req.json()
        timeout = 30*60 if debug else 10
        resp = await client.request(f"/sandbox/call/{app_id}/{func_id}", data, timeout)
        return resp.json()
    except BaseException as e:
        logger.exception(e)
        return {"message": str(e), "success": False}
