import json
import logging
import time
from typing import Union, Optional, Awaitable

from tornado.websocket import WebSocketHandler

from lesscode.utils.json import JSONEncoder


class BaseWebSocketHandler(WebSocketHandler):
    def check_origin(self, origin):
        """重写同源检查 解决跨域问题"""
        return True

    def open(self):
        """新的websocket连接后被调动"""
        logging.info(f"建立连接")

    def on_close(self):
        """websocket连接关闭后被调用"""
        logging.info(f"关闭连接")

    def on_message(self, message: Union[str, bytes]):
        """
        接收请求函数，返回数据的方法为：self.write_message(message: Union[bytes, str, Dict[str, Any]], binary: bool = False)
        :param message: 接受消到息
        :return:
        """
        while True:
            try:
                if self.ws_connection is not None and not self.ws_connection.is_closing():
                    data = self.push_message(message)
                    data = json.dumps(data, cls=JSONEncoder)
                    future = self.write_message(data)
                    future.done()
                    delay_time = 2
                    if hasattr(self, "delay_time"):
                        delay_time = getattr(self, "delay_time")
                    time.sleep(delay_time)
                else:
                    break
            except Exception as e:
                logging.info(e.__str__())
                break

    def push_message(self, message: Union[str, bytes]):
        pass
