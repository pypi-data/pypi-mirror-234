# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 15:58:05
# @Author  : Pane Li
# @File    : overview.py
"""
overview

"""
import allure
from inhandtest.tools import loop_inspector
from playwright.sync_api import expect
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Overview(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言概览状态')
    @loop_inspector('overview status')
    def assert_status(self, **kwargs):
        """
        assert overview status
        :param kwargs:  wan_image: 检查外网图标状态，ex: wan_image='"${value}" =="enable"'
                                                 or wan_status='"${value}" !="enable"'
                        wan_ip: 检查wan ip，ex: wan_ip='"${value}" =="0.0.0.0"'
                        wan_gateway: 检查wan gateway，ex: wan_gateway='"${value}" =="10.5.24.254"'
                        wan_dns: 检查wan dns，ex: wan_dns='"${value}" =="0.0.0.0"'
                        ge_01_image: 检查ge_01图标状态，ex: ge_01_image='"enable" == "${value}"' or ge_01_image='"enable" != "${value}"'
                        ge_01_ip: 检查ge_01 ip，ex: ge_01_ip='"${value}" =="0.0.0.0"'
                        ge_01_netmask: 检查ge_01 netmask，ex: ge_01_netmask='"${value}" =="0.0.0.0"'
                        ge_02_image: 检查ge_02图标状态，ex: ge_02_image='"enable" == "${value}"' or ge_02_image='"enable" != "${value}"'
                        ge_02_ip: 检查ge_02 ip，ex: ge_02_ip='"${value}" =="0.0.0.0"'
                        ge_02_netmask: 检查ge_02 netmask，ex: ge_02_netmask='"${value}" =="0.0.0.0"'
                        wireless_image: 检查wireless图标状态，ex: wireless_image='"enable" == "${value}"' or wireless_image='"enable" != "${value}"'
                        wireless_role: 检查wireless role，ex: wireless_role='"${value}" =="ap"' or wireless_role='"${value}"=="client"'
                        wireless_state: 检查wireless state，ex: wireless_state='"${value}" =="connected"' or wireless_state='"${value}"=="disconnected"'
                                                            or wireless_state='"${value}"=="enable"' or wireless_state='"${value}"=="disable"'
                        wireless_ssid: 检查wireless ssid，ex: wireless_ssid='"${value}" =="inhand-2.4G"' or wireless_ssid='"${value}"=="inhand-5G"'
                        wireless_ip: 检查wireless ip，ex: wireless_ip='"${value}" =="0.0.0.0"'
                        cellular_image: 检查cellular图标状态，ex: cellular_image='"enable" == "${value}"' or cellular_image='"enable" != "${value}"'
                        cellular_status: 检查cellular status，ex: cellular_status='"${value}" =="connect"' or cellular_status='"${value}"=="disconnect"'
                        cellular_register_status: 检查cellular register status，ex: cellular_register_status='"${value}" =="not_register"'
                                                    or cellular_register_status='"${value}"=="registering"' or cellular_register_status='"${value}"=="registered"'
                        cellular_connection_time: 检查cellular connection time，ex: cellular_connection_time='"${value}".startswith("0 day 00:")'
                        cellular_ip: 检查cellular ip，ex: cellular_ip='"${value}" =="0.0.0.0"'
                        cellular_netmask: 检查cellular netmask，ex: cellular_netmask='"${value}" =="0.0.0.0"'
                        cellular_dns：检查cellular dns，ex: cellular_dns='"${value}" =="0.0.0.0"'
                        name: 检查name，ex: name='"${value}" =="inhand"'
                        model: 检查model，ex: model='"${value}" =="IG902"'
                        serial_number: 检查serial number，ex: serial_number='"${value}" =="GT9022036001652"'
                        mac_address: 检查mac address，ex: mac_address='"${value}" =="00:0C:29:22:03:60"' 多个之间需要使用\n分隔
                        firmware_version: 检查firmware version，ex: firmware_version='"${value}" =="V2.0.6"'
                        bootloader_version: 检查bootloader version，ex: bootloader_version='"${value}" =="V2.0.6"'
                        device_time: 检查device time，ex: device_time='"${value}".startswith("2021-05-15 16")'
                        host_time: 检查host time，ex: host_time='"${value}".startswith("2021-05-15 16")'
                        system_up_time: 检查system up time，ex: system_up_time='"${value}".startswith("0 day 00:")'
                        python_edge_computing_status: 检查python edge computing status，ex: python_edge_computing_status='"${value}" =="enable"'
                                                      or python_edge_computing_status='"${value}"=="disable"'
                        python_sdk_version: 检查python sdk version，ex: python_sdk_version='"${value}" =="1.0.0"'
                        cpu_usage_rate: 检查cpu usage rate，ex: cpu_usage_rate='${value} in range(20, 80)'
                        timeout: 超时时间
                        interval: 检查间隔
        :return:
        """
        self.access_menu('overview')
        return self.eval_locator_attribute(kwargs, self.overview_locators.overview_locators)

    @allure.step('获取概览信息')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """
        get overview status
        :param keys: 同assert_overview_status keys
        :return: 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        self.access_menu('overview')
        return self.get_text(keys, self.overview_locators.overview_locators)

    @allure.step("检测流量图表是否出现")
    def traffic_report_visible(self, visible=True, timeout=30):
        """ 检测开启流量监控后概览页面的状态，关闭流量监控后概览页面的状态

        :param visible: True|False 检测流量图表是否出现
        :param timeout: 超时时间 单位秒
        :return:
        """
        # 检测是否出现流量图表
        for menu in ('overview.flow_usage_monitoring(day)', 'overview.flow_usage_monitoring(month)'):
            self.access_menu(menu)
            if visible:
                expect(self.page.locator('.ant-empty-description')).to_have_count(0, timeout=timeout * 1000)
            else:
                expect(self.page.locator('.ant-empty-description')).to_have_count(1, timeout=timeout * 1000)
