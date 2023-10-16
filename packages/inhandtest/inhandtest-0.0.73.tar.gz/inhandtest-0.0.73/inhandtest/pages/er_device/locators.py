# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:38
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : locators.py
@IDE     : PyCharm
------------------------------------
"""
from playwright.sync_api import Page, Locator


class BaseLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def docker_manager(self) -> Locator:
        return self.page.locator('#enable').nth(0)
