# -*- coding: UTF-8 -*-
# @Time : 2023/9/27 16:28 
# @Author : 刘洪波
from pymongo import MongoClient
from pytz import timezone


def mongo_client(host: str, port, user: str = None, password: str = None,
                 tz_aware: bool = True, tzinfo: str = 'Asia/Shanghai'):
    uri = f"mongodb://{host}:{port}"
    if user and password:
        uri = f"mongodb://{user}:{password}@{host}:{port}"
    elif user:
        raise ValueError('Please check user and password')
    elif password:
        raise ValueError('Please check user and password')
    return MongoClient(uri, tz_aware=tz_aware, tzinfo=timezone(tzinfo))
