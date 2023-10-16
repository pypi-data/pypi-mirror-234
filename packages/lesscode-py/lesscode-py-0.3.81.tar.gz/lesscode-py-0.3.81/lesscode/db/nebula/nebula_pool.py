# -*- coding: utf-8 -*-
import importlib
import ssl

from lesscode.db.base_connection_pool import BaseConnectionPool


class NebulaPool(BaseConnectionPool):
    """
    mysql 数据库链接创建类
    """

    async def create_pool(self):
        pass

    def sync_create_pool(self):
        try:
            nebula3_gclient_net = importlib.import_module("nebula3.gclient.net")
            nebula3_config = importlib.import_module("nebula3.Config")
        except ImportError:
            raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
        config = nebula3_config.Config()
        ssl_conf = None
        config.max_connection_pool_size = self.conn_info.max_size
        config.min_connection_pool_size = self.conn_info.min_size
        if self.conn_info.params and isinstance(self.conn_info.params, dict):
            config.timeout = self.conn_info.params.get("timeout", 0)
            config.idle_time = self.conn_info.params.get("idle_time", 0)
            config.interval_check = self.conn_info.params.get("interval_check", -1)
            ssl_config = self.conn_info.params.get("ssl_conf", {})
            if ssl_conf and isinstance(ssl_conf, dict):
                ssl_conf = nebula3_config.SSL_config()
                ssl_conf.unix_socket = ssl_config.get("unix_socket", None)
                ssl_conf.ssl_version = ssl_config.get("ssl_version", None)
                ssl_conf.cert_reqs = ssl_config.get("cert_reqs", ssl.CERT_NONE)
                ssl_conf.ca_certs = ssl_config.get("ca_certs", None)
                ssl_conf.verify_name = ssl_config.get("verify_name", None)
                ssl_conf.keyfile = ssl_config.get("keyfile", None)
                ssl_conf.certfile = ssl_config.get("certfile", None)
                ssl_conf.allow_weak_ssl_versions = ssl_config.get("allow_weak_ssl_versions", None)
        pool = nebula3_gclient_net.ConnectionPool()
        pool.init([(self.conn_info.host, self.conn_info.port)], config, ssl_conf)
        return pool
