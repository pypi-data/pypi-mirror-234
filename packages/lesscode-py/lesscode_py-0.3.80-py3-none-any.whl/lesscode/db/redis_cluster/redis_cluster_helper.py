# -*- coding: utf-8 -*-
import importlib

from tornado.options import options


class RedisClusterHelper:

    def __init__(self, pool):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.conn_info = options.database[pool]
        else:
            self.pool = pool

    def get_connection(self, sync=False):
        if sync:
            try:
                rediscluster = importlib.import_module("rediscluster")
            except ImportError as e:
                raise Exception(f"redis is not exist,run:pip install redis-py-cluster==2.1.3")
            return rediscluster.RedisCluster(connection_pool=self.pool)
        else:
            return self.pool

    async def set(self, name, value, ex=None, px=None, nx: bool = False, xx: bool = False, keepttl: bool = False):
        return await self.pool.set(name, value, ex, px, nx, xx, keepttl)

    async def get(self, name):
        return await self.pool.get(name)

    async def keys(self, pattern):
        return await self.pool.keys(pattern=pattern)

    async def exists(self, *name):
        return await self.pool.exists(*name)

    async def delete(self, names):
        if isinstance(names, list) or isinstance(names, tuple):
            return await self.pool.delete(*names)
        else:
            return await self.pool.delete(names)

    async def rpush(self, name, values: list, time=None):
        res = await self.pool.rpush(name, *values)
        if time:
            await self.pool.expire(name, time)
        return res

    async def hset(self, name, key=None, value=None, mapping=None, time=None):
        res = await self.pool.hset(name, key=key, value=value, mapping=mapping)
        if time:
            await self.pool.expire(name, time)
        return res

    async def hgetall(self, name):
        return await self.pool.hgetall(name)

    async def hget(self, name, key):
        return await self.pool.hget(name, key)

    async def hdel(self, name, key):
        return await self.pool.hdel(name, key)

    async def hexists(self, name, key):
        return await self.pool.hexists(name, key)

    async def hincrby(self, name, key, amount: int):
        return await self.pool.hincrby(name, key, amount)

    async def hincrbyfloat(self, name, key, amount: float):
        return await self.pool.hincrbyfloat(name, key, amount)

    async def hkeys(self, name):
        return await self.pool.hkeys(name)

    async def hlen(self, name):
        return await self.pool.hlen(name)

    async def hmset(self, name, mapping, time=None):
        res = await self.pool.hmset(name, mapping)
        if time:
            await self.pool.expire(name, time)
        return res

    async def hmget(self, name, keys, *args):
        return await self.pool.hmget(name, keys, *args)

    async def hsetnx(self, name, key, value):
        return await self.pool.hsetnx(name, key, value)

    async def hvals(self, name):
        return await self.pool.hvals(name)

    async def sadd(self, name, values: list, time=None):
        res = await self.pool.sadd(name, *values)
        if time:
            await self.pool.expire(name, time)
        return res

    async def scard(self, name):
        return await self.pool.scard(name)

    async def sismember(self, name, value):
        return await self.pool.sismember(name, value)

    async def smembers(self, name):
        return await self.pool.smembers(name)

    async def spop(self, name, count):
        return await self.pool.spop(name, count)

    async def srem(self, name, *values):
        return await self.pool.srem(name, *values)

    def sync_set(self, name, value, ex=None, px=None, nx: bool = False, xx: bool = False, keepttl: bool = False):
        return self.get_connection(sync=True).set(name, value, ex, px, nx, xx, keepttl)

    def sync_get(self, name):
        return self.get_connection(sync=True).get(name)

    def sync_keys(self, pattern):
        return self.get_connection(sync=True).keys(pattern=pattern)

    def sync_exists(self, *name):
        return self.get_connection(sync=True).exists(*name)

    def sync_delete(self, names):
        if isinstance(names, list) or isinstance(names, tuple):
            return self.get_connection(sync=True).delete(*names)
        else:
            return self.get_connection(sync=True).delete(names)

    def sync_rpush(self, name, values: list, time=None):
        con = self.get_connection(sync=True)
        res = con.rpush(name, *values)
        if time:
            con.expire(name, time)
        return res

    def sync_hset(self, name, key=None, value=None, mapping=None, time=None):
        con = self.get_connection(sync=True)
        res = con.hset(name, key=key, value=value, mapping=mapping)
        if time:
            con.expire(name, time)
        return res

    def sync_hgetall(self, name):
        return self.get_connection(sync=True).hgetall(name)

    def sync_hget(self, name, key):
        return self.get_connection(sync=True).hget(name, key)

    def sync_hdel(self, name, key):
        return self.get_connection(sync=True).hdel(name, key)

    def sync_hexists(self, name, key):
        return self.get_connection(sync=True).hexists(name, key)

    def sync_hincrby(self, name, key, amount: int):
        return self.get_connection(sync=True).hincrby(name, key, amount)

    def sync_hincrbyfloat(self, name, key, amount: float):
        return self.get_connection(sync=True).hincrbyfloat(name, key, amount)

    def sync_hkeys(self, name):
        return self.get_connection(sync=True).hkeys(name)

    def sync_hlen(self, name):
        return self.get_connection(sync=True).hlen(name)

    def sync_hmset(self, name, mapping, time=None):
        con = self.get_connection(sync=True)
        res = con.hmset(name, mapping)
        if time:
            con.expire(name, time)
        return res

    def sync_hmget(self, name, keys, *args):
        return self.get_connection(sync=True).hmget(name, keys, *args)

    def sync_hsetnx(self, name, key, value):
        return self.get_connection(sync=True).hsetnx(name, key, value)

    def sync_hvals(self, name):
        return self.get_connection(sync=True).hvals(name)

    def sync_sadd(self, name, values: list, time=None):
        con = self.get_connection(sync=True)
        res = con.sadd(name, *values)
        if time:
            con.expire(name, time)
        return res

    def sync_scard(self, name):
        return self.get_connection(sync=True).scard(name)

    def sync_sismember(self, name, value):
        return self.get_connection(sync=True).sismember(name, value)

    def sync_smembers(self, name):
        return self.get_connection(sync=True).smembers(name)

    def sync_spop(self, name, count):
        return self.get_connection(sync=True).spop(name, count)

    def sync_srem(self, name, *values):
        return self.get_connection(sync=True).srem(name, *values)
