# -*- coding: utf-8 -*-
import importlib

from lesscode.db.base_connection_pool import BaseConnectionPool


class MongodbPool(BaseConnectionPool):
    """
    mongodb 数据库链接创建类
    """

    def create_pool(self):
        print("mongodb create_pool")
        """
        创建mongodb 异步连接池
        :param conn_info: 连接信息
        :return:
        """
        try:
            motor = importlib.import_module("motor")
        except ImportError:
            raise Exception(f"motor is not exist,run:pip install motor==2.5.1")
        info = self.conn_info
        if info.async_enable:
            host_str = info.host.split(",")
            hosts = ",".join([f"{host}:{info.port}" for host in host_str])
            conn_info_string = f"mongodb://{info.user}:{info.password}@{hosts}"
            params = info.params
            if not isinstance(params, dict):
                if params and isinstance(params, str):
                    if params == "LDAP":
                        conn_info_string += "/?authMechanism=PLAIN"
                    elif params == "Password":
                        conn_info_string += "/?authSource=admin"
                    elif params == "X509":
                        conn_info_string += "/?authMechanism=MONGODB-X509"
                params = dict()
            pool = motor.motor_tornado.MotorClient(conn_info_string, **params)
            return pool
        else:
            raise NotImplementedError

    def sync_create_pool(self):
        try:
            pymongo = importlib.import_module("pymongo")
        except ImportError:
            raise Exception(f"pymongo is not exist,run:pip install pymongo==3.13.0")
        info = self.conn_info
        host_str = info.host.split(",")
        hosts = ",".join([f"{host}:{info.port}" for host in host_str])
        conn_info_string = f"mongodb://{info.user}:{info.password}@{hosts}"
        params = info.params
        if not isinstance(params, dict):
            if params and isinstance(params, str):
                if params == "LDAP":
                    conn_info_string += "/?authMechanism=PLAIN"
                elif params == "Password":
                    conn_info_string += "/?authSource=admin"
                elif params == "X509":
                    conn_info_string += "/?authMechanism=MONGODB-X509"
            params = dict()
        else:
            auth_type = params.pop("auth_type", "Password")
            if auth_type == "LDAP":
                conn_info_string += "/?authMechanism=PLAIN"
            elif auth_type == "Password":
                conn_info_string += "/?authSource=admin"
            elif auth_type == "X509":
                conn_info_string += "/?authMechanism=MONGODB-X509"
        pool = pymongo.MongoClient(conn_info_string, **params)
        return pool
