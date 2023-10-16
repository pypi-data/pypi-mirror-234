# -*- coding: utf-8 -*-
# @Time    : 2023/3/15 14:08:11
# @Author  : Pane Li
# @File    : _vg710_contents_locators.py
"""
_vg710_contents_locators

"""
from playwright.sync_api import Locator, Page


class VGContentsLocators:

    def __init__(self, page: Page, language='en', model='VG710'):
        self.page = page
        self.frame = self.page.frame_locator('#window_content')
        self.language = language
        self.model = model.upper()
        if language == 'en':
            self.__locale: dict = {'bootloader': 'Bootloader Version',
                                   'source_interface': 'Source Interface',
                                   'device_manager': 'Device Manager'}
        else:
            self.__locale: dict = {'bootloader': 'Bootloader版本',
                                   'source_interface': '源接口',
                                   'device_manager': '设备远程管理平台',
                                   }

    def content_span_text(self, menu) -> Locator:
        one_menu = {"en": {"system": "Administration >> System", "system_time": "Administration >> System Time",
                           "management_s": "Administration >> Management Services",
                           "user_m": "Administration >> User Management", "aaa": "Administration >> AAA",
                           "config_m": "Administration >> Config Management",
                           "device_m": "Administration >> Device Manager", 'admin': 'Administration',
                           "snmp": "Administration >> SNMP", "alarm": "Administration >> Alarm",
                           "log": "Administration >> Log", "cron_job": "Administration >> Cron job",
                           "upgrade": "Administration >> Upgrade", "reboot": "Administration >> Reboot",
                           "cellular": "Network >> Cellular", "bridge": "Network >> Bridge", 'network': 'Network',
                           "vlan": "Network >> VLAN", "adsl": "Network >> ADSL Dialup (PPPoE)",
                           "wifi": "Network >> Wi-Fi", "bluetooth": "Network >> Bluetooth",
                           "captive_": "Network >> Captive portal", "look_back": "Network >> Loopback",
                           "layer": "Network >> Layer2 Switch", 'ip_passthrough': "Network >> IP Passthrough",
                           "dhcp": "Services >> DHCP", "dns": "Services >> DNS", "ddns": "Services >> DDNS",
                           "sms": "Services >> SMS", "gnss": "Services >> GNSS", "qos": "Services >> QoS",
                           "data_usage": "Services >> Data Usage", "obd": "Services >> OBD", 'service': 'Services',
                           "power_management": "Services >> Power Management", "sla": "Link Backup >> SLA",
                           "track": "Link Backup >> Track", "vrrp": "Link Backup >> VRRP",
                           "interface_back": "Link Backup >> Interface Backup", 'link_backup': 'Link Backup',
                           'static_routing': "Routing >> Static Routing", 'routing': 'Routing',
                           "dynamic_r": "Routing >> Dynamic Routing", "multicast_r": "Routing >> Multicast Routing",
                           'acl': "Firewall >> ACL", "nat": "Firewall >> NAT", "mac_ip": "Firewall >> MAC-IP Binding",
                           "url_filter": "Firewall >> URL Filter", "advanced": "Firewall >> Advanced",
                           "ipsec": "VPN >> IPsec", "gre": "VPN >> GRE", "l2tp": "VPN >> L2TP", 'firewall': 'Firewall',
                           "openvpn": "VPN >> OpenVPN", "certificate": "VPN >> Certificate Management", 'vpn': 'VPN',
                           'app': "APP >> APP", 'docker': 'APP >> Docker', 'third_party': 'APP >> Third-Party Platform',
                           'local_mqtt': 'APP >> Local MQTT Broker', 'rest_api': 'APP >> REST API', 'app_': 'APP',
                           'azure_iot': 'APP >> Azure IoT Edge', 'user_data': 'APP >> User Data',
                           'industrial': 'Industrial',
                           'dtu': 'Industrial >> DTU', 'io': 'Industrial >> IO', '1_wire': 'Industrial >> 1-Wire',
                           'ping': 'Tools >> Ping', 'traceroute': 'Tools >> Traceroute', 'tcpdump': 'Tools >> Tcpdump',
                           'link_speed': 'Tools >> Link Speed Test', 'new_lan': 'Wizards >> New LAN',
                           'new_wan': 'Wizards >> New WAN', 'new_cellular': 'Wizards >> New Cellular',
                           'new_ipsec_tunnel': 'Wizards >> New IPsec Tunnel', 'tools': 'Tools', 'wizards': 'Wizards',
                           'ipsec_expert': 'Wizards >> IPsec Expert Config', 'l2tpv2': 'Wizards >> New L2TPv2 Tunnel',
                           'new_port_m': 'Wizards >> New Port Mapping'
                           },
                    'cn': {"system": "管理 >> 系统", "system_time": "管理 >> 系统时间",
                           "management_s": "管理 >> 管理服务", 'admin': '管理',
                           "user_m": "管理 >> 用户管理", "aaa": "管理 >> AAA",
                           "config_m": "管理 >> 配置管理",
                           "device_m": "管理 >> 设备远程管理平台",
                           "snmp": "管理 >> SNMP", "alarm": "管理 >> 告警",
                           "log": "管理 >> 系统日志", "cron_job": "管理 >> 计划任务",
                           "upgrade": "管理 >> 系统升级", "reboot": "管理 >> 重启系统",
                           "cellular": "网络 >> 拨号接口", "bridge": "网络 >> 桥接口",
                           "vlan": "网络 >> VLAN接口", "adsl": "网络 >> ADSL拨号(PPPoE)", 'network': '网络',
                           "wifi": "网络 >> Wi-Fi", "bluetooth": "网络 >> 蓝牙",
                           "captive_": "网络 >> 强制网络门户", "look_back": "网络 >> 环回接口",
                           "layer": "网络 >> 二层交换", 'ip_passthrough': "网络 >> IP Passthrough",
                           "dhcp": "服务 >> DHCP服务", "dns": "服务 >> DNS服务", "ddns": "服务 >> 动态域名",
                           "sms": "服务 >> 短信服务", "gnss": "服务 >> GNSS", "qos": "服务 >> QoS",
                           "data_usage": "服务 >> 流量控制", "obd": "服务 >> 车辆诊断", 'service': '服务',
                           "power_management": "服务 >> 电源管理", "sla": "链路备份 >> SLA",
                           "track": "链路备份 >> Track模块", "vrrp": "链路备份 >> VRRP",
                           "interface_back": "链路备份 >> 接口备份", 'link_backup': '链路备份',
                           'static_routing': "路由 >> 静态路由", 'routing': '路由',
                           "dynamic_r": "路由 >> 动态路由", "multicast_r": "路由 >> 组播路由",
                           'acl': "防火墙 >> 访问控制(ACL)", "nat": "防火墙 >> 网络地址转换(NAT)",
                           "mac_ip": "防火墙 >> MAC-IP 绑定", 'firewall': '防火墙',
                           "url_filter": "防火墙 >> URL 过滤", "advanced": "防火墙 >> 高级",
                           "ipsec": "VPN >> IPsec", "gre": "VPN >> GRE", "l2tp": "VPN >> L2TP", 'vpn': 'VPN',
                           "openvpn": "VPN >> OpenVPN", "certificate": "VPN >> 证书管理",
                           'app': "APP >> APP", 'docker': 'APP >> Docker', 'third_party': 'APP >> 第三方云平台',
                           'local_mqtt': 'APP >> 本地MQTT代理', 'rest_api': 'APP >> REST API', 'app_': 'APP',
                           'azure_iot': 'APP >> Azure IoT Edge', 'user_data': 'APP >> 自定义数据',
                           'dtu': '工业接口 >> DTU', 'io': '工业接口 >> IO接口',
                           '1_wire': '工业接口 >> 单线总线(1-Wire)', 'industrial': '工业接口', 'tools': '工具',
                           'ping': '工具 >> PING 探测', 'traceroute': '工具 >> 路由探测', 'tcpdump': '工具 >> 网络抓包',
                           'link_speed': '工具 >> 网速测试', 'new_lan': '快速向导 >> 新建LAN',
                           'new_wan': '快速向导 >> 新建WAN', 'new_cellular': '快速向导 >> 新建拨号',
                           'new_ipsec_tunnel': '快速向导 >> 新建IPsec隧道', 'wizards': '快速向导',
                           'ipsec_expert': '快速向导 >> IPsec专家配置', 'l2tpv2': '快速向导 >> 新建L2TPv2隧道',
                           'new_port_m': '快速向导 >> 新建端口映射'
                           }}
        if self.language == 'en':
            span_text = one_menu.get('en').get(menu)
        else:
            span_text = one_menu.get('cn').get(menu)
        return self.page.locator(f'//span[@id="dir_span"]').get_by_text(span_text)

    @property
    def administration_menu(self) -> Locator:
        return self.page.locator('#ulLista_administration')

    @property
    def network_menu(self) -> Locator:
        return self.page.locator('#ulLista_network')

    @property
    def services_menu(self) -> Locator:
        return self.page.locator('#ulLista_services')

    @property
    def link_backup_menu(self) -> Locator:
        return self.page.locator('#ulLista_backup')

    @property
    def routing_menu(self) -> Locator:
        return self.page.locator('#ulLista_route')

    @property
    def firewall_menu(self) -> Locator:
        return self.page.locator('#ulLista_firewall')

    @property
    def vpn_menu(self) -> Locator:
        return self.page.locator('#ulLista_vpn')

    @property
    def app_menu(self) -> Locator:
        return self.page.locator('#ulLista_python_sdk')

    @property
    def industrial_menu(self) -> Locator:
        return self.page.locator('#ulLista_industrial')

    @property
    def tools_menu(self) -> Locator:
        return self.page.locator('#ulLista_tools')

    @property
    def wizards_menu(self) -> Locator:
        return self.page.locator('#ulLista_wizards')

    @property
    def tags_menu(self) -> dict:
        return {
            'administration': {
                'default': 'system.status',
                'menu': [self.administration_menu],
                'system': {
                    'default': 'status',
                    'menu': [self.page.locator('#status_system')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('system')],
                    'status': {
                        'menu': self.page.locator('#Span_status_system_tdstatus_system'),
                        'visible_locator': [
                            self.frame.locator(f'//td[text()="{self.__locale.get("bootloader")}"]')],
                        'wait_locator': [self.frame.locator('//tr[@id="rtime"]')],
                    },
                    'basic_setup': {
                        'menu': self.page.locator('#Span_status_system_tdsetup_system'),
                        'visible_locator': [self.frame.locator('#_f_language')],
                        'wait_locator': [self.frame.locator('#_f_language')]},
                    'advanced_setup': {
                        'menu': self.page.locator('#Span_status_system_tdadv_setup_system'),
                        'visible_locator': [self.frame.locator('#_f_sfe')],
                        'wait_locator': [self.frame.locator('#_f_sfe')]}
                },
                'system_time': {
                    'default': 'system_time',
                    'menu': [self.page.locator('#setup_time')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('system_time')],
                    'system_time': {
                        'menu': self.page.locator('#Span_setup_time_tdsetup_time'),
                        'visible_locator': [self.frame.locator('#_f_tm_sel')],
                        'wait_locator': [self.frame.locator('#_f_tm_sel')]},
                    'sntp_client': {
                        'menu': self.page.locator("#Span_setup_time_tdsetup_sntp"),
                        'visible_locator': [self.frame.locator('#_f_sntp_enable')],
                        'wait_locator': [self.frame.locator('#bs-grid')]},
                    'ntp_server': {
                        'menu': self.page.locator("#Span_setup_time_tdsetup_ntp_server"),
                        'visible_locator': [self.frame.locator('#_f_ntp_enable')],
                        'wait_locator': [self.frame.locator('#_f_ntp_enable')]}

                },
                'management_services': {
                    'default': 'management_services',
                    'menu': [self.page.locator('#setup_service')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('management_s')],
                    'management_services': {
                        'menu': self.page.locator('#Span_setup_service_tdsetup_service'),
                        'visible_locator': [self.frame.locator('#_f_http_enable')],
                        'wait_locator': [self.frame.locator('#_f_http_enable')]}},
                'user_management': {
                    'default': 'user_management',
                    'menu': [self.page.locator('#setup_create_user')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('user_m')],
                    'user_management': {
                        'menu': self.page.locator('#Span_setup_create_user_tdsetup_create_user'),
                        'visible_locator': [self.frame.locator('#_f_adm_user')],
                        'wait_locator': [self.frame.locator('#_f_adm_user')]}},
                'aaa': {
                    'default': 'radius',
                    'menu': [self.page.locator('#setup_radius')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('aaa')],
                    'radius': {
                        'menu': self.page.locator('#Span_setup_radius_tdsetup_radius'),
                        'visible_locator': [self.frame.locator(
                            f'//td[text()="{self.__locale.get("source_interface")}"][@class="co4"]')],
                        'wait_locator': [self.frame.locator('#aaa-grid')]},
                    'tacacs+': {
                        'menu': self.page.locator('#Span_setup_radius_tdsetup_tacacs'),
                        'visible_locator': [self.page.locator(f'//title[text()="{self.model} -> Tacacs+"]')],
                        'wait_locator': [self.frame.locator('#aaa-grid')]},
                    'ldap': {
                        'menu': self.page.locator('#Span_setup_radius_tdsetup_ldap'),
                        'visible_locator': [self.page.locator(f'//title[text()="{self.model} -> LDAP"]')],
                        'wait_locator': [self.frame.locator('#aaa-grid')]},
                    'aaa_settings': {
                        'menu': self.page.locator('#Span_setup_radius_tdsetup_aaa'),
                        'visible_locator': [self.frame.locator(f'#aaa-grid_head1')],
                        'wait_locator': [self.frame.locator('#aaa-grid')]}},
                'config_management': {
                    'default': 'config_management',
                    'menu': [self.page.locator('#admin_config')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('config_m')],
                    'config_management': {
                        'menu': self.page.locator('#Span_admin_config_tdadmin_config'),
                        'visible_locator': [self.frame.locator('#reset-button')],
                        'wait_locator': [self.frame.locator('#reset-button')]}},
                'device_manager': {
                    'default': 'status',
                    'menu': [self.page.locator('#dn_stat')],
                    'mouse_move': (200, 0),
                    'visible_locator': [self.content_span_text('device_m')],
                    'status': {
                        'menu': self.page.locator('#Span_dn_stat_tddn_stat'),
                        'visible_locator': [
                            self.frame.locator(f'//td[text()="{self.__locale.get("device_manager")}"]')],
                        'wait_locator': [self.frame.locator('#refresh-button')]},
                    'device_manager': {
                        'menu': self.page.locator('#Span_dn_stat_tddn_config'),
                        'visible_locator': [self.frame.locator('#_f_mqtt_enable')],
                        'wait_locator': [self.frame.locator('#_f_mqtt_enable')]}},
                'snmp': {
                    'default': 'snmp',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_snmp')],
                    'visible_locator': [self.content_span_text('snmp')],
                    'snmp': {
                        'menu': self.page.locator('#Span_setup_snmp_tdsetup_snmp'),
                        'visible_locator': [self.frame.locator('#_f_snmpd_enable')],
                        'wait_locator': [self.frame.locator('#_f_snmpd_enable')]},
                    'snmptrap': {
                        'menu': self.page.locator('#Span_setup_snmp_tdsetup_snmptrap'),
                        'visible_locator': [self.frame.locator('#trapman-grid')],
                        'wait_locator': [self.frame.locator('#trapman-grid')]},
                    'snmpmibs': {
                        'menu': self.page.locator('#Span_setup_snmp_tdsetup_snmpmibs'),
                        'visible_locator': [self.frame.locator('#_snmp_mib_file')],
                        'wait_locator': [self.frame.locator('#_snmp_mib_file')]}},
                'alarm': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_alarm')],
                    'visible_locator': [self.content_span_text('alarm')],
                    'status': {
                        'menu': self.page.locator('#Span_status_alarm_tdstatus_alarm'),
                        'visible_locator': [self.frame.locator('#clear-all')],
                        'wait_locator': [self.frame.locator('#alarmlog-grid')]},
                    'alarm_input': {
                        'menu': self.page.locator('#Span_status_alarm_tdsetup_alarm_in'),
                        'visible_locator': [self.frame.locator('#_f_in_0')],
                        'wait_locator': [self.frame.locator('#_f_in_0')]},
                    'alarm_output': {
                        'menu': self.page.locator('#Span_status_alarm_tdsetup_alarm_out'),
                        'visible_locator': [self.frame.locator('#test-button')],
                        'wait_locator': [self.frame.locator('#email-alarm')]},
                    'alarm_map': {
                        'menu': self.page.locator('#Span_status_alarm_tdsetup_alarm_map'),
                        'visible_locator': [self.frame.locator('#_all_email')],
                        'wait_locator': [self.frame.locator('#adm_grid')]}},
                'log': {
                    'default': 'log',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_log')],
                    'visible_locator': [self.content_span_text('log')],
                    'log': {
                        'menu': self.page.locator('#Span_status_log_tdstatus_log'),
                        'visible_locator': [self.frame.locator('#_f_level')],
                        'wait_locator': [self.frame.locator('#_f_level')]},
                    'system_log': {
                        'menu': self.page.locator('#Span_status_log_tdadmin_log'),
                        'visible_locator': [self.frame.locator('#_f_log_remote')],
                        'wait_locator': [self.frame.locator('#server-grid')]}},
                'cron_job': {
                    'default': 'cron_job',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#scheduler')],
                    'visible_locator': [self.content_span_text('cron_job')],
                    'cron_job': {
                        'menu': self.page.locator('#Span_scheduler_tdscheduler'),
                        'visible_locator': [self.frame.locator('#schedule-grid')],
                        'wait_locator': [self.frame.locator('#schedule-grid')]}},
                'upgrade': {
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#upgrd')],
                    'visible_locator': [self.content_span_text('upgrade')],
                    'wait_locator': [self.frame.locator('#file')]},
                'reboot': {
                    'menu': [self.page.locator('#reboot')],
                    'visible_locator': [self.content_span_text('reboot')]},
            },
            'network': {
                'default': 'cellular.status',
                'menu': [self.network_menu],
                'cellular': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': self.page.locator('#status_wan1'),
                    'visible_locator': [self.content_span_text('cellular')],
                    'status': {
                        'menu': [self.page.locator('#Span_status_wan1_tdstatus_wan1')],
                        'visible_locator': [self.frame.locator('#b_connect')],
                        'wait_locator': [self.frame.locator('#b_connect')]},
                    'cellular': {
                        'menu': self.page.locator('#Span_status_wan1_tdsetup_wan1'),
                        'visible_locator': [self.frame.locator('#_f_wan1_enable')],
                        'wait_locator': [self.frame.locator('#_f_wan1_enable')]}},
                'bridge': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_eth')],
                    'visible_locator': [self.content_span_text('bridge')],
                    'status': {
                        'menu': self.page.locator('#Span_status_eth_tdstatus_eth'),
                        'visible_locator': [self.frame.locator('#br-title')],
                        'wait_locator': [self.frame.locator('#br-title')]},
                    'bridge': {
                        'menu': self.page.locator('#Span_status_eth_tdsetup_bridge'),
                        'visible_locator': [self.frame.locator('#bridge-grid')],
                        'wait_locator': [self.frame.locator('#bridge-grid')]}},
                'vlan': {
                    'default': 'vlan_trunk',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_vlan_portmode')],
                    'visible_locator': [self.content_span_text('vlan')],
                    'vlan_trunk': {
                        'menu': self.page.locator('#Span_setup_vlan_portmode_tdsetup_vlan_portmode'),
                        'visible_locator': [self.frame.locator('#ifacl-grid')],
                        'wait_locator': [self.frame.locator('#ifacl-grid')]},
                    'configure_vlan_parameters': {
                        'menu': self.page.locator('#Span_setup_vlan_portmode_tdsetup_vlan'),
                        'visible_locator': [self.frame.locator('#vlan-grid')],
                        'wait_locator': [self.frame.locator('#vlan-grid')]}},
                'adsl_dialup(pppoe)': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_pppoe')],
                    'visible_locator': [self.content_span_text('adsl')],
                    'status': {
                        'menu': self.page.locator('#Span_status_pppoe_tdstatus_pppoe'),
                        'wait_locator': [self.frame.locator('#refresh-button')]},
                    'adsl_dialup(pppoe)': {
                        'menu': self.page.locator('#Span_status_pppoe_tdsetup_pppoe'),
                        'visible_locator': [self.frame.locator('#dialpool-grid')],
                        'wait_locator': [self.frame.locator('#dialpool-grid')]}},
                'wi_fi': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_wlan0')],
                    'visible_locator': [self.content_span_text('wifi')],
                    'status': {
                        'menu': self.page.locator('#Span_status_wlan0_tdstatus_wlan0'),
                        'visible_locator': [self.frame.locator('#wifi-2g-grid')],
                        'wait_locator': [self.frame.locator('#wifi-5g-grid')]},
                    'wi_fi_24g': {
                        'menu': self.page.locator('#Span_status_wlan0_tdsetup_wlan0'),
                        'wait_locator': [self.frame.locator('#_f_wl0_enable')]},
                    'wi_fi_5g': {
                        'menu': self.page.locator('#Span_status_wlan0_tdsetup_wlan1'),
                        'wait_locator': [self.frame.locator('#_f_wl0_enable')]},
                    'advanced': {
                        'menu': self.page.locator('#Span_status_wlan0_tdsetup_adv_wlan0'),
                        'visible_locator': [self.frame.locator('#_bridge_mode')],
                        'wait_locator': [self.frame.locator('#_bridge_mode')]}},
                'bluetooth': {
                    'default': 'bluetooth_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_bluetooth')],
                    'visible_locator': [self.content_span_text('bluetooth')],
                    'bluetooth_management': {
                        'menu': self.page.locator('#Span_setup_bluetooth_tdsetup_bluetooth'),
                        'visible_locator': [self.frame.locator('#_bluetooth_enable')],
                        'wait_locator': [self.frame.locator('#_bluetooth_enable')]}},
                'captive_portal': {
                    'default': 'captive_portal',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_portal_nc')],
                    'visible_locator': [self.content_span_text('captive_')],
                    'captive_portal': {
                        'menu': self.page.locator('#Span_setup_portal_nc_tdsetup_portal_nc'),
                        'visible_locator': [self.frame.locator('#_f_enable')],
                        'wait_locator': [self.frame.locator('#_f_enable')]}},
                'loopback': {
                    'default': 'loopback',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_lo0')],
                    'visible_locator': [self.content_span_text('look_back')],
                    'loopback': {
                        'menu': self.page.locator('#Span_setup_lo0_tdsetup_lo0'),
                        'visible_locator': [self.frame.locator('#mip-grid')],
                        'wait_locator': [self.frame.locator('#mip-grid')]}},
                'layer2_switch': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_port')],
                    'visible_locator': [self.content_span_text('layer')],
                    'status': {
                        'menu': self.page.locator('#Span_status_port_tdstatus_port'),
                        'visible_locator': [self.frame.locator('#intf-grid')],
                        'wait_locator': [self.frame.locator('#intf-grid')]}},
                'ip_passthrough': {
                    'default': 'ip_passthrough',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_ippassth')],
                    'visible_locator': [self.content_span_text('ip_passthrough')],
                    'ip_passthrough': {
                        'menu': self.page.locator('#Span_setup_ippassth_tdsetup_ippassth'),
                        'visible_locator': [self.frame.locator('#_f_ippassth_enable')],
                        'wait_locator': [self.frame.locator('#_f_ippassth_enable')]}},

            },
            'services': {
                'default': 'dhcp.status',
                'menu': [self.services_menu],
                'dhcp': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_dhcp')],
                    'visible_locator': [self.content_span_text('dhcp')],
                    'status': {
                        'menu': self.page.locator('#Span_status_dhcp_tdstatus_dhcp'),
                        'visible_locator': [self.frame.locator('#dev-grid')],
                        'wait_locator': [self.frame.locator('#dev-grid')]},
                    'dhcp_server': {
                        'menu': self.page.locator('#Span_status_dhcp_tdsetup_dhcp'),
                        'visible_locator': [self.frame.locator('#interface-grid')],
                        'wait_locator': [self.frame.locator('#interface-grid')]},
                    'dhcp_relay': {
                        'menu': self.page.locator('#Span_status_dhcp_tdsetup_dhcprelay'),
                        'visible_locator': [self.frame.locator('#_f_dhcprelay_enable')],
                        'wait_locator': [self.frame.locator('#_f_dhcprelay_enable')]},
                    'dhcp_client': {
                        'menu': self.page.locator('#Span_status_dhcp_tdsetup_dhcpc'),
                        'wait_locator': [self.frame.locator('//table[@class="fields"]')]}},
                'dns': {
                    'default': 'dns_server',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_dns')],
                    'visible_locator': [self.content_span_text('dns')],
                    'dns_server': {
                        'menu': self.page.locator('#Span_setup_dns_tdsetup_dns'),
                        'visible_locator': [self.frame.locator('#_f_dns_1')],
                        'wait_locator': [self.frame.locator('#_f_dns_1')]},
                    'dns_relay': {
                        'menu': self.page.locator('#Span_setup_dns_tdsetup_dnsrelay'),
                        'visible_locator': [self.frame.locator('#_f_dnsrelay_enable')],
                        'wait_locator': [self.frame.locator('#dnsrelay-grid')]}},
                'ddns': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_ddns')],
                    'visible_locator': [self.content_span_text('ddns')],
                    'status': {
                        'menu': self.page.locator('#Span_status_ddns_tdstatus_ddns'),
                        'wait_locator': [self.frame.locator('#refresh-button')]},
                    'ddns': {
                        'menu': self.page.locator('#Span_status_ddns_tdsetup_ddns'),
                        'visible_locator': [self.frame.locator('#method-grid')],
                        'wait_locator': [self.frame.locator('#method-grid')]}},
                'sms': {
                    'default': 'basic',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_sms_basic')],
                    'visible_locator': [self.content_span_text('sms')],
                    'basic': {
                        'menu': self.page.locator('#Span_setup_sms_basic_tdsetup_sms_basic'),
                        'visible_locator': [self.frame.locator('#_f_sms_enable')],
                        'wait_locator': [self.frame.locator('#_f_sms_enable')]}},
                'gnss': {
                    'default': 'position',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_gps')],
                    'visible_locator': [self.content_span_text('gnss')],
                    'position': {
                        'menu': self.page.locator('#Span_status_gps_tdstatus_gps'),
                        'wait_locator': [self.frame.locator('#gps-time-title')]},
                    'gnss_settings': {
                        'menu': self.page.locator('#Span_status_gps_tdsetup_gps_enable'),
                        'visible_locator': [self.frame.locator('#_f_enable_gps')],
                        'wait_locator': [self.frame.locator('#_f_enable_gps')]},
                    'gnss_ip_forwarding': {
                        'menu': self.page.locator('#Span_status_gps_tdsetup_gps_tcp'),
                        'visible_locator': [self.frame.locator('#_f_tcp_enable')],
                        'wait_locator': [self.frame.locator('#_f_tcp_enable')]},
                    'gnss_serial_forwarding': {
                        'menu': self.page.locator('#Span_status_gps_tdsetup_gps_serial'),
                        'visible_locator': [self.frame.locator('#_f_s_enable')],
                        'wait_locator': [self.frame.locator('#_f_s_enable')]}},
                'qos': {
                    'default': 'traffic_control',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_traffic')],
                    'visible_locator': [self.content_span_text('qos')],
                    'traffic_control': {
                        'menu': self.page.locator('#Span_setup_traffic_tdsetup_traffic'),
                        'visible_locator': [self.frame.locator('#tcl-grid')],
                        'wait_locator': [self.frame.locator('#tcl-grid')]}},
                'data_usage': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_data_usage')],
                    'visible_locator': [self.content_span_text('data_usage')],
                    'status': {
                        'menu': self.page.locator('#Span_status_data_usage_tdstatus_data_usage'),
                        'wait_locator': [self.frame.locator('#previous_day_sim1-grid')]},
                    'data_usage': {
                        'menu': self.page.locator('#Span_status_data_usage_tdsetup_data_usage'),
                        'visible_locator': [self.frame.locator('#_f_datausage_enable')],
                        'wait_locator': [self.frame.locator('#_f_datausage_enable')]}},
                'obd': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_obd')],
                    'visible_locator': [self.content_span_text('obd')],
                    'status': {
                        'menu': self.page.locator('#Span_status_obd_tdstatus_obd'),
                        'wait_locator': [self.frame.locator('#refresh-button')]},
                    'obd': {
                        'menu': self.page.locator('#Span_status_obd_tdsetup_obd'),
                        'wait_locator': [self.frame.locator('#canbus_title')]}},
                'power_management': {
                    'default': 'power_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_power_management')],
                    'visible_locator': [self.content_span_text('power_management')],
                    'power_management': {
                        'menu': self.page.locator('#Span_setup_power_management_tdsetup_power_management'),
                        'wait_locator': [self.frame.locator('#_f_power_off_voltage')]}},
            },
            'link_backup': {
                'default': 'sla.status',
                'menu': [self.link_backup_menu],
                'sla': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_sla')],
                    'visible_locator': [self.content_span_text('sla')],
                    'status': {
                        'menu': self.page.locator('#Span_status_sla_tdstatus_sla'),
                        'visible_locator': [self.frame.locator('#stat_sla-grid')],
                        'wait_locator': [self.frame.locator('#stat_sla-grid')]},
                    'sla': {
                        'menu': self.page.locator('#Span_status_sla_tdsetup_sla'),
                        'visible_locator': [self.frame.locator('#sla-grid')],
                        'wait_locator': [self.frame.locator('#sla-grid')]}},
                'track': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_track')],
                    'visible_locator': [self.content_span_text('track')],
                    'status': {
                        'menu': self.page.locator('#Span_status_track_tdstatus_track'),
                        'visible_locator': [self.frame.locator('#stat_track-grid')],
                        'wait_locator': [self.frame.locator('#stat_track-grid')]},
                    'track': {
                        'menu': self.page.locator('#Span_status_track_tdsetup_track'),
                        'visible_locator': [self.frame.locator('#track-grid')],
                        'wait_locator': [self.frame.locator('#track-grid')]}},
                'vrrp': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_vrrp')],
                    'visible_locator': [self.content_span_text('vrrp')],
                    'status': {
                        'menu': self.page.locator('#Span_status_vrrp_tdstatus_vrrp'),
                        'wait_locator': [self.frame.locator('#vrrp-grid')]},
                    'vrrp': {
                        'menu': self.page.locator('#Span_status_vrrp_tdsetup_vrrp'),
                        'wait_locator': [self.frame.locator('#vrrp-grid')]}},
                'interface_backup': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_if_backup')],
                    'visible_locator': [self.content_span_text('interface_back')],
                    'status': {
                        'menu': self.page.locator('#Span_status_if_backup_tdstatus_if_backup'),
                        'wait_locator': [self.frame.locator('#backup-grid')]},
                    'interface_backup': {
                        'menu': self.page.locator('#Span_status_if_backup_tdsetup_if_backup'),
                        'visible_locator': [self.frame.locator('#backup-grid')],
                        'wait_locator': [self.frame.locator('#backup-grid')]}},
            },
            'routing': {
                'default': 'static_routing.route_table',
                'menu': [self.routing_menu],
                'static_routing': {
                    'default': 'route_table',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_route')],
                    'visible_locator': [self.content_span_text('static_routing')],
                    'route_table': {
                        'menu': self.page.locator('#Span_status_route_tdstatus_route'),
                        'visible_locator': [self.frame.locator('#_state')],
                        'wait_locator': [self.frame.locator('#statsroute-grid')]},
                    'static_routing': {
                        'menu': self.page.locator('#Span_status_route_tdsetup_static_route'),
                        'visible_locator': [self.frame.locator('#_f_route_type')],
                        'wait_locator': [self.frame.locator('#route-grid')]}},
                'dynamic_routing': {
                    'default': 'route_table',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#dyn_status_route')],
                    'visible_locator': [self.content_span_text('dynamic_r')],
                    'route_table': {
                        'menu': self.page.locator('#Span_dyn_status_route_tddyn_status_route'),
                        'visible_locator': [self.frame.locator('#_state')],
                        'wait_locator': [self.frame.locator('#statsroute-grid')]},
                    'rip': {
                        'menu': self.page.locator('#Span_dyn_status_route_tdsetup_dyn_rip'),
                        'visible_locator': [self.frame.locator('#_f_rip_enable')],
                        'wait_locator': [self.frame.locator('#_f_rip_enable')]},
                    'ospf': {
                        'menu': self.page.locator('#Span_dyn_status_route_tdsetup_dyn_ospf'),
                        'visible_locator': [self.frame.locator('#_f_ospf_enable')],
                        'wait_locator': [self.frame.locator('#_f_ospf_enable')]},
                    'bgp': {
                        'menu': self.page.locator('#Span_dyn_status_route_tdsetup_dyn_bgp'),
                        'visible_locator': [self.frame.locator('#_f_bgp_enable')],
                        'wait_locator': [self.frame.locator('#_f_bgp_enable')]},
                    'filtering_route': {
                        'menu': self.page.locator('#Span_dyn_status_route_tdsetup_dyn_rib'),
                        'visible_locator': [self.frame.locator('#prefix-grid')],
                        'wait_locator': [self.frame.locator('#prefix-grid')]}},
                'multicast_routing': {
                    'default': 'basic',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_mcast_route')],
                    'visible_locator': [self.content_span_text('multicast_r')],
                    'basic': {
                        'menu': self.page.locator('#Span_setup_mcast_route_tdsetup_mcast_route'),
                        'visible_locator': [self.frame.locator('#_f_mroute_enable')],
                        'wait_locator': [self.frame.locator('#mroutetab-grid')]},
                    'igmp': {
                        'menu': self.page.locator('#Span_setup_mcast_route_tdsetup_mroute_igmp'),
                        'visible_locator': [self.frame.locator('#_igmpproxy_upstream')],
                        'wait_locator': [self.frame.locator('#igmpdownstream-grid')]}},
            },
            'firewall': {
                'default': 'acl.acl',
                'menu': [self.firewall_menu],
                'acl': {
                    'default': 'acl',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_acl')],
                    'visible_locator': [self.content_span_text('acl')],
                    'acl': {
                        'menu': self.page.locator('#Span_setup_acl_tdsetup_acl'),
                        'visible_locator': [self.frame.locator('#interface-grid')],
                        'wait_locator': [self.frame.locator('#interface-grid')]}},
                'nat': {
                    'default': 'nat',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_nat')],
                    'visible_locator': [self.content_span_text('nat')],
                    'nat': {
                        'menu': self.page.locator('#Span_setup_nat_tdsetup_nat'),
                        'visible_locator': [self.frame.locator('#nat-grid')],
                        'wait_locator': [self.frame.locator('#nat-grid')]}},
                'mac_ip_binding': {
                    'default': 'mac_ip_binding',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_mac_ip_bind')],
                    'visible_locator': [self.content_span_text('mac_ip')],
                    'mac_ip_binding': {
                        'menu': self.page.locator('#Span_setup_mac_ip_bind_tdsetup_mac_ip_bind'),
                        'visible_locator': [self.frame.locator('#_f_mac_ip_enable')],
                        'wait_locator': [self.frame.locator('#_f_mac_ip_enable')]}},
                'url_filter': {
                    'default': 'url_filter',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_urlfilter')],
                    'visible_locator': [self.content_span_text('url_filter')],
                    'url_filter': {
                        'menu': self.page.locator('#Span_setup_urlfilter_tdsetup_urlfilter'),
                        'visible_locator': [self.frame.locator('#urlfilter-grid')],
                        'wait_locator': [self.frame.locator('#urlfilter-grid')]}},
                'advanced': {
                    'default': 'advanced',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_fw_adv')],
                    'visible_locator': [self.content_span_text('advanced')],
                    'advanced': {
                        'menu': self.page.locator('#Span_setup_fw_adv_tdsetup_fw_adv'),
                        'visible_locator': [self.frame.locator('#_br_nf_c_ipt')],
                        'wait_locator': [self.frame.locator('#_br_nf_c_ipt')]}},
            },
            'vpn': {
                'default': 'ipsec.status',
                'menu': [self.vpn_menu],
                'ipsec': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#vpn_ipsec_status')],
                    'visible_locator': [self.content_span_text('ipsec')],
                    'status': {
                        'menu': self.page.locator('#Span_vpn_ipsec_status_tdvpn_ipsec_status'),
                        'visible_locator': [self.frame.locator('#ike-grid')],
                        'wait_locator': [self.frame.locator('#ipsec-grid')]},
                    'ipsec_setting': {
                        'menu': self.page.locator('#Span_vpn_ipsec_status_tdvpn_ipsec_setting'),
                        'visible_locator': [self.frame.locator('#_f_ipsec_enable')],
                        'wait_locator': [self.frame.locator('#_f_ipsec_enable')]},
                    'ipsec_extern_setting': {
                        'menu': self.page.locator('#Span_vpn_ipsec_status_tdvpn_ipsec_extern'),
                        'visible_locator': [self.frame.locator('#profile-grid')],
                        'wait_locator': [self.frame.locator('#profile-grid')]}},
                'gre': {
                    'default': 'gre',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#vpn_gre')],
                    'visible_locator': [self.content_span_text('gre')],
                    'gre': {
                        'menu': self.page.locator('#Span_vpn_gre_tdvpn_gre'),
                        'visible_locator': [self.frame.locator('#gre-grid')],
                        'wait_locator': [self.frame.locator('#gre-grid')]}},
                'l2tp': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_l2tp')],
                    'visible_locator': [self.content_span_text('l2tp')],
                    'status': {
                        'menu': self.page.locator('#Span_status_l2tp_tdstatus_l2tp'),
                        'visible_locator': [self.frame.locator('#stat_l2tp-grid')],
                        'wait_locator': [self.frame.locator('#stat_l2tp-grid')]},
                    'l2tp_client': {
                        'menu': self.page.locator('#Span_status_l2tp_tdvpn_l2tpc'),
                        'visible_locator': [self.frame.locator('#l2tpclass-grid')],
                        'wait_locator': [self.frame.locator('#l2tpclass-grid')]},
                    'l2tp_server': {
                        'menu': self.page.locator('#Span_status_l2tp_tdvpn_l2tps'),
                        'visible_locator': [self.frame.locator('#_f_l2tps_enable')],
                        'wait_locator': [self.frame.locator('#_f_l2tps_enable')]}},
                'openvpn': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_openvpn')],
                    'visible_locator': [self.content_span_text('openvpn')],
                    'status': {
                        'menu': self.page.locator('#Span_status_openvpn_tdstatus_openvpn'),
                        'visible_locator': [self.frame.locator('#stat_openvpn-grid')],
                        'wait_locator': [self.frame.locator('#stat_openvpn-grid')]},
                    'openvpn_client': {
                        'menu': self.page.locator('#Span_status_openvpn_tdopenvpn_client'),
                        'visible_locator': [self.frame.locator('#l2tpclass-grid')],
                        'wait_locator': [self.frame.locator('#openvpn-client-grid')]},
                    'openvpn_server': {
                        'menu': self.page.locator('#Span_status_openvpn_tdopenvpn_server'),
                        'visible_locator': [self.frame.locator('#_f_openvpn_enable')],
                        'wait_locator': [self.frame.locator('#_f_openvpn_enable')]}},
                'certificate_management': {
                    'default': 'certificate_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#vpn_cert')],
                    'visible_locator': [self.content_span_text('certificate')],
                    'certificate_management': {
                        'menu': self.page.locator('#Span_vpn_cert_tdvpn_cert'),
                        'visible_locator': [self.frame.locator('#_f_scep_enable')],
                        'wait_locator': [self.frame.locator('#_f_scep_enable')]},
                    'root_ca': {
                        'menu': self.page.locator('#Span_vpn_cert_tdvpn_rootca'),
                        'visible_locator': [self.frame.locator('#ca-import-button')],
                        'wait_locator': [self.frame.locator('#rootca-grid')]}},
            },
            'app': {
                'default': 'app.status',
                'menu': [self.app_menu],
                'app': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_python_sdk')],
                    'visible_locator': [self.content_span_text('app')],
                    'status': {
                        'menu': self.page.locator('#Span_status_python_sdk_tdstatus_python_sdk'),
                        'wait_locator': [self.frame.locator('#pypp-stat-grid')]},
                    'app_management': {
                        'menu': self.page.locator('#Span_status_python_sdk_tdsetup_python_install'),
                        'visible_locator': [self.frame.locator('#_f_python_enable')],
                        'wait_locator': [self.frame.locator('#pyapp-grid')]}},
                'docker': {
                    'default': 'docker_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_docker')],
                    'visible_locator': [self.content_span_text('docker')],
                    'docker_management': {
                        'menu': self.page.locator('#Span_status_docker_tdstatus_docker'),
                        'visible_locator': [self.frame.locator('#_dk_enable')],
                        'wait_locator': [self.frame.locator('#docker_log')]}},
                'third_party_platform': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_3rd')],
                    'visible_locator': [self.content_span_text('third_party')],
                    'status': {
                        'menu': self.page.locator('#Span_status_3rd_tdstatus_3rd'),
                        'wait_locator': [self.frame.locator('#tcp-title')]},
                    'mqtt': {
                        'menu': self.page.locator('#Span_status_3rd_tdsetup_3rd_party_platform_mqtt'),
                        'wait_locator': [self.frame.locator('#_third_enable')]},
                    'tcp/udp': {
                        'menu': self.page.locator('#Span_status_3rd_tdsetup_3rd_party_platform_tcp'),
                        'wait_locator': [self.frame.locator('#_third_enable')]}},
                'local_mqtt_broker': {
                    'default': 'local_mqtt_broker_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_local_mqtt_broker')],
                    'visible_locator': [self.content_span_text('local_mqtt')],
                    'local_mqtt_broker_management': {
                        'menu': self.page.locator('#Span_setup_local_mqtt_broker_tdsetup_local_mqtt_broker'),
                        'visible_locator': [self.frame.locator('#_local_broker_enable')],
                        'wait_locator': [self.frame.locator('#_local_broker_enable')]}},
                'rest_api': {
                    'default': 'rest_api_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_restapi')],
                    'visible_locator': [self.content_span_text('rest_api')],
                    'rest_api_management': {
                        'menu': self.page.locator('#Span_setup_restapi_tdsetup_restapi'),
                        'visible_locator': [self.frame.locator('#_restapi_mode')],
                        'wait_locator': [self.frame.locator('#_restapi_mode')]}},
                'azure_iot_edge': {
                    'default': 'azure_iot_edge_management',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_azure_iotedge')],
                    'visible_locator': [self.content_span_text('azure_iot')],
                    'azure_iot_edge_management': {
                        'menu': self.page.locator('#Span_setup_azure_iotedge_tdsetup_azure_iotedge_mgmt'),
                        'visible_locator': [self.frame.locator('#_azure_iotedge_enable')],
                        'wait_locator': [self.frame.locator('#conf_export')]}},
                'user_data': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_user_data')],
                    'visible_locator': [self.content_span_text('user_data')],
                    'status': {
                        'menu': self.page.locator('#Span_status_user_data_tdstatus_user_data'),
                        'wait_locator': [self.frame.locator('#userdata-grid')]},
                    'user_data_management': {
                        'menu': self.page.locator('#Span_status_user_data_tdsetup_user_data'),
                        'wait_locator': [self.frame.locator('#userdata-grid')]}},
            },
            'industrial': {
                'default': 'dtu.serial_port',
                'menu': [self.industrial_menu],
                'dtu': {
                    'default': 'serial_port',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#setup_serial')],
                    'visible_locator': [self.content_span_text('dtu')],
                    'serial_port': {
                        'menu': self.page.locator('#Span_setup_serial_tdsetup_serial'),
                        'wait_locator': [self.frame.locator('#serial1_title')]},
                    'dtu_1': {
                        'menu': self.page.locator('#Span_setup_serial_tdsetup_dtu1'),
                        'wait_locator': [self.frame.locator('#_f_dtu_enable')]},
                    'dtu_2': {
                        'menu': self.page.locator('#Span_setup_serial_tdsetup_dtu2'),
                        'wait_locator': [self.frame.locator('#_f_dtu_enable')]},
                    'dtu_3': {
                        'menu': self.page.locator('#Span_setup_serial_tdsetup_dtu3'),
                        'wait_locator': [self.frame.locator('#_f_dtu_enable')]}
                },
                'io': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_serial_io')],
                    'visible_locator': [self.content_span_text('io')],
                    'status': {
                        'menu': self.page.locator('#Span_status_serial_io_tdstatus_serial_io'),
                        'wait_locator': [self.frame.locator('#io-title')]},
                    'i/o_control': {
                        'menu': self.page.locator('#Span_status_serial_io_tdsetup_serial_io_vg9'),
                        'wait_locator': [self.frame.locator('#_digital_input_up1')]}},
                '1_wire': {
                    'default': 'status',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#status_1wire')],
                    'visible_locator': [self.content_span_text('1_wire')],
                    'status': {
                        'menu': self.page.locator('#Span_status_1wire_tdstatus_1wire'),
                        'wait_locator': [self.frame.locator('#onewire-section')]}},
            },
            'tools': {
                'default': 'ping.ping',
                'menu': [self.tools_menu],
                'ping': {
                    'default': 'ping',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#tools_ping')],
                    'visible_locator': [self.content_span_text('ping')],
                    'ping': {
                        'menu': self.page.locator('#Span_tools_ping_tdtools_ping'),
                        'visible_locator': [self.frame.locator('#_f_addr')],
                        'wait_locator': [self.frame.locator('#_f_addr')]}},
                'traceroute': {
                    'default': 'traceroute',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#tools_trace')],
                    'visible_locator': [self.content_span_text('traceroute')],
                    'traceroute': {
                        'menu': self.page.locator('#Span_tools_trace_tdtools_trace'),
                        'visible_locator': [self.frame.locator('#_f_addr')],
                        'wait_locator': [self.frame.locator('#_f_addr')]}},
                'tcpdump': {
                    'default': 'tcpdump',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#tools_tcpdump')],
                    'visible_locator': [self.content_span_text('tcpdump')],
                    'tcpdump': {
                        'menu': self.page.locator('#Span_tools_tcpdump_tdtools_tcpdump'),
                        'visible_locator': [self.frame.locator('#_f_iface')],
                        'wait_locator': [self.frame.locator('#_f_iface')]}},
                'link_speed_test': {
                    'default': 'link_speed_test',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#tools_speed')],
                    'visible_locator': [self.content_span_text('link_speed')],
                    'link_speed_test': {
                        'menu': self.page.locator('#Span_tools_speed_tdtools_speed'),
                        'visible_locator': [self.frame.locator('#speed-up-button')],
                        'wait_locator': [self.frame.locator('#speed-up-button')]}},

            },
            'wizards': {
                'default': 'new_lan.new_lan',
                'menu': [self.wizards_menu],
                'new_lan': {
                    'default': 'new_lan',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_lan')],
                    'visible_locator': [self.content_span_text('new_lan')],
                    'new_lan': {
                        'menu': self.page.locator('#Span_wizards_lan_tdwizards_lan'),
                        'visible_locator': [self.frame.locator('#_f_iface')],
                        'wait_locator': [self.frame.locator('#_f_iface')]}},
                'new_wan': {
                    'default': 'new_wan',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_wan0')],
                    'visible_locator': [self.content_span_text('new_wan')],
                    'new_wan': {
                        'menu': self.page.locator('#Span_wizards_wan0_tdwizards_wan0'),
                        'visible_locator': [self.frame.locator('#_f_iface')],
                        'wait_locator': [self.frame.locator('#_f_iface')]}},
                'new_cellular': {
                    'default': 'new_cellular',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_wan1')],
                    'visible_locator': [self.content_span_text('new_cellular')],
                    'new_cellular': {
                        'menu': self.page.locator('#Span_wizards_wan1_tdwizards_wan1'),
                        'visible_locator': [self.frame.locator('#_wan1_ppp_para')],
                        'wait_locator': [self.frame.locator('#_wan1_ppp_para')]}},
                'new_ipsec_tunnel': {
                    'default': 'new_ipsec_tunnel',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_ipsec')],
                    'visible_locator': [self.content_span_text('new_ipsec_tunnel')],
                    'new_ipsec_tunnel': {
                        'menu': self.page.locator('#Span_wizards_ipsec_tdwizards_ipsec'),
                        'visible_locator': [self.frame.locator('#_f_tunnel_id')],
                        'wait_locator': [self.frame.locator('#_f_tunnel_id')]}},
                'ipsec_expert_config': {
                    'default': 'ipsec_expert_config',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_ipsec_expert_conf')],
                    'visible_locator': [self.content_span_text('ipsec_expert')],
                    'ipsec_expert_config': {
                        'menu': self.page.locator('#Span_wizards_ipsec_expert_conf_tdwizards_ipsec_expert_conf'),
                        'visible_locator': [self.frame.locator('#secrets_import')],
                        'wait_locator': [self.frame.locator('#secrets_import')]}},
                'new_l2tpv2_tunnel': {
                    'default': 'new_l2tpv2_tunnel',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_l2tp')],
                    'visible_locator': [self.content_span_text('l2tpv2')],
                    'new_l2tpv2_tunnel': {
                        'menu': self.page.locator('#Span_wizards_l2tp_tdwizards_l2tp'),
                        'visible_locator': [self.frame.locator('#_f_tunnel_id')],
                        'wait_locator': [self.frame.locator('#_f_tunnel_id')]}},
                'new_port_mapping': {
                    'default': 'new_port_mapping',
                    'mouse_move': (200, 0),
                    'menu': [self.page.locator('#wizards_portmapping')],
                    'visible_locator': [self.content_span_text('new_port_m')],
                    'new_port_mapping': {
                        'menu': self.page.locator('#Span_wizards_portmapping_tdwizards_portmapping'),
                        'visible_locator': [self.frame.locator('#_f_proto')],
                        'wait_locator': [self.frame.locator('#_f_proto')]}},
            }}
