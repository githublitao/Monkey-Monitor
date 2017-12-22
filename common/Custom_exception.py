#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
Created on 2017年8月22日

@author: li tao
"""
#   自定义异常类，可自行添加


class ConnectAdbError(Exception):
    """
    adb 连接异常
    """
    def __init__(self, err='adb 连接失败'):
        Exception.__init__(self, err)


class GetPidError(Exception):
    """
    获取应用PID异常
    """
    def __init__(self, err='adb 连接失败或应用未运行，无法获取应用PID'):
        Exception.__init__(self, err)

