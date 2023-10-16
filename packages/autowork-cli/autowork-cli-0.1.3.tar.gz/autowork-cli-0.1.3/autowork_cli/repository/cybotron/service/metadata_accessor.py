from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.common.config.BaseURLConfig import BaseURLConfig
from autowork_cli.common.config.BusinessURLConfig import BusinessURLConfig, DataTypeEnum
from autowork_cli.repository.cybotron.service.common_access import CommonAccess
from autowork_cli.repository.cybotron.model.metadataobj import GetMetaRequest, GetMetaListRequest, GetResponse, GetListResponse


class MetaDataAccessor(CommonAccess):
    def __init__(self):
        super().__init__()
        self.URL = BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env()) + BusinessURLConfig.get_url(
            DataTypeEnum.META)
        self.X_API_KEY = DefaultLoginConfig.get_api_key()

    async def get(self, req: GetMetaRequest) -> GetResponse:
        """
        单条查询接口
        """
        result = await self.get_response(req, "get")
        data = {} if not result.get('data', "") else result['data']  # 查询结果为空, 返回空字典
        return GetResponse(data=data)

    async def getList(self, req: GetMetaListRequest) -> GetListResponse:
        """
        分页查询接口
        """
        result = await self.get_response(req, "getList")
        return GetListResponse(data=result["data"], total=result["total"])
