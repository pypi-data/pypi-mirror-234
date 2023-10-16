# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 11:12:24
# @Author  : Pane Li
# @File    : __init__.py.py
"""
__init__.py

"""
from inhandtest.base_page.base_page import BasePage
from inhandtest.base_page.table_tr import Table, IgTable

IrTable = Table

__all__ = [
    'BasePage',
    'IrTable',
    'IgTable'
]
