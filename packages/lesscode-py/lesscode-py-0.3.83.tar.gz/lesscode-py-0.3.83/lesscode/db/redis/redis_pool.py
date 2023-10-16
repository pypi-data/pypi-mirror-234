# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class RedisPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    def create_pool(self):
        """
        创建mysql 异步连接池
        :return:
        """
        try:
            aioredis = importlib.import_module("aioredis")
        except ImportError:
            raise Exception(f"aioredis is not exist,run:pip install aioredis==2.0.1")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        encoding = params.pop("encoding", "utf-8")
        decode_responses = params.pop("decode_responses", True)
        if self.conn_info.async_enable:
            pool = aioredis.ConnectionPool.from_url(f"redis://{self.conn_info.host}", port=self.conn_info.port,
                                                    password=self.conn_info.password,
                                                    db=self.conn_info.db_name, encoding=encoding,
                                                    decode_responses=decode_responses, **params)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        try:
            redis = importlib.import_module("redis")
        except ImportError:
            raise Exception(f"redis is not exist,run:pip install redis==4.1.4")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        encoding = params.pop("encoding", "utf-8")
        decode_responses = params.pop("decode_responses", True)
        pool = redis.ConnectionPool.from_url(f"redis://{self.conn_info.host}", port=self.conn_info.port,
                                             password=self.conn_info.password, max_connections=self.conn_info.max_size,
                                             db=self.conn_info.db_name, encoding=encoding,
                                             decode_responses=decode_responses, **params)
        return pool
