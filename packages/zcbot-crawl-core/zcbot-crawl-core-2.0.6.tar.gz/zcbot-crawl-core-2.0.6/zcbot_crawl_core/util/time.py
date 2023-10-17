"""
Time Utilities

fast approaches to commonly used time/date related functions
"""
import datetime
import time
from typing import Optional
from dateutil import tz


def now() -> datetime.datetime:
    """
    get datetime instance of time of now
    :return: time of now
    """
    return datetime.datetime.now(tz.gettz('Asia/Shanghai'))


def __get_t(t: Optional[datetime.datetime] = None) -> datetime.datetime:
    """
    get datetime instance
    :param t: optional datetime instance
    :return: datetime instance
    """
    return t if isinstance(t, datetime.datetime) else now()


def to_str(t: Optional[datetime.datetime] = None,
           fmt: str = '%Y-%m-%d %H:%M:%S.%f') -> str:
    """
    get string formatted time
    :param t: optional datetime instance
    :param fmt: string format
    :return:
    """
    return __get_t(t).strftime(fmt)


def to_seconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to seconds
    :param t: optional datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp())


def to_milliseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to milliseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10 ** 3)


def to_microseconds(t: Optional[datetime.datetime] = None) -> int:
    """
    datetime to microseconds
    :param t: datetime instance
    :return: timestamp in seconds
    """
    return int(__get_t(t).timestamp() * 10 ** 6)


def get_dt(start_t: datetime.datetime,
           end_t: Optional[datetime.datetime] = None) -> datetime.timedelta:
    """
    get delta time
    :param start_t: start time
    :param end_t: end time
    :return: timedelta instance
    """
    return __get_t(end_t) - start_t


def to_seconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to seconds
    :param dt: timedelta instance
    :return: seconds elapsed
    """
    return int(dt.total_seconds())


def to_milliseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to milliseconds
    :param dt: timedelta instance
    :return: milliseconds elapsed
    """
    return int(dt.total_seconds() * 10 ** 3)


def to_microseconds_dt(dt: datetime.timedelta) -> int:
    """
    delta time to microseconds
    :param dt: timedelta instance
    :return: microseconds elapsed
    """
    return int(dt.total_seconds() * 10 ** 6)


def parse_timestamp(time_str, tz_str='Asia/Shanghai'):
    """
    将时间戳解析成本地时间(自动截断毫秒)
    :param time_str:
    :param tz_str:
    :return:
    """
    if time_str:
        # 1576839034000
        if len(str(time_str)) > 10:
            # 截取掉毫秒
            time_str = str(time_str)[0:10]
        return datetime.datetime.fromtimestamp(int(time_str)).astimezone(tz.gettz(tz_str))


def time_to_batch_id(dt, delta_hour=0, delta_day=0, err=''):
    """
    # 将采购时间转换为批次编号(delta为0时，时间应为iso时间)，delta为正则加为负则减
    """
    try:
        if dt and isinstance(dt, datetime.datetime):
            if delta_hour or delta_day:
                time_delta = datetime.timedelta(hours=int(delta_hour), days=int(delta_day))
                dt = dt + time_delta
            return int(dt.strftime("%Y%m%d"))
    except ValueError:
        return err


def current_timestamp13():
    """
    13位当前时间时间戳（毫秒级时间戳）
    :return:
    """
    return int(round(time.time() * 1000))


def current_timestamp10():
    """
    10位当前时间时间戳（秒级时间戳）
    :return:
    """
    return int(time.time())


if __name__ == '__main__':
    print(parse_timestamp(str(int(now().timestamp()))))
