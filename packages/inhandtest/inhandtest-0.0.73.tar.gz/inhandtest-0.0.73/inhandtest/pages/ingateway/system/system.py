# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 14:29:03
# @Author  : Pane Li
# @File    : system.py
"""
system

"""
import allure
from inhandtest.tools import loop_inspector
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class SystemTime(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言系统时间状态')
    @loop_inspector('system_time_status')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
                     local_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
                     device_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
        :return:
        """
        self.access_menu('system.system_time')
        return self.eval_locator_attribute(kwargs, self.system_locators.system_time_status_locators)

    @allure.step('获取系统时间')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys: local_time device_time

        :return: 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        self.access_menu('system.system_time')
        return self.get_text(keys, self.system_locators.system_time_status_locators)

    @allure.step('配置系统时间')
    def config(self, **kwargs):
        """ 配置系统时间, 无需配置时均不填写参数

        :param kwargs:
               time_zone: utc-12, utc-11, utc-10, utc-9, utc-8, utc-7, utc-6, utc-6_atlantic, utc-5, utc-5_colombia,
                          utc-4, utc-4_atlantic, utc-4_brazil, utc-3_30, utc-3, utc-3_brazil, utc-3_guyana, utc-2, utc-1, utc, utc_england,
                          utc+1, utc+1_france, utc+2, utc+2_greece, utc+3, utc+3_finland, utc+4, utc+5, utc+5_30, utc+6,
                          utc+7, utc+8, utc+9, utc+9_30, utc+10, utc+11, utc+12, utc+12_zealand
               time_zone_apply： True, False  ex time_zone_apply=True or time_zone_apply={'tip_messages': 'apply_success'}
               auto_daylight_saving_time: enable, disable ex: auto_daylight_saving_time='enable'
               sync_time: True, False ex: sync_time=True  or sync_time={'tip_messages': 'sync_success'}
               date: 2021-06-02 ex: date='2021-06-02'
               time_: 00:00:00 ex: time_='00:00:00'
               apply_time: True, False ex: apply_time=True or apply_time={'tip_messages': 'apply_success'}

               enable_sntp_clients: True, False ex: enable_sntp_clients=True
               sntp_interval: 60 ex: sntp_interval=60
               sntp_servers: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', '0.pool.ntp.org')]
                 [('add', {'server_address': '0.pool.ntp.org', 'port': '4444'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     port: 4444 ex: port=4444
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': '0.pool.ntp.org', 'port': '4444', 'is_exists': '0.pool.ntp.org'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', '0.pool.ntp.org', {'server_address': '1.pool.ntp.org'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit_sntp: True, False ex: submit_sntp=True or submit_sntp={'tip_messages': 'submit_success'}

               enable_ntp_server: True, False ex: enable_ntp_server=True
               pre_ntp_server: server_address ex: pre_ntp_server='0.pool.ntp.org'
               source_interface: Cellular 1、Bridge 1 ex: source_interface='Cellular 1'
               source_ip: 192.168.2.1 ex: source_ip='192.168.2.1'
               ntp_servers: [($action, **kwarg)]
                 ex: [('delete_all', )],
                 [('delete', '0.pool.ntp.org')]
                 [('add', {'server_address': '0.pool.ntp.org'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': '0.pool.ntp.org',  'is_exists': '0.pool.ntp.org'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', '0.pool.ntp.org', {'server_address': '1.pool.ntp.org'})]
                 [('enable', '0.pool.ntp.org', True)] or  [('enable', '0.pool.ntp.org', False)]
               error_text: str or list or tuple
               submit_ntp: True or False ex: submit_ntp=True  or  submit_ntp={'tip_messages': 'apply_success'}
               tip_messages: True or False ex: tip_messages=True or tip_messages={'tip_messages': 'apply_success'}
        :return:
        """
        self.access_menu('system.system_time')
        self.agg_in(self.system_locators.system_time_locators, kwargs)


class Log(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('操作系统日志')
    def log(self, **kwargs):
        """

        :param kwargs:
                     recent_lines: 20,50,100,200,all ex: recent_lines='all'
                     refresh_policy: manual_refresh, 5sec, 10sec, 15sec, 30sec, 1min, 2min, 3min, 4min, 5min, 10min, 15min, 20min, 30min
                                     ex: refresh_policy='manual_refresh'
                     refresh: True, False ex: refresh=True or refresh={'wait_for_time': 3* 1000}
                     clear_history_log: True, False ex: clear_history_log=True
                     clear_log: True, False ex: clear_log=True
                     download_log: {'file_path': $file_path, 'file_name': $file_name} ex: download_log={'file_path': './tmp', 'file_name': 'log.log'}
                     download_history_log: {'file_path': $file_path, 'file_name': $file_name} ex: download_history_log={'file_path': './tmp', 'file_name': 'log.log'}
                     download_diagnostic_data: {'file_path': $file_path, 'file_name': $file_name} ex: download_diagnostic_data={'file_path': './tmp', 'file_name': 'log.log'}
        :return:
        """
        self.access_menu('system.log.log')
        if kwargs.get('refresh_policy') == 'manual_refresh' and kwargs.get('refresh') is None:
            kwargs.update({'refresh': {'wait_for_time': 3 * 1000}})
        if kwargs.get('clear_history_log') or kwargs.get('clear_log'):
            kwargs.update({'confirm': {'tip_messages': 'log_cleared'}})
        self.agg_in(self.system_locators.log_locators, kwargs)

    @allure.step('配置系统日志')
    def config(self, **kwargs):
        """ 配置系统时间, 无需配置时均不填写参数

        :param kwargs:
               enable_remote_server: True, False ex: enable_remote_server=True
               remote_server: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', 'log.server.com')]
                 [('add', {'server_address': 'log.server.com', 'port': '4444'})]
                     add parameter:
                     server_address:  0.pool.ntp.org ex: server_address="0.pool.ntp.org"
                     port: 4444 ex: port=4444
                     error_text: str or list
                     cancel: True, False
                 [('add', {'server_address': 'log.server.com', 'port': '4444', 'is_exists': 'log.server.com'})] 如果存在0.pool.ntp.org则不添加
                 [('edit', 'log.server.com', {'server_address': 'log.server.com.cn'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               log_to_console： check, uncheck  ex log_to_console='check'
               history_log_file_size: str, int ex: history_log_file_size='100' or history_log_file_size=100
               history_log_level: debug, information, notice, warning, error, serious, alarm, emergency ex: history_log_level='debug'
               error_text: str or list or tuple
               submit: True or False ex: submit=True  or  submit={'tip_messages': 'submit_success'}
               tip_messages: True or False ex: tip_messages=True or tip_messages={'tip_messages': 'submit_success'}
        :return:
        """
        self.access_menu('system.log.configure')
        self.agg_in(self.system_locators.log_config_locators, kwargs)


class Config(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置系统日志')
    def config(self, **kwargs):
        """ 配置系统时间, 无需配置时均不填写参数

        :param kwargs:
               auto_save: True, False ex: auto_save=True
               encrypted: True, False ex: encrypted=True
               import_startup_config: str ex: import_startup_config='./tmp/config.cfg'
               startup_config_contain_private_key: True, False ex: startup_config_contain_private_key=True
               export_startup_config: dict ex: export_startup_config={'file_path': './tmp', 'file_name': 'config.cfg'}
               running_config_contain_private_key: True, False ex: running_config_contain_private_key=True
               export_running_config: dict ex: export_running_config={'file_path': './tmp', 'file_name': 'config.cfg'}
               clear_all_data_restore: True, False ex: clear_all_data_restore=True
               restore_factory_default: True, False ex: restore_factory_default=True
        :return:
        """
        self.access_menu('system.configuration_management')
        if kwargs.get('import_startup_config'):
            kwargs.update({'import_config': True, 'reboot': {'wait_for_time': 100 * 1000}})
        if kwargs.get('startup_config_contain_private_key'):
            kwargs.update({'startup_config_confirm': True})
        if kwargs.get('running_config_contain_private_key'):
            kwargs.update({'running_config_confirm': True})
        if kwargs.get('clear_all_data_restore'):
            kwargs.update({'clear_all_data_confirm': True})
        if kwargs.get('restore_factory_default'):
            kwargs.update({'restore_factory_default_ok': True})
        self.agg_in(self.system_locators.config_locators, kwargs)
        if kwargs.get('import_startup_config') or kwargs.get('restore_factory_default'):
            self.login()


class Cloud(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言平台状态')
    @loop_inspector('platform status')
    def assert_status(self, platform: str, **kwargs):
        """

        :param platform: 'ics', 'dm', 'iscada'
        :param kwargs:
               status: registering, registered, connecting, connect
        :return:
        """
        if platform == 'ics':
            self.access_menu('system.inhand cloud.inhand connect service')
        elif platform == 'dm':
            self.access_menu('system.inhand cloud.inhand device manager')
        else:
            self.access_menu('system.inhand cloud.inhand iscada cloud')
        return self.eval_locator_attribute(kwargs, self.system_locators.platform_status_locators)

    @allure.step('获取平台状态')
    def get_status(self, platform: str, keys: str or list or tuple) -> str or dict or None:
        """

        :param platform: 'ics', 'dm', 'iscada'
        :param keys:
               status
        :return:
        """
        if platform == 'ics':
            self.access_menu('system.inhand cloud.inhand connect service')
        elif platform == 'dm':
            self.access_menu('system.inhand cloud.inhand device manager')
        else:
            self.access_menu('system.inhand cloud.inhand iscada cloud')
        return self.get_text(keys, self.system_locators.platform_status_locators)

    @allure.step('配置平台')
    def config(self, platform: str, **kwargs):
        """

        :param platform: 'ics', 'dm', 'iscada'
        :param kwargs:
          ics & dm:
                enable: True, False ex: enable=True
                server_address: str custom ex: server_address='ics.inhandnetworks.com' or server_address='custom'
                custom_address: str ex: custom_address='ics.inhandnetworks.com'
                register_account: str ex: register_account='inhand@inhand.com.cn'
                enable_secure_channel: True, False ex: enable_secure_channel=True
                location: GPS, Cellular ex: location='GPS'
                lbs_upload_interval: int ex: lbs_upload_interval=3600
                keepalive: int ex: keepalive=60
                data_upload_interval: int ex: data_upload_interval=3600

            iscada:
                enable: True, False ex: enable=True
                server_address: str custom ex: server_address='ics.inhandnetworks.com' or server_address='custom'
                custom_address: str ex: custom_address='ics.inhandnetworks.com'
                keepalive: int ex: keepalive=60
            all:
                submit: True, False ex: submit=True or submit={'tip_messages': 'submit_success'}
                text_messages:
                tip_messages:
        :return:
        """
        if platform == 'ics':
            self.access_menu('system.inhand cloud.inhand connect service')
        elif platform == 'dm':
            self.access_menu('system.inhand cloud.inhand device manager')
        else:
            self.access_menu('system.inhand cloud.inhand iscada cloud')
        self.agg_in(self.system_locators.platform_locators, kwargs)


class Firmware(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言固件版本')
    @loop_inspector('firmware version')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
               version: str ex: version='V2.0.6'
        :return:
        """

        self.access_menu('system.firmware upgrade')
        return self.eval_locator_attribute(kwargs, self.system_locators.firmware_status_locators)

    @allure.step('获取固件版本')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys:
               version
        :return:
        """
        self.access_menu('system.firmware upgrade')
        return self.get_text(keys, self.system_locators.firmware_status_locators)

    @allure.step('升级固件')
    def upgrade(self, **kwargs):
        """

        :param kwargs:
          firmware: str ex: firmware='./tmp/IG9-V2.0.5.bin'
          upgrade: True, False ex: upgrade=True
          reboot: True, False ex: reboot=True
        :return:
        """
        self.access_menu('system.firmware upgrade')
        if kwargs.get('upgrade'):
            kwargs.update({'confirm': True})
        self.agg_in(self.system_locators.firmware_locators, kwargs)
        if kwargs.get('reboot'):
            self.login()
        else:
            self.agg_in(self.system_locators.firmware_locators, {'cancel_reboot': True})


class AccessTools(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('获取Access Tools状态')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys:
               https_listen_ip,https_port,telnet_listen_ip,telnet_port,ssh_listen_ip,ssh_port,developer_password
        :return:
        """
        self.access_menu('system.access tools')
        return self.get_text(keys, self.system_locators.access_tools_status_locators)

    @allure.step('配置管理工具')
    def config(self, **kwargs):
        """

        :param kwargs:
          https_listen_ip: Any, ex: https_listen_ip='Any'
          https_port: int ex: https_port=443
          web_login_timeout: int ex: web_login_timeout=300
          https_remote_access: True, False ex: https_remote_access=True
          https_remote_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': ''})]
                    add parameters:
                        source_network: str
                        ip_wildcard: str
                        error_text: str or list
                        cancel: True, False
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': '', 'is_exists': '10.5.24.97'})] 如果存在则不添加
                [('edit', '10.5.24.97', {'source_network': '10.5.24.98'})]
          enable_telnet: True, False ex: enable_telnet=True
          telnet_listen_ip: Any, ex: telnet_listen_ip='Any'
          telnet_port: int ex: telnet_port=23
          telnet_remote_access: True, False ex: telnet_remote_access=True
          telnet_remote_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': ''})]
                    add parameters:
                        source_network: str
                        ip_wildcard: str
                        error_text: str or list
                        cancel: True, False
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': '', 'is_exists': '10.5.24.97'})] 如果存在则不添加
                [('edit', '10.5.24.97', {'source_network': '10.5.24.98'})]
          enable_ssh: True, False ex: enable_ssh=True
          ssh_listen_ip: Any, ex: ssh_listen_ip='Any'
          ssh_port: int ex: ssh_port=22
          ssh_timeout: int ex: ssh_timeout=300
          ssh_key_length: int ex: ssh_key_length=2048
          ssh_remote_access: True, False ex: ssh_remote_access=True
          ssh_remote_resource:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '10.5.24.97')]
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': ''})]
                    add parameters:
                        source_network: str
                        ip_wildcard: str
                        error_text: str or list
                        cancel: True, False
                [('add', {'source_network': '10.5.24.97', 'ip_wildcard': '', 'is_exists': '10.5.24.97'})] 如果存在则不添加
                [('edit', '10.5.24.97', {'source_network': '10.5.24.98'})]
          enable_developer: True, False ex: enable_developer=True
          enable_fixed_password: True, False ex: enable_fixed_password=True
          fixed_password: str ex: fixed_password='123456'
          submit: True, False ex: submit=True or submit={'tip_messages': 'submit_success'}
          text_messages: str or list
          tip_messages: str or list
        :return:
        """
        self.access_menu('system.access tools')
        self.agg_in(self.system_locators.access_tools_locators, kwargs)


class UserManagement(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置用户管理')
    def config(self, **kwargs):
        """

        :param kwargs:
          user:
                [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'middle')]
                [('add', {'username': 'test', 'permission', 15, 'password': '123456', 'confirm_password': '123456'})]
                    add parameters:
                        username: str
                        permission: 1-15
                        password:
                        confirm_password:
                        error_text: str or list
                        cancel: True, False
                [('add', {'username': 'test', 'permission': 15, 'is_exists': 'test'})] 如果存在则不添加
                [('edit', 'test', {'username': 'test1'})]
        :return:
        """
        self.access_menu('system.user management')
        self.agg_in(self.system_locators.user_management_locators, kwargs)


class Reboot(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置重启')
    def config(self, **kwargs):
        """

        :param kwargs:
                daily_reboot: True, False ex: daily_reboot=True
                hour: 00, 01, 23 ex: hour='00'
                min: 00, 01, 59 ex: min='00'
                reboot_now: True, False ex: reboot_now=True
                submit: True, False ex: submit=True or submit={'tip_messages': 'submit_success'}
        :return:
        """
        self.access_menu('system.reboot')
        if kwargs.get('reboot_now') and kwargs.get('reboot_confirm') is None:
            kwargs.update({'reboot_confirm': True})
        self.agg_in(self.system_locators.reboot_locators, kwargs)
        if kwargs.get('reboot_now') and kwargs.get('reboot_confirm'):
            self.login()


class NetworkTools(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('设备ping')
    def ping(self, lost_package=False, **kwargs):
        """ ping包操作

        :param lost_package: None, True, False 是否丢包
        :param kwargs:
               host: str ex: host='www.baidu.com'
               count: int ex: count=4
               size: int ex: size=32
               experts_option: str 高级选项
               ping: True, False ex: ping=True
               text_messages: str or list
        :return:
        """
        self.access_menu('system.network tools')
        if kwargs.get('ping') is None:
            kwargs.update({'ping': True})
        self.agg_in(self.system_locators.ping_locators, kwargs)
        if kwargs.get('ping'):
            for i in range(0, 30):
                result = self.wait_for_response(r'/v1/task/status\?type=ping')['results']
                if result['status'] == 'success':
                    self.agg_in(self.system_locators.ping_locators, {'close': True})
                    if lost_package:
                        assert '0% packet loss' not in result['data'], f'ping not exist lost package'
                    else:
                        assert '0% packet loss' in result['data'], f'ping exist lost package'
                    break

    @allure.step('设置路由探测')
    def trace_route(self, lost_package=False, **kwargs):
        """路由探测操作

        :param lost_package: True|False 是否校验丢包
        :param kwargs:
               host: 地址 IP
               max_hop: 最大跳数 2-40
               timeout: 超时时间 2-10s
               protocol: UDP|ICMP 协议
               experts_option:专家选项
               trace: True|False 是否点击Trace
               text_messages: str or list

        :return:
        """
        self.access_menu('system.network tools')
        if kwargs.get('trace') is None:
            kwargs.update({'trace': True})
        self.agg_in(self.system_locators.trace_locators, kwargs)
        if kwargs.get('trace'):
            for i in range(0, 60):
                result = self.wait_for_response(r'/v1/task/status\?type=traceroute')['results']
                if result['status'] == 'success':
                    self.agg_in(self.system_locators.ping_locators, {'close': True})
                    if lost_package:
                        assert not result['data'], f'trace route  exist package'
                    else:
                        assert result['data'], f'trace route exist not package'
                    break

    @allure.step('抓包')
    def tcp_dump(self, **kwargs):
        """抓包操作

        :param kwargs:
            interface: Any|Cellular 1|Gigabitethernet 0/1|Bridge 1 接口
            number:抓包个数 10-1000
            experts_option: 专家选项
            text_messages: str or list
            start_capture: True|False 是否点击开始抓包
            download: {'file_path': './', 'file_name': 'xxx.pcap'} 下载文件
        :return:
        """
        self.access_menu('system.network tools')
        if kwargs.get('start_capture') is None:
            kwargs.update({'start_capture': True})
        self.agg_in(self.system_locators.tcpdump_locators, kwargs)


class System:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.time: SystemTime = SystemTime(host, username, password, protocol, port, model, language, page,
                                                  locale)
        self.log: Log = Log(host, username, password, protocol, port, model, language, page, locale)
        self.config: Config = Config(host, username, password, protocol, port, model, language, page, locale)
        self.inhand_cloud: Cloud = Cloud(host, username, password, protocol, port, model, language, page, locale)
        self.firmware: Firmware = Firmware(host, username, password, protocol, port, model, language, page, locale)
        self.access_tools: AccessTools = AccessTools(host, username, password, protocol, port, model, language, page,
                                                     locale)
        self.user: UserManagement = UserManagement(host, username, password, protocol, port, model, language, page,
                                                   locale)
        self.reboot: Reboot = Reboot(host, username, password, protocol, port, model, language, page, locale)
        self.network_tools: NetworkTools = NetworkTools(host, username, password, protocol, port, model, language, page,
                                                        locale)
