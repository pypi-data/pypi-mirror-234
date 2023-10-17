'''
Author: Hexu
Date: 2022-12-26 15:23:59
LastEditors: Hexu
LastEditTime: 2022-12-26 16:16:40
FilePath: /iw-algo-fx/intelliw/utils/redis/connection.py
Description: redis handler
'''
from redis import StrictRedis
from redis.sentinel import Sentinel

# 引擎池，uri -> engine obj
__engines = {}


class Conn:
    '''
    simple abstraction class to transparently split redis master/slave read+write operations for scaling out e.g. redis-sentinel clusters.
    '''

    def __init__(self,
                 host='localhost',
                 port='6379',
                 password=None,
                 timeout=5.0,
                 slave_only=False,
                 sentinel_master=False,
                 ssl=False,
                 db=0):
        self.host = host
        self.port = port
        self.slave_only = slave_only
        self.sentinel_master = sentinel_master

        if self.sentinel_master:
            self.conn = Sentinel([(self.host, self.port)],
                                 password=password,
                                 socket_timeout=timeout,
                                 ssl=ssl)
        else:
            self.conn = StrictRedis(host=self.host,
                                    port=self.port,
                                    password=password,
                                    db=db,
                                    socket_timeout=timeout,
                                    socket_keepalive=True,
                                    retry_on_timeout=True,
                                    decode_responses=False,
                                    ssl_cert_reqs=None,
                                    ssl=ssl)
        # Heat up the redis cache
        self.conn.ping()

    def get_master(self) -> Sentinel:
        if self.sentinel_master:
            return self.conn.master_for(self.sentinel_master)
        else:
            return self.conn

    def get_slave(self) -> StrictRedis:
        if self.sentinel_master:
            return self.conn.slave_for(self.sentinel_master)
        else:
            return self.conn

    def __getattr__(self, name):
        def handlerFunc(*args, **kwargs):
            if self.slave_only:
                return getattr(self.get_slave(), name)(*args, **kwargs)
            else:
                return getattr(self.get_master(), name)(*args, **kwargs)
        return handlerFunc


def get_engine(host='localhost',
               port='6379',
               password=None,
               timeout=5.0,
               slave_only=False,
               sentinel_master=False,
               ssl=False,
               db=0,
               use_cache=True) -> Conn:
    """

    Args:
        host(str): ip或者'localhost'
        port(str): 端口或者'6379'
        password(str): 密码
        timeout(float): 请求超时
        slave_only(bool): 仅使用单机模式
        sentinel_master(bool): 使用哨兵集群
        ssl(bool): 使用安全套接字协议
        db(int): 数据库名称
        use_cache(bool): 使用缓存

    Returns: redis connection

    """
    uri = f'{host}:{port}'
    if use_cache:
        if uri not in __engines:
            __engines[uri] = Conn(host, port, password, timeout, slave_only, sentinel_master, ssl, db)
        return __engines[uri]
    else:
        return Conn(host, port, password, timeout, slave_only, sentinel_master, ssl, db)
