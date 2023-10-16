# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 16:02:44
# @Author  : Pane Li
# @File    : locators.py
"""
locators

"""
from playwright.sync_api import Page

from inhandtest.pages.ingateway.edge_computing.edge_computing_locators import EdgeComputingLocators
from inhandtest.pages.ingateway.network.network_locators import NetworkLocators
from inhandtest.pages.ingateway.overview.overview_locators import OverviewLocators
from inhandtest.pages.ingateway.system.system_locators import SystemLocators


class IgLocators:
    def __init__(self, page: Page, locale):
        self.page = page
        self.locale = locale
        self.overview_locators = OverviewLocators(page, self.locale)
        self.network_locators = NetworkLocators(page, self.locale)
        self.edge_locators = EdgeComputingLocators(page, self.locale)
        self.system_locators = SystemLocators(page, self.locale)
