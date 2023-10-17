'''
Author: Hexu
Date: 2022-04-08 17:13:36
LastEditors: Hexu
LastEditTime: 2023-05-22 14:00:18
FilePath: /iw-algo-fx/intelliw/__init__.py
Description: intelliw
'''
__version__ = "1.2.13rc1"

logo = f"""\033[92m
-------------------------------------------------------------
         ⓐ                    _    _    ⓘ
         _  _ __    _    ___ | |  | |   _  _     _
        | || '_ \ _| |_ / _ \| |  | |  | |\ \ _ / /
        | || | | |_   _|  __/| |__| |__| | \  _  /
        |_||_| |_| |___|\___| \____\___|_|  \/ \/

           intelliw  -- {__version__} Version --
-------------------------------------------------------------\033[0m
"""
print(logo, flush=True)

from intelliw.utils import exception
