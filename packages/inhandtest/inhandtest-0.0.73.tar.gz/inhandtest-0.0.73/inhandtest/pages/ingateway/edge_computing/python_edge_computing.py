# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:34:20
# @Author  : Pane Li
# @File    : python_edge_computing.py
"""
python_edge_computing

"""
import logging
import random
import allure
from inhandtest.tools import loop_inspector
from inhandtest.base_page.table_tr import IgTable
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators
from decimal import Decimal, ROUND_HALF_UP


class PythonEdgeComputing(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Python Engine状态')
    @loop_inspector('python_engine_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               python_engine: enable,disable ex: python_engine='"${value}"=="enable"'
               sdk_version: 1.4.3 ex: sdk_version='1.4.3'
               python_version: Python3 ex: python_version='Python3'
               username: adm ex: username='adm'
               used_user_storage: 176MB/6GB3% ex: used_user_storage='"${value}".startswith("176MB")'
               app: device_supervisor.*RUNNING   ex: app='device_supervisor.*RUNNING'  检测device_supervisor是否在运行
        """
        self.access_menu('edge computing.python edge computing')
        if kwargs.get('app'):
            if not IgTable([], self.edge_locators.app_status_table).exist(kwargs.get('app'), {}):
                return False
        return self.eval_locator_attribute(kwargs, self.edge_locators.python_engine_status_locator)

    @allure.step('获取Python Engine状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               python_engine, sdk_version, python_version, username, used_user_storage, password
        """
        self.access_menu('edge computing.python edge computing')
        return self.get_text(keys, self.edge_locators.python_engine_status_locator)

    @allure.step('配置Python Edge Computing')
    def config(self, **kwargs):
        """
        :param kwargs:
               python_engine: enable,disable ex: python_engine='enable'
               sdk_upgrade: file_path ex: sdk_upgrade='C:\\Users\\Administrator\\Downloads\\inhand-1.4.3.tar.gz'
               sdk_upgrade_tip: dict sdk_upgrade_tip={'tip_messages': 'install_success', 'timeout': 100}
               password: 123456 ex: password='123456'
               start_all_app: True, False ex: app_all_start=True
               stop_all_app: True, False ex: app_all_stop=True
               restart_all_app: True, False ex: restart_all_app=True
               app: [($action, **kwarg)] ex:
                    [('enable', 'device_supervisor', True)],   # 启用 device_supervisor
                    [('enable', 'device_supervisor', False)]   # 禁用 device_supervisor
                    [('install', {'app_package': 'C:\\Users\\Administrator\\Downloads\\device_supervisor-1.0.0.tar.gz'})] # 添加 device_supervisor
                    [('import_config', 'device_supervisor', 'C:\\Users\\Administrator\\Downloads\\device_supervisor-1.0.0.conf')] # 导入device_supervisor配置
                    [('export_config', 'device_supervisor', {'file_path': 'C:\\Users\\Administrator\\Downloads', 'file_name': "device_supervisor-1.0.0.conf"})] # 导出device_supervisor配置， 文件名可以不传
                    [('uninstall', 'device_supervisor')]   # 卸载 device_supervisor
                    [('edit', 'device_supervisor', {'log_file_size': 1, 'number_of_log': 2, 'start_args': ''})]   # 编辑 device_supervisor
                    [('download_log', 'device_supervisor', {'file_path': 'C:\\Users\\Administrator\\Downloads', 'file_name': "device_supervisor-1.0.0.log"})] # 导出device_supervisor日志， 文件名可以不传
                    [('clear_log', 'device_supervisor')]   # 清除 device_supervisor 日志
                    [('start', 'device_supervisor')]  # 启动 device_supervisor
                    [('stop', 'device_supervisor')]   # 停止 device_supervisor
                    [('restart', 'device_supervisor')]   # 重启 device_supervisor
                    edit parameters:
                        log_file_size: int
                        number_of_log: int
                        start_args: str  启动参数
                        text_messages: str or list
                        cancel: True, False
               submit: True,False ex: submit=True  or submit={'tip_messages': 'APP start successful'}
               text_messages: str ex: text_messages='ip_address_conflict'
               tip_messages: ‘APP start successful’
               reset: True, False ex: reset=True
        """
        self.access_menu('edge computing.python edge computing')
        self.page.wait_for_load_state(state='networkidle')
        self.page.wait_for_timeout(1 * 1000)
        if kwargs.get('sdk_upgrade'):
            kwargs.update({'sdk_upgrade_confirm': True})
            if kwargs.get('sdk_upgrade_tip') is None:
                kwargs.update({'sdk_upgrade_tip': {'tip_messages': 'install_success', 'timeout': 100}})
        if kwargs.get('password'):
            kwargs.update({'edit_password': True, 'submit_password': True})
        if kwargs.get('app'):
            app_list_action = []
            app_status_action = []
            for action in kwargs.pop('app'):
                if action[0] in ('enable', 'install', 'import_config', 'export_config', 'uninstall', 'edit'):
                    app_list_action.append(action)
                else:
                    app_status_action.append(action)
            kwargs.update({'app_list': app_list_action, 'app_status': app_status_action})
        self.agg_in(self.edge_locators.python_edge_computing_locator, kwargs)


class DockerManager(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Docker Manager状态')
    @loop_inspector('docker_manager_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               docker_manager: enable,disable ex: docker_manager='"${value}"=="enable"'
               docker_version: 1.4.3 ex: docker_version='1.4.3'
               portainer_manager: enable,disable ex: portainer_manager='"${value}"=="enable"'
               username: adm ex: username='adm'
               password: 123456 ex: password='123456'
               port:  9000 ex: port='9000'
        """
        self.access_menu('edge computing.docker manager')
        return self.eval_locator_attribute(kwargs, self.edge_locators.docker_manager_status_locator)

    @allure.step('获取Docker Manager状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               docker_manager, docker_version, portainer_manager, username, password, port
        """
        self.access_menu('edge computing.docker manager')
        self.page.wait_for_timeout(1000)
        return self.get_text(keys, self.edge_locators.docker_manager_status_locator)

    @allure.step('配置Docker Manager')
    def config(self, **kwargs):
        """
        :param kwargs:
               docker_manager: enable,disable ex: docker_manager='enable'
               docker_upgrade: file_path ex: docker_upgrade='C:\\Users\\Administrator\\Downloads\\inhand-1.4.3.tar.gz'
               docker_upgrade_tip: 'install_failure', 'install_success', ex: docker_upgrade_tip='install_success'
               submit_docker_manager: True, False ex: submit_docker_manager=True or submit_docker_manager={'tip_messages': 'submit_success'}
               portainer_manager: enable,disable ex: portainer_manager='enable'
               password: 123456 ex: password='123456'
               port: 9000 ex: port='9000'
               submit_portainer_manager: True, False ex: submit_portainer_manager=True or submit_portainer_manager={'tip_messages': 'submit_success'}
               text_messages: str ex: text_messages='ip_address_conflict'
               tip_messages: ‘submit_success’
               reset: True, False ex: reset=True
        """
        self.access_menu('edge computing.docker manager')
        self.page.wait_for_load_state(state='networkidle')
        self.page.wait_for_timeout(1 * 1000)
        if kwargs.get('docker_upgrade'):
            kwargs.update({'docker_upgrade_confirm': True})
            if kwargs.get('docker_upgrade_tip') is None:
                kwargs.update({'docker_upgrade_tip': {'tip_messages': 'install_success', 'timeout': 100}})
        self.agg_in(self.edge_locators.docker_manager_locator, kwargs)


class MeasureMonitor(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    def __value_mapping(self, locator, value: tuple or list):
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

    def __turn_page(self, name: str, type_='controller'):
        """根据控制器/测点名称翻页

        :param name: 控制器/测点名称
        :param type_: 'controller' | 'measure' , 默认为 'controller'
        :return:
        """
        page_number = 1
        if type_ == 'controller':
            locator = list(filter(lambda x: x[0] == 'select', self.edge_locators.controller_card(name)))[0][1].get(
                'locator')
        else:
            locator = list(filter(lambda x: x[0] == 'name', self.edge_locators.measure_table(name)))[0][1].get(
                'locator')
        while True:
            if locator.is_visible():
                break
            else:
                if self.turn_page(self.edge_locators.page_father.get(type_), page_number):
                    page_number = page_number + 1
                else:  # 找不到就退出
                    raise AssertionError(f'{name} is not exist')

    def __controller(self, action: list = None):
        """

        :param action: [(action_type, value, ),]
        :return:
        """
        for ac in action:
            if ac[0] in ('add', 'apply_template'):
                self.agg_in(self.edge_locators.controller_operation, {ac[0]: True})
                self.agg_in(self.edge_locators.add_controller_all, ac[1])
            elif ac[0] == 'delete_bulk':
                all_controller = [ac[1]] if isinstance(ac[1], str) else ac[1]
                self.__controller([('check', x, True) for x in all_controller])
                self.agg_in(self.edge_locators.controller_operation, {'delete_bulk': True, 'delete_bulk_confirm': True})
            else:
                self.__turn_page(ac[1])
                if ac[0] == 'edit':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'expand': True, 'edit': True})
                    self.agg_in(self.edge_locators.add_controller_all, ac[2])
                elif ac[0] == 'check':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'check': ac[2]})
                elif ac[0] == 'select':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'select': True})
                elif ac[0] == 'set_as_template':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'expand': True, 'set_as_template': True})
                    self.agg_in(self.edge_locators.set_as_template, ac[2])
                elif ac[0] == 'delete':
                    self.agg_in(self.edge_locators.controller_card(ac[1]),
                                {'expand': True, 'delete': True, 'delete_confirm': True})
                elif ac[0] == 'enable':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'expand': True, 'enable': True})
                elif ac[0] == 'disable':
                    self.agg_in(self.edge_locators.controller_card(ac[1]), {'expand': True, 'disable': True})
                elif ac[0] == 'realtime_communication_message':
                    pass

    def __measure(self, action: list = None):
        """

        :param action: [(action_type, value, ),]
        :return:
        """
        for ac in action:
            if ac[0] == 'add':
                self.agg_in(self.edge_locators.measure_operation, {ac[0]: True})
                self.agg_in(self.edge_locators.add_measure_all, ac[1])
            elif ac[0] == 'edit':
                self.__turn_page(ac[1], 'measure')
                self.agg_in(self.edge_locators.measure_table(ac[1]), {ac[0]: True})
                self.agg_in(self.edge_locators.add_measure_all, ac[2])
            elif ac[0] == 'search':
                self.agg_in(self.edge_locators.measure_operation, {"search_name": ac[1], 'search': True})
            elif ac[0] in ('import', 'export'):
                self.agg_in(self.edge_locators.measure_operation, {ac[0]: ac[1]})
            elif ac[0] == 'check':
                self.agg_in(self.edge_locators.measure_table(ac[1]), {'check': ac[2]})
            elif ac[0] == 'check_all':
                self.agg_in(self.edge_locators.measure_operation, {ac[0]: True})
            elif ac[0] == 'delete_bulk':
                self.agg_in(self.edge_locators.measure_operation, {'check_all': False})  # 先取消选择所有的
                all_measure = [ac[1]] if isinstance(ac[1], str) else ac[1]
                self.__measure([('check', x, True) for x in all_measure])
                self.agg_in(self.edge_locators.measure_operation, {'delete_bulk': True, 'delete_bulk_confirm': True})
            elif ac[0] == 'delete_all':
                self.__measure([('check_all',)])
                self.agg_in(self.edge_locators.measure_operation, {'delete_bulk': True, 'delete_bulk_confirm': True})
            elif ac[0] == 'delete':
                self.agg_in(self.edge_locators.measure_table(ac[1]), {'delete': True, 'delete_confirm': True})
            elif ac[0] == 'value':
                if list(filter(lambda x: x[0] == 'datatype', self.edge_locators.measure_card_status(ac[1])))[0][1].get(
                        'locator').inner_text() == 'BIT':  # BIT 类型时是选择框
                    if isinstance(ac[2], str):
                        value = {'value_edit': True, 'value_select': ac[2], 'submit': {"wait_for_time": 2 * 1000}}
                    else:
                        value = {'value_edit': True}
                        ac[2]['value_select'] = ac[2].pop('value')
                        value.update(ac[2])
                else:
                    if isinstance(ac[2], str):
                        value = {'value_edit': True, 'value': ac[2], 'submit': {"wait_for_time": 2 * 1000}}
                    else:
                        value = {'value_edit': True}
                        value.update(ac[2])
                self.agg_in(self.edge_locators.measure_table(ac[1]), value)
            elif ac[0] == 'add_to_group':
                if ac[1] == 'all':
                    self.__measure([('check_all',)])
                else:
                    self.agg_in(self.edge_locators.measure_operation, {'check_all': False})  # 先取消选择所有的
                    all_measure = [ac[1]] if isinstance(ac[1], str) else ac[1]
                    self.__measure([('check', x, True) for x in all_measure])
                self.agg_in(self.edge_locators.measure_operation, {"add_to_group": True})
                self.agg_in(self.edge_locators.measure_add_to_group(ac[2]),
                            {'group_name': True, "submit": {"wait_for_time": 3 * 1000}})
            else:
                pass

    @allure.step('配置测点监控')
    def config(self, **kwargs):
        """

        :param kwargs:
               controller: [(action_type, value, ),]
                           [('add', kwargs)]
                            kwargs:
                               name: 名称
                               protocol: 'modbus.modbus tcp' | 'modbus.modbus rtu'| 'OPC.OPC-UA'|'Siemens Plc.ISO-on-TCP'
                               servers_url: 服务器地址   OPC-UA
                               ip_address: ip地址
                               port: 端口号
                               mode: 通讯方式 'Rack/Slot' | 'TSAP'    ISO-on-TCP
                               rack: 机架号   ISO-on-TCP
                               slot: 插槽号      ISO-on-TCP
                               client_tsap:   ISO-on-TCP
                               server_tsap:  ISO-on-TCP
                               slave: 从站地址
                               endpoint: 通讯方式 'RS485' | 'RS232'
                               polling_interval: 轮询周期 1~864000 s
                               multiple_polling_interval: enable | disable, 轮询周期是否可变
                               polling_interval2: 轮询周期2 1~864000 s
                               auth: anonymous | username_password| certificate_auth, OPC-UA 验证方式
                               username: 用户名  OPC-UA
                               password  : 密码 OPC-UA
                               certificate: 证书路径 OPC-UA
                               private_key: 私钥路径 OPC-UA
                               security_policy: None|Automatic detection|Basic128Rsa15|Basic256|Basic256Sha256|Aes128Sha256RsaOaep 安全策略 OPC-UA
                               security_mode: None|sign|sign_encrypt 安全模式 OPC-UA
                               description: 描述
                               advanced_settings: 展开高级设置 'expand' | 'close'
                               byte_order_16int: 16位整数字节序 'AB' | 'BA'
                               byte_order_32int: 32位整数字节序 'ABCD' | 'CDAB' | 'DCBA' | 'BADC'
                               byte_order_32float: 32位浮点数字节序 'ABCD' | 'CDAB' | 'DCBA' | 'BADC'
                               byte_order_64int: 同选择框的选项
                               byte_order_64float: 同选择框的选项
                               package_reporting： 是否启用包上报 'enable' | 'disable'
                               packet_data_polling_interval: 包数据轮询周期 100~1000 ms
                               mi_data_uploading: 毫秒数据上报（轮询几次后上报）
                               continuous_collection: 是否启用批量采集 'enable' | 'disable'
                               continuous_collection_address: 最大批量采集数 2~125
                               timeout: 超时时间 2~60000 ms
                               connect_timeout: 连接超时时间 2~60000 ms
                               periodically_upload_onchange_data: 是否启用周期上报Onchange数据
                               onchange_uploading_interval: Onchange数据上报间隔
                               communication_interval_time: 通讯间隔时间 0~1000 ms
                               coil_outputs_write_function_code: 线圈寄存器写入功能码 05 | 15
                               holding_register_write_function_code: 保持寄存器写入功能码 06 | 16
                               store_communication_message: 是否存储通讯信息 'enable' | 'disable'
                               submit: 是否提交 'submit', submit=True or submit={'tip_messages': 'submit_success'}
                               text_messages: 文本信息验证 str or list
                               tip_messages: 提示信息验证 str or list or dict
                               cancel: 是否取消  cancel=True
                            [('edit', 'old_controller_name', kwargs)]  kwargs 同add
                            [('apply_template', kwargs)] kwargs 同add, 多一个参数 template_name 模板名称
                            [('check', name, is_check)]  # 选中或取消选中控制器
                                name: str  控制器名称
                                is_check: bool  是否选中 True | False
                            [('delete_bulk', name)]  # 批量删除多个控制器
                                name: str or list 一个或多个控制器名称
                            [('select', name)]  # 点击选中控制器，方便操作对应的测点
                                name: str  控制器名称
                            [('delete', name)]  # 删除单个控制器
                                name: str  控制器名称
                            [('enable', name)]  # 启用单个控制器
                                name: str  控制器名称
                            [('disable', name)]  # 禁用单个控制器
                                name: str  控制器名称
                            [('set_as_template', name, kwargs)]
                                name: str  控制器名称
                                kwargs:
                                    name: 模板名称
                                    description: 模板描述
                                    submit: 是否提交 'submit', submit=True or submit={'tip_messages': 'submit_success'}
                                    text_messages: 文本信息验证 str or list
                                    tip_messages: 提示信息验证 str or list or dict
                                    cancel: 是否取消  cancel=True
               measure: [(action_type, value, ),]
                        [('add', kwargs)]
                            kwargs:
                                name: 名称
                                namespace: 命名空间   OPC-UA
                                address_type: String|Number   OPC-UA
                                identifier: 标识符   OPC-UA
                                register_type:   I|Q|M|DB    ISO-on-TCP
                                dbnumber: 数据库号   ISO-on-TCP
                                modbus_register_address: 寄存器地址 list  ex: ['4X', '40001']
                                register_address: 寄存器地址 str ex: '1'
                                data_type: 数据类型 bit,word,int,dword,dint,float,double,string,bcd16,ulong,long
                                read_bit_data: enable | disable
                                register_bit: 位寄存器
                                data_register_bit: 数据寄存器
                                negative_value: enable | disable
                                storage_lwtsdb: enable | disable
                                decimal_places: 小数位数
                                size: 数据长度
                                encoding_format: 编码格式 ascii, utf-8, utf-16, utf-16-big, gb2312
                                is_array: enable | disable    OPC-UA
                                read_write: 读写属性 read | write | read/write
                                mode: periodic | onchange | never
                                onchange_deadzone: onchange死区
                                unit: 单位 str
                                description: 描述
                                group: 所属组
                                polling_interval: polling_interval|polling_interval_2
                                numerical_mapping: 数值映射 enable | disable
                                data_calculation: 数据计算 no | ratio conversion | offset and zoom| bit truncation | pt/ct | value mapping
                                trans_decimal: 数据运算小数位
                                data_high_limit: 数据上限
                                data_lower_limit: 数据下限
                                high_limit_of_proportion: 比例上限
                                lower_limit_of_proportion: 比例下限
                                magnification: 放大倍数
                                offset: 偏移量
                                start_bit: 起始位
                                end_bit: 结束位
                                pt:
                                ct:
                                value_mapping: [(source, target),] 可以是多个， 代表的是最终结果
                                package_reporting: enable | disable
                                submit: 是否提交 'submit', submit=True or submit={'tip_messages': 'submit_success'}
                                text_messages: 文本信息验证 str or list
                                tip_messages: 提示信息验证 str or list or dict
                                cancel: 是否取消  cancel=True
                        [('edit', 'old_measure_name', kwargs)]  kwargs 同add
                        [('check', name, is_check)]  # 选中或取消选中控制器
                            name: str  测点名称
                            is_check: bool  是否选中 True | False
                        [('search', name)]  # 查询测点
                            name: str  测点名称
                        [('import', file_path)]  # 导入测点
                            file_path: str 导入文件路径
                        [('export', kwargs)]  # 导出测点
                            kwargs: str, 就是导出文件的文件夹
                            kwargs: dict,
                            kwargs = {'file_path': './', 'file_name': None}
                        [('delete_bulk', name)]  # 批量删除测点
                            name: str or list 一个或多个测点名称
                        [('delete_all', )]  # 删除全部测点
                        [('delete', name)]  # 删除一个测点
                            name: str  测点名称
                        [('value', name, kwargs)]  # 编辑一个测点的值
                            name: str  测点名称
                            kwargs: str or dict
                                str: 直接写更新的值
                                dict: {'value': '1', 'submit': {'tip_messages': 'submit_success'}, 'cancel': False}
                        [('add_to_group', measure_name, group_name)]  # 添加到分组
                            measure_name: str  测点名称， 当为all 时表示添加全部测点
                            group_name: str  分组名称
               group: [('action_type', value, value1)]
                    [('import', value, value1)]
                        value: str  导入文件路径
                        value1: 导入时的确认，默认为True， 也可以校验导入后的提示
                    [('export', value,)]
                        value: str  or dict   # 导出分组
                        str: 导出文件夹
                        dict: {"file_path": "./", "file_name": None}
                    [('add', kwargs)]
                        kwargs:
                            is_exists: str, 可以填写分组相关连续的信息， 如果存在就不会添加了
                            name: 名称
                            reporting_interval: 上报间隔
                            onchange_data: 是否上报变化数据 enable | disable
                            onchange_uploading_interval: 变化数据上报间隔
                            max_number:
                            storage_policy: same_as_reporting_interval| independent_storage_interval
                            storage_interval: 存储间隔
                            storage_method: gateway|usb|sd_card
                            storage_path: 存储路径
                            save: 是否保存  save=True 没有该参数时自动保存
                            cancel: 是否取消  cancel=True
                            text_messages: str or list
                            tip_messages: str or list
                    [('edit', 'old_group_name', kwargs)]  kwargs 同add
                    [('check', name, True)] or   [('check', name, False)] # 勾选或取消勾选分组
                    [('delete', name)]  # 删除分组
                    [('export_historical_data', kwargs})]
                        kwargs: str or dict
                            str: 导出文件夹
                            dict: {"file_path": "./", "file_name": None}
                    [('clear_historical_data', name)]  # 清除历史数据
                    [('check_all', value,)]
                        value: bool  勾选或取消勾选全部分组 True | False
                    [('delete_bulk', name, value1)]  # 批量删除分组
                        name: str or list 一个或多个分组名称
                        value1: {'tip_messages': 'submit_success'} or None 提示信息
              controller_template: [('action_type', value, value1)]
                    [('import', value, value1)]
                        value: str  or dict  导入文件路径
                    [('export', value,)]
                        value: str  or dict   # 导出分组
                        str: 导出文件夹
                        dict: {"file_path": "./", "file_name": None}
                    [('edit', 'old_template_name', kwargs)]
                        kwargs:
                            name: 名称
                            description: 描述
                            save: 是否保存  save=True 没有该参数时自动保存
                            cancel: 是否取消  cancel=True
                            text_messages: str or list
                            tip_messages: str or list
                    [('check', name, True)] or   [('check', name, False)] # 勾选或取消勾选
                    [('delete', name)]  # 删除
                    [('check_all', value,)]
                        value: bool  勾选或取消勾选全部分组 True | False
                    [('delete_bulk', name, value1)]  # 批量删除分组
                        name: str or list 一个或多个模板名称名称
                        value1: {'tip_messages': 'submit_success'} or None 提示信息
        :return:
        """
        self.access_menu('edge_computing.device_supervisor.measure_monitor.monitoring_list')
        if kwargs.get('group') and isinstance(kwargs.get('group'), list):
            self.access_menu('edge_computing.device_supervisor.measure_monitor.group')
            for group in kwargs.get('group'):
                if group[0] in ('add', 'edit', 'check', 'delete', 'export_historical_data', 'clear_historical_data'):
                    self.agg_in(self.edge_locators.group_locator, {'table': [group]})
                else:
                    if group[0] == 'import':
                        import_confirm = True if group[2] is None else group[2]
                        self.agg_in(self.edge_locators.group_locator,
                                    {'import': group[1], 'import_confirm': import_confirm})
                    elif group[0] == 'delete_bulk':
                        try:
                            delete_bulk_confirm = group[2]
                        except IndexError:
                            delete_bulk_confirm = True
                        self.agg_in(self.edge_locators.group_locator, {'check_all': False})
                        check_group = [group[1]] if isinstance(group[1], str) else group[1]
                        for name in check_group:
                            self.agg_in(self.edge_locators.group_locator, {'table': [('check', name, True)]})
                        self.agg_in(self.edge_locators.group_locator,
                                    {'delete_bulk': group[1], 'delete_bulk_confirm': delete_bulk_confirm})
                    else:
                        self.agg_in(self.edge_locators.group_locator, {group[0]: group[1]})
            logging.info('group: {} success'.format(kwargs.get('group')))
        if kwargs.get('controller'):
            self.__controller(kwargs.get('controller'))
            logging.info('controller: {} success'.format(kwargs.get('controller')))
        if kwargs.get('measure'):
            self.__measure(kwargs.get('measure'))
            logging.info('measure: {} success'.format(kwargs.get('measure')))
        if kwargs.get('controller_template') and isinstance(kwargs.get('controller_template'), list):
            self.access_menu('edge_computing.device_supervisor.measure_monitor.controller_template')
            for template in kwargs.get('controller_template'):
                if template[0] in ('edit', 'check', 'delete'):
                    self.agg_in(self.edge_locators.controller_template_locator, {'table': [template]})
                else:
                    if template[0] == 'import':
                        self.agg_in(self.edge_locators.controller_template_locator, {'import': template[1]})
                    elif template[0] == 'delete_bulk':
                        try:
                            delete_bulk_confirm = template[2]
                        except IndexError:
                            delete_bulk_confirm = True
                        self.agg_in(self.edge_locators.controller_template_locator, {'check_all': False})
                        check_group = [template[1]] if isinstance(template[1], str) else template[1]
                        for name in check_group:
                            self.agg_in(self.edge_locators.controller_template_locator,
                                        {'table': [('check', name, True)]})
                        self.agg_in(self.edge_locators.controller_template_locator,
                                    {'delete_bulk': template[1], 'delete_bulk_confirm': delete_bulk_confirm})
                    else:
                        self.agg_in(self.edge_locators.controller_template_locator, {template[0]: template[1]})
            logging.info('controller_template: {} success'.format(kwargs.get('controller_template')))

    @allure.step('断言测点监控列表状态')
    @loop_inspector('measure_monitor_status')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
                controller: dict or list 校验一个或多个控制器状态
                     name: str  控制器名称 必填
                     online: bool  True | False
                     status: str  enable | disable
                     protocol: str
                     address: str ex: '"10.5.23.84:502:1" in "${value}"'
                     description: str ex: '"test" in "${value}"'
                measure: dict or list 校验一个或多个测点状态
                     name: str  测点名称 必填
                     online: bool  True | False
                     group: str  所属组
                     datatype: str  数据类型
                     address: str
                     value: str ex: '"1" in "${value}"'
                     unit:  str
                     description: str
                     time: str
                timeout: int 超时时间
                interval: int 轮询间隔
        :return:
        """

        def controller(controller_info) -> bool:
            controller_name = controller_info.get('name')
            if controller_info.get('online') is not None:
                if controller_info.get('online'):
                    controller_info.update({'online_': '"default" not in "${value}"'})
                else:
                    controller_info.update({'online_': '"default" in "${value}"'})
            if controller_info.get('status') is not None:
                if controller_info.get('status') == 'enable':
                    controller_info.update({'status_': '"enableCard" not in "${value}"'})
                else:
                    controller_info.update({'status_': '"enableCard" in "${value}"'})
            self.__turn_page(controller_name)
            return self.eval_locator_attribute(controller_info,
                                               self.edge_locators.controller_card_status(controller_name))

        def measure(measure_info) -> bool:
            measure_name = measure_info.get('name')
            if measure_info.get('online') is not None:
                if measure_info.get('online'):
                    measure_info.update({'online_': '"default" not in "${value}"'})
                else:
                    measure_info.update({'online_': '"default" in "${value}"'})
            self.__turn_page(measure_name, 'measure')
            return self.eval_locator_attribute(measure_info, self.edge_locators.measure_card_status(measure_name))

        if kwargs.get('controller'):
            self.access_menu('edge_computing.device_supervisor.measure_monitor.monitoring_list')
            if isinstance(kwargs.get('controller'), dict):
                return controller(kwargs.get('controller'))
            elif isinstance(kwargs.get('controller'), tuple) or isinstance(kwargs.get('controller'), list):
                for controller_ in kwargs.get('controller'):
                    if not controller(controller_):
                        return False
                else:
                    return True
        if kwargs.get('measure'):
            self.access_menu('edge_computing.device_supervisor.measure_monitor.monitoring_list')
            if isinstance(kwargs.get('measure'), dict):
                return measure(kwargs.get('measure'))
            elif isinstance(kwargs.get('measure'), tuple) or isinstance(kwargs.get('measure'), list):
                for measure_ in kwargs.get('measure'):
                    if not measure(measure_):
                        return False
                else:
                    return True

    @allure.step('获取测点监控列表状态')
    def get_status(self, measure_name: str or list or tuple, keys: str or list or tuple) -> str or dict or None:
        """

        :param measure_name: str or list or tuple 一个或多个测点名称
        :param keys: str or list or tuple , value|time
        :return: value or {'measure_name1': value}
        """
        if measure_name:
            self.access_menu('edge_computing.device_supervisor.measure_monitor.monitoring_list')
            if isinstance(measure_name, str):
                return self.get_text(keys, self.edge_locators.measure_card_status(measure_name))
            else:
                measure_value = {}
                for name in measure_name:
                    measure_value.update({name: self.get_text(keys, self.edge_locators.measure_card_status(name))})
                return measure_value


class Cloud(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    def __measure_point(self, cloud_measure, mute_measure, close=False):
        """

        :param cloud_measure: [(action_type, value, ),]
        :param mute_measure: [(action_type, value, ),]
        :return:
        """
        if cloud_measure:
            self.access_menu('edge_computing.device_supervisor.cloud.mqtt_cloud_service.cloud_measuring_setting.cloud')
            for ac in cloud_measure:
                if ac[0] == 'search':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {"search": ac[1], 'is_search': True})
                elif ac[0] == 'page_number':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {"page_number": ac[1]})
                elif ac[0] in ('import', 'export'):
                    self.agg_in(self.edge_locators.cloud_measuring_point, {ac[0]: ac[1]})
                elif ac[0] == 'check':
                    self.agg_in(self.edge_locators.cloud_measuring_point_table(ac[1]), {'check': ac[2]})
                elif ac[0] == 'mute':
                    self.agg_in(self.edge_locators.cloud_measuring_point_table(ac[1]), {'mute': True, 'confirm': True})
                elif ac[0] == 'check_all':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {ac[0]: True})
                elif ac[0] == 'mute_bulk':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'check_all': False})  # 先取消选择所有的
                    all_measure = [ac[1]] if isinstance(ac[1], str) else ac[1]
                    self.__measure_point(cloud_measure=[('check', x, True) for x in all_measure], mute_measure=None)
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'mute_bulk': True, 'bulk_confirm': True})
                elif ac[0] == 'name':
                    if isinstance(ac[2], str):
                        value = {'name_edit': True, 'value': ac[2], 'submit': {"wait_for_time": 3 * 1000}}
                    else:
                        value = {'name_edit': True}
                        value.update(ac[2])
                    self.agg_in(self.edge_locators.cloud_measuring_point_table(ac[1]), value)
                else:
                    pass
        if mute_measure:
            self.access_menu('edge_computing.device_supervisor.cloud.mqtt_cloud_service.cloud_measuring_setting.muting')
            for ac in mute_measure:
                if ac[0] == 'search':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {"search": ac[1], 'is_search': True})
                elif ac[0] == 'page_number':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {"page_number": ac[1]})
                elif ac[0] in ('import', 'export'):
                    self.agg_in(self.edge_locators.cloud_measuring_point, {ac[0]: ac[1]})
                elif ac[0] == 'check':
                    self.agg_in(self.edge_locators.cloud_measuring_point_table(ac[1], 'mute'), {'check': ac[2]})
                elif ac[0] == 'add':
                    self.agg_in(self.edge_locators.cloud_measuring_point_table(ac[1], 'mute'), {'add': True, 'confirm': True})
                elif ac[0] == 'check_all':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {ac[0]: True})
                elif ac[0] == 'add_bulk':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'check_all': False})  # 先取消选择所有的
                    all_measure = [ac[1]] if isinstance(ac[1], str) else ac[1]
                    self.__measure_point(cloud_measure=None, mute_measure=[('check', x, True) for x in all_measure])
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'add_bulk': True, 'bulk_confirm': True})
                elif ac[0] == 'add_all':
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'measure_check_all': True})
                    self.agg_in(self.edge_locators.cloud_measuring_point, {'add_bulk': True, 'bulk_confirm': True})
                else:
                    pass
        if (cloud_measure or mute_measure) and close:
            self.agg_in(self.edge_locators.cloud_measuring_point, {'close': True})

    @allure.step('断言Cloud状态')
    @loop_inspector('cloud_status')
    def assert_status(self, cloud='mqtt_cloud_service', **kwargs):
        """
        :param cloud: mqtt_cloud_service, whiteeagle_energy_manager
        :param kwargs:
               status: not_enable|connecting|connection_successful|unknown_error|registering|registered ex: status='"${value}"=="connecting"'
               connection_time: day ex: connection_time='"${value}"=="day"'
        """
        self.access_menu(f'edge_computing.device_supervisor.cloud.{cloud}')
        return self.eval_locator_attribute(kwargs, self.edge_locators.cloud_status_locator)

    @allure.step('配置Device Supervisor Cloud')
    def config(self, **kwargs):
        """

        :param kwargs:
                enable: bool True | False 是否启用
                clear_offline_cache: bool True | False 是否清除离线缓存
                import: str, 导入文件路径
                import_confirm: bool True | False 是否确认导入, 或者可以写入 确认导入后的提示
                export: str  or dict   # 导出
                        str: 导出文件夹
                        dict: {"file_path": "./", "file_name": None}
                cloud_measure: [(action_type, value, ),]
                    [('page_number', '100page')]  修改每页显示数量
                    [('search', [$type, name]), ]  # 搜索
                        type: point_name|controller_name|group_name
                    [('check', 'test', True), ] or [('check', 'test', False), ]   # 选择与取消选择
                    [('import', path), ]  # 导入
                    [('export', path), ]  # 导出
                    [('check_all', ), ]  # 选择所有
                    [('mute', 'test',), ]  # 屏蔽
                    [('mute_bulk', ['test','test1']), ]  # 批量屏蔽
                    [('name', 'test', 'test1'), ]  # 修改名称
                mute_measure: [(action_type, value, ),]
                    [('page_number', '100page')]  修改每页显示数量
                    [('search', [$type, name]), ]  # 搜索
                        type: point_name|controller_name|group_name
                    [('check', 'test', True), ] or [('check', 'test', False), ]   # 选择与取消选择
                    [('import', path), ]  # 导入
                    [('export', path), ]  # 导出
                    [('add_all', ), ]  # 选择所有
                    [('add', 'test',), ]  # 加入
                    [('add_bulk', ['test','test1']), ]  # 批量屏蔽
                cloud_type: mqtt|iSCADA Cloud|alibaba_cloud|AWS IoT|Azure IoT
                mqtt_server: str
                mqtt_client_id: str
                mqtt_auth: True|False
                mqtt_username: str
                mqtt_password: str
                mqtt_last_will: 'expand' | 'collapse'
                mqtt_last_will_topic: str
                mqtt_last_will_qos: 0|1|2
                mqtt_last_will_retain: 'true'|'false'
                mqtt_last_will_payload: str

                ics_local_configuration: True|False
                ics_server: str
                ics_keepalive: int

                alibaba_region_id: str
                alibaba_auth_method: unique_certificate_per_device|unique_certificate_per_product
                alibaba_product_key: str
                alibaba_device_name: str
                alibaba_device_secret: str
                alibaba_tls_model: str, 文件路径

                aws_endpoint: str
                aws_client_id: str
                aws_certificate: str, 文件路径
                aws_private_key: str, 文件路径
                aws_root_ca: str, 文件路径

                azure_auth_method: Symmetric key|X.509 Self-Signed|X.509 CA-Signed
                azure_connection_string: str
                azure_hub_name: str
                azure_device_id: str
                azure_device_certificate: str, 文件路径
                azure_device_key: str, 文件路径

                mqtt_advanced_settings: True|False
                port: int
                keep_alive: int
                tls: 'symmetric'|'disable'|'asymmetric'
                verify_method: verify_client_ca|verify_client_certificate_and_key
                verify_server_certificate: True|False
                root_ca: str, 文件路径
                client_private_key: str, 文件路径
                client_certificate: str, 文件路径
                clean_session: no|yes
                mqtt_version: v3.1 |v3.1.1

                submit: bool or dict,

                publish: [($action, **kwarg)]
                 [('delete', 'test')]
                 [('add', kwarg)]
                     add parameter:
                     is_exists: name, 如果存在就不添加
                     name: str
                     trigger: measuring_point|alarm_message
                     label: list 多个选项
                     topic: str
                     qos: 0|1|2
                     entry_function: main
                     quick_function: str,  换行使用\n
                     save: True|False
                     text_messages: str or list
                     tip_messages: str or list
                     cancel: True, False
                 [('edit', 'name', kwarg)]
                 多个操作时使用列表 [('add',{}), ('add',{})]
                 subscribe: [($action, **kwarg)]
                 [('delete', 'test')]
                 [('add', kwarg)]
                     add parameter:
                     is_exists: name, 如果存在就不添加
                     name: str
                     topic: str
                     qos: 0|1|2
                     entry_function: main
                     payload_type: Plaintext|Base64|JSON|Hex
                     quick_function: str,  换行使用\n
                     save: True|False
                     text_messages: str or list
                     tip_messages: str or list
                     cancel: True, False
                 [('edit', 'name', kwarg)]
                 多个操作时使用列表 [('add',{}), ('add',{})]
        :return:
        """
        self.access_menu('edge_computing.device_supervisor.cloud')
        if kwargs.get('cloud_measure') or kwargs.get('mute_measure'):
            self.agg_in(self.edge_locators.cloud_locator, {'enable': True})
            self.__measure_point(kwargs.get('cloud_measure'), kwargs.get('mute_measure'), True)
        if kwargs.get('import') and kwargs.get('import_confirm') is None:
            kwargs.update({'import_confirm': True})
        if kwargs.get('clear_offline_cache'):
            kwargs.update({'cache_confirm': True})
        self.agg_in(self.edge_locators.cloud_locator, kwargs)


class Alarm(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Device Supervisor告警')
    def config(self, **kwargs):
        """

        :param kwargs:
                realtime: dict
                    page_number: 50page|30page|100page
                rules: [('action_type', value, value1)]
                    [('page_number', value, )]
                        value: 50page|30page|100page
                    [('import', value, value1)]
                        value: str  导入文件路径
                        value1: 导入时的确认，默认为True， 也可以校验导入后的提示
                    [('export', value,)]
                        value: str  or dict   # 导出
                        str: 导出文件夹
                        dict: {"file_path": "./", "file_name": None}
                    [('add', kwargs)]
                        kwargs:
                            is_exists: str, 可以填写告警相关连续的信息， 如果存在就不会添加了
                            name: 名称
                            controller: 控制器名称
                            measure: 测点名称
                            level: remind|warning|secondary|important|serious
                            condition: 告警条件， list，['=', '13', '&&', '>', '13'], 不需要的值可以写None
                            content: 告警内容
                            label: 标签
                            save: 是否保存  save=True 没有该参数时自动保存
                            cancel: 是否取消  cancel=True
                            text_messages: str or list
                            tip_messages: str or list
                    [('edit', 'old_alarm_name', kwargs)]  kwargs 同add
                    [('check', name, True)] or   [('check', name, False)] # 勾选或取消勾选分组
                    [('delete', name)]  # 删除
                    [('check_all', value,)]
                        value: bool  勾选或取消勾选全部分组 True | False
                    [('delete_bulk', name, value1)]  # 批量删除分组
                        name: str or list 一个或多个告警名称
                        value1: {'tip_messages': 'submit_success'} or None 提示信息
                    [('add_to_label', name, label_name)]  # 添加到标签
                        name: str or list 一个或多个告警名称
                        label_name: str  标签名称
                history: [('action_type', value, value1)]
                    [('page_number', value, )]
                        value: 50page|30page|100page
                    [('search', **kwargs,)]
                        name: str 搜索的名字
                        start_time： 2023-05-29 16:38 開始時間
                        end_time： 2023-05-29 16:38 結束時間
                    [('check_all', value,)]
                        value: bool  勾选或取消勾选全部分组 True | False
                    [('check', name, True)] or   [('check', name, False)] # 勾选或取消勾选分组
                    [('delete', name)]  # 删除
                    [('delete_bulk', name, value1)]  # 批量删除分组
                        name: str or list 一个或多个告警名称
                        value1: {'tip_messages': 'submit_success'} or None 提示信息
                label: [('action_type', value, value1)]
                    [('page_number', value, )]
                        value: 50page|30page|100page
                    [('import', value, value1)]
                        value: str  导入文件路径
                        value1: 导入时的确认，默认为True， 也可以校验导入后的提示
                    [('export', value,)]
                        value: str  or dict   # 导出
                        str: 导出文件夹
                        dict: {"file_path": "./", "file_name": None}
                    [('add', kwargs)]
                            kwargs:
                                is_exists: str, 可以填写告警相关连续的信息， 如果存在就不会添加了
                                name: 名称
                                save: 是否保存  save=True 没有该参数时自动保存
                                cancel: 是否取消  cancel=True
                                text_messages: str or list
                                tip_messages: str or list
                    [('check', name, True)] or   [('check', name, False)] # 勾选或取消勾选分组
                    [('delete', name)]  # 删除
                    [('check_all', value,)]
                        value: bool  勾选或取消勾选全部 True | False
                    [('delete_bulk', name, value1)]  # 批量删除
                        name: str or list 一个或多个名称
                        value1: {'tip_messages': 'submit_success'} or None 提示信息
        :return:
        """
        if kwargs.get('label'):
            self.access_menu('edge_computing.device_supervisor.alarm.alarm label')
            for label in kwargs.get('label'):
                if label[0] in ('add', 'check', 'delete'):
                    self.agg_in(self.edge_locators.alarm_label_locator, {'table': [label]})
                else:
                    if label[0] == 'import':
                        import_confirm = True if label[2] is None else label[2]
                        self.agg_in(self.edge_locators.alarm_label_locator,
                                    {'import': label[1], 'import_confirm': import_confirm})
                    elif label[0] in ('delete_bulk',):
                        self.agg_in(self.edge_locators.alarm_label_locator, {'check_all': False})
                        check_group = [label[1]] if isinstance(label[1], str) else label[1]
                        for name in check_group:
                            self.agg_in(self.edge_locators.alarm_label_locator, {'table': [('check', name, True)]})
                        try:
                            delete_bulk_confirm = label[2]
                        except IndexError:
                            delete_bulk_confirm = True
                        self.agg_in(self.edge_locators.alarm_label_locator,
                                    {'delete_bulk': label[1], 'delete_bulk_confirm': delete_bulk_confirm})
                    else:
                        self.agg_in(self.edge_locators.alarm_label_locator, {label[0]: label[1]})
            logging.info('device supervisor alarm label: {} success'.format(kwargs.get('label')))
        if kwargs.get('rules'):
            self.access_menu('edge_computing.device_supervisor.alarm.alarm rules')
            for rule in kwargs.get('rules'):
                if rule[0] in ('add', 'edit', 'check', 'delete'):
                    self.agg_in(self.edge_locators.alarm_rules_locator, {'table': [rule]})
                else:
                    if rule[0] == 'import':
                        try:
                            import_confirm = rule[2]
                            self.agg_in(self.edge_locators.alarm_rules_locator,
                                        {'import': rule[1], 'import_confirm': import_confirm})
                        except IndexError:
                            self.agg_in(self.edge_locators.alarm_rules_locator, {'import': rule[1]})
                    elif rule[0] in ('delete_bulk', 'add_to_label'):
                        self.agg_in(self.edge_locators.alarm_rules_locator, {'check_all': False})
                        check_group = [rule[1]] if isinstance(rule[1], str) else rule[1]
                        for name in check_group:
                            self.agg_in(self.edge_locators.alarm_rules_locator, {'table': [('check', name, True)]})
                        if rule[0] == 'add_to_label':
                            self.agg_in(self.edge_locators.alarm_rules_locator, {'add_to_label': True})
                            self.agg_in(self.edge_locators.alarm_add_to_label(rule[2]),
                                        {'label_name': 'check', 'submit': True})
                        else:
                            try:
                                delete_bulk_confirm = rule[2]
                            except IndexError:
                                delete_bulk_confirm = True
                            self.agg_in(self.edge_locators.alarm_rules_locator,
                                        {'delete_bulk': rule[1], 'delete_bulk_confirm': delete_bulk_confirm})
                    else:
                        self.agg_in(self.edge_locators.alarm_rules_locator, {rule[0]: rule[1]})
            logging.info('device supervisor alarm rules: {} success'.format(kwargs.get('rules')))
        if kwargs.get('realtime'):
            self.access_menu('edge_computing.device_supervisor.alarm.realtime alarms')
            self.agg_in(self.edge_locators.alarm_realtime_locator, kwargs.get('realtime'))
        if kwargs.get('history'):
            self.access_menu('edge_computing.device_supervisor.alarm.history alarms')
            for history in kwargs.get('history'):
                if history[0] in ('check', 'delete'):
                    self.agg_in(self.edge_locators.alarm_history_locator, {'table': [history]})
                else:
                    if history[0] == 'search':
                        self.agg_in(self.edge_locators.alarm_history_locator, history[1].update({"search": True}))
                    elif history[0] in ('delete_bulk',):
                        self.agg_in(self.edge_locators.alarm_history_locator, {'check_all': False})
                        check_group = [history[1]] if isinstance(history[1], str) else history[1]
                        for name in check_group:
                            self.agg_in(self.edge_locators.alarm_history_locator, {'table': [('check', name, True)]})
                        try:
                            delete_bulk_confirm = history[2]
                        except IndexError:
                            delete_bulk_confirm = True
                        self.agg_in(self.edge_locators.alarm_history_locator,
                                    {'delete_bulk': history[1], 'delete_bulk_confirm': delete_bulk_confirm})
                    else:
                        self.agg_in(self.edge_locators.alarm_history_locator, {history[0]: history[1]})
            logging.info('device supervisor alarm history: {} success'.format(kwargs.get('history')))

    @allure.step("断言Device Supervisor告警状态")
    @loop_inspector('device_supervisor_alarm_status')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
            realtime:
               str: 连续告警相关字段，需自己国际化， 这种是判断有
               list: 连续告警相关字段，需自己国际化， 这种是判断有多个
               dict: 当为字典时 key是连续告警相关字段， value是判断是否有告警，True是有告警，False是无告警
                {'alarm_name': True or False}
        :return:
        """

        def _status(value_, type_):
            if value_:
                if type_ == 'realtime':
                    self.access_menu('edge_computing.device_supervisor.alarm.realtime alarms')
                    alarm = IgTable([], self.edge_locators.alarm_realtime_table)
                else:
                    self.access_menu('edge_computing.device_supervisor.alarm.history alarms')
                    alarm = IgTable([], self.edge_locators.alarm_history_table)
                if isinstance(value_, str):
                    realtime_expect = {value_: True}
                elif isinstance(value_, list) or isinstance(value_, tuple):
                    realtime_expect = {realtime: True for realtime in value_}
                elif isinstance(value_, dict):
                    realtime_expect = value_
                else:
                    raise TypeError('realtime type error')
                for key, value in realtime_expect.items():
                    if value and not alarm.exist(key, locale={}):
                        return False
                    if not value and alarm.exist(key, locale={}):
                        return False
                else:
                    return True
            else:
                return True

        if not _status(kwargs.get('realtime'), 'realtime'):
            return False
        if not _status(kwargs.get('history'), 'history'):
            return False
        else:
            return True


