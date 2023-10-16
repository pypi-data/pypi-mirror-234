# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class SqlAlchemyPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    def sync_create_pool(self):
        db_type = "mysql"
        params = self.conn_info.params
        if not params or not isinstance(params, dict):
            params = {}
        if params:
            if params.get("db_type"):
                db_type = params.pop("db_type")
        if db_type == "mysql":
            url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
                self.conn_info.db_name)
        elif db_type == "postgresql":
            url = 'postgresql+psycopg2://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
                self.conn_info.db_name)
        elif db_type == "tidb":
            url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
                self.conn_info.db_name)
        elif db_type == "ocean_base":
            url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                self.conn_info.user, self.conn_info.password, self.conn_info.host, self.conn_info.port,
                self.conn_info.db_name)
        else:
            raise Exception("UNSUPPORTED DB TYPE")
        try:
            sqlalchemy = importlib.import_module("sqlalchemy")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        echo = params.pop("echo", True)
        pool_recycle = params.pop("pool_recycle", 3600)
        max_overflow = params.pop("max_overflow", 0)
        pool_timeout = params.pop("pool_timeout", 10)
        pool_pre_ping = params.pop("pool_pre_ping", True)
        engine = sqlalchemy.create_engine(url, echo=echo,
                                          pool_size=self.conn_info.min_size,
                                          pool_recycle=pool_recycle,
                                          max_overflow=max_overflow,
                                          pool_timeout=pool_timeout,
                                          pool_pre_ping=pool_pre_ping, **params)
        return engine
