# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 13:23:17
# @Author  : Pane Li
# @File    : network.py
"""
network

"""
import allure
from inhandtest.tools import loop_inspector
from inhandtest.base_page.base_page import BasePage
from inhandtest.pages.ingateway.locators import IgLocators


class Cellular(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言蜂窝状态')
    @loop_inspector('cellular_status')
    def assert_status(self, **kwargs):
        """

        :param kwargs:
                     active_sim: SIM 1,SIM 2,sim 1,sim 2 ex: active_sim='"${value}" =="sim 1"'
                     imei: 123456789012345 ex: imei='"${value}" == "123456789012345"'
                     imsi: 123456789012345 ex: imsi='"${value}" == "123456789012345"'
                     iccid: 123456789012345 ex: iccid='"${value}" == "123456789012345"'
                     register_status: not_register,registering,connected,disconnected ex: register_status='"${value}" == "not_register"'
                     operator: China Mobile,China Unicom,China Telecom ex: operator='"${value}" == "China Mobile"'
                     network_type: 2G,3G,4G ex: network_type='"${value}" == "2G"'
                     lac: 1234 ex: lac='${value} == 1234'
                     cell_id: 1234 ex: cell_id='${value} == 1234'
                     status: not_register,registering,connected,disconnected ex: status='"${value}" == "connected"'
                     ip_address: 192.168.2.1 ex: ip_address='"${value}" == "192.168.2.1"'
                     netmask: 255.255.255.0 ex: netmask='"${value}" == "255.255.255.0"'
                     gateway: 192.168.2.1 ex: gateway='"${value}" == "192.168.2.1"'
                     dns:  61.139.2.69 ex: dns='"${value}" == "61.139.2.69"'
                     mtu: 1500 ex: mtu='${value} == 1500'
                     connect_time: 00:00:00 ex: connect_time='"${value}".startswith("00:00")'
        :return:
        """
        self.access_menu('network.network_interface.cellular')
        return self.eval_locator_attribute(kwargs, self.network_locators.cellular_status_locators)

    @allure.step('获取蜂窝信息')
    def get_status(self, keys: str or list or tuple) -> str or dict or None:
        """

        :param keys:
                     active_sim: SIM 1,SIM 2
                     imei: 123456789012345
                     imsi: 123456789012345
                     iccid: 123456789012345
                     register_status: Registering, 中文情况下返回中文，英文情况下返回英文
                     operator: China Mobile,中文情况下返回中文，英文情况下返回英文
                     network_type: 2G,3G,4G
                     lac: 1234
                     cell_id: 1234
                     status: Registering, 中文情况下返回中文，英文情况下返回英文
                     ip_address: 192.168.2.1
                     netmask: 255.255.255.0
                     gateway: 192.168.2.1
                     dns:  61.139.2.69
                     mtu: 1500
                     connect_time: 00:00:00
        :return: 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        self.access_menu('network.network_interface.cellular')
        return self.get_text(keys, self.network_locators.cellular_status_locators)

    @allure.step('配置蜂窝网')
    def config(self, **kwargs):
        """ 配置蜂窝网参数, 无需配置时均不填写参数

        :param kwargs:
               cellular_enable: enable,disable ex: cellular_enable="enable"
               profile: [($action, **kwarg)]
                  ex: [('delete_all', )],
                 [('delete', '2GSM')]
                 [('add', {'network_type': 'GSM', 'apn': '3gnet', 'access_number': '*99***1#', 'auth_method': 'auto', 'username': 'gprs', 'password': 'gprs'})]
                     add parameter:
                     network_type: GSM,CDMA, ex: network_type="GSM"
                     apn: 3gnet ex: apn="3gnet"
                     access_number: *99***1# ex: access_number="*99***1#"
                     auth_method: auto,PAP,CHAP,MS-CHAP,MS-CHAPv2 ex: auth_method="auto"
                     username: gprs ex: username="gprs"
                     password: gprs ex: password="gprs"
                     text_messages: str or list
                     cancel: True, False
                 [('add', {'network_type': 'GSM', 'apn': '3gnet', 'access_number': '*99***1#',
                          'auth_method': 'auto', 'username': 'gprs', 'password': 'gprs', 'is_exists': 'GSM3gnet'})] 如果存在GSM3gnet则不添加
                 [('edit', '2GSM', {'network_type': 'GSM', 'apn': '4gnet'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               dual_sim_enable: enable,disable ex: dual_sim_enable="enable"
               main_sim: SIM1,SIM2,Random,Sequence ex: main_sim="SIM1"
               max_number_of_dial: 10 ex: max_number_of_dial=10
               min_connected_time: 10 ex: min_connected_time=10
               backup_sim_timeout: 10 ex: backup_sim_timeout=10
               network_type: 2G,3G,4G,auto ex: network_type="auto"
               sim1_profile: auto,1,2,3 ex: sim1_profile="auto"
               sim1_roaming: enable,disable ex: sim1_roaming="enable"
               sim1_pincode: 1234 ex: sim1_pincode=1234
               sim1_csq_threshold: 10 ex: sim1_csq_threshold=10
               sim1_csq_detect_interval: 10 ex: sim1_csq_detect_interval=10
               sim1_csq_detect_retries: 10 ex: sim1_csq_detect_retries=10
               sim2_profile: auto,1,2,3 ex: sim2_profile="auto"
               sim2_roaming: enable,disable ex: sim2_roaming="enable"
               sim2_pincode: 1234 ex: sim2_pincode=1234
               sim2_csq_threshold: 10 ex: sim2_csq_threshold=10
               sim2_csq_detect_interval: 10 ex: sim2_csq_detect_interval=10
               sim2_csq_detect_retries: 10 ex: sim2_csq_detect_retries=10
               static_ip_enable:  enable,disable ex: static_ip_enable="enable"
               static_ip: '192.168.2.1' ex: static_ip="192.168.2.1"
               static_peer: '192.168.2.1' ex: static_peer="192.168.2.1"
               radial_interval: 10 ex: radial_interval=10
               icmp_probes: expand,close ex: icmp_probes="expand"
               icmp_detection_server1: '8.8.8.8' ex: icmp_detection_server1="8.8.8.8"
               icmp_detection_server2: '8.8.8.8' ex: icmp_detection_server2="8.8.8.8"
               icmp_detection_interval: 10 ex: icmp_detection_interval=10
               icmp_detection_max_retries: 10 ex: icmp_detection_max_retries=10
               icmp_detection_timeout: 10 ex: icmp_detection_timeout=10
               icmp_detection_strict: enable,disable ex: icmp_detection_strict="enable"
               advanced_settings: 'expand' ex: advanced_settings="expand"
               init_command: 'AT+CPIN?' ex: init_command="AT+CPIN?"
               mru: 1500 ex: mru=1500
               rssi_poll_interval: 10 ex: rssi_poll_interval=10
               mtu: 1500 ex: mtu=1500
               dial_timeout: 10 ex: dial_timeout=10
               use_default_asyncmap: enable,disable ex: use_default_asyncmap="enable"
               use_peer_dns: enable,disable ex: use_peer_dns="enable"
               lcp_interval: 10 ex: lcp_interval=10
               lcp_max_retries: 10 ex: lcp_max_retries=10
               infinitely_dial_retry: enable,disable ex: infinitely_dial_retry="enable"
               debug: enable,disable ex: debug="enable"
               expert_options: 'AT+CPIN?'
               text_messages: str or list or tuple ex: text_messages="Please enter an integer for 1 ~ 604800"
               submit: True or False ex: submit=True  or  submit={'tip_messages': 'cellular_configuration_changed_successful'}
               confirm: True or False ex: submit=True  or  submit={'tip_messages': 'cellular_configuration_changed_successful'}
                        拨号参数集配置变更后 在submit后还需要点击confirm才能生效
               reset: True or False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.cellular')
        self.agg_in(self.network_locators.cellular_locators, kwargs)


class Ethernet(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言网络状态')
    @loop_inspector('ethernet_status')
    def assert_status(self, port='gigabitethernet 0/1', **kwargs):
        """
        :param port: gigabitethernet 0/1,gigabitethernet 0/2
        :param kwargs:
               network_type: static_ip, dynamic_address_dhcp, ex: network_type='"${value}"=="static_ip"'
               ip_address: 192.168.2.1 ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status： up, down ex: status='"${value}"=="up"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:")'
               description: eth0 ex: description='"${value}"=="eth0"'
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        return self.eval_locator_attribute(kwargs, self.network_locators.ethernet_status_locators)

    @allure.step('获取网络状态')
    def get_status(self, keys: str or list, port='gigabitethernet 0/1') -> str or dict or None:
        """
        :param port: gigabitethernet 0/1,gigabitethernet 0/2
        :param keys:
               network_type:
               ip_address:
               netmask:
               gateway:
               dns:
               mtu:
               status：
               connection_time:
               description:
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        return self.get_text(keys, self.network_locators.ethernet_status_locators)

    @allure.step('配置网络')
    def config(self, port='gigabitethernet 0/1', **kwargs):
        """ 配置网络, 在配置网口2 时需要先去网桥关闭网口2桥接口，否则无法配置

        :param port:  gigabitethernet 0/1,gigabitethernet 0/2
        :param kwargs:
                network_type: static_ip, dynamic_address_dhcp, ex: network_type='static_ip'
                ip_address: 192.168.2.1 ex: ip_address='192.168.2.1'
                netmask: 255.255.255.0 ex: netmask='255.255.255.0'
                speed_duplex: auto_negotiation, 1000m full duplex, 1000m half duplex, 100m full duplex, 100m half duplex, 10m full duplex, 10m half duplex
                              ex: speed_duplex='1000m full duplex'
                mtu: 1500 ex: mtu=1500
                track_l2_state: enable, disable ex: track_l2_state='enable'
                shutdown: enable, disable ex: shutdown='enable'
                description: eth0 ex: description='eth0'
                secondary_ip_settings:
                    [($action, **kwarg)]
                    ex: [('delete_all', )],
                     [('delete', '192.168.2.1255.255.255.0')]
                     [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                     add parameter:
                        secondary_ip:
                        netmask:
                        text_messages: str or list
                        cancel: True, False
                     [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                     [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                     多个操作时使用列表 [('add',{}), ('add',{})]
                submit: True, False ex: submit=True or submit={'tip_messages': 'submit_success'}
                text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
                tip_messages: 'submit_success' ex: tip_messages='submit_success'  提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu(f'network.network_interface.ethernet.{port}')
        try:
            self.agg_in(self.network_locators.ethernet_locators, kwargs)
        except TimeoutError:
            raise TimeoutError(f'please check bridge member of {port} is enabled or not')


class Bridge(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言网桥接口状态')
    @loop_inspector('bridge_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1 ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status： up, down ex: status='"${value}"=="up"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00")'
               description: eth0 ex: description='"${value}"=="eth0"'
        """
        self.access_menu('network.network_interface.bridge')
        return self.eval_locator_attribute(kwargs, self.network_locators.bridge_status_locators)

    @allure.step('获取网桥接口状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address:
               netmask:
               mtu:
               status：
               connection_time:
               description:
        """
        self.access_menu('network.network_interface.bridge')
        return self.get_text(keys, self.network_locators.bridge_status_locators)

    @allure.step('配置网桥接口')
    def config(self, **kwargs):
        """ 配置网桥接口

        :param kwargs:
                ip_address: 192.168.2.1 ex: ip_address='192.168.2.1'
                netmask: 255.255.255.0 ex: netmask='255.255.255.0'
                description: eth0 ex: description='eth0'
                secondary_ip_settings:
                [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                    secondary_ip:
                    netmask:
                    text_messages: str or list
                    cancel: True, False
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
                ge_01: enable, disable ex: ge_01='enable'
                ge_02: enable, disable ex: ge_02='enable'
                submit: True, False ex: submit=True or submit={'tip_messages': 'submit_success'}
                text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
                tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.bridge')
        self.agg_in(self.network_locators.bridge_locators, kwargs)


class Wlan(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言WLAN状态')
    @loop_inspector('wlan_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               station_role: ap,client ex: station_role='"${value}"=="ap"'
               wlan_status: enable, disable ex: wlan_status='"${value}"=="enable"'
               mac_address: 00:00:00:00:00:00 ex: mac_address='"${value}"=="00:00:00:00:00:00"'
               ssid: inhand-xxxx ex: ssid='"${value}"=="inhand-xxxx"'
               channel: 1,2,3,4,5,6,7,8,9,10,11 ex: channel='"${value}"=="1"'
               auth_method: OPEN, SHARED, WPA-PSK, WPA, WPA2-PSK, WPA2, WPAPSK/WPA2PSK ex: auth_method='"${value}"=="OPEN"'
               encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104 ex: encrypt_mode='"${value}"=="TKIP"'
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               wireless_connection_status: connect, disconnect ex: wireless_connection_status='"${value}"=="connect"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00")'
        """
        self.access_menu('network.network_interface.wlan')
        return self.eval_locator_attribute(kwargs, self.network_locators.wlan_status_locators)

    @allure.step('获取WLAN状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               station_role:
               wlan_status:
               mac_address:
               ssid：
               channel:
               auth_method:
               encrypt_mode
               ip_address
               netmask
               gateway
               dns
               wireless_connection_status
               connection_time
        """
        self.access_menu('network.network_interface.wlan')
        return self.get_text(keys, self.network_locators.wlan_status_locators)

    @allure.step('配置WLAN')
    def config(self, **kwargs):
        """如遇到需要等待的情况，自行在添加，不在通用方法中添加， 该方法也可以分拆成多个步骤执行

        :param kwargs:
               enable_wifi: enable,disable ex: enable_wifi="enable"
               station_role: ap,client ex: station_role="ap"
               sta_default_route: enable,disable ex: sta_default_route="enable"
               sta_ssid: inhand-xxxx ex: sta_ssid="inhand-xxxx"
               sta_scan: {'wait_for_time': 5*1000}, False ex: sta_scan={'wait_for_time': 5*1000} 点击完扫描后会等待5s
               sta_connect: 'inhand-visitor80:8d:b7:eb:80:90'
               sta_auth_method: OPEN, SHARED, WPA-PSK, WPA, WPA2-PSK, WPA2 ex: sta_auth_method="OPEN"
               sta_encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104, ex: sta_encrypt_mode="TKIP"
               sta_wpa_psk: 12345678 ex: sta_wpa_psk="12345678"
               sta_wpa_psk_key: 12345678 ex: sta_wpa_psk_key="12345678"
               sta_auth_mode: EAP-PEAP, EAP-TLS ex: sta_auth_mode="EAP-PEAP"
               sta_inner_auth: mschapv2, md5, ex: sta_inner_auth="mschapv2"
               sta_username: inhand ex: sta_user_name="inhand"
               sta_password: inhand ex: sta_password="inhand"
               sta_network_type: static_ip, dynamic_address_dhcp ex: sta_network_type="static_ip"
               sta_ip_address: 192.168.3.1 ex: sta_ip_address="192.168.3.1"
               sta_netmask: 255.255.255.0, ex: sta_netmask="255.255.255.0"

               ap_ssid_broadcast: enable,disable ex: ap_ssid_broadcast="enable"
               ap_bridge: enable,disable ex: ap_bridge="enable"
               ap_band: 2.4G,5G ex: ap_band="2.4G"
               ap_radio_type: 802.11b/g,802.11b,802.11g,802.11n,802.11g/n,802.11b/g/n  ex: ap_radio_type="802.11b/g/n"
               ap_channel: 1,2,3,4,5,6,7,8,9,10,11,12,13 ex: ap_channel="1"
               ap_ssid: inhand-xxxx ex: ap_ssid="inhand-xxxx"
               ap_auth_method: OPEN, SHARED, WPA-PSK, WPAPSK/WPA2PSK, ex: ap_auth_method="OPEN"
               ap_encrypt_mode: TKIP, AES, NONE, WEP40,  WEP104, ex: ap_encrypt_mode="TKIP"
               ap_wep_key: 123456, ex: ap_wep_key="123456"
               ap_wpa_psk_key: 12345678, ex: ap_wpa_psk_key="12345678"
               ap_bandwidth: 20MHz,40MHz, ex: ap_bandwidth="20MHz"
               ap_stations_limit: 1,2,3,4,5,6,7,8,9,10, ex: ap_stations_limit="1"
               submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: errors_tip='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.wlan')
        if kwargs.get('sta_connect'):
            kwargs.update({'sta_connect': [('connect', kwargs.get('sta_connect'))]})
        self.agg_in(self.network_locators.wlan_locators, kwargs)


class Wan(BasePage, IgLocators):
    __doc__ = 'IG502 function: wan'

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言WAN状态')
    @loop_inspector('wan_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               network_type: static_ip,dynamic_address_dhcp ex: network_type='"${value}"=="static_ip"'
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               gateway: 192.168.2.1 ex: gateway='"${value}"=="192.168.2.1"'
               dns: 61.139.2.69 ex: dns='"${value}"=="61.139.2.69"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status: up, down ex: status='"${value}"=="up"'
               description: ex: description='"${value}"=="WAN1"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:00")'
        """
        self.access_menu('network.network_interface.wan')
        return self.eval_locator_attribute(kwargs, self.network_locators.wan_status_locators)

    @allure.step('获取WAN状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               network_type, ip_address, netmask, gateway, dns, mtu, status, description, connection_time
        """
        self.access_menu('network.network_interface.wan')
        return self.get_text(keys, self.network_locators.wan_status_locators)

    @allure.step('配置WAN')
    def config(self, **kwargs):
        """

        :param kwargs:
               interface_type: WAN,LAN ex: interface_type='WAN'
               network_type: static_ip,dynamic_address_dhcp ex: network_type='static_ip'
               ip_address: 192.168.2.1, ex: ip_address='192.168.2.1'
               netmask: 255.255.255.0, ex: netmask='255.255.255.0'
               gateway: 192.168.2.1, ex: gateway='192.168.2.1'
               dns: 8.8.8.8 ex: dns='8.8.8.8'
               mtu: 1500 ex: mtu='1500'
               track_l2_state: enable,disable ex: track_l2_state='enable'
               shutdown: enable,disable ex: shutdown='enable'
               description: ex: description='WAN1'
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                 add parameter:
                    secondary_ip:
                    netmask:
                    text_messages
                    cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
                reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.wan')
        self.agg_in(self.network_locators.wan_locators, kwargs)


class Lan(BasePage, IgLocators):
    __doc__ = 'IG502 function: lan'

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言LAN状态')
    @loop_inspector('lan_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
               mtu: 1500 ex: mtu='"${value}"=="1500"'
               status: up, down ex: status='"${value}"=="up"'
               description: ex: description='"${value}"=="WAN1"'
               connection_time: 0 day 00:00:00 ex: connection_time='"${value}".startswith("0 day 00:00")'
        """
        self.access_menu('network.network_interface.lan')
        return self.eval_locator_attribute(kwargs, self.network_locators.lan_status_locators)

    @allure.step('获取LAN状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address, netmask, mtu, status, description, connection_time
        """
        self.access_menu('network.network_interface.lan')
        return self.get_text(keys, self.network_locators.lan_status_locators)

    @allure.step('配置LAN')
    def config(self, **kwargs):
        """

        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='192.168.2.1'
               netmask: 255.255.255.0, ex: netmask='255.255.255.0'
               shutdown: enable,disable ex: shutdown='enable'
               description: ex: description='WAN1'
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                        secondary_ip:
                        netmask:
                        text_messages: str or list
                        cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.lan')
        self.agg_in(self.network_locators.lan_locators, kwargs)


class Loopback(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG502', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Loopback状态')
    @loop_inspector('loopback_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               ip_address: 192.168.2.1, ex: ip_address='"${value}"=="192.168.2.1"'
               netmask: 255.255.255.0 ex: netmask='"${value}"=="255.255.255.0"'
        """
        self.access_menu('network.network_interface.loopback')
        return self.eval_locator_attribute(kwargs, self.network_locators.loopback_status_locators)

    @allure.step('获取Loopback状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               ip_address, netmask
        """
        self.access_menu('network.network_interface.loopback')
        return self.get_text(keys, self.network_locators.loopback_status_locators)

    @allure.step('配置Loopback')
    def config(self, **kwargs):
        """

        :param kwargs:
               secondary_ip_settings:
               [($action, **kwarg)] ex: [('delete_all', )],
                 [('delete', '192.168.2.1255.255.255.0')]
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0'})]
                    add parameter:
                        secondary_ip:
                        netmask:
                        text_messages: str or list
                        cancel: True,
                 [('add', {'secondary_ip': '192.168.2.1', 'netmask': '255.255.255.0', 'is_exists': '192.168.2.1255.255.255.0'})]  如果存在就不加
                 [('edit', '192.168.2.1255.255.255.0', {'secondary_ip': '192.168.3.1', 'netmask': '255.255.255.0'})]
                 多个操作时使用列表 [('add',{}), ('add',{})]
               submit: True,False ex: submit=True or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_interface.loopback')
        self.agg_in(self.network_locators.loopback_locators, kwargs)


class Dhcp(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Dhcp')
    def config(self, **kwargs):
        """

        :param kwargs:
               dhcp_server:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'Gigabitethernet 0/110.5.24.97')]
                [('add', {'enable_dhcp_server': 'enable', 'interface': 'Gigabitethernet 0/1',
                         'start_address': '192.168.2.2', 'end_address': '192.168.2.234', 'lease': 1440})]
                   add parameters:
                        enable_dhcp_server: 'enable', 'disable'
                        interface: 'Gigabitethernet 0/1', 'Cellular 1',
                        start_address:
                        end_address:
                        lease: 30-10080
                        text_messages: str or list
                        cancel: True, False
                [('add', {'enable_dhcp_server': 'enable', 'interface': 'Gigabitethernet 0/1',
                         'start_address': '192.168.2.2', 'end_address': '192.168.2.234', 'lease': 1440, 'is_exists': 'Gigabitethernet 0/110.5.24.97'})] 如果存在则不添加
                [('edit', 'Gigabitethernet 0/110.5.24.97', {'enable_dhcp_server': 'enable'})]
                多个操作时使用列表 [('add',{}), ('add',{})]
               windows_name_server: www.baidu.com ex: windows_name_server='www.baidu.com'
               static_ip_setting:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', '00:00:00:00:00:0010.5.24.97')]
                [('add', {'mac_address': '00:00:00:00:00:00', 'ip_address': '10.5.24.97'})]
                    add parameters:
                        mac_address: 00:00:00:00:00:00
                        ip_address:
                        text_messages: str or list
                        cancel: True, False
                [('add', {'mac_address': '00:00:00:00:00:00', 'ip_address': '10.5.24.97', 'is_exists': '00:00:00:00:00:00'})] 如果存在则不添加
                [('edit', '00:00:00:00:00:00', {'mac_address': '00:00:00:00:00:01'})]
               submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.dhcp')
        self.agg_in(self.network_locators.dhcp_locators, kwargs)


class Dns(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Dns')
    def config(self, **kwargs):
        """

        :param kwargs:
               primary_dns: 8.8.8.8 ex: primary_dns='8.8.8.8'
               secondary_dns: 114.114.114.114 ex: secondary_dns='114.114.114.114'
               submit_dns_server: True,False ex: submit_dns_server=True
               enable_dns_relay: enable,disable ex: enable_dns_relay='enable'
               domain_ip_address_pair:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'ss.dc.com10.5.24.97')]
                [('add', {'host': 'ss.dc.com', 'ip_address1': '10.5.24.97', 'ip_address2': '10.5.24.98'})]
                    add parameters:
                        host: ss.dc.com
                        ip_address1:
                        ip_address2:
                        text_messages: str or list
                        cancel: True, False
                [('add', {'host': 'ss.dc.com', 'ip_address1': '10.5.24.97', 'ip_address2': '10.5.24.98', 'is_exists': 'ss.dc.com10.5.24.97'})] 如果存在则不添加
                [('edit', 'ss.dc.com10.5.24.97', {'host': 'ss.db.com'})]
               submit_domain_ip_address_pair: True,False ex: submit_domain_ip_address_pair=True  or submit_domain_ip_address_pair={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.dns')
        self.agg_in(self.network_locators.dns_locators, kwargs)


class Gps(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言GPS状态')
    @loop_inspector('gps_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               gps_status: enable,disable, ex: gps_status='"${value}"=="enable"'
               time_: 0 day 00:00:00 ex: time_='"${value}".startswith("0 day 00:00")'
               location: 成都市 ex: location='"${value}".startswith("成都市")'
               speed:

        """
        self.access_menu('network.network_services.gps.gps configure')
        return self.eval_locator_attribute(kwargs, self.network_locators.gps_status_locators)

    @allure.step('获取GPS状态')
    def get_status(self, keys: str or list) -> str or dict or None:
        """
        :param keys:
               gps_status, time_, location, speed
        """
        self.access_menu('network.network_services.gps.gps configure')
        return self.get_text(keys, self.network_locators.gps_status_locators)

    @allure.step('配置GPS')
    def config(self, enable=True, tip_messages='submit_success'):
        """

        :param enable: True,False ex: enable=True
        :param tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
        :return:
        """
        self.access_menu('network.network_services.gps.gps configure')
        if tip_messages:
            self.agg_in(self.network_locators.gps_locators, {'enable': enable, 'tip_messages': tip_messages})
        else:
            self.agg_in(self.network_locators.gps_locators, {'enable': enable})

    @allure.step('配置GPS IP Forwarding')
    def config_ip_forwarding(self, **kwargs):
        """ 需要注意的是，在不同的模式下，只有部分参数可用

        :param kwargs:
               enable: True,False ex: enable=True
               type_: client,server ex: type_='client'
               transmit_protocol: UDP,TCP ex: transmit_protocol='UDP'
               connection_type: long_lived,short_lived ex: connection_type='long_lived'
               keepalive_interval: 30 ex: keepalive_interval=30
               keepalive_retry: 3 ex: keepalive_retry=3
               idle_timeout: 60 ex: idle_timeout=60
               local_port: 10000 ex: local_port=10000
               min_reconnect_interval: 60 ex: min_reconnect_interval=60
               max_reconnect_interval: 300 ex: max_reconnect_interval=300
               source_interface: Cellular 1,Dot11radio 1,Gigabitethernet 0/1,Gigabitethernet 0/2, Openvpn 1, Bridge 1 ex: source_interface='Cellular 1'
               reporting_interval: 60 ex: reporting_interval=60
               include_rmc: enable,disable ex: include_rmc='enable'
               include_gsa: enable,disable ex: include_gsa='enable'
               include_gga: enable,disable ex: include_gga='enable'
               include_gsv: enable,disable ex: include_gsv='enable'
               message_prefix: prefix, ex: message_prefix='prefix'
               message_suffix: suffix, ex: message_suffix='suffix'
               destination_ip_address:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'ss.dc.com10.5.24.97')]
                [('add', {'server': 'ss.dc.com', 'port': 10000})]
                    add parameter:
                        server:
                        port:
                        text_messages: str or list
                        cancel: True, False
                [('add', {'server': 'ss.dc.com', 'port': 10000, 'is_exists': 'ss.dc.com10000'})] 如果存在则不添加
                [('edit', 'ss.dc.com10000', {'server': 'ss.db.com'})]
               submit: True,False ex: submit=True or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.gps.gps ip forwarding')
        self.agg_in(self.network_locators.gps_ip_forwarding_locators, kwargs)

    @allure.step('配置GPS Serial Forwarding')
    def config_serial_forwarding(self, **kwargs):
        """ 需要注意的是，在不同的模式下，只有部分参数可用

        :param kwargs:
               enable: True,False ex: enable=True
               serial_type: RS232,RS485,server ex: type_='client'
               baudrate: 9600,19200,38400,57600,115200 ex: baudrate=9600
               data_bits: 7,8 ex: data_bits=5
               parity: none,odd,even ex: parity='none'
               stop_bit: 1,2 ex: stop_bits=1
               software_flow_control: enable,disable ex: software_flow_control='enable'
               include_rmc: enable,disable ex: include_rmc='enable'
               include_gsa: enable,disable ex: include_gsa='enable'
               include_gga: enable,disable ex: include_gga='enable'
               include_gsv: enable,disable ex: include_gsv='enable'
               submit: True,False ex: submit=True or submit={'tip_messages': 'submit_success'}
               text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
               tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
               reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.network_services.gps.gps serial forwarding')
        self.agg_in(self.network_locators.gps_serial_forwarding_locators, kwargs)


class HostList(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言HostList状态')
    @loop_inspector('host_list_status')
    def assert_status(self, **kwargs):
        """
        :param kwargs:
               interface: Gigabitethernet 0/1,Gigabitethernet 0/2, ex: interface='Gigabitethernet 0/1'
               mac_address: 00:00:00:00:00:00 ex: mac_address='00:00:00:00:00:00'
               ip_address: 1.1.1.1 ex: ip_address='1.1.1.1'
               host: host1 ex: host='host1'
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """
        if kwargs:
            self.access_menu('network.network_services.host_list')
            exist = True if kwargs.get('exist') is None else kwargs.pop('exist')
            value = ''
            for cl_ in ('interface', 'mac_address', 'ip_address', 'host'):
                if kwargs.get(cl_):
                    value = value + kwargs.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                return self.table_tr(self.network_locators.hostlist_status_locators, [('exist', value)], 'host list')[0]
            else:
                return not \
                    self.table_tr(self.network_locators.hostlist_status_locators, [('exist', value)], 'host list')[0]
        else:
            return True


class RoutingStatus(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言Routing Status状态')
    @loop_inspector('routing_status')
    def assert_status(self, routing_type='all', **kwargs):
        """
        :param routing_type: 'all', 'connected_routing', 'static_routing', 'ospf', 'bgp', 'rip'
        :param kwargs:
               destination: 0.0.0.0
               netmask: 0.0.0.0
               gateway:
               interface: Gigabitethernet 0/1, Gigabitethernet 0/2, Bridge 1, Loopback 1
               distance: 255/0
               time:
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """

        if kwargs:
            self.access_menu('network.routing.routing_status')
            self.agg_in(self.network_locators.routing_locators, {'routing_type': routing_type}),
            exist = True if kwargs.get('exist') is None else kwargs.pop('exist')
            value = ''
            for cl_ in ('destination', 'netmask', 'interface', 'distance', 'time'):
                if kwargs.get(cl_):
                    value = value + kwargs.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                return \
                    self.table_tr(self.network_locators.routing_table_locators, [('exist', value)], 'routing status')[0]
            else:
                return not \
                    self.table_tr(self.network_locators.routing_table_locators, [('exist', value)], 'routing status')[0]
        else:
            return True


class StaticRouting(BasePage, IgLocators):
    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置Static Routing')
    def config(self, **kwargs):
        """

        :param kwargs:
                routing: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', '0.0.0.0Gigabitethernet 0/1')]
                    [('add', {'destination': '0.0.0.0', 'netmask': '0.0.0.0', 'interface': 'Gigabitethernet 0/1', 'gateway': '10.5.17.254','distance': 255, 'track_id': 1})]
                        add parameter:
                            destination:
                            netmask:
                            interface:
                            gateway:
                            distance:
                            track_id:
                            text_messages: str or list
                            cancel: True,False ex: cancel=True
                    [('edit', '0.0.0.0Gigabitethernet 0/1', {'destination': '1.1.1.1'})]
                    [('add', {'destination': '0.0.0.0', 'netmask': '10.5.24.97', 'interface': 'Gigabitethernet 0/1', 'is_exists': '10.5.24.97Gigabitethernet 0/1'})] 如果存在则不添加
                    [('edit', '10.5.24.97Gigabitethernet 0/1', {'destination': '1.1.1.1'})]
                submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
                text_messages: 'ip_address_conflict' ex: text_messages='ip_address_conflict'
                tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
                reset: True ex: reset=True
        :return:
        """
        self.access_menu('network.routing.static routing')
        self.agg_in(self.network_locators.static_routing_locators, kwargs)


class Acl(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置ACL规则')
    def config(self, default_filter_strategy='permit', **kwargs):
        """
        :param default_filter_strategy: 'permit', 'deny',
        :param kwargs:
               access_control_strategy: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', '10010')]
                    [('add', {'acl_type': 'standard', 'id': 100,'sequence_number': 40, 'action': 'permit', 'protocol': 'IP',})]
                    add parameters:
                        acl_type: 'standard', 'extended'
                        id: int
                        sequence_number: 1-100
                        action: 'permit', 'deny'
                        protocol: 'IP', 'ICMP', 'TCP', 'UDP', 'GRE', 'ESP', 'AH', 'OSPF', 'L2TpV3', '1-255'
                        protocol_id: 1-255
                        source_ip: '1.1.1.1'
                        source_wildcard: str
                        source_port: Any,=,!=,>,<,Range
                        source_port_value: 1-65535
                        source_port_value1: 1-65535
                        destination_ip:  '1.1.1.1'
                        destination_wildcard: str
                        destination_port: Any,=,!=,>,<,Range
                        destination_port_value: 1-65535
                        destination_port_value1: 1-65535
                        icmp_type: used_describe, use_type_code
                        icmp_describe:  'all' or other
                        icmp_type_value:  str
                        icmp_code: str
                        fragments: enable, disable
                        established: enable, disable
                        log: enable, disable
                        destination: str
                        text_messages: str or list
                        cancel: True, False
                    [('add', {'acl_type': 'standard', 'id': 100, 'sequence_number': 40, 'is_exists': '10040'})] 如果存在则不添加
                    [('edit', '10040', {'sequence_number': 60})]
               access_control_list: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'Cellular 1')]
                    [('add', {'interface': 'Cellular 1', 'in_acl': '100','out_acl': '102', 'admin_acl': '104'})]
                    add parameters:
                        interface: 'Cellular 1', 'Bridge 1', 'Openvpn 1', 'Gigabitethernet 0/1', 'Gigabitethernet 0/2',
                        in_acl: 100
                        out_acl: 100
                        admin_acl: 102
                        text_messages: str or list
                        cancel: True, False
                    [('add', {'interface': 'Cellular 1', 'in_acl': 100, 'out_acl': 102, 'is_exists': 'Cellular 1'})] 如果存在则不添加
                    [('edit', 'Cellular 1', {'in_acl': 102})]
              submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
              text_messages: str ex: text_messages='ip_address_conflict'
              tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
              reset: True, False ex: reset=True
        """
        self.access_menu('network.firewall.acl')
        self.agg_in(self.network_locators.acl_locators, {'default_filter_strategy': default_filter_strategy}),
        if kwargs:
            self.agg_in(self.network_locators.acl_locators, kwargs)


class Nat(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('配置NAT规则')
    def config(self, **kwargs):
        """

        :param kwargs:
               nat_rules: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'SNAT.*ACL:100')]
                    [('add', {'action': 'SNAT', 'source_network': 'inside', 'translation_type': 'IP to IP'})]
                    add parameters:
                        action: SNAT, DNAT, 1:1NAT
                        source_network: 'inside', 'outside'
                        translation_type: IP to IP, IP to INTERFACE, IP PORT to IP PORT, ACL to INTERFACE, ACL to IP, INTERFACE to IP, INTERFACE PORT to IP PORT, Virtual IP to IP, Virtual IP to INTERFACE,
                        transmit_protocol: TCP, UDP
                        match_ip: str
                        match_port: str
                        match_end_port: str
                        match_acl: str
                        match_interface: 'Cellular 1'
                        virtual_ip: str
                        real_ip: str
                        interface: 'Cellular 1'
                        translated_ip: str
                        translated_interface: 'Cellular 1'
                        translated_port: str
                        translated_end_port: str
                        source_ip: str
                        source_netmask: str
                        log: enable, disable
                        destination: str
                        text_messages: str or list
                        cancel: True, False
                    [('add', {'action': 'SNAT', 'source_network': 'inside', 'translation_type': 'IP to IP', 'is_exists': 'SNAT.*ACL:100'})] 如果存在则不添加
                    [('edit', 'SNAT.*ACL:100', {'action': 'SNAT'})]
               network_interface: [($action, **kwarg)] ex: [('delete_all', )],
                    [('delete', 'Cellular 1')]
                    [('add', {'interface': 'Cellular 1', 'interface_type': 'inside'})]
                    add parameters:
                        interface: 'Cellular 1', 'Bridge 1', 'Openvpn 1', 'Gigabitethernet 0/1', 'Gigabitethernet 0/2',
                        interface_type: inside, outside
                        text_messages: str or list
                        cancel: True, False
                    [('add', {'interface': 'Cellular 1', 'interface_type': 'inside', 'is_exists': 'Cellular 1'})] 如果存在则不添加
                    [('edit', 'Cellular 1', {'interface_type': 'outside'})]
              submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
              text_messages: str ex: text_messages='ip_address_conflict'
              tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
              reset: True, False ex: reset=True
        """
        if kwargs:
            self.access_menu('network.firewall.nat')
            self.agg_in(self.network_locators.nat_locators, kwargs)


class Vpn(BasePage, IgLocators):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        super().__init__(host, username, password, protocol, port, model, language, page, locale=locale)
        IgLocators.__init__(self, page, locale)

    @allure.step('断言L2tp Status状态')
    @loop_inspector('l2tp_status')
    def assert_status(self, client: dict = None, server: dict = None):
        """
        :param client: 字典，包含以下key
                tunnel_name:
                l2tp_server:
                status: disconnect, connect, disable
                time:
                local_ip_address
                remote_ip_address
                local_session_id
                remote_session_id
                exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        :param server: 字典，包含以下key
               tunnel_name:
               status: disconnect, connect, disable
               time:
               local_ip_address
               remote_ip_address
               exist: True,False ex: exist=True # True:存在,False:不存在， 默认查询存在
        """
        result = True
        if client or server:
            self.access_menu('network.vpn.l2tp.status')
        if client is not None:
            exist = True if client.get('exist') is None else client.pop('exist')
            value = ''
            for cl_ in ('tunnel_name', 'l2tp_server', 'status', 'time', 'local_ip_address', 'remote_ip_address',
                        'local_session_id', 'remote_session_id'):
                if client.get(cl_):
                    value = value + client.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                result = \
                    self.table_tr(self.network_locators.l2tp_client_status_locators, [('exist', value)],
                                  'routing status')[0]
            else:
                result = not \
                    self.table_tr(self.network_locators.l2tp_client_status_locators, [('exist', value)],
                                  'routing status')[0]
        if server is not None:
            exist = True if server.get('exist') is None else server.pop('exist')
            value = ''
            for cl_ in ('tunnel_name', 'status', 'time', 'local_ip_address', 'remote_ip_address'):
                if server.get(cl_):
                    value = value + server.get(cl_)
                else:
                    value = value + '.*'
            if exist:
                result = \
                    self.table_tr(self.network_locators.l2tp_server_status_locators, [('exist', value)],
                                  'routing status')[0]
            else:
                result = not \
                    self.table_tr(self.network_locators.l2tp_server_status_locators, [('exist', value)],
                                  'routing status')[0]
        return result

    @allure.step('配置L2tp Client')
    def config_client(self, **kwargs):
        """ 注意如果是删除，需要先删除关联项，再删除本身，否则多次删除会删除不了

        :param kwargs:
            l2tp_class:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'nameyes')]
                [('add', {'name': 'name', 'auth': 'yes', 'hostname': hostname, 'challenge_secret': challenge_secret})]
                    add parameter:
                        name:
                        auth: yes, no
                        hostname:
                        challenge_secret:
                        text_messages: str or list
                        cancel: True, False
                [('add', {'name': 'name', 'hostname': hostname, 'is_exists': 'nameyes'})] 如果存在则不添加
                [('edit', 'nameyes', {'name': 'name1'})]
                [('associate_delete', 'nameyes')]   # 删除关联项
            pseudowire_class:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'namel2tp_class')]
                [('add', {'name': 'name', 'l2tp_class': l2tp_class, 'source_interface': source_interface, 'data_encapsulation_method': data_encapsulation_method, 'tunnel_management_protocol': tunnel_management_protocol})]'})]
                    add parameter:
                        name:
                        l2tp_class: l2tp_class
                        source_interface: 'Cellular 1', 'Bridge 1'
                        data_encapsulation_method: 'L2TPv2', 'L2TPv3'
                        tunnel_management_protocol: 'L2TPv2', 'NONE', 'L2TPv3'
                        text_messages: str or list
                        cancel: True, False
                [('add', {'name': 'name', 'l2tp_class': l2tp_class, 'is_exists': 'namel2tp_class'})] 如果存在则不添加
                [('edit', 'namel2tp_class', {'name': 'name1'})]
                [('associate_delete', 'namel2tp_class')]   # 删除关联项
            l2tpv2_tunnel:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'id')]
                [('add', {'enable': True, 'id': id, 'l2tp_server': l2tp_server, 'pseudowire_class': pseudowire_class, 'auth_type': auth_type, 'username': username, 'password': password, 'local_ip_address': local_ip_address})]
                    add parameter:
                        enable: True, False
                        id: str or int
                        l2tp_server:
                        pseudowire_class:
                        auth_type: 'AUTO', 'PAP', 'CHAP'
                        username: str
                        password: str
                        local_ip_address: str
                        remote_ip_address: str
                        text_messages: str or list
                        cancel: True, False
                [('add', {'enable': True, 'id': id, 'is_exists': 'id'})] 如果存在则不添加
                [('edit', 'id', {'enable': False})]
                [('associate_delete', 'id')]   # 删除关联项
            l2tpv3_tunnel:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'id')]
                [('add', {'enable': True, 'id': id, 'peer_id': peer_id})]
                    add parameter:
                        enable: True, False
                        id: str or int
                        peer_id:
                        pseudowire_class:
                        protocol: 'IP', 'UDP'
                        source_port: int
                        destination_port: int
                        xconnect_interface: str
                        text_messages: str or list
                        cancel: True, False
                [('add', {'enable': True, 'id': id, 'is_exists': 'id'})] 如果存在则不添加
                [('edit', 'id', {'enable': False})]
                [('associate_delete', 'id')]   # 删除关联项
            l2tpv3_session:
               [($action, **kwarg)] ex: [('delete_all', )],
                [('delete', 'local_session_id')]
                [('add', {'local_session_id': local_session_id, 'remote_session_id': remote_session_id})]
                    add parameter:
                        local_session_id: str or int
                        remote_session_id: str or int
                        local_tunnel_id:
                        local_session_ip_address:
                        text_messages: str or list
                        cancel: True, False
                [('add', {'local_session_id': local_session_id, 'is_exists': 'local_session_id'})] 如果存在则不添加
                [('edit', 'local_session_id', {'local_session_id': local_session_id})]
                [('associate_delete', 'local_session_id')]   # 删除关联项
            submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
            text_messages: str or list
            tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
            reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.vpn.l2tp.l2tp client')
        self.agg_in(self.network_locators.l2tp_client_locators, kwargs)

    @allure.step('配置L2tp Service')
    def config_service(self, **kwargs):
        """

        :param kwargs:
            enable： True,False ex: enable=True
            username: str
            password: str
            auth_type: 'AUTO', 'PAP', 'CHAP'
            local_ip_address: str
            client_start_ip: str
            client_end_ip: str
            link_detection_interval:  int
            max_retries_for_link: int
            enable_mppe: True,False ex: enable_mppe=True
            enable_tunnel_auth: True,False ex: enable_tunnel_auth=True
            export_options: str
            submit: True,False ex: submit=True  or submit={'tip_messages': 'submit_success'}
            text_messages: str or list
            tip_messages: submit_success ex: tip_messages='submit_success' 提交后需要验证成功的提示框
            reset: True,False ex: reset=True
        :return:
        """
        self.access_menu('network.vpn.l2tp.l2tp service')
        self.agg_in(self.network_locators.l2tp_service_locators, kwargs)


