# -*- coding: utf-8 -*-
import json
import traceback
from typing import Optional, Awaitable, Union

from tornado.web import RequestHandler

from lesscode.utils.es_log.record_log import es_record_log
from lesscode.utils.json import JSONEncoder
from lesscode.web.business_exception import BusinessException
from lesscode.web.response_result import ResponseResult
from lesscode.web.status_code import StatusCode


class NativeHandler(RequestHandler):
    def prepare(self):
        self.process_request(self.request)

    def process_request(self, request):
        """
        预处理请求中间件，对请求内容进行改写
        :param request:
        :return:
        """
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        视图中间件，对视图进行处理
        :param request:
        :param view_func:
        :param view_args:
        :param view_kwargs:
        :return:
        """
        pass

    def process_exception(self, exception: Exception):
        """
        异常处理中间件
        :param exception:
        :return:
        """
        if isinstance(exception, BusinessException):
            self.write(json.dumps(ResponseResult(status_code=exception.status_code), ensure_ascii=False))
        else:
            self.write(json.dumps(ResponseResult(StatusCode.INTERNAL_SERVER_ERROR(exception)), ensure_ascii=False))

    def process_response(self, data):
        """
        处理响应数据的中间件
        :param data:
        :return:
        """
        self.write(data)

    def write_error(self, status_code, **kwargs):
        es_record_log(request=self.request, message=traceback.format_exc(), level="error", status_code=status_code)
        self.process_exception(exception=kwargs.get('exc_info')[1])

    def write(self, chunk: Union[str, bytes, dict] = None):
        super(NativeHandler, self).write(chunk)
        self.finish()

    def json_response(self, data):
        if not isinstance(data, str) and not isinstance(data, bytes) and not isinstance(data, dict):
            data = json.dumps(ResponseResult(data=data), ensure_ascii=False, cls=JSONEncoder)
        self.process_response(data)

    def response(self, data):
        self.process_response(data)

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
