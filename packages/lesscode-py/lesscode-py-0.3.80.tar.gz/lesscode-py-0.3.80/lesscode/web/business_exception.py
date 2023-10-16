# -*- coding: utf-8 -*-


class BusinessException(RuntimeError):
    """
    BusinessException 统一异常类型，增加状态码信息
    """

    def __init__(self, status_code):
        super(BusinessException, self).__init__(status_code[1])
        self.status_code = status_code
