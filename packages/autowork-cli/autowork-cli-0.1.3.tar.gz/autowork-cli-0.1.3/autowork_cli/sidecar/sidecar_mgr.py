import json
import logging
import os
import signal

import requests
import uvicorn

from autowork_cli.common.lang import logger_setting
from autowork_cli.common.lang.singleton import SingletonMeta

logger = logging.getLogger(__name__)


class SidecarManager(metaclass=SingletonMeta):
    def __init__(self, port: int = 9080):
        self.port = port
        self.app_port = 9000

    def start(self):
        logger.info("redirecting to app port: " + str(self.app_port))
        uvicorn.run("autowork_cli.sidecar.sidecar_app:app", host="0.0.0.0", port=self.port, log_level="info")

    def status(self):
        health = self.__read_health()
        return health

    def stop(self):
        health = self.__read_health()
        pid = health["pid"]
        if pid:
            os.kill(pid, signal.SIGTERM)

    def __read_health(self):
        try:
            resp = requests.get("http://localhost:" + str(self.port) + "/health", timeout=1.0).text
            return json.loads(resp)
        except (requests.ConnectionError, requests.ReadTimeout):
            return {"pid": None}


if __name__ == '__main__':
    logger_setting.init()
    mgr = SidecarManager()
    mgr.start()
