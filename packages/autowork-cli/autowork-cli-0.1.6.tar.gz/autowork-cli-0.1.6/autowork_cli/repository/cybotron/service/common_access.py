# -*- coding: utf-8 -*-
import logging
from typing import Dict
from autowork_cli.repository.cybotron.model.metadataobj import *
from autowork_cli.common.lang.async_requests import AsyncRequests

logger = logging.getLogger(__name__)


class CommonAccess:

    def __init__(self):
        self.URL = None
        self.X_API_KEY = None
        self.client = AsyncRequests("")

    async def create(self, req: CreateRequest) -> CreateResponse:
        """
        单条创建接口
        """
        result = await self.get_response(req, "create")
        return CreateResponse(lastId=result["lastId"])

    # async def get(self, req: GetRequest) -> GetResponse:
    #     """
    #     单条查询接口
    #     """
    #     result = await self.get_response(req, "get")
    #     data = {} if not result.get('data', "") else result['data']  # 查询结果为空, 返回空字典
    #     return GetResponse(data=data)
    #
    # async def getList(self, req: GetListRequest) -> GetListResponse:
    #     """
    #     分页查询接口
    #     """
    #     result = await self.get_response(req, "getList")
    #     return GetListResponse(data=result["data"], total=result["total"])

    async def update(self, req: UpdateRequest) -> UpdateResponse:
        """
        单条修改接口
        """
        result = await self.get_response(req, "update")
        return UpdateResponse(count=result["count"], lastId=result["lastId"])

    async def delete(self, req: DeleteRequest) -> DeleteResponse:
        """
        单条删除接口
        """
        result = await self.get_response(req, "delete")
        return DeleteResponse(count=result["count"])

    async def bulkCreate(self, req: BulkCreateRequest) -> BulkCreateResponse:
        """
        批量创建接口
        """
        result = await self.get_response(req, "bulkCreate")
        return BulkCreateResponse(count=result["count"])

    async def bulkUpdate(self, req: BulkUpdateRequest) -> BulkUpdateResponse:
        """
        批量修改接口
        """
        result = await self.get_response(req, "bulkUpdate")
        return BulkUpdateResponse(count=result["count"])

    async def bulkDelete(self, req: BulkDeleteRequest) -> BulkDeleteResponse:
        """
        批量删除接口
        """
        result = await self.get_response(req=req, method="bulkDelete")
        return BulkDeleteResponse(count=result["count"])

    async def get_response(self, req, method: str = "", re_method: str = "post") -> Dict:
        """
        请求数据
        """
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.X_API_KEY
        }
        app_code = req.appCode
        table_code = req.tableCode
        url = f"{self.URL}/{app_code}/{table_code}/{method}"
        logger.info(f"url:{url}, headers：{headers}, json:{req.dict()}")
        request = self.client.build_request(method=re_method, url=url, timeout=15, json=req.dict(), headers=headers)
        response = await self.client.send(request)
        response = response.json()
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]

    async def get_response_json(self, url: str = "", json: str = "", method: str = "", headers: Dict = None) -> str:
        """
        请求数据, 抽取公共使用
        """
        request = self.client.build_request(method=method, url=url, timeout=15, json=json, headers=headers)
        response = await self.client.send(request)
        response = response.json()
        return response
