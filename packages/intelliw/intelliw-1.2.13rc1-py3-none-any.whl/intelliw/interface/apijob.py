#!/usr/bin/env python
# coding: utf-8
import logging
import os
import json
import time
import traceback

import flask
import datetime
import threading
import numpy as np
from importlib.util import find_spec
from flask import Flask as _Flask

from intelliw.utils import message
from intelliw.config import config
from intelliw.core.infer import Infer
from intelliw.utils.logger import _get_framework_logger
from intelliw.interface import apihandler
from intelliw.utils.util import get_json_encoder


def encode_default(obj, func):
    if isinstance(obj, (np.integer, np.floating, np.bool_)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (datetime.datetime, datetime.timedelta)):
        return obj.__str__()
    return func(obj)


if hasattr(flask.json, 'provider'):
    from flask.json.provider import DefaultJSONProvider, _default as FlaskDefault


    class FlaskJSONProvider(DefaultJSONProvider):
        """重载flask的json encoder, 确保jsonfy()能解析numpy的json"""

        @staticmethod
        def _default(obj):
            return encode_default(obj, FlaskDefault)

        default = _default


    class Flask(_Flask):
        """重载flask的json_provider_class, 确保能解析numpy的json"""
        json_provider_class = FlaskJSONProvider
else:
    from flask.json import JSONEncoder as _JSONEncoder


    class FlaskJSONEncoder(_JSONEncoder):
        """重载flask的json encoder, 确保jsonfy()能解析numpy的json"""

        def default(self, obj):
            return encode_default(obj, super(FlaskJSONEncoder, self).default)


    class Flask(_Flask):
        """重载flask的jsonencoder, 确保能解析numpy的json"""
        json_encoder = FlaskJSONEncoder

logger = _get_framework_logger()


class Application():
    """推理服务路由类
    example:
        @Application.route("/infer-api", method='get', need_feature=True)
        def infer(self, test_data):
            pass
    args:
        path           访问路由   /infer-api
        method         访问方式，支持 get post push delete head patch options
        need_feature   是否需要使用特征工程, 如果是自定义与推理无关的函数, 请设置False
    """

    # Set URL handlers
    HANDLERS = []

    def __init__(self, custom_router):
        file_dir_path = os.path.dirname(__file__)
        self.app = Flask(
            __name__,
            template_folder=os.path.join(file_dir_path, "templates"),
            static_folder=os.path.join(file_dir_path, "static")
        )
        self.__handler_process(custom_router)

    def __call__(self):
        return self.app

    @classmethod
    def route(cls, path, **options):
        """
        register api route
        """

        def decorator(function):
            cls.HANDLERS.append((
                path, apihandler.MainHandler,
                {'func': function.__name__,
                 'method': options.pop('method', 'post').lower(),
                 'need_feature': options.pop('need_feature', True)}))
            return function

        return decorator

    def __handler_process(self, routers):
        # 加载自定义api, 配置在algorithm.yaml中
        for router in routers:
            Application.HANDLERS.append((
                router["path"], apihandler.MainHandler,
                {'func': router["func"],
                 'method': router.get("method", "post").lower(),
                 'need_feature': router.get("need_feature", True)}))

        # 检查用户是否完全没有配置路由
        if len(Application.HANDLERS) == 0:
            Application.HANDLERS.append((
                '/predict', apihandler.MainHandler,
                {'func': 'infer', 'method': 'post', 'need_feature': True}))  # 默认值

        # 集中绑定路由
        _route_cache = {}
        for router, _, info in Application.HANDLERS:
            func, method, need_feature = info.get('func'), info.pop(
                'method'), info.get('need_feature')
            if _route_cache.get(router + func, None):
                continue
            _route_cache[router + func] = True
            self.app.add_url_rule(
                router,
                view_func=apihandler.MainHandler.as_view(router),
                methods=[method], defaults=info)
            logger.info("方法: %s 加载成功, 访问路径：%s, 访问方法: %s, 是否需要特征处理: %s",
                        func, router, method, need_feature)

        # healthcheck
        # gateway
        self.app.add_url_rule(
            '/healthcheck',
            view_func=apihandler.HealthCheckHandler.as_view("healthcheck"))

        # eureka
        self.app.add_url_rule(
            '/CloudRemoteCall/',
            view_func=apihandler.EurekaHealthCheckHandler.as_view("eurekahealthcheck"))


class ApiService:
    """
    intelliw api service
    """

    def __init__(self, port, path, response_addr):
        self.port = port  # 8888
        self.report_interval = config.PERODIC_INTERVAL or 10
        infer = Infer(path, response_addr, self.report_interval)
        self.reporter = infer.pipeline.recorder
        self.custom_router = infer.pipeline.custom_router
        self.app = Application(self.custom_router)()
        self.app.config.update({"infer": infer, "reporter": self.reporter})

        self._report_start()

    def _report_start(self):
        """
        report start
        """
        msg = [{'status': 'start',
                'inferid': config.INFER_ID,
                'instanceid': config.INSTANCE_ID,
                'inferTaskStatus': []}]
        self.reporter.report(message.CommonResponse(
            200, "inferstatus", '',
            json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)
        ))

    def _eureka_server(self):
        if len(config.EUREKA_SERVER) > 0:
            from intelliw.core.linkserver import linkserver
            try:
                should_register = config.EUREKA_APP_NAME != ''
                iports = json.loads(config.REGISTER_CLUSTER_ADDRESS)
                profile = config.EUREKA_ZONE or 'test'
                linkserver.client(
                    config.EUREKA_SERVER, config.EUREKA_PROVIDER_ID,
                    should_register, config.EUREKA_APP_NAME, iports, profile)
                logger.info("eureka server client init success, register:%s, server name: %s",
                            should_register, config.EUREKA_APP_NAME)
            except Exception as e:
                logger.error(
                    f"eureka server client init failed, error massage: {e}")

    def _flask_server(self):
        # 定时批量上报
        if self.report_interval > 0:
            timer = threading.Timer(
                self.report_interval,
                self.report_callback
            )
            timer.daemon = True
            timer.start()

        if (config.INFER_MULTI_PROCESS or config.INFER_MULTI_THREAD) and find_spec("gunicorn"):
            from intelliw.utils import gunicorn_server
            worker, thread = 1, None
            if config.INFER_MULTI_PROCESS:
                worker = gunicorn_server.number_of_workers(config.CPU_COUNT)
            if config.INFER_MULTI_THREAD:
                thread = gunicorn_server.number_of_threads(config.CPU_COUNT)
            setting = gunicorn_server.default_config(
                f'0.0.0.0:{self.port}',
                workers=worker,
                threads=thread,
            )
            logger.info(f"intelliw gunicorn server  worker: {worker}, thread: {thread}")
            gunicorn_server.GunServer(self.app, setting, logger).run()
        else:
            self.app.run('0.0.0.0', self.port, debug=False, threaded=True)

    def report_callback(self):
        """
        infer report
        """
        infer = self.app.config["infer"]
        logger.info(f"infer request callback start, report interval: {self.report_interval}")
        while True:
            try:
                infer.report_callback()
            except Exception as e:
                logger.error(f"infer request callback error： {e}")
                traceback.print_exc()
            time.sleep(self.report_interval)

    def run(self):
        """
        start server
        """
        self._eureka_server()
        self._flask_server()
