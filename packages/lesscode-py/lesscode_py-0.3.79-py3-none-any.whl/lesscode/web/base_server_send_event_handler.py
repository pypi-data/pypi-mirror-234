import json
import time
from typing import Optional, Awaitable

from tornado.iostream import StreamClosedError
from tornado.options import options
from tornado.web import RequestHandler

from lesscode.utils.json import JSONEncoder
from lesscode.web.business_exception import BusinessException
from lesscode.web.response_result import ResponseResult
from lesscode.web.status_code import StatusCode


class BaseServerSentEventHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def __init__(self, *args, **kwargs):
        super(BaseServerSentEventHandler, self).__init__(*args, **kwargs)
        self.set_header('Content-Type', 'text/event-stream')

    def get_request_arguments(self):
        _arguments = dict()
        query_arguments = self.request.query_arguments or dict()
        if query_arguments:
            for k, v in query_arguments.items():
                if isinstance(v, list) or isinstance(v, tuple):
                    if len(v) > 0:
                        _arguments.update({k: v[0]})
        content_type = self.request.headers.get('Content-Type')
        if content_type:
            if "application/json" in content_type:
                request_body = self.request.body
                if request_body:
                    body_arguments = json.loads(self.request.body.decode())
                    _arguments.update(body_arguments)
            else:
                body_arguments = self.request.body_arguments
                if body_arguments and isinstance(body_arguments, dict):
                    _arguments.update(body_arguments)
        return _arguments

    def handler(self):
        arguments = self.get_request_arguments()
        push_flag = arguments.get("push_flag", True)
        delay_time = 2
        if hasattr(self, "delay_time"):
            delay_time = getattr(self, "delay_time")
        try:
            while push_flag:
                message = self.push_message(**arguments)
                if message:
                    message = json.dumps(message, cls=JSONEncoder)
                    self.write(f'data:{message}\n\n')
                time.sleep(delay_time)
                self.flush()
            else:
                self.finish()  # 结束长连接
        except StreamClosedError as e:
            self.finish()
        except RuntimeError as e:
            self.finish()

    def get(self):
        self.handler()

    def post(self):
        self.handler()

    def push_message(self, *args, **kwargs):
        pass

    def set_default_headers(self):
        """ 设置header参数
            重写父类方法
        :return:
        """
        if not options.cors:
            origin = self.request.headers.get("Origin")
            if origin:
                self.set_header("Access-Control-Allow-Origin", origin)
            else:
                self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Request-Id", self.request.headers.get("Request-Id", ""))
            self.set_header("Plugin-Running-Time", self.request.headers.get("Plugin-Running-Time", ""))
            self.set_header("Access-Control-Allow-Headers",
                            "x-requested-with,Authorization,Can-read-cache,Content-Type,User")
            self.set_header("Access-Control-Allow-Methods", "POST,GET,PUT,DELETE,OPTIONS")
            self.set_header("Access-Control-Expose-Headers", "Access-Token")
            self.set_header("Access-Control-Allow-Credentials", "true")
            self.set_header('Content-Type', 'text/event-stream')
        else:
            origin = self.request.headers.get("Origin")
            if origin:
                self.set_header("Access-Control-Allow-Origin", origin)
            else:
                self.set_header("Access-Control-Allow-Origin", "*")
            for key, value in options.cors.items():
                self.set_header(key, value)

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

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.process_exception(exception=kwargs.get('exc_info')[1])