class Network:

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='IG902', language='en', page=None, locale: dict = None):
        self.ethernet: Ethernet = Ethernet(host, username, password, protocol, port, model, language, page, locale)
        self.cellular: Cellular = Cellular(host, username, password, protocol, port, model, language, page, locale)
        self.bridge: Bridge = Bridge(host, username, password, protocol, port, model, language, page, locale)
        self.wlan: Wlan = Wlan(host, username, password, protocol, port, model, language, page, locale)
        self.wan: Wan = Wan(host, username, password, protocol, port, model, language, page, locale)
        self.lan: Lan = Lan(host, username, password, protocol, port, model, language, page, locale)
        self.loopback: Loopback = Loopback(host, username, password, protocol, port, model, language, page, locale)
        self.dhcp: Dhcp = Dhcp(host, username, password, protocol, port, model, language, page, locale)
        self.dns: Dns = Dns(host, username, password, protocol, port, model, language, page, locale)
        self.gps: Gps = Gps(host, username, password, protocol, port, model, language, page, locale)
        self.host_list: HostList = HostList(host, username, password, protocol, port, model, language, page, locale)
        self.routing_status: RoutingStatus = RoutingStatus(host, username, password, protocol, port, model, language,
                                                           page, locale)
        self.static_routing: StaticRouting = StaticRouting(host, username, password, protocol, port, model, language,
                                                           page, locale)
        self.acl: Acl = Acl(host, username, password, protocol, port, model, language, page, locale)
        self.nat: Nat = Nat(host, username, password, protocol, port, model, language, page, locale)
        self.vpn: Vpn = Vpn(host, username, password, protocol, port, model, language, page, locale)
