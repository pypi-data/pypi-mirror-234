# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class MysqlPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        """
        创建mysql 异步连接池
        :return:
        """
        try:
            aiomysql = importlib.import_module("aiomysql")
        except ImportError:
            raise Exception(f"pymysql is not exist,run:pip install aiomysql==0.0.22")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        pool_recycle = params.pop("pool_recycle", 3600)
        autocommit = params.pop("autocommit", True)
        if self.conn_info.async_enable:
            pool = await aiomysql.create_pool(host=self.conn_info.host, port=self.conn_info.port,
                                              user=self.conn_info.user,
                                              password=self.conn_info.password,
                                              pool_recycle=pool_recycle,
                                              db=self.conn_info.db_name, autocommit=autocommit,
                                              minsize=self.conn_info.min_size,
                                              maxsize=self.conn_info.max_size, **params)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        try:
            pymysql = importlib.import_module("pymysql")
        except ImportError:
            raise Exception(f"pymysql is not exist,run:pip install pymysql==0.9.3")
        try:
            pooled_db = importlib.import_module("dbutils.pooled_db")
        except ImportError:
            raise Exception(f"DBUtils is not exist,run:pip install DBUtils==3.0.2")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        blocking = params.pop("blocking", True)
        mincached = params.pop("mincached", self.conn_info.min_size)
        maxusage = params.pop("maxusage", self.conn_info.min_size)
        maxshared = params.pop("maxshared", self.conn_info.max_size)
        maxcached = params.pop("maxcached", self.conn_info.max_size)
        ping = params.pop("ping", 1)
        charset = params.pop("charset", "utf8mb4")
        autocommit = params.pop("autocommit", True)
        read_timeout = params.pop("read_timeout", 30)
        pool = pooled_db.PooledDB(creator=pymysql, host=self.conn_info.host, port=self.conn_info.port,
                                  user=self.conn_info.user,
                                  passwd=self.conn_info.password, db=self.conn_info.db_name,
                                  mincached=mincached, blocking=blocking, maxusage=maxusage,
                                  maxshared=maxshared, maxcached=maxcached,
                                  ping=ping, maxconnections=self.conn_info.max_size, charset=charset,
                                  autocommit=autocommit,
                                  read_timeout=read_timeout, **params)
        return pool
