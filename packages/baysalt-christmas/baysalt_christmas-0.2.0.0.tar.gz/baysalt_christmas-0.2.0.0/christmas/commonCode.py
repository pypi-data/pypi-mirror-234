# -*- coding: utf-8 -*-
#  日期 : 2022/11/30 11:33
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""

import contextlib
import datetime
import numpy as np
import os
import sys
import time
from .cprintfs import osprint, osprints, cprintf


def convertToTime(strDate=None, listDate=None, _input_format=None, tzinfo=datetime.timezone.utc):
    """
    将 %Y%m%d 格式的8位字符串，转换为日期
    :param strDate: %Y%m%d 格式的8位日期字符串
    :param listDate: %Y%m%d 格式的8位日期字符串列表
    :param _input_format: 输入日期格式
    :param tzinfo: 时区
    :return: datetime 类型的日期
    """
    date = datetime.datetime.now()  # 默认取当天日期

    if strDate is not None and type(strDate) == str:
        with contextlib.suppress(Exception):
            if _input_format == 'WRF_output':
                date = datetime.datetime.strptime(strDate, "%Y-%m-%d_%H:%M:%S")  # 2022-11-09_01:00:00
            elif len(strDate) == 8:
                date = datetime.datetime.strptime(strDate, "%Y%m%d")
            elif len(strDate) == 10:
                date = datetime.datetime.strptime(strDate, "%Y%m%d%H")
            elif len(strDate) == 12:
                date = datetime.datetime.strptime(strDate, "%Y%m%d%H%M")
            elif len(strDate) == 14:
                date = datetime.datetime.strptime(strDate, "%Y%m%d%H%M%S")
            elif len(strDate) == 19:
                if strDate[10] == ' ':
                    date = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")  # 2022-11-09 01:00:00
                elif strDate[10] == '_':
                    date = datetime.datetime.strptime(strDate, "%Y-%m-%d_%H:%M:%S")  # 2022-11-09_01:00:00
                elif strDate[10] == 'T':
                    date = datetime.datetime.strptime(strDate, "%Y-%m-%dT%H:%M:%S")  # 2022-11-09T01:00:00
        date = date.replace(tzinfo=tzinfo)
    elif listDate is not None and type(listDate) == list:
        with contextlib.suppress(Exception):
            date = [convertToTime(i, _input_format) for i in listDate]
    elif type(strDate) != str and type(listDate) != list:
        raise TypeError('strDate must be str or listDate must be list')
    return date


def new_filename(_pre, _lon, _lat, _date, _res):
    """
    根据前缀、经纬度、日期、分辨率生成输出文件名
    :param _pre: 输出文件前缀
    :param _lon: 经度
    :param _lat: 纬度
    :param _date: 日期
    :param _res: 分辨率
    :return: 输出文件名
    """
    if np.min(_lon) < 0:
        lon_1 = str(format(abs(np.min(_lon)), '.2f')).zfill(6) + 'W'
    else:
        lon_1 = str(format(abs(np.min(_lon)), '.2f')).zfill(6) + 'E'
    if np.max(_lon) < 0:
        lon_2 = str(format(abs(np.max(_lon)), '.2f')).zfill(6) + 'W'
    else:
        lon_2 = str(format(abs(np.max(_lon)), '.2f')).zfill(6) + 'E'
    if np.min(_lat) < 0:
        lat_1 = str(format(abs(np.min(_lat)), '.2f')).zfill(5) + 'S'
    else:
        lat_1 = str(format(abs(np.min(_lat)), '.2f')).zfill(5) + 'N'
    if np.max(_lat) < 0:
        lat_2 = str(format(abs(np.max(_lat)), '.2f')).zfill(5) + 'S'
    else:
        lat_2 = str(format(abs(np.max(_lat)), '.2f')).zfill(5) + 'N'
    filename = f'{_pre}_{lon_1}_{lon_2}_{lat_1}_{lat_2}_{str(_date)}_{str(_res)}.nc'
    del lon_1, lon_2, lat_1, lat_2
    return filename


def get_date():
    """
    获取日期
    :return:
    """
    date = ''
    if len(sys.argv) == 1:
        date = datetime.datetime.now().strftime("%Y%m%d")
    elif len(sys.argv) >= 2 and len(sys.argv[1]) == 8:
        date = sys.argv[1]
    return date


def make_dir(path):
    """
    创建文件夹
    :param path: 文件夹路径
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def makedirs(*path):
    """
    创建文件夹
    :param path: 文件夹路径
    :return:
    """
    for p in path:
        if not os.path.exists(p):
            os.makedirs(p)


def rmfiles(*path):
    """
    删除文件
    :param path: 文件路径
    :return:
    """
    for p in path:
        if os.path.exists(p):
            os.remove(p)


def rmdirs(*path):
    """
    删除文件夹
    :param path: 文件夹路径
    :return:
    """
    for p in path:
        if os.path.exists(p):
            os.removedirs(p)


class FtpUploadTracker:
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self, totalSize, sizeWritten):
        self.totalSize = totalSize

    def handle(self, block):
        self.sizeWritten += len(block)
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)

        if self.lastShownPercent != percentComplete:
            self.lastShownPercent = percentComplete
            if percentComplete % 10 == 0:
                print(f'{str(percentComplete)}% complete')
            # print(str(percentComplete) +"% complete")


def split_path(_path, _split='/'):
    """
    如果路径名最后一位是'/'，则去掉
    :param _path: 路径名
    :param _split: 分隔符
    :return: 路径名
    """
    with contextlib.suppress(IndexError):
        if _path[-1] == _split:
            _path = _path[:-1]
    return _path


def timer(func):
    def inside(self):
        t1 = time.time()
        func(self)
        t2 = time.time()
        print('task time:{:.2f}s'.format(t2 - t1))

    return inside


def whether_instanced(_class):
    """
    判断是否被实例化
    :param _class: 类名
    """
    has_instance = False
    instanced = {}
    instances = globals().copy()

    for var_name, var_value in instances.items():
        if isinstance(var_value, _class):
            has_instance = True
            instanced[var_name] = var_value

    return has_instance, instanced
