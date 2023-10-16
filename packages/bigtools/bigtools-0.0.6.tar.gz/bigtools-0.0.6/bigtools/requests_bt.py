# -*- coding: UTF-8 -*-
# @Time : 2023/9/27 17:58 
# @Author : 刘洪波
import time
import random
import requests
from requests.adapters import HTTPAdapter
from functools import wraps
from tqdm import tqdm


def get_requests_session(max_retries: int = 3):
    """
    使用requests Session，使抓取数据的时候可以重试
    # 默认设置重试次数为3次
    """
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=max_retries))
    session.mount('https://', HTTPAdapter(max_retries=max_retries))
    return session


class DealException(object):
    """处理异常返回的装饰器"""
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(e)
        return wrapped_function


# 下载数据
def download(url: str, file_name: str, headers: dict, read_timeout: int = 15,
             file_size=0, max_retries: int = 3):
    if 'Range' in headers:
        del headers['Range']

    requests_session = get_requests_session(max_retries)

    @DealException()
    def get_data():
        return requests_session.get(url, headers=headers, stream=True, timeout=(read_timeout, 5))
    resp_ = get_data()
    total_ = int(resp_.headers.get('content-length', 0))
    if file_size < total_:
        file_op = 'wb'
        if file_size:
            headers['Range'] = f'bytes={file_size}-'
            file_op = 'ab'
        time.sleep(random.random())
        resp = get_data()
        with open(file_name, file_op) as file, tqdm(
            desc=file_name,
            total=total_,
            initial=file_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    else:
        print(file_name, ' ✅')
        time.sleep(random.randint(1, 3))
