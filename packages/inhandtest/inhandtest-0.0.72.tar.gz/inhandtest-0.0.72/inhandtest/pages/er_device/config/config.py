# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/19 13:47
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : config.py
@IDE     : PyCharm
------------------------------------
"""
import allure

from inhandtest.base_page import BasePage
from inhandtest.pages.er_device.config.config_locators import ConfigLocators


class Config(BasePage, ConfigLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, **kwargs):
        super().__init__(host, username, password, protocol, port, model, language, page, **kwargs)
        ConfigLocators.__init__(self, page, kwargs.get('locale'))

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


class EAP600Config():
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, **kwargs):
        self.__config = Config(host, username, password, protocol, port, model, language, page, **kwargs)

    def wan(self, **kwargs):
        """

        """
        return self.__config.config(**kwargs)



if __name__ == '__main__':
    a = EAP600Config()
    a.wan()