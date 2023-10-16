# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class PostgresqlPool(BaseConnectionPool):
    """
    Postgresql 数据库链接创建类
    """

    async def create_pool(self):
        print("Postgresql create_pool")
        """
        创建postgresql 异步连接池
        :param conn_info: 连接信息
        :return: AsyncConnectionPool
        """
        try:
            aiopg = importlib.import_module("aiopg")
        except ImportError:
            raise Exception(f"aiopg is not exist,run:pip install aiopg==1.3.3")
        info = self.conn_info
        if info.async_enable:
            params = self.conn_info.params
            if not isinstance(params, dict):
                params = dict()
            pool = await aiopg.create_pool(host=info.host, port=info.port, user=info.user,
                                           password=info.password,
                                           database=info.db_name, **params)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        try:
            psycopg2 = importlib.import_module("psycopg2")
        except ImportError:
            raise Exception(f"psycopg2-binary is not exist,run:pip install psycopg2-binary==2.9.3")
        try:
            pooled_db = importlib.import_module("dbutils.pooled_db")
        except ImportError:
            raise Exception(f"DBUtils is not exist,run:pip install DBUtils==3.0.2")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        pool = pooled_db.PooledDB(psycopg2, host=self.conn_info.host, port=self.conn_info.port,
                                  user=self.conn_info.user,
                                  password=self.conn_info.password, database=self.conn_info.db_name, **params)
        return pool
