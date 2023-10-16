#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2023/3/25 10:54
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import datetime
import numpy as np
import pandas as pd
from . import convertToTime


def build_date(_date):  # sourcery skip: inline-immediately-returned-variable
    """
    根据要跑模型的日期推出附近日期
    :param _date: 要跑模型的日期
    :return: 附近日期信息
    """
    today = str(_date)
    ymd_yes = (datetime.datetime.strptime(today, '%Y%m%d') - datetime.timedelta(days=1)).strftime('%Y%m%d')
    ymd_yes2 = (datetime.datetime.strptime(today, '%Y%m%d') - datetime.timedelta(days=2)).strftime('%Y%m%d')
    ymd_yes3 = (datetime.datetime.strptime(today, '%Y%m%d') - datetime.timedelta(days=3)).strftime('%Y%m%d')
    year_yes = ymd_yes[:4]
    month_yes = ymd_yes[4:6]
    year_yes2 = ymd_yes2[:4]
    month_yes2 = ymd_yes2[4:6]
    year_yes3 = ymd_yes3[:4]
    month_yes3 = ymd_yes3[4:6]
    ymd_tom = (datetime.datetime.strptime(today, '%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d')
    ymd_tom2 = (datetime.datetime.strptime(today, '%Y%m%d') + datetime.timedelta(days=2)).strftime('%Y%m%d')
    ymd_tom3 = (datetime.datetime.strptime(today, '%Y%m%d') + datetime.timedelta(days=3)).strftime('%Y%m%d')
    year_tom = ymd_tom[:4]
    month_tom = ymd_tom[4:6]
    year_tom2 = ymd_tom2[:4]
    month_tom2 = ymd_tom2[4:6]
    year_tom3 = ymd_tom3[:4]
    month_tom3 = ymd_tom3[4:6]
    Nearby_date = {
        'ymd_yes': ymd_yes,
        'year_yes': year_yes,
        'month_yes': month_yes,
        'ymd_yes2': ymd_yes2,
        'year_yes2': year_yes2,
        'month_yes2': month_yes2,
        'ymd_yes3': ymd_yes3,
        'year_yes3': year_yes3,
        'month_yes3': month_yes3,
        'ymd_tom': ymd_tom,
        'year_tom': year_tom,
        'month_tom': month_tom,
        'ymd_tom2': ymd_tom2,
        'year_tom2': year_tom2,
        'month_tom2': month_tom2,
        'ymd_tom3': ymd_tom3,
        'year_tom3': year_tom3,
        'month_tom3': month_tom3
    }
    return Nearby_date


def Times2Ttime(_Times):
    """
    将datetime格式的时间转换为Ttime格式
    :param _Times: datetime格式的时间
    :return: Ttime格式的时间
    """
    pass


class Ttime:
    def __init__(self, _Times=None, TIME=None):
        """
        _Times: datetime格式的时间

        """
        if TIME is not None:
            TIME = ["".join(TIME[i].astype(str).tolist()) for i in range(len(TIME))]
            self.Times = convertToTime(listDate=TIME)
        else:
            if type(_Times[0]) == np.datetime64:
                _Times = [pd.to_datetime(_Times[i]) for i in range(len(_Times))]

            self.Times = _Times
        self.time = np.NaN * np.zeros(len(self.Times))
        self.TIME = []
        self.TIME_str = [str() for _ in range(len(self.Times))]
        self.TIME_char = np.array([str() for _ in range(len(self.Times))])
        self.units = 'seconds since 1970-01-01 00:00:00'
        self.ymd = ''
        self.construct()

    def construct(self):
        # Times ---> datetime || type: datetime.datetime
        # time ---> positive  || type: np.float64
        # TIME_str ---> str  || type: str
        # TIME_char ---> char || type: np.chararray
        self.time = [i.timestamp() for i in self.Times]
        self.TIME = [i.strftime('%Y-%m-%d %H:%M:%S') for i in self.Times]
        self.TIME_str = np.array(self.TIME)
        
        char_array = np.chararray([len(self.TIME)], len(self.TIME[0]))
        for i in range(len(self.TIME)):
            char_array[i] = self.TIME[i]
        self.TIME_char = np.array(char_array)
        self.ymd = [i.strftime('%Y%m%d') for i in self.Times]
