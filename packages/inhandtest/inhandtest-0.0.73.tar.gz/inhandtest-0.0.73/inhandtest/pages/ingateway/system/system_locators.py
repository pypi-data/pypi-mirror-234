# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 14:29:16
# @Author  : Pane Li
# @File    : system_locators.py
"""
system_locators

"""
from playwright.sync_api import Page


class SystemTimeLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')
        self.utc_key = (
            'utc-12', 'utc-11', 'utc-10', 'utc-9', 'utc-8', 'utc-7', 'utc-6', 'utc-6_atlantic', 'utc-5',
            'utc-5_colombia', 'utc-4', 'utc-4_atlantic', 'utc-4_brazil', 'utc-3_30', 'utc-3', 'utc-3_brazil',
            'utc-3_guyana', 'utc-2', 'utc-1', 'utc', 'utc_england,', 'utc+1', 'utc+1_france', 'utc+2', 'utc+2_greece',
            'utc+3', 'utc+3_finland', 'utc+4', 'utc+5', 'utc+5_30', 'utc+6', 'utc+7', 'utc+8', 'utc+9', 'utc+9_30',
            'utc+10', 'utc+11', 'utc+12', 'utc+12_zealand')

    @property
    def system_time_status_locators(self) -> list:
        return [
            ('local_time',
             {'locator': self.page.locator(f'//label[text()="{self.locale.local_time}"]').locator('../../div[2]'),
              'type': 'text'}),
            ('device_time',
             {'locator': self.page.locator(f'//label[text()="{self.locale.device_time}"]').locator(
                 '../../div[2]/div/span/div/span'), 'type': 'text'}),
        ]

    @property
    def system_time_locators(self) -> list:
        return [
            ('time_zone', {'locator': self.page.locator('.ant-select.ant-select-enabled').first, 'type': 'select',
                           'param': {utc: self.locale.get(utc) for utc in self.utc_key}}),
            ('time_zone_apply',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(0),
              'type': 'button'}),
            ('auto_daylight_saving_time',
             {'locator': self.page.locator('.ant-checkbox-input'), 'type': 'check'}),
            ('sync_time',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(1), 'type': 'button'}),
            ('date', {'locator': self.page.locator('#date'), 'type': 'fill_date'}),
            ('time_', {'locator': self.page.locator('.ant-time-picker'), 'type': 'fill_date'}),
            ('apply_time',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-round').nth(2), 'type': 'button'}),
            ('enable_sntp_clients', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('sntp_interval', {'locator': self.page.locator('#update_interval'), 'type': 'text',
                               'relation': [('enable_sntp_clients', True)]}),
            ('sntp_servers', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('port', {'locator': self.pop_up.locator('#port'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('enable_sntp_clients', True)]}),
            ('submit_sntp',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(0),
              'type': 'button'}),
            ('enable_ntp_server', {'locator': self.page.locator('#enable').nth(1), 'type': 'switch_button'}),
            ('pre_ntp_server', {'locator': self.page.locator('#master'), 'type': 'text',
                                'relation': [('enable_ntp_server', True)]}),
            ('source_interface', {'locator': self.page.locator('#source_interface'), 'type': 'select',
                                  'relation': [('enable_ntp_server', True)]}),
            ('source_ip', {'locator': self.page.locator('#source_ip'), 'type': 'select',
                           'relation': [('enable_ntp_server', True)]}),
            ('ntp_servers', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                'action_confirm': self.page.locator('.ant-popover-inner').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit_ntp',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]


class LogLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def log_locators(self) -> list:
        return [
            ('recent_lines',
             {'locator': self.page.locator('.ant-select-sm.ant-select.ant-select-enabled'), 'type': 'select',
              'param': {'all': self.locale.all_}}),
            ('refresh_policy', {'locator': self.page.locator('.ant-select.ant-select-enabled').nth(1), 'type': 'select',
                                'param': {'manual_refresh': self.locale.manual_refresh, 'sec': self.locale.sec,
                                          'min': self.locale.min}}),
            ('refresh', {'locator': self.page.locator('.ant-btn.ant-btn-sm'), 'type': 'button'}),
            (
                'clear_history_log',
                {'locator': self.page.locator('//button[@class="ant-btn"]').nth(0), 'type': 'button'}),
            ('clear_log', {'locator': self.page.locator('//button[@class="ant-btn"]').nth(1), 'type': 'button'}),
            ('download_log',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(2), 'type': 'download_file'}),
            ('download_history_log',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(3), 'type': 'download_file'}),
            ('download_diagnostic_data',
             {'locator': self.page.locator('//button[@class="ant-btn"]').nth(4), 'type': 'download_file'}),
            ('confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm'),
              'type': 'button'}),

        ]

    @property
    def log_config_locators(self) -> list:
        return [
            ('enable_remote_server', {'locator': self.page.locator('#log_to_remote_enable'), 'type': 'check'}),
            ('remote_server', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server_address', {'locator': self.pop_up.locator('#server_addr'), 'type': 'text'}),
                    ('port', {'locator': self.pop_up.locator('#server_port'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('enable_remote_server', True)]}),
            ('log_to_console', {'locator': self.page.locator('#log_to_console'), 'type': 'check'}),
            ('history_log_file_size',
             {'locator': self.page.locator('//input[@class="ant-input-number-input"]'), 'type': 'text'}),
            ('history_log_level',
             {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
              'param': {'emergency': self.locale.emergency, 'alarm': self.locale.alarm,
                        'serious': self.locale.serious, 'error': self.locale.error, 'warning': self.locale.warning,
                        'notice': self.locale.notice, 'information': self.locale.information,
                        'debug': self.locale.debug}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]


class ConfigLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def config_locators(self) -> list:
        return [
            ('auto_save', {'locator': self.page.locator('//button[@role="switch"]').nth(0), 'type': 'switch_button',
                           'wait_for': {'type': 'timeout', 'timeout': 1 * 1000, }}),
            ('encrypted', {'locator': self.page.locator('//button[@role="switch"]').nth(1), 'type': 'switch_button'}),

            ('startup_config_contain_private_key',
             {'locator': self.page.locator('.ant-checkbox-input').nth(0), 'type': 'check'}),
            ('startup_config_confirm',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button'}),
            ('export_startup_config',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]').nth(1),
              'type': 'download_file'}),

            ('running_config_contain_private_key',
             {'locator': self.page.locator('.ant-checkbox-input').nth(1), 'type': 'check'}),
            ('running_config_confirm',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button'}),
            ('export_running_config',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]').nth(2),
              'type': 'download_file'}),

            ('clear_all_data_restore',
             {'locator': self.page.locator('.ant-checkbox-input').nth(2), 'type': 'check'}),
            ('clear_all_data_confirm',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button'}),

            ('import_startup_config',
             {'locator': self.page.locator('//button[@class="ant-btn"]'), 'type': 'upload_file'}),
            ('import_config',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]').nth(0), 'type': 'button'}),
            ('reboot',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button'}),

            ('restore_factory_default', {'locator': self.page.locator('.ant-btn.ant-btn-danger'),
                                         'type': 'button'}),
            ('restore_factory_default_ok',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm'),
              'type': 'button'}),
        ]


class InhandCloudLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def platform_status_locators(self) -> list:
        return [
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'registering': self.locale.registering_, 'registered': self.locale.registered,
                                          'connecting': self.locale.connecting, 'connect': self.locale.connect}}),
        ]

    @property
    def platform_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('//button').nth(0), 'type': 'switch_button', }),
            ('server_address', {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
                                'param': {'custom': self.locale.custom}, 'relation': [('enable', True)]}),
            ('custom_address', {'locator': self.page.locator('//input[@class="ant-input"]').nth(0), 'type': 'text',
                                'relation': [('enable', True)]}),
            ('register_account', {'locator': self.page.locator('#register_account'), 'type': 'text',
                                  'relation': [('enable', True)]}),
            ('advance_settings', {'locator': self.locale.advanced_settings, 'type': 'expand',
                                  'relation': [('enable', True)]}),
            ('enable_secure_channel', {'locator': self.page.locator('#tls'), 'type': 'switch_button',
                                       'relation': [('enable', True), ('advance_settings', 'expand')]}),
            ('location', {'locator': self.page.locator('#location_type'), 'type': 'radio_select',
                          'relation': [('enable', True), ('advance_settings', 'expand')]}),
            ('lbs_upload_interval', {'locator': self.page.locator('#lbs_upload_interval'), 'type': 'text',
                                     'relation': [('enable', True), ('advance_settings', 'expand')]}),
            ('keepalive', {'locator': self.page.locator('#channel_keepalive'), 'type': 'text',
                           'relation': [('enable', True), ('advance_settings', 'expand')]}),
            ('data_upload_interval', {'locator': self.page.locator('#dataflow_upload_interval'), 'type': 'text',
                                      'relation': [('enable', True), ('advance_settings', 'expand')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]


class FirmwareLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def firmware_status_locators(self) -> list:
        return [
            ('version', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.current_version}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def firmware_locators(self) -> list:
        return [
            ('firmware',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-dashed"]'), 'type': 'upload_file'}),
            ('upgrade',
             {'locator': self.page.locator('.upload-demo-start'), 'type': 'button'}),
            ('confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm'),
              'type': 'button', 'wait_for': {'type': 'visible',
                                             'locator': self.page.locator('.ant-modal-content').locator(
                                                 '.ant-btn.ant-btn-primary'), 'timeout': 300 * 1000}}),
            ('cancel_reboot',
             {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
              'type': 'button'}),
            ('reboot',
             {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button', 'wait_for': {'type': 'timeout',
                                             'timeout': 100 * 1000}}),
        ]


class AccessToolLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def access_tools_status_locators(self) -> list:
        return [
            ('https_listen_ip', {'locator': self.page.locator('//div[@id="https.listen_ip_addr"]'), 'type': 'select'}),
            ('https_port', {'locator': self.page.locator('//input[@id="https.port"]'), 'type': 'fill'}),
            ('telnet_listen_ip',
             {'locator': self.page.locator('//div[@id="telnet.listen_ip_addr"]'), 'type': 'select'}),
            ('telnet_port', {'locator': self.page.locator('//input[@id="telnet.port"]'), 'type': 'fill'}),
            ('ssh_listen_ip',
             {'locator': self.page.locator('//div[@id="ssh.listen_ip_addr"]'), 'type': 'select'}),
            ('ssh_port', {'locator': self.page.locator('//input[@id="ssh.port"]'), 'type': 'fill'}),
            ('developer_password',
             {'locator': self.page.locator('//input[@id="devlopMode.debug_password"]'), 'type': 'fill'}),

        ]

    @property
    def access_tools_locators(self) -> list:
        return [
            ('https_listen_ip', {'locator': self.page.locator('//div[@id="https.listen_ip_addr"]'), 'type': 'select'}),
            ('https_port', {'locator': self.page.locator('//input[@id="https.port"]'), 'type': 'text'}),
            ('web_login_timeout', {'locator': self.page.locator('//input[@id="web_login_timeout"]'), 'type': 'text'}),
            ('https_remote_access',
             {'locator': self.page.locator('//button[@id="https.remote_access"]'), 'type': 'switch_button'}),
            ('https_remote_resource', {'locator': {
                "locator": self.page.locator('//label[@for="https.enable.form"]').locator('../../..').locator(
                    '.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('source_network',
                     {'locator': self.pop_up.locator('#source_network'), 'type': 'text'}),
                    ('ip_wildcard',
                     {'locator': self.pop_up.locator('#wildcard_mask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('https_remote_access', 'enable')]}),

            ('enable_telnet',
             {'locator': self.page.locator('//button[@id="telnet.enable"]'), 'type': 'switch_button'}),
            ('telnet_listen_ip',
             {'locator': self.page.locator('//div[@id="telnet.listen_ip_addr"]'), 'type': 'select',
              'relation': [('enable_telnet', 'enable')]}),
            ('telnet_port', {'locator': self.page.locator('//input[@id="telnet.port"]'), 'type': 'text',
                             'relation': [('enable_telnet', 'enable')]}),
            ('telnet_remote_access',
             {'locator': self.page.locator('//button[@id="telnet.remote_access"]'), 'type': 'switch_button',
              'relation': [('enable_telnet', 'enable')]}),
            ('telnet_remote_resource', {'locator': {
                "locator": self.page.locator('//label[@for="telnet.enable.form"]').locator('../../..').locator(
                    '.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('source_network',
                     {'locator': self.pop_up.locator('#source_network'), 'type': 'text'}),
                    ('ip_wildcard',
                     {'locator': self.pop_up.locator('#wildcard_mask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr',
                'relation': [('telnet_remote_access', 'enable')]}),

            ('enable_ssh',
             {'locator': self.page.locator('//button[@id="ssh.enable"]'), 'type': 'switch_button'}),
            ('ssh_listen_ip',
             {'locator': self.page.locator('//div[@id="ssh.listen_ip_addr"]'), 'type': 'select',
              'relation': [('enable_ssh', 'enable')]}),
            ('ssh_port', {'locator': self.page.locator('//input[@id="ssh.port"]'), 'type': 'text',
                          'relation': [('enable_ssh', 'enable')]}),
            ('ssh_timeout', {'locator': self.page.locator('//input[@id="ssh.timeout"]'), 'type': 'text',
                             'relation': [('enable_ssh', 'enable')]}),
            ('ssh_key_length', {'locator': self.page.locator('//input[@id="ssh.key_length"]'), 'type': 'select',
                                'relation': [('enable_ssh', 'enable')]}),
            ('ssh_remote_access',
             {'locator': self.page.locator('//button[@id="ssh.remote_access"]'), 'type': 'switch_button',
              'relation': [('enable_ssh', 'enable')]}),
            ('ssh_remote_resource', {'locator': {
                "locator": self.page.locator('//label[@for="ssh.enable.form"]').locator('../../..').locator(
                    '.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('source_network',
                     {'locator': self.pop_up.locator('#source_network'), 'type': 'text'}),
                    ('ip_wildcard',
                     {'locator': self.pop_up.locator('#wildcard_mask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr',
                'relation': [('ssh_remote_access', 'enable')]}),

            ('enable_developer',
             {'locator': self.page.locator('//button[@id="devlopMode.debug_enable"]'), 'type': 'switch_button'}),
            ('enable_fixed_password',
             {'locator': self.page.locator('//button[@id="devlopMode.fixed_passwd"]'), 'type': 'switch_button',
              'relation': [('enable_developer', 'enable')]}),
            (
                'fixed_password',
                {'locator': self.page.locator('//input[@id="devlopMode.debug_password"]'), 'type': 'text',
                 'relation': [('enable_developer', 'enable'), ('enable_fixed_password', 'enable')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
        ]


class UserLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def user_management_locators(self) -> list:
        return [
            ('user', {'locator': {
                "locator": self.page.locator('.antd-pro-pages-gateway-system-user-management-index-outerBox'),
                "action_confirm": self.page.locator('.ant-popover-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                "columns": [
                    ('username',
                     {'locator': self.pop_up.locator('#username'), 'type': 'text'}),
                    ('permission', {'locator': self.pop_up.locator('#privilege'), 'type': 'select'}),
                    ('password', {'locator': self.pop_up.locator('#password'), 'type': 'text'}),
                    ('confirm_password', {'locator': self.pop_up.locator('#passwordConfirm'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
        ]


class RebootLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def reboot_locators(self) -> list:
        return [
            ('daily_reboot', {'locator': self.page.locator('//button[@role="switch"]'), 'type': 'switch_button'}),
            ('hour', {'locator': self.page.locator('.ant-select.ant-select-enabled').nth(0), 'type': 'select',
                      'relation': [('daily_reboot', 'enable')]}),
            ('min', {'locator': self.page.locator('.ant-select.ant-select-enabled').nth(1), 'type': 'select',
                     'relation': [('daily_reboot', 'enable')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit), 'type': 'button'}),
            ('reboot_now', {'locator': self.page.locator('.ant-btn.ant-btn-danger'), 'type': 'button'}),
            ('reboot_confirm',
             {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button',
              'wait_for': {'type': 'timeout', 'timeout': 100 * 1000}}),
        ]


class NetworkToolsLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def ping_locators(self) -> list:
        return [
            ('host', {'locator': self.page.locator('#host').nth(0), 'type': 'text'}),
            ('count', {'locator': self.page.locator('#ping_count').nth(0), 'type': 'text'}),
            ('size', {'locator': self.page.locator('#packet_size').nth(0), 'type': 'text'}),
            ('expert_options', {'locator': self.page.locator('#expert_options').nth(0), 'type': 'text'}),
            ('text_messages', {'type': 'text_messages'}),
            ('ping', {'locator': self.page.locator('//button[@type="submit"]').nth(0), 'type': 'button'}),
            ('close',
             {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn ant-btn-primary"]'),
              'type': 'button'}),
        ]

    @property
    def trace_locators(self) -> list:
        return [
            ('host', {'locator': self.page.locator('#host').nth(1), 'type': 'text'}),
            ('max_hop', {'locator': self.page.locator('#maximum_hops').nth(0), 'type': 'text'}),
            ('timeout', {'locator': self.page.locator('#timeout').nth(0), 'type': 'text'}),
            ('protocol', {'locator': self.page.locator('#transmit_protocol').nth(0), 'type': 'select'}),
            ('expert_options', {'locator': self.page.locator('#expert_options').nth(1), 'type': 'text'}),
            ('text_messages', {'type': 'text_messages'}),
            ('trace', {'locator': self.page.locator('//button[@type="submit"]').nth(1), 'type': 'button'}),
            ('close',
             {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn ant-btn-primary"]'),
              'type': 'button'}),
        ]

    @property
    def tcpdump_locators(self) -> list:
        return [
            ('interface', {'locator': self.page.locator('#interface'), 'type': 'select'}),
            ('number', {'locator': self.page.locator('#capture_number'), 'type': 'text'}),
            ('expert_options', {'locator': self.page.locator('#expert_options').nth(2), 'type': 'text'}),
            ('text_messages', {'type': 'text_messages'}),
            ('start_capture',
             {'locator': self.page.locator('//button', has_text=self.locale.start_capture), 'type': 'button',
              'wait_for': [{'type': 'visible', 'timeout': 300 * 1000,
                           'locator': self.page.locator('//button', has_text=self.locale.start_capture)},
                           {'type': 'timeout', 'timeout': 1 * 1000}]}),
            ('download',
             {'locator': self.page.locator('//button', has_text=self.locale.download_capture_file),
              'type': 'download_file', }),

        ]


class SystemLocators(SystemTimeLocators, LogLocators, ConfigLocators, InhandCloudLocators, FirmwareLocators,
                     AccessToolLocators, UserLocators, RebootLocators, NetworkToolsLocators):
    pass
