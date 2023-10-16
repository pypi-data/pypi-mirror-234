# -*- coding: utf-8 -*-
import importlib
from functools import reduce

from tornado.options import options


# DataObject = None
# ResultSet = None
# mclient = None
# GraphStorageClient = None
# try:
#     DataObject = importlib.import_module("nebula3.data.DataObject")
#     ResultSet = importlib.import_module("nebula3.data.ResultSet")
#     mclient = importlib.import_module("nebula3.mclient")
#     GraphStorageClient = importlib.import_module("nebula3.sclient.GraphStorageClient")
# except ImportError as e:
#     raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")


class NebulaHelper:
    def __init__(self, pool):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.conn_info = options.database[pool]
        else:
            self.pool, self.conn_info = pool, None

    def exec_gql(self, sql, space=None):
        space = space if space else self.conn_info.db_name
        if not space:
            raise Exception(f"nebula no selection space")
        with self.pool.session_context(self.conn_info.user, self.conn_info.password) as session:
            session.execute(f'USE {space}')
            result = session.execute(sql)
        return result

    def fetch_data(self, sql, space=None):
        result = self.exec_gql(sql, space)
        result = convert(result)
        return result


class NebulaStorageHelper:
    def __init__(self, meta_cache_config: dict = None, storage_address_config: dict = None,
                 graph_storage_client_timeout=60000):
        self.meta_cache_config = meta_cache_config
        self.storage_address_config = storage_address_config
        self.graph_storage_client_timeout = graph_storage_client_timeout

    def get_meta_cache(self):
        meta_cache = None
        if self.meta_cache_config:
            try:
                mclient = importlib.import_module("nebula3.mclient")
            except ImportError:
                raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
            meta_addrs = self.meta_cache_config.get("meta_addrs")
            timeout = self.meta_cache_config.get("timeout", 2000)
            load_period = self.meta_cache_config.get("load_period", 10)
            decode_type = self.meta_cache_config.get("decode_type", 'utf-8')
            meta_cache = mclient.MetaCache(meta_addrs, timeout, load_period, decode_type)
        return meta_cache

    def get_storage_address(self, storage_address):
        try:
            mclient = importlib.import_module("nebula3.mclient")
        except ImportError:
            raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
        storage_address = [mclient.HostAddr(host=sa.get("host"), port=sa.get("port")) for sa in storage_address]
        return storage_address

    def get_graph_storage_client(self, storage_address):
        meta_cache = self.get_meta_cache()
        storage_address = self.get_storage_address(storage_address)
        try:
            graph_storage_client = importlib.import_module("nebula3.sclient.GraphStorageClient")
        except ImportError:
            raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
        graph_storage_client = graph_storage_client.GraphStorageClient(meta_cache, storage_address,
                                                                       self.graph_storage_client_timeout)
        return graph_storage_client

    def scan_vertex(self, storage_address, *args, **kwargs):
        graph_storage_client = self.get_graph_storage_client(storage_address)
        resp = graph_storage_client.scan_vertex(*args, **kwargs)
        data = []
        while resp.has_next():
            result = resp.next()
            for vertex_data in result:
                data.append(vertex_data)
        return data

    def scan_edge(self, storage_address, *args, **kwargs):
        graph_storage_client = self.get_graph_storage_client(storage_address)
        resp = graph_storage_client.scan_edge(*args, **kwargs)
        data = []
        while resp.has_next():
            result = resp.next()
            for edge_data in result:
                data.append(edge_data)
        return data


class CaseAS:
    @staticmethod
    def cast_as():
        try:
            data_object = importlib.import_module("nebula3.data.DataObject")
        except ImportError:
            raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
        return {data_object.Value.NVAL: "as_null",
                data_object.Value.__EMPTY__: "as_empty",
                data_object.Value.BVAL: "as_bool",
                data_object.Value.IVAL: "as_int",
                data_object.Value.FVAL: "as_double",
                data_object.Value.SVAL: "as_string",
                data_object.Value.LVAL: "as_list",
                data_object.Value.UVAL: "as_set",
                data_object.Value.MVAL: "as_map",
                data_object.Value.TVAL: "as_time",
                data_object.Value.DVAL: "as_date",
                data_object.Value.DTVAL: "as_datetime",
                data_object.Value.VVAL: "as_node",
                data_object.Value.EVAL: "as_relationship",
                data_object.Value.PVAL: "as_path",
                data_object.Value.GGVAL: "as_geography",
                data_object.Value.DUVAL: "as_duration"
                }


def list_dict_duplicate_removal(data_list):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + data_list)


def merge_nebula_value(data_list: list) -> dict:
    nodes = []
    relationships = []

    for data in data_list:
        nodes.extend(list(data.values())[0]["nodes"])
        relationships.extend(list(data.values())[0]["relationships"])
    result_dict = {"nodes": list_dict_duplicate_removal(nodes),
                   "relationships": list_dict_duplicate_removal(relationships)}
    return result_dict


def customized_cast_with_dict(val):
    try:
        data_object = importlib.import_module("nebula3.data.DataObject")
    except ImportError:
        raise Exception(f"nebula3 is not exist,run:pip install nebula3-python==3.4.0")
    _type = val._value.getType()
    cast_as = CaseAS.cast_as()
    method = cast_as.get(_type)
    if method is not None:
        value = getattr(val, method, lambda *args, **kwargs: None)()
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = customized_cast_with_dict(v)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = customized_cast_with_dict(v)
        elif isinstance(value, set):
            new_value = set()
            for v in value:
                new_value.add(customized_cast_with_dict(v))
            value = new_value
        elif isinstance(value, tuple):
            new_value = []
            for v in value:
                new_value.append(customized_cast_with_dict(v))
            value = tuple(new_value)
        elif isinstance(value, data_object.Relationship):
            value = {k: customized_cast_with_dict(v) for k, v in value.properties().items()}
        elif isinstance(value, data_object.PathWrapper):
            nodes = []
            relationships = []
            for node in value.nodes():
                vid = customized_cast_with_dict(node.get_id())
                for tag in node.tags():
                    point = {"_vid": vid, "_tag": tag}
                    point.update({k: customized_cast_with_dict(v) for k, v in node.properties(tag).items()})
                    nodes.append(point)
            for rel in value.relationships():
                relationship = {"_name": rel.edge_name(), "_start": customized_cast_with_dict(rel.start_vertex_id()),
                                "_end": customized_cast_with_dict(rel.end_vertex_id())}
                relationship.update({k: customized_cast_with_dict(v) for k, v in rel.properties().items()})
                relationships.append(relationship)
            value = {"nodes": nodes, "relationships": relationships}
        elif isinstance(value, data_object.Node):
            nodes = []
            for tag in value.tags():
                point = {"_vid": customized_cast_with_dict(value.get_id()), "_tag": tag}
                point.update({k: customized_cast_with_dict(v) for k, v in value.properties(tag).items()})
                nodes.append(point)
            value = {"nodes": nodes}
        elif isinstance(value, data_object.Null):
            value = None
        return value
    raise KeyError("No such key: {}".format(_type))


def convert(resp):
    assert resp.is_succeeded()
    value_list = []
    for recode in resp:
        record = recode
        if hasattr(recode, "keys"):
            record = {}
            for key in recode.keys():
                val = customized_cast_with_dict(recode.get_value_by_key(key))
                record[key] = val
        if record:
            value_list.append(record)
    return value_list
