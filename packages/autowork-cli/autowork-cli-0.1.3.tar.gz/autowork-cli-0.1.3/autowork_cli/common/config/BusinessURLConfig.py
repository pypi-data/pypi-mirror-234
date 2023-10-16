from enum import Enum

URL_DICT = {
    "DATA": "/cbn/api/v1/data",
    "METADATA": "/cbn/api/v1/metadata",
    "FLOW": "/cbn/api/v1/service"
}


class DataTypeEnum(Enum):
    DATA = 'DATA'
    META = 'METADATA'
    FLOW = 'FLOW'


class BusinessURLConfig:
    @staticmethod
    def get_data_url():
        return URL_DICT['DATA']

    @staticmethod
    def get_metadata_url():
        return URL_DICT['METADATA']

    @staticmethod
    def get_flow_url():
        return URL_DICT['FLOW']

    @staticmethod
    def get_url(datatype: DataTypeEnum):
        return URL_DICT[datatype.value]
