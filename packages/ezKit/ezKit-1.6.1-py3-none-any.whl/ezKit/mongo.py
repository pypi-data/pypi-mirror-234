from loguru import logger
from pymongo import MongoClient

from . import utils


class Mongo():

    client = MongoClient()

    def __init__(self, mongo_url=None):
        ''' Initiation '''
        if mongo_url != None:
            self.client = MongoClient(mongo_url)

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            logger.exception(e)

    def connect_test(self, debug: bool = False):
        info = 'MongoDB连接测试'
        try:
            logger.info(f'{info}[执行]')
            self.client.server_info()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e) if utils.v_true(debug, bool) else next
            return False

    def collection(self, database, name):
        return self.client[database][name]

    def collection_insert(self, database, collection, data, drop=None):
        db_collection = self.client[database][collection]
        info = '插入数据'
        try:
            logger.info(f'{info}[执行]')
            # 是否删除 collection
            if drop == True:
                # 删除 collection
                db_collection.drop()
            # 插入数据
            if utils.v_true(data, dict):
                # 插入一条数据
                result = db_collection.insert_one(data)
            elif utils.v_true(data, list):
                # 插入多条数据
                result = db_collection.insert_many(data)
            else:
                logger.error(f'{info}[失败]')
                logger.error('数据类型错误')
                return False
            logger.success(f'{info}[成功]')
            return result
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False
