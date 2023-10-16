from autowork_cli.common.config.BaseURLConfig import BaseURLConfig
from autowork_cli.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from autowork_cli.common.config.ClientConfig import LOG_APP_CODE, LOG_TABLE_CODE
from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.common.request.CybotronSyncClient import CybotronSyncClient
from autowork_cli.repository.cybotron.service.common_access import CommonAccess


class LogAccessor(CommonAccess):

    def __init__(self):
        super().__init__()
        self.URL = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env()) + BusinessURLConfig.get_url(
            DataTypeEnum.DATA)
        self.X_API_KEY = DefaultLoginConfig.get_api_key()

    @staticmethod
    def send_log(log_message: dict) -> bool:
        client = CybotronSyncClient()
        base_url = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env())
        business_url = f"{base_url}{BusinessURLConfig.get_url(DataTypeEnum.DATA)}/{LOG_APP_CODE}/{LOG_TABLE_CODE}/create"

        req = {
            "values": log_message,
            "options": {
                "conflictToUpdate": False
            }
        }
        res = client.send(business_url, 'POST', req)
        if res.get('success'):
            return True
        else:
            return False
