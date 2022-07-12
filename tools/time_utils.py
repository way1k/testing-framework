import datetime
import time


def current_timestamp() -> int:
    """Current time in milliseconds"""
    return int(round(time.time() * 1000))


def time_to_timestamp(s_time: str, time_format: str = "%d/%m/%Y") -> int:
    """
    Convert time to timestamp
    Time format example: "%d/%m/%Y"
    """
    return int(datetime.datetime.strptime(s_time, time_format).timestamp())


def str_to_datetime(str_time: str, time_format: str = "%d/%m/%y %H:%M:%S") -> datetime.datetime:
    """
    Convert str to datetime obj
    :param str_time: time str
    :param time_format: format for datetime parse
    """
    return datetime.datetime.strptime(str_time, time_format)


def timestamp_to_datetime(time_stamp: int) -> datetime.datetime:
    """
    Convert str to datetime obj
    :param time_stamp: time str
    """
    return datetime.datetime.fromtimestamp(time_stamp)
