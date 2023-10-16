# -*- coding: utf-8 -*-
# @Time    : 2022/11/7 16:38
# @Author  : navysummer
# @Email   : navysummer@yeah.net
import datetime
import importlib
import json
import logging
import traceback

from tornado.options import options

from lesscode.utils.json import JSONEncoder


def es_record_log(request, message="", level="info", status_code=200, task_id=None):
    log_es_config = options.log_es_config if options.log_es_config else {}
    if log_es_config.get("enable"):
        request_headers = dict(request.headers)
        request_params = dict(request.query_arguments)
        content_type = request.headers.get('Content-Type')
        request_body = request.body
        try:
            request_body = request_body.decode()
        except Exception as e:
            traceback.print_exc()
        request_id = request_headers.get("Request-Id", "")
        log_data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_id": task_id,
            "level": level,
            "request": {
                "id": request_id,
                "header": request_headers,
                "params": request_params,
                "url": request.path,
                "Content-Type": content_type,
                "method": request.method,
                "body": request_body,
                "real_ip": request.remote_ip
            },
            "status_code": status_code,
            "message": message
        }
        connect_name = log_es_config.get("connect_name")
        protocol = log_es_config.get('protocol', 'http')
        es_index = log_es_config.get('index', "request_log")
        logging.info(f"es_record_log task task_id={task_id}")
        send_es(protocol, connect_name, es_index, log_data)


def send_es(protocol, connect_name, es_index, body):
    try:
        httpx = importlib.import_module("httpx")
    except ImportError as e:
        raise Exception(f"httpx is not exist,run:pip install httpx==0.24.1")
    try:
        pool, conn_info = options.database[connect_name]
        url = f"{protocol}://{conn_info.host}:{conn_info.port}/{es_index}/_doc/"
        res = httpx.post(
            url,
            data=json.dumps(body, ensure_ascii=False, cls=JSONEncoder).encode('utf-8'),
            headers={'content-type': "application/json"},
            auth=httpx.BasicAuth(conn_info.user, conn_info.password)
        )

        if res.ok:
            logging.info(f"send es url={url} success")
        else:
            logging.info(f"send es url={url} fail")
    except Exception as e:
        logging.error(traceback.format_exc())
