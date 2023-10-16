# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 11:32
# @Author  : navysummer
# @Email   : navysummer@yeah.net
import importlib
import logging

from tornado.options import options


def upms_register(item, full_url):
    if options.rms_register_enable:
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        client_name = item[3] if item[3] else options.application_name
        title = item[4] if item[4] else full_url
        en_name = item[5] if item[5] else full_url
        access = item[6] if item[6] else 0
        client_res = httpx.get(url=f"{options.rms_register_server}/upms/client/fetchall",
                               params={"client_name": client_name}).json()
        if not client_res.get("data"):
            httpx.post(url=f"{options.rms_register_server}/upms/client/insert",
                       json={"client_name": client_name})
            client_res = httpx.get(url=f"{options.rms_register_server}/upms/client/fetchall",
                                   params={"client_name": client_name}).json()
        client_id = client_res.get("data")[0].get("id")
        resource_res = httpx.get(
            url=f"{options.rms_register_server}/upms/resource/fetchall",
            params={"client_name": client_name, "resource_type": 2, "url": full_url}).json()
        if not resource_res.get("data"):
            res = httpx.post(url=f"{options.rms_register_server}/upms/resource/insert",
                             json={"client_id": client_id, "resource_type": 2, "url": full_url, "label": title,
                                   "en_name": en_name, "access": access}).json()
            if res.get("status") == "00000":
                logging.info(f"add url={full_url} to rms success")
            else:
                logging.info(f"add url={full_url} to rms fail")


def resource_register(resource_type: int, url: str, label: str, access: int, parent_id: str, full_url: str = None):
    if options.resource_register_enable:
        try:
            httpx = importlib.import_module("httpx")
        except ImportError as e:
            raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
        if resource_type == 2:
            url = url if url else full_url
            label = label if label else full_url
            access = access if access else 0
        client_id = options.client_id
        resource_res = httpx.post(
            url=f"{options.rms_register_server}/upms/resource/lesscode/insert",
            json={"client_id": client_id, "resource_type": resource_type, "url": url, "label": label, "access": access,
                  "parent_id": parent_id}).json()
        logging.info(resource_res)
        return resource_res["data"]
