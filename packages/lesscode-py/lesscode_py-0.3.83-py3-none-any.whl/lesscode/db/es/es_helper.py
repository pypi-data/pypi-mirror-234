# -*- coding: utf-8 -*-
import importlib
import json
import logging
import os
import traceback
from datetime import datetime

from tornado.options import options


class EsHelper:
    """
    ElasticsearchHelper  ES数据库操作实现
    """

    def __init__(self, pool):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.conn_info = options.database[pool]
        else:
            self.pool = pool

    async def send_es_post(self, bool_must_list=None, param_list=None, route_key="", sort_list=None, size=10,
                           offset=0,
                           track_total_hits=False):
        params = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            },
            "size": size,
            "from": offset,
        }
        if track_total_hits:
            params["track_total_hits"] = track_total_hits
        if param_list:
            params["_source"] = {"include": param_list}
        if sort_list:
            params["sort"] = sort_list
        start_time = datetime.now()

        res = self.pool.es_selector_way(url_func_str=self.pool.format_es_post_url, param_dict={
            "route_key": route_key,
        }, find_condition=params)
        logging.info("进程{}，路由{},查询时间{}".format(os.getpid(), route_key, datetime.now() - start_time))

        if "error" in list(res.keys()):
            logging.info(res)
        return res["hits"]

    async def format_es_return(self, bool_must_list=None, param_list=None, route_key="", sort_list=None, size=10,
                               offset=0,
                               track_total_hits=False, is_need_es_score=False, is_need_decrypt_oralce=False, res=None):
        if not res:
            res = await self.send_es_post(bool_must_list, param_list, route_key=route_key, sort_list=sort_list,
                                          size=size,
                                          offset=offset,
                                          track_total_hits=track_total_hits)

        result_list = []
        try:
            es_utils = importlib.import_module("lesscode_utils.es_utils")
        except ImportError as e:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils")
        for r in res["hits"]:
            result_list.append(
                es_utils.format_es_param_result(r, param_list, is_need_decrypt_oralce, is_need_es_score, route_key))
        result_dict = {
            "data_count": res["total"]["value"],
            "data_list": result_list
        }
        return result_dict

    async def format_es_scan(self, bool_must_list=None, param_list=None, route_key="", scroll="5m", size=10000,
                             is_need_decrypt_oralce=False, limit=None):
        logging.info("扫描开始，条件是{},查询字段是{}".format(json.dumps(bool_must_list), json.dumps(param_list)))
        skip = 0
        request_param = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            }
            , "size": size,
        }
        if param_list:
            request_param["_source"] = {"include": param_list}
        res = self.pool.es_selector_way(url_func_str=self.pool.format_scroll_url, param_dict={
            "route_key": route_key,
            "scroll": scroll
        }, find_condition=request_param)
        data_size = len(res["hits"]["hits"])
        logging.info(
            "扫描{}:{}条花费时间{}ms,".format(route_key, str(skip) + "-" + str(skip + data_size), res["took"]))
        scroll_id = res["_scroll_id"]
        result_list = []
        try:
            encryption_algorithm = importlib.import_module("lesscode_utils.encryption_algorithm")
        except ImportError:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils")
        for data in res["hits"]["hits"]:
            if is_need_decrypt_oralce:
                data["_id"] = encryption_algorithm.AES.encrypt(key=options.aes_key, text=data["_id"])
            data["_source"]["_id"] = data["_id"]
            result_list.append(data["_source"])
        while True:
            skip = skip + data_size

            res = self.pool.es_selector_way(url_func_str=self.pool.format_scroll_id_url, param_dict={
            }, find_condition={
                "scroll": scroll,
                "scroll_id": scroll_id})
            data_size = len(res["hits"]["hits"])
            logging.info(
                "扫描{}:{}条花费时间{}ms,".format(route_key, str(skip) + "-" + str(skip + data_size), res["took"]))
            scroll_id = res.get("_scroll_id")
            # end of scroll
            if scroll_id is None or not res["hits"]["hits"]:
                break
            for data in res["hits"]["hits"]:
                data["_source"]["_id"] = data["_id"]
                result_list.append(data["_source"])
            if limit and limit <= len(result_list):
                break
        return result_list

    async def format_es_group(self, bool_must_list=None, route_key="", aggs=None):
        params = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            },
            "size": 0,
            "aggs": aggs
        }
        res = self.pool.es_selector_way(url_func_str=self.pool.format_es_post_url, param_dict={
            "route_key": route_key,
        }, find_condition=params)
        return res

    async def es_search(self, route_key, body):
        path = f"/{route_key}/_search"
        url = self.pool.format_url(path)
        res = self.pool.format_es_post(url, body=body)
        return res

    def sync_send_es_post(self, bool_must_list=None, param_list=None, route_key="", sort_list=None, size=10,
                          offset=0,
                          track_total_hits=False):
        params = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            },
            "size": size,
            "from": offset,
        }
        if sort_list:
            params["sort"] = sort_list
        try:
            if options.correction_param.get("enable"):
                mappings = self.pool.es_selector_way(url_func_str=self.pool.format_es_mapping_url,
                                                     param_dict={"route_key": route_key},
                                                     request_way="get").get(route_key, {}).get("mappings", {}).get(
                    "properties", {})
                self.correction_param(params, mappings)
        except:
            logging.info(traceback.format_exc())
        if track_total_hits:
            params["track_total_hits"] = track_total_hits
        if param_list:
            params["_source"] = {"include": param_list}
        start_time = datetime.now()

        res = self.pool.es_selector_way(url_func_str=self.pool.format_es_post_url, param_dict={
            "route_key": route_key,
        }, find_condition=params)
        logging.info("进程{}，路由{},查询时间{}".format(os.getpid(), route_key, datetime.now() - start_time))
        if "error" in list(res.keys()):
            logging.info(res)
            return None
        return res["hits"]

    def correction_param(self, param, mappings):
        for k in param:
            if k in ["terms", "term", "range", "wildcard", "sort"]:
                param[k] = self.correction_field(param[k], mappings, keyword_flag=True)
            elif k in ["match", "match_phrase"]:
                param[k] = self.correction_field(param[k], mappings)
            else:
                if isinstance(param[k], dict):
                    self.correction_param(param[k], mappings)
                elif isinstance(param[k], list):
                    for i in param[k]:
                        self.correction_param(i, mappings)

    def correction_field(self, value, mappings, keyword_flag=False):
        if isinstance(value, dict):
            if value.get("field"):
                column = value["field"]
                column = self.check_replace_keyword(column, mappings, keyword_flag)
                value["field"] = column
                return value
            else:
                column = list(value.keys())[0]
                data_value = value[column]
                column = self.check_replace_keyword(column, mappings, keyword_flag)
                return {
                    column: data_value
                }
        elif isinstance(value, list):
            for index, i in enumerate(value):
                column = list(i.keys())[0]
                data_value = i[column]
                column = self.check_replace_keyword(column, mappings, keyword_flag)
                value[index] = {
                    column: data_value
                }
        return value

    def check_replace_keyword(self, column, mappings, keyword_flag):
        column = column.replace(".keyword", "")
        es_mapping_value = self.get_es_filed_mapping(column, mappings)
        if es_mapping_value:
            if es_mapping_value.get("text") and es_mapping_value.get("keyword"):
                if keyword_flag:
                    column = f'{column}.keyword'
        return column

    def get_es_filed_mapping(self, field, mappings):
        field_list = field.split(".")
        res = self.get_field_children_mapping(field_list, mappings)
        if res:
            if res.get("fields"):
                result = {
                    res["type"]: 1,
                    list(res["fields"].values())[0]["type"]: 1
                }
            else:
                result = {
                    res["type"]: 1
                }
        else:
            result = {}
        return result

    def get_field_children_mapping(self, field_list, mapping):
        if field_list:
            if mapping:
                mapping = mapping.get(field_list[0])
            field_list = field_list[1:]
            if field_list and mapping:
                mapping = mapping.get("properties")
                return self.get_field_children_mapping(field_list, mapping)
            else:
                return mapping

    def get_mapping_text_and_keyword_column(self, mapping, reuslt, column=""):
        for key in mapping:
            # 获取value的key都有什么是否拥有type和fields
            value_mapping = mapping[key]
            if value_mapping.get("type") in ["text", "keyword"] and value_mapping.get("index", True):
                if value_mapping.get("fields"):
                    reuslt[f'{column}.{key}' if column else key] = {
                        "text": 1,
                        "keyword": 1
                    }
                else:
                    reuslt[f'{column}.{key}' if column else key] = {
                        value_mapping["type"]: 1
                    }
            elif isinstance(value_mapping.get("type"), str):
                continue
            else:
                self.get_mapping_text_and_keyword_column(mapping[key], reuslt,
                                                         (f'{column}.{key}' if column else key) if key not in [
                                                             "properties", "fields",
                                                             "keyword"] else column)

    def sync_format_es_return(self, bool_must_list=None, param_list=None, route_key="", sort_list=None, size=10,
                              offset=0,
                              track_total_hits=False, is_need_es_score=False, is_need_decrypt_oralce=False, res=None):
        if not res:
            res = self.sync_send_es_post(bool_must_list, param_list, route_key=route_key, sort_list=sort_list,
                                         size=size,
                                         offset=offset,
                                         track_total_hits=track_total_hits)
        result_list = []
        data_count = 0
        try:
            es_utils = importlib.import_module("lesscode_utils.es_utils")
        except ImportError as e:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils")
        if res:
            for r in res["hits"]:
                result_list.append(
                    es_utils.format_es_param_result(r, param_list, is_need_decrypt_oralce, is_need_es_score, route_key))
            data_count = res["total"]["value"]
        result_dict = {
            "data_count": data_count,
            "data_list": result_list
        }
        return result_dict

    def sync_format_es_scan(self, bool_must_list=None, param_list=None, route_key="", scroll="5m", size=10000,
                            is_need_decrypt_oralce=False, limit=0, offset=0, sort_list=None):
        logging.info("扫描开始，条件是{},查询字段是{}".format(json.dumps(bool_must_list), json.dumps(param_list)))
        skip = 0
        limit = offset + limit
        params = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            }
            , "size": size
        }
        if sort_list:
            params["sort"] = sort_list
        try:
            if options.correction_param.get("enable"):
                mappings = self.pool.es_selector_way(url_func_str=self.pool.format_es_mapping_url,
                                                     param_dict={"route_key": route_key},
                                                     request_way="get").get(route_key, {}).get("mappings", {}).get(
                    "properties", {})
                self.correction_param(params, mappings)
        except:
            logging.error(traceback.format_exc())
        if param_list:
            params["_source"] = {"include": param_list}
        res = self.pool.es_selector_way(url_func_str=self.pool.format_scroll_url, param_dict={
            "route_key": route_key,
            "scroll": scroll
        }, find_condition=params)
        data_size = len(res["hits"]["hits"])
        logging.info(
            "扫描{}:{}条花费时间{}ms,".format(route_key, str(skip) + "-" + str(skip + data_size), res["took"]))
        scroll_id = res["_scroll_id"]
        result_list = []
        try:
            encryption_algorithm = importlib.import_module("lesscode_utils.encryption_algorithm")
        except ImportError:
            raise Exception(f"lesscode_utils is not exist,run:pip install lesscode_utils")
        for data in res["hits"]["hits"]:
            if is_need_decrypt_oralce:
                data["_id"] = encryption_algorithm.AES.encrypt(key=options.aes_key, text=data["_id"])
            data["_source"]["_id"] = data["_id"]
            result_list.append(data["_source"])
        while True:
            skip = skip + data_size

            res = self.pool.es_selector_way(url_func_str=self.pool.format_scroll_id_url, param_dict={
            }, find_condition={
                "scroll": scroll,
                "scroll_id": scroll_id})
            data_size = len(res["hits"]["hits"])
            logging.info(
                "扫描{}:{}条花费时间{}ms,".format(route_key, str(skip) + "-" + str(skip + data_size), res["took"]))
            scroll_id = res.get("_scroll_id")
            # end of scroll
            if scroll_id is None or not res["hits"]["hits"]:
                break
            for data in res["hits"]["hits"]:
                if is_need_decrypt_oralce:
                    data["_id"] = encryption_algorithm.AES.encrypt(key=options.aes_key, text=data["_id"])
                data["_source"]["_id"] = data["_id"]
                result_list.append(data["_source"])
            if limit and limit <= len(result_list):
                break
        return result_list[offset:offset + limit]

    def sync_format_es_group(self, bool_must_list=None, route_key="", aggs=None):
        params = {
            "query": {
                "bool": {
                    "must": bool_must_list
                }
            },
            "size": 0,
            "aggs": aggs
        }
        try:
            if options.correction_param.get("enable"):
                mappings = self.pool.es_selector_way(url_func_str=self.pool.format_es_mapping_url,
                                                     param_dict={"route_key": route_key},
                                                     request_way="get").get(route_key, {}).get("mappings", {}).get(
                    "properties", {})
                self.correction_param(params, mappings)
        except:
            logging.error(traceback.format_exc())

        res = self.pool.es_selector_way(url_func_str=self.pool.format_es_post_url, param_dict={
            "route_key": route_key,
        }, find_condition=params)
        if "error" in list(res.keys()):
            logging.info(res)
            return {
                "aggregations": {
                    "NAME": {
                        "buckets": []
                    }
                }
            }
        return res

    def sync_delete_one(self, route_key, id, doc_type="_doc"):
        path = f"/{route_key}/{doc_type}/{id}"
        url = self.pool.format_url(path)
        res = self.pool.format_es_delete(url=url)
        return res

    def sync_delete_data(self, route_key, params=None, doc_type="_doc"):
        if params is None:
            params = []
        path = f"/{route_key}/{doc_type}/_delete_by_query"
        url = self.pool.format_url(path)
        data = {
            "query": {
                "bool": {
                    "must": params
                }
            }
        }
        res = self.pool.format_es_delete(url=url, data=data)
        return res

    def sync_update_data(self, route_key, params, new_data: dict, doc_type="_doc"):
        path = f"/{route_key}/{doc_type}/_update_by_query"
        url = self.pool.format_url(path)
        data = {
            "query": {
                "bool": {
                    "must": params
                }
            },
            "script": {
                "source": ""
            }
        }
        source = ""
        for k, v in new_data.items():
            source += f'ctx._source.{k}={v};'
        data["script"]["source"] = source
        res = self.pool.format_es_post(url=url, body=data)
        return res

    def sync_update_one(self, route_key, id, data, doc_type="_doc"):
        path = f"/{route_key}/{doc_type}/{id}/_update"
        url = self.pool.format_url(path)
        res = self.pool.format_es_post(url, body=data)
        return res

    def sync_insert_one(self, route_key, data, id=None, doc_type="_doc"):
        if id:
            path = f"/{route_key}/{id}/{doc_type}"
        else:
            path = f"/{route_key}/{doc_type}"
        url = self.pool.format_url(path)
        res = self.pool.format_es_post(url, body=data)
        return res

    def sync_insert_data(self, route_key, data, doc_type="_doc"):
        path = f"/{route_key}/{doc_type}/_bulk"
        url = self.pool.format_url(path)
        res = self.pool.format_es_post(url, body=data)
        return res

    def sync_es_search(self, route_key, body):
        path = f"/{route_key}/_search"
        url = self.pool.format_url(path)
        self.correction_body(route_key, body)
        res = self.pool.format_es_post(url, body=body)
        if "error" in res:
            raise Exception(f"res={res}")
        return res

    def correction_body(self, route_key, body):
        try:
            es_mapping_res = self.sync_es_mapping(route_key)
            es_mapping = es_mapping_res.get(route_key, {}).get("mappings", {}).get("properties", {})
            self.correction_param(body, es_mapping)
        except Exception as e:
            traceback.format_exc()

    def sync_es_search_format_hits(self, route_key, body):
        res = self.sync_es_search(route_key, body)
        hits = res.get("hits", {})
        data_count = hits.get("total", {}).get("value", 0)
        data_list = hits.get("hits", [])
        result = {
            "data_count": data_count,
            "data_list": data_list
        }
        return result

    def sync_es_search_format_aggregations(self, route_key, body):
        res = self.sync_es_search(route_key, body)
        hits = res.get("hits", {})
        data_count = hits.get("total", {}).get("value", 0)
        data_list = hits.get("hits", [])
        aggregations = res.get("aggregations")
        result = {
            "data_count": data_count,
            "data_list": data_list,
            "aggregations": aggregations
        }
        return result

    def sync_es_scan(self, route_key, body, scroll="5m"):
        path = f"/{route_key}/_search?scroll={scroll}"
        url = self.pool.format_url(path)
        self.correction_body(route_key, body)
        res = self.pool.format_es_post(url, body=body)
        data_list = []
        if "error" in res:
            raise Exception(f"res={res}")
        hits = res.get("hits", {}).get("hits", [])
        for x in hits:
            data_list.append(x)
        scroll_id = res.get("_scroll_id")
        scroll_path = f"/_search/scroll"
        scroll_url = self.pool.format_url(scroll_path)
        while scroll_id:
            res = self.pool.format_es_post(scroll_url, body={'scroll': scroll, 'scroll_id': scroll_id})
            if "error" in res:
                raise Exception(f"res={res}")
            hits = res.get("hits", {}).get("hits", [])
            scroll_id = res.get("_scroll_id")
            if hits:
                for x in hits:
                    data_list.append(x)
            else:
                break
        data_count = len(data_list)
        result = {
            "data_count": data_count,
            "data_list": data_list
        }
        return result

    def sync_es_mapping(self, route_key, field: str = None):
        path = f"/{route_key}/_mapping"
        if field:
            path = f"{path}/field/{field}"
        url = self.pool.format_url(path)
        res = self.pool.format_es_get(url)
        return res

    def sync_es_request(self, path, method, params=None, body=None):
        url = self.pool.format_url(path)
        method = method.lower()
        if method in ["get", "post", "put", "delete"]:
            res = None
            if method == "get":
                res = self.pool.format_es_get(url=url, params=params)
            elif method == "post":
                res = self.pool.format_es_post(url=url, body=body, params=params)
            elif method == "put":
                res = self.pool.format_es_put(url=url, body=body, params=params)
            elif method == "delete":
                res = self.pool.format_es_delete(url=url, params=params)
            return res
        else:
            raise Exception(f"method={method} is not supported")
