# -*- coding: UTF-8 -*-
# @Time : 2023/9/27 17:50 
# @Author : 刘洪波
import socket
import os
from jsonschema import validate


def extract_ip():
    """获取机器ip"""
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception as e:
        print(e)
        ip = ''
    finally:
        st.close()
    return ip


def get_file_size(file_path):
    """
    获取文件大小
    :param:  file_path:文件路径（带文件名）
    :return: file_size：文件大小
    """
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    else:
        return 0


def equally_split_list(list_data: list, num: int):
    """
    将一个list_data按长度num均分
    :param list_data:
    :param num:
    :return:
    """
    return [list_data[i*num:(i+1)*num] for i in range(int(len(list_data)/num) + 1) if list_data[i*num:(i+1)*num]]


def json_validate(schema, json_data):
    """
    验证json是否是模板规定的格式
    :param schema: 模板
    :param json_data:
    :return:
    """
    result = True
    error = None
    try:
        validate(instance=json_data, schema=schema)
    except Exception as e:
        error = e
        result = False
        print(e)
    return result, error
