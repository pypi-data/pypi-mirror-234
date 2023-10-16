# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 13:13:22
# @Author  : Pane Li
# @File    : network_locators.py
"""
network_locators

"""
from playwright.sync_api import Page


class CellularLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def cellular_status_locators(self) -> list:
        return [
            ('active_sim', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.active_sim}"]]/div[2]'),
                'type': 'text', 'param': {'sim': 'SIM'}}),
            ('imei', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.imei_code}"]]/div[2]'),
                'type': 'text'}),
            ('imsi', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.imsi_code}"]]/div[2]'),
                'type': 'text'}),
            ('iccid', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.iccid_code}"]]/div[2]'),
                'type': 'text'}),
            ('register_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.register_status}"]]/div[2]'),
                'type': 'text',
                'param': {'not_register': self.locale.not_register, 'registering': self.locale.registering,
                          'disconnected': self.locale.disconnect, 'connected': self.locale.connect}}),
            ('operator', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.operator}"]]/div[2]'),
                'type': 'text'}),
            ('network_type', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.network_type}"]]/div[2]'),
                'type': 'text'}),
            ('lac', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.lac}"]]/div[2]'),
                'type': 'text'}),
            ('cell_id', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.cell_id}"]]/div[2]'),
                'type': 'text'}),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text',
                'param': {'not_register': self.locale.not_register, 'registering': self.locale.registering,
                          'disconnected': self.locale.disconnect, 'connected': self.locale.connect}}),
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('gateway', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gateway}"]]/div[2]'),
                'type': 'text'}),
            ('dns', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.dns}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text'}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def cellular_locators(self) -> list:
        return [
            ('cellular_enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('profile', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('network_type', {'locator': self.pop_up.locator('#network_type'), 'type': 'select'}),
                    ('apn', {'locator': self.pop_up.locator('#apn'), 'type': 'text'}),
                    ('access_number', {'locator': self.pop_up.locator('#access_number'), 'type': 'text'}),
                    ('auth_method', {'locator': self.pop_up.locator('#auth_method'), 'type': 'select',
                                     'param': {'auto': self.locale.auto}}),
                    ('username', {'locator': self.pop_up.locator('#username'), 'type': 'text'}),
                    ('password', {'locator': self.pop_up.locator('#password'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('cellular_enable', 'enable')]}),
            ('dual_sim_enable', {'locator': self.page.locator('#enable_dual_sim'), 'type': 'switch_button',
                                 'relation': [('cellular_enable', 'enable')]}),
            ('main_sim', {'locator': self.page.locator('#main_sim'), 'type': 'select',
                          'param': {'Random': self.locale.random, 'Sequence': self.locale.sequence},
                          'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('max_number_of_dial', {'locator': self.page.locator('#max_dial_times'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('min_connected_time', {'locator': self.page.locator('#min_dial_times'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('backup_sim_timeout', {'locator': self.page.locator('#backup_sim_timeout'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('dual_sim_enable', 'enable')]}),
            ('network_type', {'locator': self.page.locator('#network_type').first, 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim1_profile', {'locator': self.page.locator('#sim1_profile'), 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim1_roaming', {'locator': self.page.locator('#sim1_roaming'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim1_pincode', {'locator': self.page.locator('#sim1_pincode'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_threshold', {'locator': self.page.locator('#sim1_csq_threshold'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_detect_interval', {'locator': self.page.locator('#sim1_csq_detect_interval'), 'type': 'text',
                                          'relation': [('cellular_enable', 'enable')]}),
            ('sim1_csq_detect_retries', {'locator': self.page.locator('#sim1_csq_detect_retries'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable')]}),
            ('sim2_profile', {'locator': self.page.locator('#sim2_profile'), 'type': 'select',
                              'param': {'auto': self.locale.auto}, 'relation': [('cellular_enable', 'enable')]}),
            ('sim2_roaming', {'locator': self.page.locator('#sim2_roaming'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim2_pincode', {'locator': self.page.locator('#sim2_pincode'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_threshold', {'locator': self.page.locator('#sim2_csq_threshold'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_detect_interval', {'locator': self.page.locator('#sim2_csq_detect_interval'), 'type': 'text',
                                          'relation': [('cellular_enable', 'enable')]}),
            ('sim2_csq_detect_retries', {'locator': self.page.locator('#sim2_csq_detect_retries'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable')]}),
            ('static_ip_enable', {'locator': self.page.locator('#static_ip'), 'type': 'switch_button',
                                  'relation': [('cellular_enable', 'enable')]}),
            ('static_ip', {'locator': self.page.locator('#ip_addr'), 'type': 'text',
                           'relation': [('cellular_enable', 'enable'), ('static_ip_enable', 'enable')]}),
            ('static_peer', {'locator': self.page.locator('#peer_addr'), 'type': 'text',
                             'relation': [('cellular_enable', 'enable'), ('static_ip_enable', 'enable')]}),
            ('radial_interval', {'locator': self.page.locator('#peer_addr'), 'type': 'text',
                                 'relation': [('cellular_enable', 'enable')]}),
            ('icmp_probes', {'locator': self.locale.icmp_probes,
                             'type': 'expand', 'relation': [('cellular_enable', 'enable')]}),
            ('icmp_detection_server1', {'locator': self.page.locator('#icmp.dest_addr1'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_server2', {'locator': self.page.locator('#icmp.dest_addr2'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_interval', {'locator': self.page.locator('#icmp.interval'), 'type': 'text',
                                         'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_max_retries', {'locator': self.page.locator('#icmp.retires'), 'type': 'text',
                                            'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_timeout', {'locator': self.page.locator('#icmp.timeout'), 'type': 'text',
                                        'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('icmp_detection_strict', {'locator': self.page.locator('#icmp.strict'), 'type': 'switch_button',
                                       'relation': [('cellular_enable', 'enable'), ('icmp_probes', 'expand')]}),
            ('advanced_settings', {'locator': self.locale.advanced_settings,
                                   'type': 'expand', 'relation': [('cellular_enable', 'enable')]}),
            ('init_command', {'locator': self.page.locator('#init_command'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('mru', {'locator': self.page.locator('#mru'), 'type': 'text',
                     'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('rssi_poll_interval', {'locator': self.page.locator('#rssi_poll_interval'), 'type': 'text',
                                    'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('mtu', {'locator': self.page.locator('#mtu'), 'type': 'text',
                     'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('dial_timeout', {'locator': self.page.locator('#dial_timeout'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('use_default_asyncmap', {'locator': self.page.locator('#use_default_asyncmap'), 'type': 'switch_button',
                                      'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('use_peer_dns', {'locator': self.page.locator('#use_peer_dns'), 'type': 'switch_button',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('lcp_interval', {'locator': self.page.locator('#lcp_interval'), 'type': 'text',
                              'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('lcp_max_retries', {'locator': self.page.locator('#lcp_max_retries'), 'type': 'text',
                                 'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('infinitely_dial_retry', {'locator': self.page.locator('#infinitely_dial_retry'), 'type': 'switch_button',
                                       'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('debug', {'locator': self.page.locator('#debug'), 'type': 'switch_button',
                       'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('expert_options', {'locator': self.page.locator('#expert_options'), 'type': 'text',
                                'relation': [('cellular_enable', 'enable'), ('advanced_settings', 'expand')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('confirm',
             {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn ant-btn-primary"]'),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class EthernetLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def ethernet_status_locators(self) -> list:
        return [
            ('network_type', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.network_type}"]]/div[2]'),
                'type': 'text', 'param': {'static_ip': self.locale.static_ip,
                                          'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('gateway', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gateway}"]]/div[2]'),
                'type': 'text'}),
            ('dns', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.dns}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text'}),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def ethernet_locators(self) -> list:
        return [
            ('network_type', {'locator': self.page.locator('#internet'), 'type': 'select',
                              'param': {'static_ip': self.locale.static_ip,
                                        'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('speed_duplex', {'locator': self.page.locator('#speed_duplex'), 'type': 'select',
                              'param': {'auto_negotiation': self.locale.auto_negotiation, 'full': self.locale.full,
                                        'half': self.locale.half, 'duplex': self.locale.duplex, 'm': 'M'}}),
            ('mtu', {'locator': self.page.locator('#mtu'), 'type': 'text'}),
            ('track_l2_state', {'locator': self.page.locator('#track_l2_state'), 'type': 'switch_button'}),
            ('shutdown', {'locator': self.page.locator('#shutdown'), 'type': 'switch_button'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.pop_up.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.pop_up.locator('#netmask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class BridgeLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def bridge_status_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text'}),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def bridge_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.pop_up.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask', {'locator': self.pop_up.locator('#netmask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('ge_01', {'locator': self.page.locator('//button[@id="gigabitethernet 0/1"]'), 'type': 'switch_button'}),
            ('ge_02', {'locator': self.page.locator('//button[@id="gigabitethernet 0/2"]'), 'type': 'switch_button'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class WlanLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def wlan_status_locators(self) -> list:
        return [
            ('station_role', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.station_role}"]]/div[2]'),
                'type': 'text', 'param': {'ap': self.locale.ap, 'client': self.locale.client}}),
            ('wlan_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.wlan_status}"]]/div[2]'),
                'type': 'text', 'param': {'enable': self.locale.enable, 'disable': self.locale.disable}}),
            ('mac_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mac_address}"]]/div[2]'),
                'type': 'text'}),
            ('ssid', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="SSID"]]/div[2]'),
                'type': 'text'}),
            ('channel', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.channel}"]]/div[2]'),
                'type': 'text'}),
            ('auth_method', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.auth_method}"]]/div[2]'),
                'type': 'text', 'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()}}),
            ('encrypt_mode', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.encrypt_mode}"]]/div[2]'),
                'type': 'text'}),
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('gateway', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gateway}"]]/div[2]'),
                'type': 'text'}),
            ('dns', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="DNS"]]/div[2]'),
                'type': 'text'}),
            ('wireless_connection_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.wireless_connection_status}"]]/div[2]'),
                'type': 'text', 'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect}}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),

        ]

    @property
    def wlan_locators(self) -> list:
        return [
            ('enable_wifi', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('station_role', {'locator': self.page.locator('#station_role'), 'type': 'radio_select',
                              'param': {'ap': self.locale.ap, 'client': self.locale.client},
                              'relation': [('enable_wifi', 'enable')]}),
            ('sta_default_route', {'locator': self.page.locator('#sta_default_route'), 'type': 'switch_button',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_ssid', {'locator': self.page.locator('#sta_ssid'), 'type': 'text',
                          'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_scan', {'locator': self.page.locator(f'//button[@type="button"]/span[text()="{self.locale.scan}"]'),
                          'type': 'button', 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_connect',
             {'locator': {"locator": self.page.locator('.antd-pro-components-in-gateway-network-profile-outerBox'),
                          }, 'type': 'table_tr', 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_auth_method', {'locator': self.page.locator('#sta_auth_method'), 'type': 'select',
                                 'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()},
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_encrypt_mode', {'locator': self.page.locator('#sta_encrypt_mode'), 'type': 'select',
                                  'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_wep_key', {'locator': self.page.locator('#sta_wep_key'), 'type': 'text',
                             'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_wpa_psk_key', {'locator': self.page.locator('#sta_wpa_psk_key'), 'type': 'text',
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_auth_mode', {'locator': self.page.locator('#sta_auth_mode'), 'type': 'radio_select',
                               'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_inner_auth', {'locator': self.page.locator('#sta_inner_auth'), 'type': 'radio_select',
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_username', {'locator': self.page.locator('#sta_username'), 'type': 'text',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_password', {'locator': self.page.locator('#sta_password'), 'type': 'text',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_network_type', {'locator': self.page.locator('#sta_dhcp'), 'type': 'radio_select',
                                  'param': {'static_ip': self.locale.static_ip,
                                            'dynamic_address_dhcp': self.locale.dynamic_address_dhcp},
                                  'relation': [('enable_wifi', 'enable'), ('station_role', 'client')]}),
            ('sta_ip_address', {'locator': self.page.locator('#ip_addr'), 'type': 'text'}),
            ('sta_netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('ap_ssid_broadcast', {'locator': self.page.locator('#ap_ssid_broadcast'), 'type': 'switch_button',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_bridge', {'locator': self.page.locator('#ap_briage'), 'type': 'switch_button',
                           'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_band', {'locator': self.page.locator('#ap_band'), 'type': 'select',
                         'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_radio_type', {'locator': self.page.locator('#ap_radio_type'), 'type': 'select',
                               'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_channel', {'locator': self.page.locator('#ap_channel'), 'type': 'select',
                            'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_ssid', {'locator': self.page.locator('#ap_ssid'), 'type': 'text',
                         'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_auth_method', {'locator': self.page.locator('#auth_method'), 'type': 'select',
                                'param': {'OPEN': self.locale.open.upper(), 'SHARED': self.locale.shared.upper()},
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_encrypt_mode', {'locator': self.page.locator('#encrypt_mode'), 'type': 'select',
                                 'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_wep_key', {'locator': self.page.locator('#wep_key'), 'type': 'text',
                            'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_wpa_psk_key', {'locator': self.page.locator('#wpa_psk_key'), 'type': 'text',
                                'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_bandwidth', {'locator': self.page.locator('#ap_bandwidth'), 'type': 'select',
                              'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('ap_stations_limit', {'locator': self.page.locator('#ap_max_associations'), 'type': 'text',
                                   'relation': [('enable_wifi', 'enable'), ('station_role', 'ap')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'text_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class WanLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def wan_status_locators(self) -> list:
        return [
            ('network_type', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.network_type}"]]/div[2]'),
                'type': 'text', 'param': {'static_ip': self.locale.static_ip,
                                          'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('gateway', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gateway}"]]/div[2]'),
                'type': 'text'}),
            ('dns', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="DNS"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text', }),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
        ]

    @property
    def wan_locators(self) -> list:
        return [
            ('interface_type', {'locator': self.page.locator('#internetType'), 'type': 'radio_select'}),
            ('network_type', {'locator': self.page.locator('#internet'), 'type': 'select',
                              'param': {'static_ip': self.locale.static_ip,
                                        'dynamic_address_dhcp': self.locale.dynamic_address_dhcp}}),
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('gateway', {'locator': self.page.locator('#gateway'), 'type': 'text'}),
            ('dns', {'locator': self.page.locator('#primary_dns'), 'type': 'text'}),
            ('mtu', {'locator': self.page.locator('#mtu'), 'type': 'text'}),
            ('track_l2_state', {'locator': self.page.locator('#track_l2_state'), 'type': 'switch_button'}),
            ('shutdown', {'locator': self.page.locator('#shutdown'), 'type': 'switch_button'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.page.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.page.locator('.ant-modal-content').locator('#netmask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class LanLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def lan_status_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
            ('mtu', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.mtu}"]]/div[2]'),
                'type': 'text', }),
            ('status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.status}"]]/div[2]'),
                'type': 'text', 'param': {'up': 'Up', 'down': 'Down'}}),
            ('description', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.description}"]]/div[2]'),
                'type': 'text'}),
            ('connection_time', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.connection_time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
        ]

    @property
    def lan_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator('#primary_ip'), 'type': 'text'}),
            ('netmask', {'locator': self.page.locator('#netmask'), 'type': 'text'}),
            ('description', {'locator': self.page.locator('#description'), 'type': 'text'}),
            ('shutdown', {'locator': self.page.locator('#shutdown'), 'type': 'switch_button'}),
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.page.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.page.locator('.ant-modal-content').locator('#netmask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class LoopbackLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def loopback_status_locators(self) -> list:
        return [
            ('ip_address', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.ip_address}"]]/div[2]'),
                'type': 'text'}),
            ('netmask', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.netmask}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def loopback_locators(self) -> list:
        return [
            ('secondary_ip_settings', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('secondary_ip', {'locator': self.page.locator('#secondary_ip'), 'type': 'text'}),
                    ('netmask',
                     {'locator': self.page.locator('.ant-modal-content').locator('#netmask'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class DhcpLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def dhcp_locators(self) -> list:
        return [
            ('dhcp_server', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(0),
                "columns": [
                    ('enable_dhcp_server',
                     {'locator': self.page.locator('.ant-modal-content').locator('#enable'), 'type': 'switch_button'}),
                    ('interface',
                     {'locator': self.page.locator('.ant-modal-content').locator('#interface'), 'type': 'select'}),
                    ('start_address',
                     {'locator': self.page.locator('.ant-modal-content').locator('#start_addr'), 'type': 'text'}),
                    ('end_address',
                     {'locator': self.page.locator('.ant-modal-content').locator('#end_addr'), 'type': 'text'}),
                    ('lease',
                     {'locator': self.page.locator('.ant-modal-content').locator('#lease'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('windows_name_server', {'locator': self.page.locator('#windows_name_server'), 'type': 'text'}),
            ('static_ip_setting', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(1),
                "columns": [
                    ('mac_address', {'locator': self.pop_up.locator('#mac_addr'), 'type': 'text'}),
                    ('ip_address', {'locator': self.pop_up.locator('#ip_addr'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr', 'param': {'enable': self.locale.enable, 'not_enable': self.locale.not_enable}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class DnsLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def dns_locators(self) -> list:
        return [
            ('primary_dns', {'locator': self.page.locator('#primary_dns'), 'type': 'text'}),
            ('secondary_dns', {'locator': self.page.locator('#secondary_dns'), 'type': 'text'}),
            ('submit_dns_server',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(0),
              'type': 'button'}),
            ('enable_dns_relay', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('domain_ip_address_pair', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('host',
                     {'locator': self.pop_up.locator('#host'), 'type': 'text'}),
                    ('ip_address1', {'locator': self.pop_up.locator('#ip_addr1'), 'type': 'text'}),
                    ('ip_address2', {'locator': self.pop_up.locator('#ip_addr2'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit_domain_ip_address_pair',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class GpsLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def gps_status_locators(self) -> list:
        return [
            ('gps_status', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.gps_status}"]]/div[2]'),
                'type': 'text', 'param': {'enable': self.locale.enable, 'disable': self.locale.disable}}),
            ('time_', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.time}"]]/div[2]'),
                'type': 'text', 'param': {'day': self.locale.day}}),
            ('location', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.location}"]]/div[2]'),
                'type': 'text'}),
            ('speed', {'locator': self.page.locator(
                f'//div[./div[@class="antd-pro-components-description-list-index-term"][text()="{self.locale.speed}"]]/div[2]'),
                'type': 'text'}),
        ]

    @property
    def gps_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator(f'//button'), 'type': 'switch_button'})
        ]

    @property
    def gps_ip_forwarding_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator(f'#enable'), 'type': 'switch_button'}),
            ('type_', {'locator': self.page.locator('#type'), 'type': 'select',
                       'param': {'client': self.locale.client, 'server': self.locale.server},
                       'relation': [('enable', True)]}),
            ('transmit_protocol', {'locator': self.page.locator('#client_transmit_proto'), 'type': 'select',
                                   'relation': [('enable', True)]}),
            ('connection_type', {'locator': self.page.locator('#connect_type'), 'type': 'select',
                                 'param': {'long_lived': self.locale.long_lived,
                                           'short_lived': self.locale.short_lived},
                                 'relation': [('enable', True)]}),
            ('keepalive_interval',
             {'locator': self.page.locator('#keepalive_interval'), 'type': 'text', 'relation': [('enable', True)]}),
            ('keepalive_retry',
             {'locator': self.page.locator('#keepalive_retry'), 'type': 'text', 'relation': [('enable', True)]}),
            ('idle_timeout',
             {'locator': self.page.locator('#idle_time'), 'type': 'text', 'relation': [('enable', True)]}),
            ('local_port',
             {'locator': self.page.locator('#server_local_port'), 'type': 'text', 'relation': [('enable', True)]}),
            ('min_reconnect_interval',
             {'locator': self.page.locator('#client_min_reconnect_interval'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('max_reconnect_interval',
             {'locator': self.page.locator('#client_max_reconnect_interval'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('source_interface', {'locator': self.page.locator('#client_source_interface'), 'type': 'select',
                                  'relation': [('enable', True)]}),
            ('reporting_interval', {'locator': self.page.locator('#trap_interval'), 'type': 'text',
                                    'relation': [('enable', True)]}),
            ('include_rmc', {'locator': self.page.locator('#rmc'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsa', {'locator': self.page.locator('#gsa'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gga', {'locator': self.page.locator('#gga'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsv', {'locator': self.page.locator('#gsv'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('message_prefix', {'locator': self.page.locator('#prefix'), 'type': 'text',
                                'relation': [('enable', True)]}),
            ('message_suffix', {'locator': self.page.locator('#suffix'), 'type': 'text',
                                'relation': [('enable', True)]}),
            ('destination_ip_address', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                "columns": [
                    ('server',
                     {'locator': self.page.locator('.ant-modal-content').locator('#server_ip'), 'type': 'text'}),
                    ('port',
                     {'locator': self.page.locator('.ant-modal-content').locator('#server_port'), 'type': 'text'}),
                    ('save',
                     {'locator': self.page.locator('.ant-modal-content').locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel',
                     {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                      'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]

    @property
    def gps_serial_forwarding_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('serial_type',
             {'locator': self.page.locator('#serial_type'), 'type': 'select', 'relation': [('enable', True)]}),
            ('baudrate',
             {'locator': self.page.locator('#baudrate'), 'type': 'select', 'relation': [('enable', True)]}),
            ('data_bits',
             {'locator': self.page.locator('#data_bits'), 'type': 'select', 'relation': [('enable', True)]}),
            ('parity',
             {'locator': self.page.locator('#parity'), 'type': 'select', 'relation': [('enable', True)],
              'param': {'none': self.locale.none, 'even': self.locale.even, 'odd': self.locale.odd}}),
            ('stop_bit',
             {'locator': self.page.locator('#stop_bit'), 'type': 'select', 'relation': [('enable', True)]}),
            ('software_flow_control',
             {'locator': self.page.locator('#soft_flow_control'), 'type': 'switch_button',
              'relation': [('enable', True)]}),
            ('include_rmc', {'locator': self.page.locator('#rmc'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsa', {'locator': self.page.locator('#gsa'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gga', {'locator': self.page.locator('#gga'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('include_gsv', {'locator': self.page.locator('#gsv'), 'type': 'switch_button',
                             'relation': [('enable', True)]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class HostListLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def hostlist_status_locators(self) -> dict:
        return {"locator": self.page.locator('.ant-table-scroll-position-left')}


class RoutingStatusLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def routing_locators(self) -> list:
        return [
            ('routing_type', {'locator': self.page.locator('.ant-select.ant-select-enabled'), 'type': 'select',
                              'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                                        'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                                        'rip': 'RIP'}}),
        ]

    @property
    def routing_table_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-scroll-position-left'),
            'type': 'table_tr',
            'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                      'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                      'rip': 'RIP'}}


class StaticRoutingLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale

    @property
    def static_routing_locators(self) -> list:
        return [
            ('routing',
             {'locator': {'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                          "columns": [
                              ('destination', {'locator': self.page.locator('#destination'), 'type': 'text'}),
                              ('netmask',
                               {'locator': self.page.locator('.ant-modal-content').locator('#netmask'),
                                'type': 'text'}),
                              ('interface',
                               {'locator': self.page.locator('.ant-modal-content').locator('#interface'),
                                'type': 'select'}),
                              ('gateway',
                               {'locator': self.page.locator('.ant-modal-content').locator('#gateway'),
                                'type': 'text'}),
                              ('distance',
                               {'locator': self.page.locator('.ant-modal-content').locator('#distance'),
                                'type': 'text'}),
                              ('track_id',
                               {'locator': self.page.locator('.ant-modal-content').locator('#track'), 'type': 'text'}),
                              ('save',
                               {'locator': self.page.locator('.ant-modal-content').locator(
                                   '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                              ('text_messages', {'type': 'text_messages'}),
                              ('tip_messages', {'type': 'tip_messages'}),
                              ('cancel',
                               {'locator': self.page.locator('.ant-modal-content').locator(
                                   '//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                          ]},
              'param': {'all': self.locale.all, 'connected_routing': self.locale.connected_routing,
                        'static_routing': self.locale.static_routing, 'ospf': 'OSPF', 'bgp': 'BGP',
                        'rip': 'RIP'}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class AclLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def acl_locators(self) -> list:
        common = self.pop_up.locator('.ant-select.ant-select-enabled')
        return [
            ('default_filter_strategy',
             {'locator': self.page.locator('#default_policy'), 'type': 'radio_select',
              'param': {'permit': self.locale.permit, 'deny': self.locale.deny}}),
            ('access_control_strategy',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox'),
                 "columns": [
                     ('acl_type', {'locator': self.pop_up.locator('#acl_type'), 'type': 'radio_select',
                                   'param': {'standard': self.locale.standard, 'extended': self.locale.extended}}),
                     ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                     ('sequence_number', {'locator': self.pop_up.locator('#sequence_number'), 'type': 'text'}),
                     ('action', {'locator': self.pop_up.locator('#action'), 'type': 'radio_select',
                                 'param': {'permit': self.locale.permit, 'deny': self.locale.deny}}),
                     ('protocol', {'locator': common.nth(0), 'type': 'select'}),
                     ('protocol_id', {'locator': common.nth(0).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('source_ip', {'locator': self.pop_up.locator('//input[@id="acl_source.ip"]'), 'type': 'text'}),
                     ('source_wildcard',
                      {'locator': self.pop_up.locator('//input[@id="acl_source.wildcard_mask"]'), 'type': 'text'}),
                     ('source_port', {'locator': common.nth(1), 'type': 'select'}),
                     ('source_port_value', {'locator': common.nth(1).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('source_port_value1', {'locator': common.nth(1).locator('../div[3]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('destination_ip',
                      {'locator': self.pop_up.locator('//input[@id="acl_destination.ip"]'), 'type': 'text'}),
                     ('destination_wildcard',
                      {'locator': self.pop_up.locator('//input[@id="acl_destination.wildcard_mask"]'),
                       'type': 'text'}),
                     ('destination_port', {'locator': common.nth(2), 'type': 'select'}),
                     ('destination_port_value', {'locator': common.nth(2).locator('../div[2]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('destination_port_value1', {'locator': common.nth(2).locator('../div[3]').locator(
                         '//input[@role="spinbutton"]'), 'type': 'text'}),
                     ('icmp_type', {'locator': self.page.locator('#icmp_type'), 'type': 'radio_select',
                                    'param': {'used_describe': self.locale.used_describe,
                                              'use_type_code': self.locale.use_type_code}}),
                     ('icmp_describe', {'locator': self.page.locator('#icmp_describe_value'), 'type': 'select'}),
                     ('icmp_type_value', {'locator': self.page.locator('#icmp_code_value'), 'type': 'text'}),
                     ('icmp_code', {'locator': self.page.locator('#icmp_type_value'), 'type': 'text'}),
                     ('fragments', {'locator': self.page.locator('.ant-modal-content').locator('#fragments'),
                                    'type': 'switch_button'}),
                     ('established', {'locator': self.page.locator('.ant-modal-content').locator('#established'),
                                      'type': 'switch_button'}),
                     ('log', {'locator': self.page.locator('.ant-modal-content').locator('#log'),
                              'type': 'switch_button'}),
                     ('description', {'locator': self.page.locator('.ant-modal-content').locator('#description'),
                                      'type': 'text'}),
                     ('save',
                      {'locator': self.page.locator('.ant-modal-content').locator(
                          '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button', "always_do": True}),
                 ]},
                 'type': 'table_tr'}),
            ('access_control_list',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox'),
                 "columns": [
                     ('interface', {'locator': self.page.locator('#interface'), 'type': 'select'}),
                     ('in_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#inbound_acl'), 'type': 'select'}),
                     ('out_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#outbound_acl'), 'type': 'select'}),
                     ('admin_acl',
                      {'locator': self.page.locator('.ant-modal-content').locator('#admin_acl'), 'type': 'select'}),
                     ('save',
                      {'locator': self.page.locator('.ant-modal-content').locator(
                          '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button', "always_do": True}),
                 ]},
                 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class NatLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def nat_locators(self) -> list:
        return [
            ('nat_rules',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(0),
                 "columns": [
                     ('action', {'locator': self.pop_up.locator('#action'), 'type': 'select'}),
                     ('source_network', {'locator': self.pop_up.locator('#source_network'), 'type': 'radio_select',
                                         'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
                     ('translation_type', {'locator': self.pop_up.locator('#translation_type'), 'type': 'select'}),
                     ('virtual_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.ip_addr"]'), 'type': 'text'}),
                     ('interface',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.interface"]'), 'type': 'select'}),
                     ('real_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.ip_addr"]'), 'type': 'text'}),
                     ('source_ip',
                      {'locator': self.pop_up.locator('//input[@id="source_range.ip_addr"]'), 'type': 'text'}),
                     ('source_netmask',
                      {'locator': self.pop_up.locator('//input[@id="source_range.netmask"]'), 'type': 'text'}),
                     ('transmit_protocol',
                      {'locator': self.pop_up.locator('#transmit_protocol'), 'type': 'radio_select'}),
                     ('match_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.ip_addr"]'), 'type': 'text'}),
                     ('match_interface',
                      {'locator': self.pop_up.locator('//div[@id="transmit_source.interface"]'), 'type': 'select'}),
                     ('match_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.port"]'), 'type': 'text'}),
                     ('match_end_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_source.end_port"]'), 'type': 'text'}),
                     ('match_acl',
                      {'locator': self.pop_up.locator('//div[@id="transmit_source.acl_num"]'), 'type': 'select'}),
                     ('translated_ip',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.ip_addr"]'), 'type': 'text'}),
                     ('translated_interface',
                      {'locator': self.pop_up.locator('//div[@id="transmit_dest.interface"]'), 'type': 'select'}),
                     ('translated_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.port"]'), 'type': 'text'}),
                     ('translated_end_port',
                      {'locator': self.pop_up.locator('//input[@id="transmit_dest.end_port"]'), 'type': 'text'}),
                     ('log', {'locator': self.pop_up.locator('#log'), 'type': 'switch_button'}),
                     ('description', {'locator': self.pop_up.locator('#description'), 'type': 'text'}),
                     ('save',
                      {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                       'type': 'button'}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button', "always_do": True}),
                 ]},
                 'type': 'table_tr', 'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
            ('network_interface',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table1-index-outerBox').nth(1),
                 "columns": [
                     ('interface', {'locator': self.page.locator('#interface'), 'type': 'select'}),
                     ('interface_type',
                      {'locator': self.pop_up.locator('#type'), 'type': 'radio_select',
                       'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
                     ('save',
                      {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel',
                      {'locator': self.page.locator('.ant-modal-content').locator('//button[@class="ant-btn"]'),
                       'type': 'button', "always_do": True}),
                 ]},
                 'type': 'table_tr', 'param': {'inside': self.locale.inside, 'outside': self.locale.outside}}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class L2tpLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def l2tp_client_status_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-empty.ant-table-scroll-position-left').nth(0),
                'type': 'table_tr',
                'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,
                          'disable': self.locale.disable}}

    @property
    def l2tp_server_status_locators(self) -> dict:
        return {'locator': self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-empty.ant-table-scroll-position-left').nth(1),
                'type': 'table_tr',
                'param': {'disconnect': self.locale.disconnect, 'connect': self.locale.connect,
                          'disable': self.locale.disable}}

    @property
    def l2tp_client_locators(self) -> list:
        return [
            ('l2tp_class', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(0),
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('auth', {'locator': self.pop_up.locator('#authentication'), 'type': 'radio_select',
                              'param': {'yes': self.locale.yes, 'no': self.locale.no}}),
                    ('hostname', {'locator': self.pop_up.locator('#hostname'), 'type': 'text'}),
                    ('challenge_secret', {'locator': self.pop_up.locator('#challenge_secret'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr',
                'param': {'yes': self.locale.yes, 'no': self.locale.no}}),
            ('pseudowire_class', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(1),
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('l2tp_class', {'locator': self.pop_up.locator('#class'), 'type': 'select'}),
                    ('source_interface', {'locator': self.pop_up.locator('#source_interface'), 'type': 'select'}),
                    ('data_encapsulation_method',
                     {'locator': self.pop_up.locator('#data_encapsulation_method'), 'type': 'select'}),
                    ('tunnel_management_protocol',
                     {'locator': self.pop_up.locator('#tunnel_management_protocol'), 'type': 'select'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv2_tunnel', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(2),
                "columns": [
                    ('enable', {'locator': self.pop_up.locator('#enable'), 'type': 'switch_button'}),
                    ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                    ('l2tp_server', {'locator': self.pop_up.locator('#server'), 'type': 'text'}),
                    ('pseudowire_class', {'locator': self.pop_up.locator('#pseudowire_class'), 'type': 'select'}),
                    ('auth_type', {'locator': self.pop_up.locator('#authentication_type'), 'type': 'select',
                                   'param': {'AUTO': self.locale.auto}}),
                    ('username', {'locator': self.pop_up.locator('#username'), 'type': 'text'}),
                    ('password', {'locator': self.pop_up.locator('#password'), 'type': 'text'}),
                    ('local_ip_address', {'locator': self.pop_up.locator('#local_ip_address'), 'type': 'text'}),
                    ('remote_ip_address', {'locator': self.pop_up.locator('#remote_ip_address'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv3_tunnel', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(3),
                "columns": [
                    ('enable', {'locator': self.pop_up.locator('#enable'), 'type': 'switch_button'}),
                    ('id', {'locator': self.pop_up.locator('#id'), 'type': 'text'}),
                    ('peer_id', {'locator': self.pop_up.locator('#peer_id'), 'type': 'text'}),
                    ('pseudowire_class', {'locator': self.pop_up.locator('#pseudowire_class'), 'type': 'select'}),
                    ('protocol', {'locator': self.pop_up.locator('#protocol'), 'type': 'select'}),
                    ('source_port', {'locator': self.pop_up.locator('#source_port'), 'type': 'text'}),
                    ('destination_port', {'locator': self.pop_up.locator('#destination_port'), 'type': 'text'}),
                    ('xconnect_interface', {'locator': self.pop_up.locator('#xconnect_interface'), 'type': 'select'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('l2tpv3_session', {'locator': {
                "locator": self.page.locator('.antd-pro-components-in-gateway-editable-table-index-tableBox').nth(4),
                "columns": [
                    ('local_session_id', {'locator': self.pop_up.locator('#local_session_id'), 'type': 'text'}),
                    ('remote_session_id', {'locator': self.pop_up.locator('#remote_session_id'), 'type': 'text'}),
                    ('local_tunnel_id', {'locator': self.pop_up.locator('#local_tunnel_id'), 'type': 'select'}),
                    ('local_session_ip_address',
                     {'locator': self.pop_up.locator('#local_session_ip_address'), 'type': 'text'}),
                    ('save',
                     {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]}, 'type': 'table_tr'}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]

    @property
    def l2tp_service_locators(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('username', {'locator': self.page.locator('#username'), 'type': 'text', 'relation': [('enable', True)]}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'text', 'relation': [('enable', True)]}),
            ('auth_type',
             {'locator': self.page.locator('#authentication_type'), 'type': 'select', 'relation': [('enable', True)],
              'param': {'AUTO': self.locale.auto}}),
            ('local_ip_address',
             {'locator': self.page.locator('#local_ip_address'), 'type': 'text', 'relation': [('enable', True)]}),
            ('client_start_ip',
             {'locator': self.page.locator('#client_start_ip_address'), 'type': 'text',
              'relation': [('enable', True)]}),
            ('client_end_ip',
             {'locator': self.page.locator('#client_end_ip_address'), 'type': 'text', 'relation': [('enable', True)]}),
            ('link_detection_interval', {'locator': self.page.locator('#link_detection_interval'), 'type': 'text',
                                         'relation': [('enable', True)]}),
            ('max_retries_for_link', {'locator': self.page.locator('#max_retries_for_link'), 'type': 'text',
                                      'relation': [('enable', True)]}),
            ('enable_mppe', {'locator': self.page.locator('#enable_mppe'), 'type': 'switch_button'}),
            ('enable_tunnel_auth',
             {'locator': self.page.locator('#enable_tunnel_authentication'), 'type': 'switch_button'}),
            ('challenge_secrets', {'locator': self.page.locator('#challenge_secrets'), 'type': 'text',
                                   'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('server_name', {'locator': self.page.locator('#server_name'), 'type': 'text',
                             'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('client_name', {'locator': self.page.locator('#client_name'), 'type': 'text',
                             'relation': [('enable', True), ('enable_tunnel_auth', True)]}),
            ('export_options',
             {'locator': self.page.locator('#export_options'), 'type': 'text', 'relation': [('enable', True)]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
        ]


class NetworkLocators(EthernetLocators, CellularLocators, BridgeLocators, WlanLocators, WanLocators, LanLocators,
                      LoopbackLocators, DhcpLocators, DnsLocators, GpsLocators, HostListLocators,
                      RoutingStatusLocators, StaticRoutingLocators, AclLocators, NatLocators, L2tpLocators):
    pass
