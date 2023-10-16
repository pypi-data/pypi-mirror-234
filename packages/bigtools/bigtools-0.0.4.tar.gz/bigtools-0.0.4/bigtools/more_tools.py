# -*- coding: UTF-8 -*-
# @Time : 2023/9/27 17:50 
# @Author : 刘洪波
import socket
import os


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
