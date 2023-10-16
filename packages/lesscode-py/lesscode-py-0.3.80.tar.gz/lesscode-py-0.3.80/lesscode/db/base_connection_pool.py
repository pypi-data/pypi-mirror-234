# -*- coding: utf-8 -*-
from lesscode.db.connection_info import ConnectionInfo


class BaseConnectionPool:

    def __init__(self, conn_info: ConnectionInfo):
        self.conn_info = conn_info

    async def create_pool(self):
        """
        创建连接池
        :return:
        """
        raise NotImplementedError

    def sync_create_pool(self):
        """
        创建连接池
        :return:
        """
        raise NotImplementedError
