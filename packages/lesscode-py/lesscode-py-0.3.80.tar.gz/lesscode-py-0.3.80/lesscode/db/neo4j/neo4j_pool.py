# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class Neo4jPool(BaseConnectionPool):
    """
    Neo4j 数据库链接创建类
    """

    async def create_pool(self):
        """
        创建Neo4j 连接池
        :return:
        """
        try:
            neo4j = importlib.import_module("neo4j")
        except ImportError:
            raise Exception(f"neo4j is not exist,run:pip install neo4j==5.0.0")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        driver = neo4j.AsyncGraphDatabase.driver(f"bolt://{self.conn_info.host}:{self.conn_info.port}",
                                                 auth=(self.conn_info.user, self.conn_info.password), **params)
        return driver

    def sync_create_pool(self):
        """
        创建Neo4j 连接池
        :return:
        """
        try:
            neo4j = importlib.import_module("neo4j")
        except ImportError:
            raise Exception(f"neo4j is not exist,run:pip install neo4j==5.0.0")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        driver = neo4j.GraphDatabase.driver(f"bolt://{self.conn_info.host}:{self.conn_info.port}",
                                            auth=(self.conn_info.user, self.conn_info.password), **params)
        return driver
