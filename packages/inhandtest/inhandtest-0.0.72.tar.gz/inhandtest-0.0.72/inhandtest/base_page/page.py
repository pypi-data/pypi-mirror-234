# -*- coding: utf-8 -*-
# @Time    : 2023/9/21 15:14:57
# @Author  : Pane Li
# @File    : page.py
"""
page

"""
import os
from typing import List

import allure
import logging
import re
from collections import Counter
from playwright.sync_api import Page, Locator, expect, TimeoutError, Error
from inhandtest.base_page.table_tr import Table, IgTable


class Page_:
    __true_option = ['true', 'yes', '是', True, 1]

    def __init__(self, page: Page, host, model, locale):
        self.page = page
        self.host = host
        self.model = model
        self.locale = locale

    @allure.step('页面抓取接口返回结果')
    def wait_for_response(self, url: str, timeout=30) -> dict:
        """

        :param url:  pattern 匹配的正则表达式,
        :param timeout: 默认30秒
        :return: 返回结果
        """
        with self.page.expect_response(lambda response: re.search(url, response.url) and response.status == 200,
                                       timeout=timeout * 1000) as response_info:
            logging.debug("Device %s fetch url %s " % (self.host, response_info.value.url))
        logging.info("Device %s the api response is  %s " % (self.host, response_info.value.json()))
        return response_info.value.json()

    @allure.step('填写输入框')
    def fill(self, locator: Locator, value: str or int, log_desc=None, force=False) -> None:
        """ 基础输入

        :param locator:  元素定位
        :param value: 输入的值
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param force: 强制写入
        :return:
        """
        if value is not None:
            locator.clear()
            locator.fill(str(value), force=force)
            locator.blur()  # 鼠标移出输入框
            if log_desc:
                logging.info(f'Device {self.host} fill {log_desc} {value}')

    @allure.step('点击元素')
    def click(self, locator: Locator or list or tuple, log_desc=None, dialog_message: str = None,
              tip_messages: str or list = None, text_messages: str or list = None, wait_for_time: int = None,
              tip_messages_timeout=30) -> None:
        """ 封装公共的点击操作 支持多个元素点击, 对点击最后一次的属性做校验

        :param locator:  元素定位
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param dialog_message: str  点击按钮后有dialog弹出，并且期望对信息做验证， 支持模糊匹配, 点击最后一个元素
        :param tip_messages: str or list 点击后等待该tip出现 再等待tip消失，如果有多个，使用列表传入 内容是正则表达式
                            tip_messages 是支持模糊匹配
                            该项校验 页面元素必须停留时间1秒及更多时间，否则不容易检测到导致报错， 点击最后一个元素
        :param text_messages: str or list 点击后等待该文本内容出现，如果有多个，使用列表传入， 内容是正则表达式
        :param wait_for_time: ms  当做完所有操作后是否需要等待时间， 点击最后一个元素
        :param tip_messages_timeout: 默认30秒， 单位秒
        :return:
        """

        def last_click(last_locator: Locator):
            if not last_locator.is_disabled():
                if dialog_message:
                    self.dialog_massage(last_locator.click, dialog_message)
                else:
                    last_locator.click()
                if log_desc:
                    logging.info(f'Device {self.host} click {log_desc}')
                self.tip_messages(tip_messages, tip_messages_timeout)
                self.text_messages(text_messages, tip_messages_timeout)
                if wait_for_time:
                    self.page.wait_for_timeout(wait_for_time)
            else:
                logging.warning(f'Device {self.host} click {log_desc} is disabled')

        if isinstance(locator, (tuple, list)):
            for locator_ in locator[:-1]:
                locator_.click()
            last_click(locator[-1])
        elif isinstance(locator, Locator):
            last_click(locator)
        else:
            logging.exception(f'locator type error {locator}')
            raise TypeError(f'locator type error {locator}')

    @allure.step('检查框')
    def check(self, locator: Locator, action=True, log_desc=None,
              tip_messages: str or re.Pattern or list = None) -> None:
        """ 封装公共的单选操作
        :param locator:  元素定位
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param action: 'check'|'uncheck'| None | '是' | 'Yes'
        :param tip_messages: str or re.Pattern or list 点击后等待该tip出现 再等待tip消失，如果有多个，使用列表传入
                            该项校验 页面元素必须停留时间1秒及更多时间，否则不容易检测到导致报错
        :return:
        """
        try:
            if action is not None:
                if action in ['check', 'enable'] + self.__true_option:
                    locator.check()
                else:
                    locator.uncheck()
                if log_desc:
                    logging.info(f'Device {self.host} {log_desc} {action}')
                self.tip_messages(tip_messages)
        except Error:
            pass

    @allure.step('下拉单项选择')
    def select_option(self, locator: Locator, value: str or int, log_desc=None, transform: dict = None) -> None:
        """ 封装公共的下拉选择操作

        :param locator:  元素定位
        :param value: str or int, 下拉选择option的value属性值、或label
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param transform: dict, 用于转换value的值，如 {'enable': 'true', 'disable': 'false'} 主要是国际化转换
        :return:
        """

        def scroll_into_view_action(all_option_: Locator, option_: Locator, times=100):
            select = False
            option_end = None
            for find_time in range(0, times):
                if option_.count() == 1:
                    option_.click()
                    select = True
                    break
                elif option_.count() == 0:
                    if option_end != all_option_.last.inner_text():
                        option_end = all_option_.last.inner_text()
                        all_option_.last.scroll_into_view_if_needed()
                        logging.debug(f'scroll down the scroll bar {find_time + 1} tims')
                    else:
                        logging.debug(f'scroll down the bottom')
                        break
                else:
                    logging.exception(f'found more option elements')
                    raise Exception('found more option elements')
            if not select:
                for find_time in range(0, times):
                    if option_.count() == 1:
                        option_.click()
                        break
                    elif option_.count() == 0:
                        if option_end != all_option_.first.inner_text():
                            option_end = all_option_.first.inner_text()
                            all_option_.first.scroll_into_view_if_needed()
                            logging.debug(f'scroll up the scroll bar {find_time + 1}')
                        else:
                            logging.debug(f'scroll up the top')
                            break
                    else:
                        logging.exception(f'found more option elements')
                        raise Exception('found more option elements')
                else:
                    logging.exception(f'scroll bar too lang, more 100 times')
                    raise Exception('scroll bar too lang, more 100 times')

        if value is not None:
            value = str(transform[value]) if transform and value in transform.keys() else str(value)
            locator.wait_for(state='visible')
            if locator.get_attribute('aria-controls') or locator.locator('.ant-select-selection').get_attribute(
                    'aria-controls'):
                if locator.get_attribute("aria-controls"):  # ER805 设备的下拉选择
                    now_option = locator.locator('../..').locator('.ant-select-selection-item').inner_text()
                    option_p = self.page.locator(f'//div[@id="{locator.get_attribute("aria-controls")}"]').locator(
                        '..').locator('//div[@class="rc-virtual-list-holder-inner"]')
                    option = option_p.locator(f'//div[@title="{value}"]')
                    all_option = option_p.locator('.ant-select-item.ant-select-item-option')
                else:  # IG902 设备的下拉选择
                    now_option = locator.locator(
                        '//div/div/div[@class="ant-select-selection-selected-value"]').inner_text()
                    option_id = locator.locator(".ant-select-selection").get_attribute("aria-controls")
                    all_option = self.page.locator(f'//div[@id="{option_id}"]').locator('//ul[@role="listbox"]/li')
                    option = self.page.locator(f'//div[@id="{option_id}"]').locator(
                        f'//ul[@role="listbox"]/li').get_by_text(value, exact=True)
                if now_option != value:
                    locator.scroll_into_view_if_needed()
                    if not locator.is_editable():
                        locator.click(force=True)
                    else:
                        locator.click()
                    scroll_into_view_action(all_option, option)
            else:  # IR300 等设备的下拉选择
                locator.select_option(value)  # value 可以为label 或者value
                if locator.locator(f'//option[@value="{value}"]').count() == 1:
                    value = locator.locator(f'//option[@value="{value}"]').inner_text()
            if log_desc:
                logging.info(f"Device {self.host} select {log_desc} of {value}")

    @allure.step('下拉多项选择')
    def select_more(self, locator: Locator, value: list or str, log_desc=None, transform: dict = None) -> None:
        """下拉多项选择

        :param locator: 元素定位
        :param value: 一个或多个选项
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param transform: dict, 用于转换value的值，如 {'enable': 'true', 'disable': 'false'} 主要是国际化转换
        :return:
        """
        if value is not None:
            value = [value] if isinstance(value, str) else value
            value = [str(transform[value_]) if transform and value_ in transform.keys() else str(value_) for value_ in
                     value]
            if 'IG' in self.model:
                # 先找出现有已选择的选项， 如果不是就要取消，如果是就不管，
                already_choices = locator.locator('//li[@class="ant-select-selection__choice"]')
                for i in range(0, already_choices.count()):
                    if already_choices.nth(i).locator('//div[1]').inner_text() in value:
                        value.remove(already_choices.nth(i).locator('//div[1]').inner_text())
                    else:
                        self.click(already_choices.nth(i).locator('//span/i[1]'))
                if value:
                    for i_ in range(0, 3):
                        locator.click()
                        try:
                            option_id = locator.locator(".ant-select-selection").get_attribute("aria-controls")
                            for i in value:
                                option = self.page.locator(f'//div[@id="{option_id}"]').locator(
                                    f'//ul[@role="listbox"]/li').get_by_text(i, exact=True)
                                option.click()
                            break
                        except TimeoutError:
                            logging.error("多选框未选择正常")
                    else:
                        raise

            if log_desc:
                logging.info(f"Device {self.host} select {log_desc} more {value}")

    @allure.step('下拉多层級选择')
    def select_multi(self, locator: Locator, value: str, log_desc=None, transform: dict = None) -> None:
        """ 封装公共的下拉多級选择, 如 IG902 设备的APP下拉多級选择

        :param locator:  元素定位
        :param value: str 多個需使用点号隔开
        :param log_desc: 功能描述，用英文 如 Static Routing Destination
        :param transform: dict, 用于转换value的值，如 {'enable': 'true', 'disable': 'false'} 主要是国际化转换
        :return:
        """
        if value is not None:
            value = [str(transform[value_]) if transform and value_ in transform.keys() else str(value_) for value_ in
                     value.split('.')]
            if locator.locator('//span[@class="ant-cascader-picker-label"]').inner_text() != value[-1]:
                locator.click()
                for i in value:
                    self.page.locator(f'//li[text()="{i}"]').click()
                if log_desc:
                    logging.info(f"Device {self.host} select {log_desc} of {value}")

    @allure.step('切换按钮')
    def switch_button(self, locator: Locator, action: str = 'enable', log_desc=None) -> None:
        """控制通用开关按钮开关， 如拨号的开关

        :param locator:  开关按钮元素
        :param action: enable, disable, None, True, False 可以开启或关闭，但是并没有提交，只是点击了下
        :param log_desc:  开关功能描述
        :return: None
        """
        if action is not None:
            locator.wait_for(state='visible')
            if (isinstance(action, str) and action.lower() == 'enable') or (isinstance(action, bool) and action):
                if locator.get_attribute('aria-checked') == 'false' or not locator.get_attribute('aria-checked'):
                    locator.click(force=True)
                    if log_desc:
                        logging.info(f"Device {self.host} {log_desc} enabled")
            else:
                if locator.get_attribute('aria-checked') == 'false' or not locator.get_attribute('aria-checked'):
                    pass
                else:
                    locator.click(force=True)
                    if log_desc:
                        logging.info(f"Device {self.host} {log_desc} disabled")

    @allure.step('多点选框操作')
    def radio_select(self, locator: Locator, value: str, log_desc=None, transform: dict = None) -> None:
        """ 当前只有IG和ER的设备有单选框

        :param locator: 在所有label元素的上级div定位
        :param value: 选项的值，注意国际化
        :param log_desc: 选项的描述
        :param transform: dict, 用于转换value的值，如 {'enable': 'true', 'disable': 'false'} 主要是国际化转换
        :return:
        """
        if value:
            value = str(transform[value]) if transform and value in transform.keys() else str(value)
            locator.wait_for(state='visible')
            option = locator.locator(f'//label', has_text=re.compile(value))
            if option.count() == 1:
                if 'ant-radio-wrapper-checked' not in option.get_attribute('class'):
                    option.click(force=True)
                    if log_desc:
                        logging.info(f"Device {self.host} {log_desc} radio select {value}")
                else:
                    if log_desc:
                        logging.debug(f"Device {self.host} {log_desc} radio already select {value}")
            else:
                logging.exception(f'found {value} option {option.count()} elements')
                raise Exception(f'found {value} option {option.count()} elements')

    @allure.step('单点选框操作')
    def radio(self, locator: Locator, value, log_desc=None, transform: dict = None) -> None:
        """ 当前只有IG和ER的设备有单选框

        :param locator: 在所有label元素的上级div定位
        :param value: 选项的值，注意国际化
        :param log_desc: 选项的描述
        :param transform: dict, 用于转换value的值，如 {'enable': 'true', 'disable': 'false'} 主要是国际化转换
        :return:
        """
        if value is not None:
            value = transform[value] if transform and value in transform.keys() else value
            if value in ['check'] + self.__true_option:
                locator.check()
            else:
                locator.uncheck()
            if log_desc is not None:
                logging.debug(f"Device {self.host} {log_desc} radio {value}")

    @allure.step('伸缩按钮')
    def expand(self, left_text: str, action: str = 'expand') -> None:
        """ 伸缩按钮

        :param left_text: 伸缩按钮 左边的文本，需要注意国际化
        :param action: expand|close|None
        :return:
        """
        text_locator = self.page.get_by_text(left_text, exact=True)
        expand_option = ['expand', 'EXPAND'] + self.__true_option
        if action is not None:
            text_locator.wait_for(state='visible')
            if text_locator.count() > 1:
                logging.exception(f'found {left_text} {text_locator.count()} elements')
                raise
            else:
                if 'IG' in self.model:  # IG 产品
                    if 'right' in text_locator.locator('..').locator('//i').get_attribute('aria-label'):
                        if action in expand_option:
                            self.click(text_locator.locator('..'), f'expand {left_text}')
                    else:
                        if action not in expand_option:
                            self.click(text_locator.locator('..'), f'closed {left_text}')
                elif 'ER' in self.model:  # ER805
                    locator = self.page.locator(f'svg[data-icon="right"]:right-of(:text-is("{left_text}"))').first
                    if action in expand_option:
                        if not locator.get_attribute('style'):
                            self.click(locator, f'expand {left_text}')
                    else:
                        if locator.get_attribute('style') == 'transform: rotate(90deg);':
                            self.click(locator, f'closed {left_text}')
                else:
                    logging.exception(f'not support this expand')
                    raise Exception("not support this expand")

    @allure.step('上传文件')
    def upload_file(self, locator: Locator, file_path: str, dialog_massage: str = None,
                    tip_messages: str or re.Pattern or list = None) -> None:
        """

        :param locator:
        :param file_path:
        :param dialog_massage: str
        :param tip_messages: str or re.Pattern or list
        :return:
        """

        def upload():
            if file_path:
                if os.path.isfile(file_path) and os.path.exists(file_path):
                    with self.page.expect_file_chooser() as fc:
                        locator.click()
                    file_chooser = fc.value
                    file_chooser.set_files(file_path)
                    logging.info(f'Device {self.host} upload {file_path} success')
                else:
                    logging.error(f'{file_path} Does Not Exist.')

        if dialog_massage:
            self.dialog_massage(upload, dialog_massage)
        else:
            upload()
        self.tip_messages(tip_messages)

    @allure.step('下载文件')
    def download_file(self, locator: Locator, file_path: str, file_name: str = None) -> None:
        """默认为日志路径

        :param locator: 下载按钮元素
        :param file_path: 下载文件的路径, 不需要跟文件名，
        :param file_name: 如果文件名
        :return:
        """
        if file_path is not None:
            if os.path.isdir(file_path) and os.path.exists(file_path):
                if not locator.is_disabled():
                    with self.page.expect_download() as download_info:
                        locator.click()
                    download = download_info.value
                    file_name = download.suggested_filename if file_name is None else file_name
                    download.save_as(os.path.join(file_path, file_name))
                    logging.info(
                        f'Device {self.host} download {download.suggested_filename} to path {file_path} success')
                else:
                    logging.warning(f'Device {self.host} {locator} is disabled')
            else:
                logging.error(f'{file_path} Does Not Exist.')

    @allure.step('输入时间或日期')
    def fill_date(self, locator: Locator, date: str) -> None:
        """输入时间或日期

        :param locator:
        :param date: 日期，格式为 2020-01-01
        :return:
        """
        self.click(locator)
        if locator.get_attribute('class') == 'ant-calendar-picker':  # date
            locator_ = self.page.locator('.ant-calendar-input')
        else:
            locator_ = self.page.locator('.ant-time-picker-panel-input')
        locator_.fill(date)
        locator_.press('Enter')
        self.page.wait_for_timeout(500)

    @allure.step("校验dialog message")
    def dialog_massage(self, f, message: str = '') -> None:
        """对话框提示进行校验， 使用时需要在base_locator 里面定义dialog_massage 且返回字典数据

        :param f:  是一个操作函数，执行后会有dialog弹窗出现
        :param message: 校验的信息, 支持模糊匹配
        :return:
        """
        if message:
            message = self.locale.get(message) if self.locale.get(message) else message
            with self.page.expect_event('dialog') as dialog_info:
                f()
            assert message in dialog_info.value.message, f'{self.host} assert {message} dialog error'
            logging.info(f'Device {self.host} assert dialog {message} success')

    @allure.step("校验tip messages")
    def tip_messages(self, messages: str or re.Pattern or list = None, timeout=30) -> None:
        """ 某些提交操作会出现文本的提示，提示在过几秒钟后会消失，对于该类消息的验证使用该方法，
            使用时需要在base_locator tip_messages 且返回字典数据

        :param messages: str or re.Pattern  点击后等待该tip出现 再等待tip消失，
                            messages str 是支持模糊匹配 如果有多个，使用列表传入
                            re.compile(message)  支持正则   如果有多个，使用列表传入
                            re.compile(message, re.IGNORECASE) 支持正则忽略大小写  如果有多个，使用列表传入
                            该项校验 页面元素必须停留时间1秒及更多时间，否则不容易检测到导致报错
        :param timeout: 校验超时时间
        :return:
        """
        if messages:
            if isinstance(messages, str):
                tip_messages = [self.locale.get(messages)] if self.locale.get(messages) else [messages]
            elif isinstance(messages, re.Pattern):
                tip_messages = [messages]  # 正则表达式 时需要自己做国际化转换
            elif isinstance(messages, list):
                tip_messages = [self.locale.get(message) if self.locale.get(message) else message for message in
                                messages]
            else:
                raise Exception("messages type error")
            for message in tip_messages:
                expect(self.page.get_by_text(message)).to_be_visible(timeout=timeout * 1000)
                expect(self.page.get_by_text(message)).to_be_hidden(timeout=timeout * 1000)
                logging.info(f'{self.host} assert tip {message} visible success')

    @allure.step("校验text messages")
    def text_messages(self, messages: str or re.Pattern or list = None, timeout=10) -> None:
        """ 对文本内容做验证，如在输入框输入错误内容时出现的文本，该类文本会一直存在
        :param messages: str or re.Pattern
                            messages str 是支持模糊匹配 如果有多个，使用列表传入
                            re.compile(message)  支持正则   如果有多个，使用列表传入
                            re.compile(message, re.IGNORECASE) 支持正则忽略大小写  如果有多个，使用列表传入
        :param timeout: 校验超时时间
        :return:
        """
        if messages:
            if isinstance(messages, str):
                messages = [self.locale.get(messages)] if self.locale.get(messages) else [messages]
            elif isinstance(messages, re.Pattern):
                messages = [messages]  # 正则表达式 时需要自己做国际化转换
            elif isinstance(messages, list):
                messages = [self.locale.get(message) if self.locale.get(message) else message for message in messages]
            else:
                raise Exception("messages type error")
            text_messages = Counter(messages)  # 处理多个相同的文本
            for message, count in text_messages.items():
                for i_ in range(0, count):
                    expect(self.page.get_by_text(message).nth(i_)).to_be_visible(timeout=timeout * 1000)
                    logging.info(f'{self.host} assert text the {i_}th {message}  visible success')

    @allure.step("校验元素Title")
    def title_messages(self, messages: str or re.Pattern or list = None, timeout=10) -> None:
        """ 对元素的属性title做内容验证，
        :param messages: str or re.Pattern
                            messages str 是支持模糊匹配 如果有多个，使用列表传入
                            re.compile(message)  支持正则   如果有多个，使用列表传入
                            re.compile(message, re.IGNORECASE) 支持正则忽略大小写  如果有多个，使用列表传入
        :param timeout: 校验超时时间
        :return:
        """
        if messages:
            if isinstance(messages, str):
                messages = [self.locale.get(messages)] if self.locale.get(messages) else [messages]
            elif isinstance(messages, re.Pattern):
                messages = [messages]  # 正则表达式 时需要自己做国际化转换
            elif isinstance(messages, list):
                messages = [self.locale.get(message) if self.locale.get(message) else message for message in messages]
            else:
                raise Exception("messages type error")
            text_messages = Counter(messages)
            for message, count in text_messages.items():
                for i_ in range(0, count):
                    expect(self.page.get_by_title(message).nth(i_)).to_be_visible(timeout=timeout * 1000)
                    logging.info(f'{self.host} assert title the {i_}th {message} visible success')

    @allure.step('设置页面翻页')
    def page_refresh(self, locator: Locator, refresh_time: str or int) -> None:
        """
        :param locator: 元素定位
        :param refresh_time: str or int
                        '0'|'3'|'4'|'5'|'10'|'15'|'30'|'60'|'120'|'180'|'240'|'300'|'600'|'900'|'1200'|'1800'
        :return:
        """
        # 待完善
        if isinstance(refresh_time, int):
            refresh_time = str(refresh_time)
        if self.model in ('VG710', 'IR302'):
            if locator.evaluate("el => el.value") == str(
                    refresh_time) and locator.is_disabled():
                pass
            else:
                if locator.is_disabled():
                    self.click(locator.locator('..').locator('#refresh-button'), 'refresh button')
                    self.page.wait_for_timeout(500)
                self.select_option(locator, refresh_time, 'refresh time select')
                self.click(locator.locator('..').locator('#refresh-button'), 'refresh button ok')

    def turn_page(self, father_locator: Locator = None, page_number=1):
        """分页， 指定点到第几页  只有IG 产品拥有该方法

        :param father_locator: 当同一页面存在多个分页时，需要传入父元素定位组合成链式定位，确认唯一
        :param page_number: 第几页
        :return: 找不到页数时返回False
        """
        if self.model in ('IG902', 'IG502'):
            locator = self.page.locator(f'.ant-pagination-item-{page_number}')
            if father_locator:
                locator = father_locator.locator(f'.ant-pagination-item-{page_number}')
            if locator.is_visible():
                self.click(locator, f'turn page {page_number}', wait_for_time=500)
                return True
            else:
                return False
        else:
            raise Exception(f'{self.model} not support turn page')

    def monaco(self, locator: Locator, value: str, log_desc=None):
        """慕尼黑编辑器输入

        :param locator:
        :param value: 换行需要使用\n
        :param log_desc:
        :return:
        """
        self.click(locator, )
        self.page.keyboard.press('Control+A')
        self.page.keyboard.press('Delete')
        self.page.keyboard.type(value)
        logging.info(f'{log_desc} monaco-editor：{value}')

    def value_mapping(self, locator, value: tuple or list):
        """ 目前只有IG產品有

        :param locator:
        :param value:
        :return:
        """
        for i in range(0, locator.get('table').locator('//tbody/tr').count()):
            self.click(locator.get('table').locator('//tbody/tr').nth(0).locator('//td[3]/a'))
            self.click(locator.get('ok'))
            self.page.wait_for_timeout(1000)
        for i in range(0, len(value)):
            self.click(locator.get('add'))
            self.fill(locator.get('table').locator('//tbody/tr').nth(i).locator('//td[1]').locator('//input'),
                      value[i][0])
            self.fill(locator.get('table').locator('//tbody/tr').nth(i).locator('//td[2]').locator('//input'),
                      value[i][1])
            self.page.wait_for_timeout(500)

    @allure.step("操作表格")
    def table_tr(self, locators: dict, value: list, agg_function, log_desc=None) -> List[int or None] or None:
        """

        :param locators: {"locator": $locator2, "param": {$key2: $value2}, "columns": list, 'unique_columns': list}
        :param value: [($action,{**kwarg})] ex: [('delete_all', )],  [('edit', $old, $new)]多个操作时使用列表 [('add',{}), ('add',{})]
        :param agg_function: 聚合多种操作，表格本身就是多种操作
        :param log_desc: 日志描述
        :return:
        """
        if self.model in ('IG902', 'IG502'):
            tr = IgTable(locators.get('columns'), locators.get('locator'), locators.get('param'), log_desc,
                         locators.get('action_confirm'), locators.get('pop_up_locator'))
            exist_tr = []
            if value:
                for value_ in value:
                    if value_[0] in ('add', 'install'):
                        tr.add(agg_function, **value_[1])
                        if value_[0] == 'install':  # app 的安装，安装完成页面要重新加载，需要固定等点时间
                            self.page.wait_for_timeout(5000)
                    elif value_[0] == 'delete_all':
                        tr.delete_all()
                    elif value_[0] in ('delete', 'uninstall'):
                        tr.delete(value_[1])
                    elif value_[0] == 'exist':
                        exist_tr.append(tr.exist(value_[1], self.locale))
                    elif value_[0] == 'edit':
                        tr.edit(agg_function, value_[1], **value_[2])
                    elif value_[0] == 'connect':
                        tr.connect(value_[1])
                    elif value_[0] == 'associate_delete':
                        tr.associate_delete(value_[1])
                    elif value_[0] in ('download_log', 'export_config', 'export_historical_data'):
                        if isinstance(value_[2], str):
                            file_path = value_[2]
                            file_name = None
                        elif isinstance(value_[2], dict):
                            file_path = value_[2].get('file_path')
                            file_name = value_[2].get('file_name')
                        else:
                            logging.exception('download file_path type error')
                            raise TypeError('download file_path type error')
                        tr.download(self.download_file, value_[1], file_path, file_name)
                    elif value_[0] in ('upload', 'import_config'):
                        tr.upload(self.upload_file, value_[1], value_[2])
                    elif value_[0] == 'start':
                        tr.start(value_[1])
                    elif value_[0] == 'stop':
                        tr.stop(value_[1])
                    elif value_[0] == 'restart':
                        tr.restart(value_[1])
                    elif value_[0] in ('check', 'enable'):
                        tr.check(self.check, value_[1], value_[2])
                    elif value_[0] == 'clear_log':
                        tr.clear_log(value_[1])
                    elif value_[0] == 'clear_historical_data':
                        tr.clear_historical_data(value_[1])
                return exist_tr
        else:
            tr = Table(locators.get('columns'), locators.get('locator'),
                       locators.get('unique_columns'), locators.get('param'), log_desc)
            exist_tr = []
            if value:
                for value_ in value:
                    if value_[0] == 'add':
                        tr.add(**value[1])
                    elif value_[0] == 'delete_all':
                        tr.delete_all()
                    elif value_[0] == 'delete':
                        tr.delete(**value[1])
                    elif value_[0] == 'exist':
                        exist_tr.append(tr.exist(**value[1]))
                    elif value_[0] == 'edit':
                        tr.edit(value[1], value[2])
                return exist_tr
