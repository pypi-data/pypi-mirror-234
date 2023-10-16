import logging
import threading
import time

from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.common.local.clientinfo import ClientInfo
from autowork_cli.common.request.CybotronAsyncClient import CybotronAsyncClient
from autowork_cli.common.request.CybotronSyncClient import CybotronSyncClient

logger = logging.getLogger(__name__)


class DevRouterRegister:
    time_interval = 15  # 定时注册
    interval_stop = False  # 是否停止注册
    dev_register_url = "/cbn/api/v1/dev/register"
    unregister_url = "/cbn/api/v1/dev/unregister"
    query_url = "/cbn/api/v1/dev/query"

    @classmethod
    def start(cls):
        cls.interval_stop = False
        upload_thread = threading.Thread(target=cls.run, daemon=True,
                                         name="注册开发者路由")
        upload_thread.start()

    @classmethod
    def run(cls):
        error_count = 0
        first_register = True
        while True:
            if cls.interval_stop:
                break

            if error_count > 10:
                logger.error(f"开发者路由注册失败：【重试超过{error_count}次，停止重试】")
                break
            try:
                result = cls.register()
                if first_register:
                    logger.info(f"开发者路由注册成功: {result}")
                    first_register = False
                error_count = 0
            except Exception as e:
                logger.error(e)
                logger.error(f"开发者路由注册失败：【{e}】")
                error_count += 1

            time.sleep(cls.time_interval)
        return True

    @classmethod
    async def stop(cls):
        cls.interval_stop = True
        client = CybotronAsyncClient()
        response = await client.post(cls.unregister_url, json={})
        if response["success"] is True:
            return True
        return False

    @classmethod
    async def query(cls):
        client = CybotronAsyncClient()
        response = await client.get(cls.query_url)
        if "result" not in response:
            return None
        return response["result"]

    @classmethod
    def register(cls):
        ip_address = ClientInfo.get_ip()
        config = DefaultLoginConfig
        dev_apps_config = config.get_dev_apps()
        if not dev_apps_config:
            logger.error("开发者路由注册失败：【未配置开发应用】")
        data = {"devApps": dev_apps_config.split(","), "serviceId": "SandboxFunction", "address": ip_address}

        client = CybotronSyncClient()
        response = client.post(cls.dev_register_url, json=data)
        if response["success"] is True:
            return data
        return False
