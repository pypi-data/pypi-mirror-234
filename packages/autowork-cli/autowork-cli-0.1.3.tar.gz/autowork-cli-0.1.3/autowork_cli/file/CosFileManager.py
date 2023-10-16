# -*- coding:utf-8 -*-
from enum import Enum

import requests

from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.common.config.BaseURLConfig import BaseURLConfig
from autowork_cli.common.config.ClientConfig import USER_AGENT
from autowork_cli.common.lang.async_requests import AsyncRequests
from autowork_cli.repository.cybotron.service.data_accessor import DataAccessor
from autowork_cli.repository.cybotron.model.metadataobj import GetOptions
from autowork_cli.repository.cybotron.model.metadataobj import GetListRequest


class BucketExpireTime(Enum):
    E_FOREVER = "tc_forever"
    E_30_DAYS = "tc_30days"
    E_3_MONTH = "tc_3months"
    E_1_YEAR = "tc_1year"

    @staticmethod
    def get_expire_time(expire_type: int):
        match expire_type:
            case 1:
                return BucketExpireTime.E_FOREVER
            case 2:
                return BucketExpireTime.E_30_DAYS
            case 3:
                return BucketExpireTime.E_3_MONTH
            case _:
                return BucketExpireTime.E_1_YEAR


class CosFileManager:
    """
    文件存储腾讯云接口类
    """

    def __init__(self):
        self.remote_data_accessor = DataAccessor()
        self.client = AsyncRequests(BaseURLConfig.get_api_base_url(DefaultLoginConfig.get_env()))

    @classmethod
    def __save_file_with_response(cls, local_file_path, response):
        """
        根据网络响应，保存文件
        :param local_file_path: 本地保存的文件路径
        :param response: 云端响应
        :return:
        """
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
                    f.flush()

    async def __get_bucket(self, expire_time: BucketExpireTime) -> str:
        """
        查询元数据表，获取到指定时间的桶id
        :param expire_time: 有效时间
        :return: 数据库中的桶id
        """
        options = GetOptions()
        req = GetListRequest(
            appCode="metabase",
            tableCode="mb_file_bucket",
            options=options,
            filter={"code": expire_time.value}
        )
        res_list = await self.remote_data_accessor.getList(req)
        if res_list.total > 0:
            return res_list.data[0].get('id')
        else:
            raise Exception(
                f'腾讯云存储，上传或下载时，没有从数据库中获取到存储桶id，metabase mb_file_bucket {expire_time}')

    async def __send_request(self, url: str, file_path: str, bucket_id: str):
        """
        给元数据后台发送请求
        :param url: 接口url
        :param file_path: 腾讯云文件路径
        :param bucket_id: 桶id
        :return: 接口返回的result
        """
        req = self.client.build_request(
            method="post", url=url, timeout=15,
            json={
                "bucketId": bucket_id,
                "filePath": file_path,
                "expiration": None
            },
            headers={
                'User-Agent': USER_AGENT,
                'X-API-KEY': DefaultLoginConfig.get_api_key()
            }
        )
        response = await self.client.send(req)
        response = response.json()
        if not response.get("success"):
            raise Exception(response.get("message"))
        return response["result"]

    async def upload_file(self, local_file_path, cloud_file_path, expire_time=BucketExpireTime.E_FOREVER) -> str:
        """
        上传文件
        :param local_file_path: 本地要上传的文件路径
        :param cloud_file_path: 云端存储文件路径
        :param expire_time: 有效时间
        :return: 成功/失败
        """
        # 读取文件内容
        bucket_id = await self.__get_bucket(expire_time)
        with open(local_file_path, 'rb') as f:
            url = await self.__send_request('/cbn/api/v1/file/upload/generatePreSignedUrl', cloud_file_path, bucket_id)
            response = requests.put(url=url, data=f.read())
            if response.status_code != 200:
                raise Exception(response.text)
            return str(url).split('?')[0]

    async def download_file(self, local_file_path, cloud_file_path, expire_time=BucketExpireTime.E_FOREVER):
        """
        下载文件
        :param local_file_path: 本地要下载的路径
        :param cloud_file_path: 云端文件路径
        :param expire_time: 有效时间
        :return:
        """
        bucket_id = await self.__get_bucket(expire_time)
        url = await self.__send_request('/cbn/api/v1/file/download/generatePreSignedUrl', cloud_file_path, bucket_id)
        response = requests.get(url=url)
        self.__save_file_with_response(local_file_path, response)
