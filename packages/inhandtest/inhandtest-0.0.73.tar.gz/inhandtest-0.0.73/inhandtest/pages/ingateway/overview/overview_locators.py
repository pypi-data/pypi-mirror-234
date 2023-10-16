# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 15:46:53
# @Author  : Pane Li
# @File    : overview_locators.py
"""
overview_locators

"""
from playwright.sync_api import Page, Locator


class OverviewLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def row_(self) -> Locator:
        return self.page.locator('//div[@class="ant-row"]')

    @property
    def overview_locators(self) -> list:
        return [('wan_image',
                 {'locator': self.row_.locator('//div/div/i[@class="anticon anticon-global"]').get_attribute('style'),
                  'type': 'text', 'param': {'enable': 'color: rgb(62, 176, 68);'}}),
                ('wan_ip', {'locator': self.page.locator('//div[./span[text()="WAN IP"]]/span[2]'), 'type': 'text'}),
                ('wan_gateway', {'locator': self.row_.nth(1).locator('//div[2]/div[3]/span[2]'), 'type': 'text'}),
                ('wan_dns', {'locator': self.page.locator('//div[./span[text()="DNS"]]/span[2]'), 'type': 'text'}),
                ('ge_01_image', {'locator': self.row_.nth(2).locator('//div/div/img[@alt="#"]').get_attribute('src'),
                                 'type': 'text', 'param': {'enable': 'PC9zdmc', '==': ' in ', '!=': ' not in '}}),
                ('ge_01_ip', {'locator': self.row_.nth(2).locator('//div[2]/div[2]/span[2]'), 'type': 'text'}),
                ('ge_01_netmask', {'locator': self.row_.nth(2).locator('//div[2]/div[3]/span[2]'), 'type': 'text'}),
                ('ge_02_image', {'locator': self.row_.nth(3).locator('//div/div/img[@alt="#"]').get_attribute('src'),
                                 'type': 'text', 'param': {'enable': 'PC9zdmc', '==': ' not in ', '!=': ' in '}}),
                ('ge_02_ip', {'locator': self.row_.nth(3).locator('//div[2]/div[2]/span[2]'), 'type': 'text'}),
                ('ge_02_netmask', {'locator': self.row_.nth(3).locator('//div[2]/div[3]/span[2]'), 'type': 'text'}),
                ('wireless_image',
                 {'locator': self.row_.nth(5).locator('//div/div/i').get_attribute('style'), 'type': 'text',
                  'param': {'enable': 'color: rgb(62, 176, 68);'}}),
                ('wireless_role', {'locator': self.row_.nth(5).locator('//div[2]/div/span[2]'),
                                   'type': 'text', 'param': {'client': self.locale.client, 'ap': self.locale.ap}}),
                ('wireless_state', {'locator': self.row_.nth(5).locator('//div[2]/div[2]/span[2]'),
                                    'type': 'text',
                                    'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,
                                              'enable': self.locale.enable, 'disable': self.locale.disable}}),
                ('wireless_ssid', {'locator': self.row_.nth(5).locator('//div[2]/div[3]/span[2]'), 'type': 'text'}),
                ('wireless_ip', {'locator': self.row_.nth(5).locator('//div[2]/div[4]/span[2]'), 'type': 'text'}),
                ('cellular_image', {'locator': self.row_.nth(6).locator('//div/div/img[@alt="#"]').get_attribute('src'),
                                    'type': 'text', 'param': {'enable': 'PC9zdmc', '==': ' in ', '!=': ' not in '}}),
                ('cellular_status', {'locator': self.row_.nth(6).locator('//div[2]/div/span[2]'),
                                     'type': 'text',
                                     'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,}}),
                ('cellular_register_status', {'locator': self.row_.nth(6).locator('//div[2]/div[3]/span[2]'),
                                              'type': 'text',
                                              'param': {'not_register': self.locale.not_register,
                                                        'registering': self.locale.registering,
                                                        'registered': self.locale.registered}}),
                ('cellular_connection_time', {'locator': self.row_.nth(6).locator('//div[2]/div[4]/span[2]'),
                                              'type': 'text', 'param': {'day': self.locale.day}}),
                ('cellular_ip', {'locator': self.row_.nth(6).locator('//div[2]/div[5]/span[2]'), 'type': 'text'}),
                ('cellular_netmask', {'locator': self.row_.nth(6).locator('//div[2]/div[6]/span[2]'), 'type': 'text'}),
                ('cellular_dns', {'locator': self.row_.nth(6).locator('//div[2]/div[7]/span[2]'), 'type': 'text'}),
                ('name', {'locator': self.row_.nth(7).locator('//div/div[2]/div/div/span'), 'type': 'text'}),
                ('model', {'locator': self.row_.nth(7).locator('//div[2]/div[2]/p'), 'type': 'text'}),
                ('serial_number', {'locator': self.row_.nth(7).locator('//div[3]/div[2]/p'), 'type': 'text'}),
                ('mac_address', {'locator': self.row_.nth(7).locator('//div[4]/div[2]/p'), 'type': 'text'}),
                ('firmware_version', {'locator': self.row_.nth(7).locator('//div[5]/div[2]/p'), 'type': 'text'}),
                ('bootloader_version', {'locator': self.row_.nth(7).locator('//div[6]/div[2]/p'), 'type': 'text'}),
                ('device_time', {'locator': self.row_.nth(7).locator('//div[7]/div[2]/p'), 'type': 'text'}),
                ('host_time', {'locator': self.row_.nth(7).locator('//div[8]/div[2]/p'), 'type': 'text'}),
                ('system_up_time', {'locator': self.row_.nth(7).locator('//div[9]/div[2]/p'), 'type': 'text',
                                    'param': {'day': self.locale.day}}),
                ('python_edge_computing_status',
                 {'locator': self.row_.nth(8).locator('//div[2]/div/div/div/div[2]/p'), 'type': 'text',
                  'param': {'enable': self.locale.enable, 'disable': self.locale.disable}}),
                ('python_sdk_version',
                 {'locator': self.row_.nth(8).locator('//div[2]/div/div/div[2]/div[2]/p'), 'type': 'text'}),
                ('cpu_usage_rate',
                 {'locator': self.page.locator('.ant-progress-text').inner_text().replace('%', ''), 'type': 'text'}),
                ]
