# -*- coding: UTF-8 -*-
# @Time : 2023/10/7 17:16 
# @Author : 刘洪波
import os
import sys


def check_make_dir(dir_str: str):
    """检查路径是否存在，不存在就创建"""
    if not os.path.exists(dir_str):
        os.makedirs(dir_str)


def get_execution_dir():
    """获取执行代码的目录"""
    return sys.path[0]
