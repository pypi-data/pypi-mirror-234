'''
Author: hexu
Date: 2021-10-25 15:20:34
LastEditTime: 2023-05-24 15:15:48
LastEditors: Hexu
Description: api处理函数
FilePath: /iw-algo-fx/intelliw/interface/apihandler.py
'''
import time
import json
import traceback
from inspect import isfunction

import flask
from flask import current_app as app
from flask import request, jsonify, views
import intelliw.utils.message as message
from intelliw.config import config
from intelliw.utils.util import get_json_encoder
from intelliw.utils.logger import _get_framework_logger

logger = _get_framework_logger()


class Request:
    """
    intelliw server request
    """

    def __init__(self) -> None:
        self.header = None
        self.json = ""
        self.query = {}
        self.form = {}
        self.files = []
        self.body = ""
        self.batch_params = {}


class BaseHandler():
    """
    BaseHandler
    """

    def __init__(self):
        self.infer_request = Request()

    def request_process(self):
        """
        request process
        """
        is_ok = True
        try:
            self.infer_request.header = request.headers

            # query
            query = request.args.to_dict()
            self.infer_request.query = query

            # body
            self.infer_request.body = request.get_data()
            req_data = {}
            content_type = request.headers.get('Content-Type', "").strip()
            if content_type.startswith('application/x-www-form-urlencoded') or \
                    content_type.startswith('multipart/form-data'):
                req_data = request.form.to_dict(False)
                self.infer_request.form = req_data
            elif content_type.startswith('application/json'):
                req_data = request.json
                self.infer_request.json = req_data

            # 如果body中没东西，那请求内容可以尝试从query中获取
            if not req_data:
                req_data = query

            # files
            self.infer_request.files = request.files
        except Exception as e:
            stack = traceback.format_exc()
            req_data = message.APIResponse(
                400, "api", f"API服务请求解析错误: {e}, Body: {str(request.data)}, Stack: {stack}")
            return req_data, not is_ok
        return req_data, is_ok

    def response_process(self, data, func, need_feature, is_stream=False):
        """
        response process
        """
        try:
            result, emsg = app.config["infer"].infer(
                data, self.infer_request, func, need_feature)
            if emsg is None:
                if is_stream and isfunction(result):
                    return result, True
                resp = message.APIResponse(200, "api", '', result)
            else:
                resp = message.APIResponse(500, "api", emsg, result)
        except Exception as e:
            self.error_report(e)
            resp = message.APIResponse(
                500, "api", f"API服务处理推理数据错误 {e}")
        return resp, False

    def error_report(self, err: Exception):
        """
        error report 
        """
        stack_info = traceback.format_exc()
        logger.error("API服务处理推理数据错误 %s stack: %s", err, stack_info)
        msg = [{'status': 'inferfalied',
                'inferid': config.INFER_ID,
                'instanceid': config.INSTANCE_ID,
                'inferTaskStatus': [{
                    "id": config.INFER_ID, "issuccess": False,
                    "starttime": int(time.time() * 1000),
                    "endtime": int(time.time() * 1000),
                    "message": "API服务处理推理数据错误"
                }]}]

        app.config["reporter"].report(
            message.CommonResponse(500, "inferstatus", f"API服务处理推理数据错误 {err}",
                                   json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))


class HealthCheckHandler(views.MethodView):
    """健康检查"""

    def post(self):
        """
        request method post
        """
        resp = message.HealthCheckResponse(200, "api", 'ok', "")
        return jsonify(resp())

    def get(self):
        """
        request method get
        """
        resp = message.HealthCheckResponse(200, "api", 'ok', "")
        return jsonify(resp())


class EurekaHealthCheckHandler(views.MethodView):
    """eureka健康检查"""

    def get(self):
        """
        request method get
        """
        return "ok", 200


class MainHandler(views.MethodView):
    """
    server request entrypoint
    """

    def get(self, func, need_feature=True):
        """
        request method get
        """
        return self.__do(func, need_feature)

    def post(self, func, need_feature=True):
        """
        request method post
        """
        return self.__do(func, need_feature)

    def put(self, func, need_feature=True):
        """
        request method put
        """
        return self.__do(func, need_feature)

    def delete(self, func, need_feature=True):
        """
        request method delete
        """
        return self.__do(func, need_feature)

    def options(self, func, need_feature=True):
        """
        request method options
        """
        return self.__do(func, need_feature)

    def patch(self, func, need_feature=True):
        """
        request method patch
        """
        return self.__do(func, need_feature)

    def head(self, func, need_feature=True):
        """
        request method head
        """
        return self.__do(func, need_feature)

    def __do(self, func, need_feature):
        base = BaseHandler()
        result, is_ok = base.request_process()

        # 简单评估下是否为流式请求
        is_stream = False
        if isinstance(result, dict) and 'stream' in result:
            is_stream = True

        # 进行推理处理
        if is_ok:
            result, is_stream = base.response_process(result, func, need_feature, is_stream=is_stream)

        # 再次确定是否为流式请求
        if is_stream:
            return flask.Response(result(), mimetype="text/event-stream")
        return jsonify(result())
