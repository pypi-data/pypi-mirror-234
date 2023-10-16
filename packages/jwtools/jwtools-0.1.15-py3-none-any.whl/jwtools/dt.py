import datetime
import hashlib
import random
import time
import os
import sys
import traceback
from typing import Dict, Tuple, List


def time_s3(decimal: int = 0) -> float:
    """
    获取当前时间秒级时间戳,保留3位小数
    Return the current time in seconds since the Epoch.
    :return: int|float
    """
    return time_s(3)


def time_s(decimal: int = 0) -> int | float:
    """
    获取当前时间秒级时间戳
    Return the current time in seconds since the Epoch.
    :return: int|float
    """
    if decimal == 0:
        return int(time.time())
    else:
        t = str(time.time())
        d = t.split('.')
        result = t[:len(d[0]) + decimal + 1]
        return float(result)


def time_ms() -> int:
    """
    获取当前时间毫秒级时间戳
    Return the current time in milliseconds since the Epoch.
    :return: int
    """
    t = time.time()
    return int(round(t * 1000))


def time_work(start: float, end: float = None) -> float:
    """
    计算时间差值
    :param start: 开始时间戳
    :param end: 结束时间戳
    :return:
    """
    if end is None:
        end = time.time()

    result = {
        'start': start,
        "end": end,
        'worktime': end - start
    }
    return result


def time_to_timestamp(source_time: str) -> float:
    """
    从时间获取时间戳
    :param source_time:
    :return:
    """
    z1 = source_time.split('.')
    # print(z1)
    a1 = z1[0]
    a2 = float('0.' + z1[1])
    # 先转换为时间数组
    time_array = time.strptime(a1, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(time_array))
    # print(a2)
    dt = timeStamp + a2
    return dt


def timestamp_to_time(timestamp: float) -> str:
    """
    毫秒时间戳转时间显示 显示3位毫秒
    :param timestamp: 毫秒时间戳 如： 1582898150.001
    :return:
    """
    dz = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp))) + '.' + str(timestamp).split('.')[1][0:3]
    return dz


def work_times(times: list, detail=False):
    """
    计算时间间隔信息，
        times = []
        time1 = time.time()
        times.append((time1, 'time1'))
        time2 = time.time()
        times.append((time2, 'time2'))
        result = work_times(times)

    :param times: 时间信息 [(time1, 'time1')]
    :param detail: 是否包含详细信息
    :return:
    """
    # print(times)
    tt = [{'name': times[i][1], 'time': times[i][0] - times[i - 1][0], 'start': times[i - 1][0], 'end': times[i][0]} for i in range(1, len(times))]
    if detail:
        tt = list(map(lambda item: {'name': item['name'], 'time': item['time']}, tt))

    # print_vf(*tt)
    return tt
