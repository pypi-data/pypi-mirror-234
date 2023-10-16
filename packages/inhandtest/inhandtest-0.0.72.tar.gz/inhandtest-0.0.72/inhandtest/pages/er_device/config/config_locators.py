# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:47
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : config_locators.py
@IDE     : PyCharm
------------------------------------
"""
from playwright.sync_api import Page


class ConfigLocators():
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def config_locator(self) -> list:
        return [
            ('docker_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('docker_manager1', {'locator': 'expand', 'type': 'switch_button'}),
            ('docker_manager2', {'locator': [self.page.locator('#enable').nth(0), self.page.locator('#enable').nth(0)],
                                 'type': 'switch_button'}),
            ('docker_version',
             {'locator': {"ER805_V2.0.10": self.page.locator('#enable').nth(0),
                          "ER805": self.page.locator('#enable').nth(0), 'ER605': self.page.locator('#enable').nth(0)},
              'type': 'text'}),
            ('docker_version1', {'locator': {"ER805": 'expand', 'ER605': 'expand'}, 'type': 'text'}),
        ]