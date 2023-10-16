import uuid
from datetime import datetime, tzinfo
from typing import Union


class JobInfo:
    def __init__(self, func, name: str = None, year: Union[int, str] = None, month: Union[int, str] = None,
                 day: Union[int, str] = None,
                 week: Union[int, str] = None, day_of_week: Union[int, str] = None,
                 hour: Union[int, str] = None, minute: Union[int, str] = None, second: Union[int, str] = None,
                 start_date: Union[datetime, str] = None, end_date: Union[datetime, str] = None,
                 timezone: Union[tzinfo, str] = None, func_args: Union[list, tuple] = None, func_kwargs: dict = None,
                 *args, **kwargs):
        uid = uuid.uuid4().hex
        self.id = uid
        self.name = name or uid
        self.func = func
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second
        self.start_date = start_date
        self.end_date = end_date
        self.timezone = timezone
        self.func_args = func_args
        self.func_kwargs = func_kwargs
        self.args = args
        self.kwargs = kwargs
