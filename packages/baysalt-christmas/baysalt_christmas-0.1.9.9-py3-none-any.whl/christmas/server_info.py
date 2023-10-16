#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2022/12/2 00:10
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import os
import getpass
import socket


def grep_from_top(_exe):  # sourcery skip: inline-immediately-returned-variable
    """
    从top命令中获取进程信息
    :param _exe: 进程名
    :return:
    """
    # ps -ef | grep top | grep -v grep | awk '{print $2}'
    script = f'ps -ef  | grep {_exe}' + ' | grep -v  grep | awk \'{print $2}\''
    pid = os.popen(script).read()
    return pid


def grep_from_top_mpi(_exe):
    """
    从top命令中获取进程信息
    :param _exe: 进程名
    :return:
    """
    # ps -ef | grep top | grep -v grep | awk '{print $2}'
    script = f'ps -ef  | grep {_exe}' + ' | grep -v  grep | awk \'{print $2}\' | wc -l'
    mpi_num = int(os.popen(script).read())
    if mpi_num != 0:
        mpi_num -= 1
    return mpi_num


def get_free_core():
    """
    获取空闲可用的cpu数
    :return: 空闲可用的cpu数
    """
    cpu_num = os.popen("echo $(grep processor /proc/cpuinfo | wc -l)").read()
    used_cpu_percent = os.popen("echo $(top -n 1 -b | grep Cpu | awk '{print $2}')").read()
    used_cpu_num = int(float(used_cpu_percent) / 100 * int(cpu_num))
    cpu_num = int(cpu_num)
    free_cpu_num = cpu_num - used_cpu_num
    return cpu_num, free_cpu_num


def get_serve_info():
    """
    获取服务器信息
    :return: 服务器信息
    """
    user = getpass.getuser()
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return user, hostname, ip
