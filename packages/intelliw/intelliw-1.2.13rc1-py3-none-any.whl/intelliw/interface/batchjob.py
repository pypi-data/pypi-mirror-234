#!/usr/bin/env python
# coding: utf-8
import json
import os
import threading
import time
import traceback
from flask import Flask, jsonify, request

from intelliw.utils.crontab import Crontab
from intelliw.datasets.datasets import get_dataset, get_datasource_writer, \
    DataSets, MultipleDataSets
from intelliw.core.recorder import Recorder
from intelliw.core.infer import Infer
from intelliw.utils import message
from intelliw.datasets.datasource_base import DataSourceReaderException, DataSourceWriterException
from intelliw.utils.util import get_json_encoder
from intelliw.config import config
from intelliw.utils.logger import _get_framework_logger

logger = _get_framework_logger()

batchjob_infer = "batchjob-infer"

INFER_CONTROLLER: Infer = None  # type: ignore


class Request:
    def __init__(self, batch_params={}) -> None:
        self.batch_params = batch_params


def get_batch_msg(issuccess, msg, status=True, starttime=None, user_param={}, system_param={}):
    """
    批处理上报信息，inferTaskStatus 不为空，会被记录为一次调用，标识一次批处理的状态
    """
    infer_task_status = []
    if status:
        infer_task_status = [
            {
                "id": config.INFER_ID, "issuccess": issuccess,
                "starttime": starttime, "endtime": int(time.time() * 1000),
                "message": msg
            }
        ]
    out_msg = [
        {
            'status': 'start' if issuccess else 'end',
            'inferid': config.INFER_ID,
            'instanceid': config.INSTANCE_ID,
            'inferTaskStatus': infer_task_status,
            "params": {"user": user_param, "system": system_param}
        }
    ]
    return json.dumps(out_msg, cls=get_json_encoder(), ensure_ascii=False)


def validate_batch_job(reporter, path):
    global INFER_CONTROLLER
    INFER_CONTROLLER = Infer(path, reporter)
    msg = get_batch_msg(True, '定时推理校验通过，上线成功', status=False)
    reporter.report(message.CommonResponse(200, batchjob_infer,
                                           '定时推理校验通过，上线成功',
                                           json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))


def infer_job(reporter, dataset_cfg, output_dataset_cfg, params={}):
    """
    request json {"user":None, "system": None}
    response json {
                    'status': 'start' if issuccess else 'end',
                    'inferid': config.INFER_ID,
                    'instanceid': config.INSTANCE_ID,
                    'inferTaskStatus': inferTaskStatus,
                    "params": {"user":None, "system": None}
                }
    """
    user_param = params.get("user", {})
    system_param = params.get("system", {})

    def input():
        datasets = get_dataset(dataset_cfg)
        alldata = datasets.read_all_data()
        # 保持与训练一致
        if isinstance(datasets, MultipleDataSets):
            return alldata
        elif isinstance(datasets, DataSets):
            return [alldata]
        else:
            return None

    def output(r):
        writer = get_datasource_writer(output_dataset_cfg)
        res_data = writer.write(r)
        if res_data['status'] != 1:
            raise DataSourceWriterException(res_data['msg'])

    start_time = int(time.time() * 1000)
    result, stack_info, info = None, None, ""
    try:
        # 输入
        alldata = input()

        # 批处理
        req = Request(user_param)
        global INFER_CONTROLLER
        result = INFER_CONTROLLER.pipeline._infer_process(alldata, req)
        logger.info('批处理处理结果 %s', result)

        # 输出
        output(result)
    except DataSourceReaderException as e:
        info = f"批处理输入数据错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    except DataSourceWriterException as e:
        info = f"批处理输出数据错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    except Exception as e:
        info = f"批处理执行错误: {e}"
        stack_info = f"{info}, stack:\n{traceback.format_exc()}"
    else:
        info = "批处理输出数据成功"
    finally:
        status_code = 200
        if stack_info is not None:
            status_code = 500
            logger.error(stack_info)

        msg = get_batch_msg(True, info, user_param=result,
                            system_param=system_param, starttime=start_time)
        reporter.report(
            message.CommonResponse(status_code, batchjob_infer, info, msg)
        )


class JobServer:
    @staticmethod
    def healthcheck():
        resp = message.HealthCheckResponse(200, "api", 'ok', "")
        return jsonify(resp())

    @staticmethod
    def run(reporter, dataset_cfg, output_dataset_cfg):
        msg = "server job start"
        logger.info(msg)
        threading.Thread(
            target=infer_job,
            args=(reporter, dataset_cfg,
                  output_dataset_cfg, request.json)
        ).start()
        return jsonify({"code": "1", "msg": msg})


class BatchService:
    def __init__(self, corn, path, dataset_cfg, output_dataset_cfg, response_addr=None, task='infer'):
        self.reporter = Recorder(response_addr)
        if task != 'infer':
            _msg = '批处理任务任务错误，TASK环境变量必须为infer'
            msg = get_batch_msg(False, _msg, status=False)
            self.reporter.report(message.CommonResponse(500, batchjob_infer,
                                                        _msg,
                                                        json.dumps(msg, cls=get_json_encoder(), ensure_ascii=False)))
        self.corn = corn
        self.only_server = not corn
        self.dataset_cfg = dataset_cfg
        self.output_dataset_cfg = output_dataset_cfg
        self.path = path

    def _format_parse(self):
        return [{
            'crontab': f.strip(),
            'func': infer_job,
            'args': (self.reporter, self.dataset_cfg, self.output_dataset_cfg)
        } for f in self.corn.split("|")]

    def _cronjob(self):
        job_list = self._format_parse()
        crontab = Crontab(job_list, True)
        crontab.start()
        logger.info("Start cronjob")

    def _server(self):
        app = Flask(__name__)
        args = {"reporter": self.reporter, "dataset_cfg": self.dataset_cfg,
                "output_dataset_cfg": self.output_dataset_cfg}
        app.add_url_rule("/batch-predict", view_func=JobServer.run,
                         methods=["POST"], defaults=args)
        app.add_url_rule(
            "/healthcheck", view_func=JobServer.healthcheck, methods=["POST", "GET"])
        logger.info(
            "Server Start: \n\033[33m[POST] /batch-predict\n[POST, GET] /healthcheck\033[0m"
        )
        app.run('0.0.0.0', 8888, threaded=True)

    def run(self):
        validate_batch_job(self.reporter, self.path)
        if self.only_server:
            logger.info(
                "\033[33mCronjob Format is Empty, Only Server Mode\033[0m")
            self._server()
        else:
            logger.info(
                "\033[33mCronjob Format is %s,Cronjob and Server Mode\033[0m", self.corn)
            self._cronjob()
            self._server()
