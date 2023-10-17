'''
Author: Hexu
Date: 2022-09-26 13:34:19
LastEditors: Hexu
LastEditTime: 2022-12-26 16:18:04
FilePath: /iw-algo-fx/intelliw/utils/redis/__init__.py
Description: 
'''
try:
    import redis
except ImportError:
    raise ImportError("\033[31mIf use redis, you need: pip install redis (>=4.3) \033[0m")

from .connection import get_engine