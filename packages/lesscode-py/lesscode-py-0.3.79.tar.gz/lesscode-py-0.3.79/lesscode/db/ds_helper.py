# -*- coding: utf-8 -*-

from tornado.options import options

from lesscode.db.base_sql_helper import BaseSqlHelper
from lesscode.db.condition_wrapper import ConditionWrapper


class DSHelper(BaseSqlHelper):
    """
    对外暴露的工具类，对数据库操作采用代理模式进行了包装
    """

    def __init__(self, pool_name):
        """
        初始化sql工具
        :param pool_name: 连接池名称
        """
        self.pool, self.conn_info = options.database[pool_name]
        clazz = None
        if self.conn_info.dialect == "postgresql":
            # self.db_helper = PostgresqlHelper(self.pool)
            clazz = getattr(__import__("lesscode.db.postgresql.postgresql_helper", fromlist="PostgresqlHelper"),
                            "PostgresqlHelper")
        elif self.conn_info.dialect == "mysql":
            # self.db_helper = MysqlHelper(self.pool)
            clazz = getattr(__import__("lesscode.db.mysql.mysql_helper", fromlist="MysqlHelper"), "MysqlHelper")
            # 执行用例
            self.db_helper = clazz(self.pool)
        elif self.conn_info.dialect == "mongodb":
            clazz = getattr(__import__("lesscode.db.mongodb.mongodb_helper", fromlist="MongodbHelper"), "MongodbHelper")
            # self.db_helper = MongodbHelper(self.pool)
        elif self.conn_info.dialect == "elasticsearch":
            clazz = getattr(
                __import__("lesscode.db.elasticsearch.elasticsearch_helper", fromlist="ElasticsearchHelper"),
                "ElasticsearchHelper")
        elif self.conn_info.dialect == "esapi":
            clazz = getattr(__import__("lesscode.db.es.es_helper", fromlist="EsHelper"), "EsHelper")
        elif self.conn_info.dialect == "redis":
            clazz = getattr(
                __import__("lesscode.db.redis.redis_helper", fromlist="RedisHelper"),
                "RedisHelper")
        if clazz:
            self.db_helper = clazz(self.pool)

    async def insert_data(self, table_name: str, data):
        return await self.db_helper.insert_data(table_name, data)

    async def insert_one_data(self, table_name: str, data: dict):
        return await self.db_helper.insert_one_data(table_name, data)

    async def insert_many_data(self, table_name: str, data: list):
        return await self.db_helper.insert_many_data(table_name, data)

    async def update_data(self, condition_wrapper: ConditionWrapper, param: dict):
        return await self.db_helper.update_data(condition_wrapper, param)

    async def delete_data(self, condition_wrapper: ConditionWrapper):
        return await self.db_helper.delete_data(condition_wrapper)

    async def fetchone_data(self, condition_wrapper: ConditionWrapper):
        return await self.db_helper.fetchone_data(condition_wrapper)

    async def fetchall_data(self, condition_wrapper: ConditionWrapper):
        return await self.db_helper.fetchall_data(condition_wrapper)

    async def fetchall_page(self, condition_wrapper: ConditionWrapper, page_num=1, page_size=10):
        return await self.db_helper.fetchall_page(condition_wrapper, page_num, page_size)

    async def execute_sql(self, sql: str, param=None):
        return await self.db_helper.execute_sql(sql, param)

    async def executemany_sql(self, sql: str, param=None):
        return await self.db_helper.executemany_sql(sql, param)

    async def execute_fetchone(self, sql: str, param=None):
        return await self.db_helper.execute_fetchone(sql, param)

    async def execute_fetchall(self, sql: str, param=None):
        return await self.db_helper.execute_fetchall(sql, param)

    def prepare_insert_sql(self, table_name: str, item: dict):
        return self.db_helper.prepare_insert_sql(table_name, item)

    def prepare_update_sql(self, condition_wrapper: ConditionWrapper, param: dict):
        return self.db_helper.prepare_update_sql(condition_wrapper, param)

    def prepare_delete_sql(self, condition_wrapper: ConditionWrapper):
        return self.db_helper.prepare_delete_sql(condition_wrapper)

    def prepare_condition_sql(self, conditions: list):
        return self.db_helper.prepare_condition_sql(conditions)

    def prepare_query_sql(self, condition_wrapper: ConditionWrapper):
        return self.db_helper.prepare_query_sql(condition_wrapper)

    def prepare_page_sql(self, condition_wrapper: ConditionWrapper, page_num: int, page_size: int):
        return self.db_helper.prepare_page_sql(condition_wrapper, page_num, page_size)

    def sync_insert_data(self, table_name: str, data):
        return self.db_helper.sync_insert_data(table_name, data)

    def sync_insert_one_data(self, table_name: str, data: dict):
        return self.db_helper.sync_insert_one_data(table_name, data)

    def sync_insert_many_data(self, table_name: str, data: list):
        return self.db_helper.sync_insert_many_data(table_name, data)

    def sync_update_data(self, condition_wrapper: ConditionWrapper, param: dict):
        return self.db_helper.sync_update_data(condition_wrapper, param)

    def sync_delete_data(self, condition_wrapper: ConditionWrapper):
        return self.db_helper.sync_delete_data(condition_wrapper)

    def sync_fetchone_data(self, condition_wrapper: ConditionWrapper):
        return self.db_helper.sync_fetchone_data(condition_wrapper)

    def sync_fetchall_data(self, condition_wrapper: ConditionWrapper):
        return self.db_helper.sync_fetchall_data(condition_wrapper)

    def sync_fetchall_page(self, condition_wrapper: ConditionWrapper, page_num=1, page_size=10):
        return self.db_helper.sync_fetchall_page(condition_wrapper, page_num, page_size)

    def sync_execute_sql(self, sql: str, param=None):
        return self.db_helper.sync_execute_sql(sql, param)

    def sync_executemany_sql(self, sql: str, param=None):
        return self.db_helper.sync_executemany_sql(sql, param)

    def sync_execute_fetchone(self, sql: str, param=None):
        return self.db_helper.sync_execute_fetchone(sql, param)

    def sync_execute_fetchall(self, sql: str, param=None):
        return self.db_helper.sync_execute_fetchall(sql, param)

    def sync_connect(self, database: str = None, table: str = None):
        if self.conn_info.dialect == "postgresql":
            return self.pool
        elif self.conn_info.dialect == "mysql":
            return self.pool
        elif self.conn_info.dialect == "mongodb":
            collection = self.pool[database][table]
            return collection
        elif self.conn_info.dialect == "elasticsearch":
            return self.pool
        elif self.conn_info.dialect == "esapi":
            return self.pool
        elif self.conn_info.dialect == "redis":
            connect = self.pool.get_connection(sync=True)
            return connect
        else:
            return Exception(f"connect type ({self.conn_info.dialect}) is not supported")

    async def connect(self, database: str = None, table: str = None):
        if self.conn_info.dialect == "postgresql":
            return self.pool
        elif self.conn_info.dialect == "mysql":
            return self.pool
        elif self.conn_info.dialect == "mongodb":
            collection = self.pool[database][table]
            return collection
        elif self.conn_info.dialect == "elasticsearch":
            return self.pool
        elif self.conn_info.dialect == "esapi":
            return self.pool
        elif self.conn_info.dialect == "redis":
            connect = self.pool.get_connection()
            return connect
        else:
            return Exception(f"connect type ({self.conn_info.dialect}) is not supported")