class ParameterSettings(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Device Supervisor参数设置')
    def config(self, **kwargs):
        """

        :param kwargs:
               band_485: 300|1200|2400|4800|9600|19200|38400|57600|115200|230400
               band_232: 300|1200|2400|4800|9600|19200|38400|57600|115200|230400
               data_bits_485： 7|8
               data_bits_232： 7|8
               parity_485： none|odd|even
               parity_232： none|odd|even
               stop_bits_485: 1|2
               stop_bits_232: 1|2
               submit_serial: True or {'tip_message': 'submit_success'}
               log_level: info|debug|warning|error
               historical_alarm_max: int
               cache_data_storage_method: usb|sd_card|gateway
               cache_data_storage_path: str
               cache_data_max: int
               communication_storage_method: usb|sd_card|gateway
               communication_storage_path: str
               communication_max: int
               submit_default_parameter: True or {'tip_message': 'submit_success'}
               import: str , 上传文件路径
               import_confirm: True or {'tip_message': 'submit_success'} 可以不传
               export: str or dict, 导出文件路径
               parameter: [(action, value)]
                    [('add', kwargs)]
                    kwargs:
                        key: str
                        value: str
                    [('edit', 'old_name', kwargs)]  kwargs 同add
                    [('delete', name)]  # 删除
        :return:
        """
        self.access_menu('edge_computing.device_supervisor.parameter settings')
        if kwargs.get('import') and kwargs.get('import_confirm') is None:
            kwargs['import_confirm'] = {'wait_for_time': 3 * 1000}
        self.agg_in(self.edge_locators.parameter_locator, kwargs)


class DeviceSupervisor:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.measure = MeasureMonitor(host, username, password, protocol, port, model, language, page, locale)
        self.alarm = Alarm(host, username, password, protocol, port, model, language, page, locale)
        self.cloud = Cloud(host, username, password, protocol, port, model, language, page, locale)
        self.parameter = ParameterSettings(host, username, password, protocol, port, model, language, page, locale)

    @allure.step("数据运算计算")
    def data_calculation(self, transform_type, input_value, decimal=2, data_high_limit=0, data_lower_limit=0,
                         high_limit_of_proportion=0, lower_limit_of_proportion=0, magnification=0, offset=0, pt=0, ct=0,
                         start_bit=0, end_bit=0, datatype='INT', reverse=False) -> int or float:
        """数据运算计算测点值

        :param transform_type: 1:比例换算 | 2:偏移及缩放 | 3:位截取 | 4:PT/CT
        :param input_value: 输入值
        :param decimal: 最后保留小数位
        :param data_high_limit: 数据上限
        :param data_lower_limit: 数据下限
        :param high_limit_of_proportion: 比例上限
        :param lower_limit_of_proportion: 比例下限
        :param magnification: 倍率
        :param offset: 偏移量
        :param pt: PT
        :param ct: CT
        :param start_bit: 位截取起始位
        :param end_bit: 位截取截止位
        :param reverse: True | False
        :return:
        """
        operator_value = operation_value = 0.0
        if transform_type == 1:
            if reverse:
                operator_value = ((input_value - lower_limit_of_proportion) * (data_high_limit - data_lower_limit) / \
                                  (high_limit_of_proportion - lower_limit_of_proportion)) + data_lower_limit
            else:
                operation_value = (Decimal(high_limit_of_proportion) - Decimal(lower_limit_of_proportion)) / \
                                  (Decimal(data_high_limit) - Decimal(data_lower_limit)) * (
                                          Decimal(input_value) - Decimal(data_lower_limit)) + \
                                  Decimal(lower_limit_of_proportion)
        elif transform_type == 2:
            if reverse:
                operator_value = (input_value - offset) / magnification
            else:
                operation_value = Decimal(input_value) * Decimal(magnification) + Decimal(offset)
        elif transform_type == 3:
            if 'BCD' in datatype.upper():
                input_value = int(str(input_value), 16)
            bin_value = bin((1 << 64) + input_value)
            operation_value = int(bin_value[::-1][start_bit:end_bit + 1][::-1], 2)
        elif transform_type == 4:
            if reverse:
                operator_value = (input_value / ct / pt - offset) / magnification
            else:
                operation_value = (Decimal(input_value) * Decimal(magnification) + Decimal(offset)) * Decimal(
                    pt) * Decimal(ct)
        else:
            raise Exception('NonsupportTransformType')
        if reverse:
            if isinstance(input_value, int):
                return int(operator_value)
            else:
                return operator_value
        else:
            if transform_type != 3:
                logging.info(type(operation_value))
                decimal_value = Decimal(operation_value).quantize(Decimal('0.'.ljust(decimal + 2, '0')),
                                                                  rounding=ROUND_HALF_UP)
                logging.info('The number is {}, after operation is {}'.format(input_value, decimal_value))
                # operation_value = round(operation_value, decimal)
                if len(str(decimal_value).split('.')[0]) >= 22:
                    logging.info('The number is {}, greater than 20 are represented by scientific notation!'.format(
                        operation_value))
                    return '{:.16e}'.format(operation_value)
                else:
                    return decimal_value
            else:
                return operation_value

    @allure.step("生成数据运算配置")
    def generate_config_parameter(self, transform_type: int, datatype: str):
        """

        :param transform_type: 1:比例换算 | 2:偏移及缩放 | 3:位截取 | 4:PT/CT
        :param datatype: 数据类型 BYTE| SINT| BCD| INT| WORD| DINT| DWORD| LONG| ULONG| FLOAT| DOUBLE
        :return:
        """
        datatype_list = {'SINT': (-(2 ** 8 // 2), (2 ** 8 - 1) // 2), 'BYTE': (0, 2 ** 8 - 1), 'BCD16': (0, 9999),
                         'INT': (-(2 ** 16 // 2), (2 ** 16 - 1) // 2), 'WORD': (0, 2 ** 16 - 1),
                         'DINT': (-(2 ** 32 // 2), (2 ** 32 - 1) // 2), 'BCD32': (0, 99999999),
                         'DWORD': (0, 2 ** 32 - 1), 'LONG': (-(2 ** 64 // 2), (2 ** 64 - 1) // 2),
                         'ULONG': (0, 2 ** 64 - 1)}
        digit_list = {'SINT': (0, 7), 'BYTE': (0, 7), 'BCD16': (0, 15), 'INT': (0, 15), 'WORD': (0, 15),
                      'DINT': (0, 31),
                      'DWORD': (0, 31), 'BCD32': (0, 31), 'LONG': (0, 63), 'ULONG': (0, 63)}
        type_ = datatype.upper()
        if transform_type == 1:
            if type_ in ['FLOAT', 'DOUBLE']:
                value_range = sorted([round(random.uniform(-9999999999, 9999999999), 6) for i in range(2)])
            else:
                value_range = sorted(
                    [random.randint(datatype_list[type_][0], datatype_list[type_][1]) for i in range(2)])
            scale_range = sorted([round(random.uniform(-9999999999, 9999999999), 6) for i in range(2)])
            gain_value = value_range + scale_range
            logging.info('config parameter: {}'.format(gain_value))
            return gain_value
        elif transform_type == 2:
            zoom_range = [round(random.uniform(-9999, 9999), 6) for i in range(2)]
            return zoom_range
        elif transform_type == 3:
            start_bit = random.randint(digit_list[type_][0], digit_list[type_][1])
            end_bit = random.randint(digit_list[type_][0], digit_list[type_][1])
            while end_bit == start_bit:
                end_bit = random.randint(digit_list[type_][0], digit_list[type_][1])
            bit_range = sorted([start_bit, end_bit])
            return bit_range
        else:
            pt_range = [round(random.uniform(-999, 999), 6) for i in range(4)]
            return pt_range

    @allure.step('根据数据类型生成随机值')
    def generate_random_value(self, datatype, magnification=1, offset=0, pt=1, ct=1):
        """
        根据数据类型生成随机数
        :param datatype:  数据类型 BYTE| SINT| BCD| INT| WORD| DINT| DWORD| LONG| ULONG| FLOAT| DOUBLE
        :param magnification: 倍率
        :param offset: 偏移量
        :param pt:
        :param ct:
        :return:
        """
        type_ = datatype.upper()
        datatype_list = {'SINT': (-(2 ** 8 // 2), (2 ** 8 - 1) // 2), 'BYTE': (0, 2 ** 8 - 1), 'BCD16': (0, 9999),
                         'INT': (-(2 ** 16 // 2), (2 ** 16 - 1) // 2), 'WORD': (0, 2 ** 16 - 1),
                         'DINT': (-(2 ** 32 // 2), (2 ** 32 - 1) // 2), 'BCD32': (0, 99999999),
                         'DWORD': (0, 2 ** 32 - 1), 'LONG': (-(2 ** 64 // 2), (2 ** 64 - 1) // 2),
                         'ULONG': (0, 2 ** 64 - 1)}
        if type_ in ['FLOAT', 'DOUBLE']:
            low, high = sorted(
                [(-999999 * magnification + offset) * pt * ct, (999999 * magnification - offset) * pt * ct])
            value = round(random.uniform(low, high), 2)
        else:
            if magnification == 1 and offset == 0 and pt == 1 and ct == 1:
                if type_ in ['BYTE', 'SINT', 'BCD16', 'INT', 'WORD']:
                    value = random.randint(datatype_list[type_][0], datatype_list[type_][1])
                elif type_ in ['DINT', 'LONG', ]:
                    value = random.randint(-32768, 32767)
                elif type_ in ['DWORD', 'ULONG', 'BCD32']:
                    value = random.randint(0, 65535)
            else:
                low, high = sorted([int((datatype_list[type_][0] * magnification + offset) * pt * ct),
                                    int((datatype_list[type_][1] * magnification + offset) * pt * ct)])
                value = random.randint(low, high)
                if value < datatype_list[type_][0]:
                    value = datatype_list[type_][0]
                elif value > datatype_list[type_][1]:
                    value = datatype_list[type_][1]
                else:
                    pass
        logging.info(f'generate random value {value}')
        return value


class EdgeComputing:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.python_edge: PythonEdgeComputing = PythonEdgeComputing(host, username, password, protocol, port,
                                                                    model, language, page, locale)
        self.docker_manager: DockerManager = DockerManager(host, username, password, protocol, port, model, language,
                                                           page, locale)
        self.device_supervisor: DeviceSupervisor = DeviceSupervisor(host, username, password, protocol, port, model,
                                                                    language, page, locale)
