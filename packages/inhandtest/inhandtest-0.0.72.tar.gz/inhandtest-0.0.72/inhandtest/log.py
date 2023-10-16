# -*- coding: utf-8 -*-
# @Time    : 2023/6/14 14:07:30
# @Author  : Pane Li
# @File    : log.py
"""
log

"""
import logging


def enable_log(filename: str = None, console_level='info'):
    """

    :param filename:  日志文件名称 ex: './test.log'
    :param console_level: 'info', 'debug'
    :return:
    """
    if console_level.lower() == 'info':
        console_level = logging.INFO
    else:
        console_level = logging.DEBUG
    import colorlog
    console_handler = logging.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s %(levelname)s [%(module)s]:%(message)s',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(formatter)
    if filename is not None:
        file_handler = logging.FileHandler(filename)  # 日志文件及名称
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s]:%(message)s'))
        logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
        file_handler.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
    console_handler.setLevel(console_level)
