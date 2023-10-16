# -*- coding: utf-8 -*-
import importlib
import random


class EsRequest:

    def __init__(self, host, port, user, password):

        # 主机地址
        self.host = host
        # 端口号
        self.port = port
        # 用户名
        self.user = user
        # 密码
        self.password = password
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        self.auth = httpx.BasicAuth(user, password)
        host_str = host.split(",")
        self.hosts = [host for host in host_str]

    def es_selector_way(self, url_func_str, param_dict, find_condition=None, request_way="post"):
        if request_way == "get":
            request_way = self.format_es_get
        else:
            request_way = self.format_es_post
        res = None
        # 随机打乱列表
        random.shuffle(self.hosts)
        for host in self.hosts:
            param_dict["host"] = host
            param_dict["port"] = self.port
            url = url_func_str(**param_dict)
            try:
                res = request_way(url, find_condition)
                if res.get("took"):
                    break
            except:
                continue
        return res

    def format_es_post(self, url, body, params=None):
        """
        发送http请求
        :param params:
        :param url:
        :param body:
        :return:
        """
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        r = httpx.post(
            url,
            json=body,
            headers={'content-type': "application/json"},
            params=params,
            auth=self.auth
        )
        res = r.json()
        return res

    def format_es_put(self, url, body, params=None):
        """
        发送http请求
        :param params:
        :param url:
        :param body:
        :return:
        """
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        r = httpx.put(
            url,
            params=params,
            json=body,
            headers={'content-type': "application/json"},
            auth=self.auth
        )
        res = r.json()
        return res

    def format_es_get(self, url, params=None):
        """
        发送http请求
        :param params:
        :param url:
        :return:
        """
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        r = httpx.get(
            url,
            params=params,
            headers={'content-type': "application/json"},
            auth=self.auth
        )
        res = r.json()
        return res

    def format_es_delete(self, url, params=None):
        """
        发送http请求
        :param params:
        :param url:
        :return:
        """
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        r = httpx.delete(
            url,
            params=params,
            headers={'content-type': "application/json"},
            auth=self.auth
        )
        res = r.json()
        return res

    def format_scroll_url(self, host=None, port=None, route_key=None, scroll=None):
        return self.replace_url_kwargs("http://{host}{port}/{route_key}/_search?scroll={scroll}",
                                       {"host": host, "port": port, "route_key": route_key, "scroll": scroll})

    def format_scroll_id_url(self, host=None, port=None, ):
        return self.replace_url_kwargs("http://{host}{port}/_search/scroll",
                                       {"host": host, "port": port})

    def format_es_post_url(self, host=None, port=None, route_key=None):
        return self.replace_url_kwargs("http://{host}{port}/{route_key}/_search",
                                       {"host": host, "port": port, "route_key": route_key})

    def format_url(self, path, host=None, port=None):
        return self.replace_url_kwargs("http://{host}{port}{path}",
                                       {"host": host, "port": port, "path": path})

    def format_es_mapping_url(self, host=None, port=None, route_key=None):
        return self.replace_url_kwargs("http://{host}{port}/{route_key}/_mapping",
                                       {"host": host, "port": port, "route_key": route_key})

    def replace_url_kwargs(self, replace_url, replace_kwargs):
        if not replace_kwargs["host"]:
            replace_kwargs["host"] = self.host
        if not replace_kwargs["port"]:
            replace_kwargs["port"] = self.port
        if replace_kwargs.get("port"):
            replace_kwargs["port"] = f':{replace_kwargs["port"]}'
        else:
            replace_kwargs["port"] = ""
        replace_url = replace_url.format(**replace_kwargs)
        return replace_url

    def close(self):
        pass
