'''
Author: Hexu
Date: 2022-03-14 09:53:59
LastEditors: Hexu
LastEditTime: 2023-05-24 15:59:01
FilePath: /iw-algo-fx/intelliw/core/infer.py
Description: Infer core
'''
# coding: utf-8
from intelliw.interface.apihandler import Request
from intelliw.core.pipeline import Pipeline


class Infer:
    """
    infer entrypoint
    """
    def __init__(self, path, reporter_addr=None, report_interval=-1):
        self.pipeline = Pipeline(reporter_addr, report_interval)
        self.pipeline.importmodel(path)

    def infer(self, data, request=Request(), func='infer', need_feature=True):
        """
        infer
        """
        return self.pipeline.infer(data, request, func, need_feature)

    def report_callback(self):
        """
        report_callback
        """
        self.pipeline.report_callback_infer()
