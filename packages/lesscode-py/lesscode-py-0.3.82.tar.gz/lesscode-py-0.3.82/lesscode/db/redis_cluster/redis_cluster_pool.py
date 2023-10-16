# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class RedisClusterPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        """
        创建mysql 异步连接池
        :return:
        """
        try:
            aioredis_cluster = importlib.import_module("aioredis_cluster")
        except ImportError:
            raise Exception(f"aioredis is not exist,run:pip install aioredis-cluster==2.3.1")
        if self.conn_info.async_enable:
            params = self.conn_info.params
            if not isinstance(params, dict):
                params = dict()
            retry_min_delay = params.pop("retry_min_delay")
            retry_max_delay = params.pop("retry_max_delay")
            max_attempts = params.pop("max_attempts")
            state_reload_interval = params.pop("state_reload_interval")
            follow_cluster = params.pop("follow_cluster")
            idle_connection_timeout = params.pop("idle_connection_timeout")
            username = self.conn_info.user
            password = self.conn_info.password
            encoding = params.pop("encoding")
            connect_timeout = params.pop("connect_timeout")
            attempt_timeout = params.pop("attempt_timeout")
            ssl = params.pop("ssl")
            pool = await aioredis_cluster.create_redis_cluster(startup_nodes=self.conn_info.host,
                                                               retry_min_delay=retry_min_delay,
                                                               retry_max_delay=retry_max_delay,
                                                               max_attempts=max_attempts,
                                                               state_reload_interval=state_reload_interval,
                                                               follow_cluster=follow_cluster,
                                                               idle_connection_timeout=idle_connection_timeout,
                                                               username=username,
                                                               password=password,
                                                               encoding=encoding,
                                                               pool_minsize=self.conn_info.min_size,
                                                               pool_maxsize=self.conn_info.max_size,
                                                               connect_timeout=connect_timeout,
                                                               attempt_timeout=attempt_timeout,
                                                               ssl=ssl, **params)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        try:
            rediscluster = importlib.import_module("rediscluster")
        except ImportError:
            raise Exception(f"redis is not exist,run:pip install redis-py-cluster==2.1.3")
        params = self.conn_info.params
        if not isinstance(params, dict):
            params = dict()
        init_slot_cache = params.pop("init_slot_cache", True)
        max_connections_per_node = params.pop("init_slot_cache", False)

        skip_full_coverage_check = params.pop("skip_full_coverage_check", False)
        nodemanager_follow_cluster = params.pop("nodemanager_follow_cluster", False)
        host_port_remap = params.pop("nodemanager_follow_cluster", None)
        pool = rediscluster.ClusterConnectionPool(startup_nodes=self.conn_info.host, init_slot_cache=init_slot_cache,
                                                  max_connections=self.conn_info.max_size,
                                                  max_connections_per_node=max_connections_per_node,
                                                  skip_full_coverage_check=skip_full_coverage_check,
                                                  nodemanager_follow_cluster=nodemanager_follow_cluster,
                                                  host_port_remap=host_port_remap, db=self.conn_info.db_name,
                                                  username=self.conn_info.user, password=self.conn_info.password,
                                                  **params)
        return pool
