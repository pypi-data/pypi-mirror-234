import importlib
from contextlib import contextmanager

from tornado.options import options


class SqlAlchemyHelper:
    def __init__(self, pool):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.conn_info = options.database[pool]
        else:
            self.pool = pool

    @contextmanager
    def make_session(self, **kwargs):
        try:
            sqlalchemy_orm = importlib.import_module("sqlalchemy.orm")
        except ImportError:
            raise Exception(f"sqlalchemy is not exist,run:pip install sqlalchemy==1.4.36")
        session = None
        try:
            db_session = sqlalchemy_orm.scoped_session(sqlalchemy_orm.sessionmaker(bind=self.pool, **kwargs))
            session = db_session()
            yield session
        except Exception:
            if session:
                session.rollback()
            raise
        else:
            session.commit()
        finally:
            if session:
                session.close()


def alchemy_default_to_dict(params, data, repetition=False):
    data_list = []
    key_list = []
    if repetition:
        for arg in params:
            if arg.key:
                key_list.append(arg.key)
            else:
                key_list.append(arg.name)
    else:
        for arg in params:
            arg = str(arg)
            if "(" in arg and ")" in arg:
                key_list.append(arg.split(".")[-1][:-1])
            else:
                key_list.append(arg.split(".")[-1])
    if isinstance(data, list):
        for d in data:
            dict_data = dict(zip(key_list, d))
            data_list.append(dict_data)
        return data_list
    else:
        if data:
            return dict(zip(key_list, data))
        else:
            return {}


def sqlalchemy_paging(query, limit_number, offset_number):
    data_list = query.limit(limit_number).offset(offset_number).all()
    data_count = query.count()
    return {"count": data_count, "dataSource": data_list}


def covert_relationship_property(attr, attr_value):
    if attr.__class__.__name__ == 'ColumnProperty':
        return attr_value
    elif attr.__class__.__name__ in ['RelationshipProperty', 'Relationship']:
        attrs = []
        for ar, ar_value in attr.mapper.attrs.items():
            if ar_value.__class__.__name__ == 'ColumnProperty' and ar not in attrs:
                attrs.append(ar)
        if attr_value.__class__.__name__ == 'InstrumentedList' or isinstance(attr_value, list):
            new_data = []
            for item in attr_value:
                info = dict()
                for ar in attrs:
                    new_attr_value = getattr(item, ar)
                    if new_attr_value.__class__.__name__ not in ['RelationshipProperty', 'InstrumentedList']:
                        info[ar] = new_attr_value
                    else:
                        info = covert_relationship_property(ar, new_attr_value)
                if info:
                    new_data.append(info)
            return new_data
        else:
            new_data = dict()
            for column, value in attr.entity.attrs.items():
                if value.__class__.__name__ not in ['RelationshipProperty', 'InstrumentedList']:
                    val = getattr(attr_value, column)
                    if val.__class__.__name__ not in ['RelationshipProperty', 'InstrumentedList']:
                        new_data[column] = val
            return new_data
    else:
        return attr_value


def query_set_to_dict(obj):
    if obj:
        if hasattr(obj, "__mapper__"):
            obj_dict = {}
            mapper = obj.__mapper__
            if hasattr(mapper, "attrs"):
                attrs = mapper.attrs
                for column, attr in attrs.items():
                    attr_value = getattr(obj, column)
                    value = covert_relationship_property(attr, attr_value)
                    if not value.__class__.__name__ == 'RelationshipProperty':
                        obj_dict[column] = value

            return obj_dict
        elif hasattr(obj, "keys"):
            return {key: getattr(obj, key) for key in obj.keys()}
        elif hasattr(obj, "_asdict"):
            return obj._asdict()
        else:
            return dict(obj)
    else:
        return obj


def query_set_to_list(query_set):
    ret_list = []
    for obj in query_set:
        ret_dict = query_set_to_dict(obj)
        ret_list.append(ret_dict)
    return ret_list


def result_to_json(data):
    if isinstance(data, list):
        return query_set_to_list(data)
    else:
        return query_set_to_dict(data)


def result_page(query, page_num=1, page_size=10):
    offset_number = (page_num - 1) * page_size if page_num >= 1 else 0
    data_list = result_to_json(query.limit(page_size).offset(offset_number).all())
    data_count = query.count()
    return {"count": data_count, "dataSource": data_list}
