# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 15:58:44
# @Author  : Pane Li
# @File    : _ir3XX_contents_locators.py
"""
_ir3XX_contents_locators

"""
from playwright.sync_api import Locator, Page


class Ir3XXContentsLocators:

    def __init__(self, page: Page, language='en', model='ir302'):
        """

        :param page:
        :param language:
        :param model:  该文件适配ir302、ir305、ir615型号
        """
        self.page = page
        self.frame = self.page.frame_locator('#content-window_content')
        self.language = language
        self.model = model.upper()
        if language == 'en':
            self.__locale: dict = {'filtering': 'Filtering',
                                   'device_access_filtering': 'Device Access Filtering',
                                   'port_mapping': 'Port Mapping',
                                   'modem': 'Modem', 'network_connections': 'Network Connections',
                                   'traffic_statistics': 'Traffic Statistics',
                                   'device_manager': 'Device Manager', 'third_party': 'Third Party Software Notices'
                                   }
        else:
            self.__locale: dict = {'filtering': '访问控制',
                                   'device_access_filtering': '设备访问控制',
                                   'port_mapping': '端口映射',
                                   'modem': 'Modem状态', 'network_connections': '网络连接',
                                   'traffic_statistics': '流量状态',
                                   'device_manager': '远程管理平台', 'third_party': '第三方软件声明'
                                   }

    @property
    def system_menu(self) -> Locator:
        return self.page.locator('#system')

    @property
    def network_menu(self) -> Locator:
        return self.page.locator('#network')

    @property
    def services_menu(self) -> Locator:
        return self.page.locator('#services')

    @property
    def firewall_menu(self) -> Locator:
        return self.page.locator('#fw')

    @property
    def qos_menu(self) -> Locator:
        return self.page.locator('#qos')

    @property
    def vpn_menu(self) -> Locator:
        return self.page.locator('#vpn')

    @property
    def tools_menu(self) -> Locator:
        return self.page.locator('#tools')

    @property
    def application_menu(self) -> Locator:
        return self.page.locator('#app_portal')

    @property
    def status_menu(self) -> Locator:
        return self.page.locator('#stat')

    @property
    def tags_menu(self) -> dict:
        return {
            'system': {
                'default': 'basic_setup',
                'menu': [self.system_menu],
                'basic_setup': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_system'),
                    'visible_locator': [self.frame.locator('#_language')],
                    'wait_locator': [self.frame.locator('#_language')]},
                'time': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_time'),
                    'visible_locator': [self.frame.locator('#_tm_sel')],
                    'wait_locator': [self.frame.locator('#_tm_sel')]},
                'serial_port': {   # 只有615 有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_com'),
                    'visible_locator': [self.frame.locator('#_f_com0_baud')],
                    'wait_locator': [self.frame.locator('#_f_com0_baud')]},
                'admin_access': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#admin_access'),
                    'visible_locator': [self.frame.locator('#adm-grid')],
                    'wait_locator': [self.frame.locator('#adm-grid')]},
                'admin_log': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#admin_log'),
                    'visible_locator': [self.frame.locator('#_f_log_remote')],
                    'wait_locator': [self.frame.locator('#_f_log_remote')]},
                'config_management': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#admin_config'),
                    'visible_locator': [self.frame.locator('#hw-reset-disable')],
                    'wait_locator': [self.frame.locator('#hw-reset-disable')]},
                'scheduler': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#admin_sched'),
                    'visible_locator': [self.frame.locator('#_f_cron_rb_enable')],
                    'wait_locator': [self.frame.locator('#_f_cron_rb_enable')]},
                'reboot': {
                    'menu': self.page.locator('#reboot')},
                'logout': {
                    'menu': self.page.locator('#logout')},
            },
            'network': {
                'default': 'cellular',
                'menu': [self.network_menu],
                'cellular': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_wan1'),
                    # 'visible_locator': [self.frame.locator('#_f_wan1_enable')],
                    'wait_locator': [self.frame.locator('#_f_wan1_enable')]},
                'wan/lan_switch': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_wan0"),
                    'visible_locator': [self.frame.locator('#_wan0_lan_mode')],
                    'wait_locator': [self.frame.locator('#_wan0_lan_mode')]},
                'wan(sta)': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_wan2"),
                    'visible_locator': [self.frame.locator('#_wan2_proto')],
                    'wait_locator': [self.frame.locator('#_wan2_proto')]},
                'lan': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_lan0"),
                    'visible_locator': [self.frame.locator('#_lan0_proto')],
                    'wait_locator': [self.frame.locator('#_lan0_proto')]},
                'vlan': {                                     # IR305 、IR615有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_vlan"),
                    'visible_locator': [self.frame.locator('#vlan-grid')],
                    'wait_locator': [self.frame.locator('#vlan-grid')]},
                'switch_wlan_mode': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_switchmode"),
                    'visible_locator': [self.frame.locator('#_wl0_ap')],
                    'wait_locator': [self.frame.locator('#_wl0_ap')]},
                'wlan': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_wl0"),
                    'visible_locator': [self.frame.locator('#_f_wl0_enable')],
                    'wait_locator': [self.frame.locator('#_f_wl0_enable')]},
                'wlan_client': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_wlclient0"),
                    'visible_locator': [self.frame.locator('#_f_wl0_enable')],
                    'wait_locator': [self.frame.locator('#_f_wl0_enable')]},
                'link_backup': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#link_backup"),
                    'visible_locator': [self.frame.locator('#_f_linkbackup_enable')],
                    'wait_locator': [self.frame.locator('#_f_linkbackup_enable')]},
                'vrrp': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#service_vrrpd"),
                    'visible_locator': [self.frame.locator('#_f_vrrpd0_enable')],
                    'wait_locator': [self.frame.locator('#_f_vrrpd0_enable')]},
                'ip_passthrough': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_ippass"),
                    'visible_locator': [self.frame.locator('#_f_passthrough_enable')],
                    'wait_locator': [self.frame.locator('#_f_passthrough_enable')]},
                'static_route': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#route_static"),
                    'visible_locator': [self.frame.locator('#route-grid')],
                    'wait_locator': [self.frame.locator('#route-grid')]},
                'ospf': {          # IR305 、IR615有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator("#setup_ospf"),
                    'visible_locator': [self.frame.locator('#_f_ospf_enable')],
                    'wait_locator': [self.frame.locator('#_f_ospf_enable')]},
            },
            'services': {
                'default': 'dhcp_service',
                'menu': [self.services_menu],
                'dhcp_service': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dhcpd'),
                    # 'visible_locator': [self.frame.locator('#_f_dhcpd_enable')],
                    'wait_locator': [self.frame.locator('#_f_dhcpd_enable')]},
                'dns': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_dns'),
                    'visible_locator': [self.frame.locator('#_f_dns_1')],
                    'wait_locator': [self.frame.locator('#_f_dns_1')]},
                'dns_relay': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dnsrelay'),
                    'visible_locator': [self.frame.locator('#dnsrelay-grid')],
                    'wait_locator': [self.frame.locator('#dnsrelay-grid')]},
                'ddns': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#setup_ddns'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text='DDNS')],
                    'wait_locator': [self.page.locator('#content-window_top', has_text='DDNS')]},
                'device_manager': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_mqtt'),
                    'visible_locator': [self.frame.locator('#_mqtt_enable')],
                    'wait_locator': [self.frame.locator('#_mqtt_enable')]},
                'device_manager_legacy': {  # 只有IR615有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_ovdp'),
                    'visible_locator': [self.frame.locator('#_f_ovdp_mode')],
                    'wait_locator': [self.frame.locator('#_f_ovdp_mode')]},
                'snmp': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_snmpd'),
                    'visible_locator': [self.frame.locator('#_f_snmpd_enable')],
                    'wait_locator': [self.frame.locator('#_f_snmpd_enable')]},
                'snmptrap': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_snmptrap'),
                    'visible_locator': [self.frame.locator('#snmptrap-grid')],
                    'wait_locator': [self.frame.locator('#snmptrap-grid')]},
                'i/o': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_io'),
                    'visible_locator': [self.frame.locator('#io-input-title')],
                    'wait_locator': [self.frame.locator('#io-input-title')]},
                'dtu_rs232': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dtu'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text='DTU RS232')],
                    'wait_locator': [self.page.locator('#content-window_top', has_text='DTU RS232')]},
                'dtu_rs485': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dtu'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text='DTU RS232')],
                    'wait_locator': [self.page.locator('#content-window_top', has_text='DTU RS232')]},
                'dtu': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dtu'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text='DTU')],
                    'wait_locator': [self.page.locator('#content-window_top', has_text='DTU')]},
                'sms': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_sms'),
                    'visible_locator': [self.frame.locator('#acl-grid')],
                    'wait_locator': [self.frame.locator('#acl-grid')]},
                'traffic_manager': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_traffic'),
                    'visible_locator': [self.frame.locator('#_f_tra_enable')],
                    'wait_locator': [self.frame.locator('#_f_tra_enable')]},
                'alarm_manager': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_alarm'),
                    'visible_locator': [self.frame.locator('#alarm-input-title')],
                    'wait_locator': [self.frame.locator('#alarm-input-title')]},
                'user_experience_plan': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_experience'),
                    'visible_locator': [self.frame.locator('#_mqtt_experience_mode')],
                    'wait_locator': [self.frame.locator('#_mqtt_experience_mode')]},
            },
            'firewall': {
                'default': 'basic',
                'menu': [self.firewall_menu],
                'basic': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_basic'),
                    # 'visible_locator': [self.frame.locator('#_f_strict')],
                    'wait_locator': [self.frame.locator('#_f_strict')]},
                'filtering': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_acl'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('filtering'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('filtering'))]},
                'device_access_filtering': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_sys_acl'),
                    'visible_locator': [self.page.locator('#content-window_top',
                                                          has_text=self.__locale.get('device_access_filtering'))],
                    'wait_locator': [self.page.locator('#content-window_top',
                                                       has_text=self.__locale.get('device_access_filtering'))]},
                'content_filtering': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_content'),
                    'visible_locator': [self.frame.locator('#webfilter-grid')],
                    'wait_locator': [self.frame.locator('#webfilter-grid')]},
                'port_mapping': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_portmap'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('port_mapping'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('port_mapping'))]},
                'virtual_ip_mapping': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_vip'),
                    'visible_locator': [self.frame.locator('#vip-grid')],
                    'wait_locator': [self.frame.locator('#vip-grid')]},
                'dmz': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_dmz'),
                    'visible_locator': [self.frame.locator('#_f_dmz_enable')],
                    'wait_locator': [self.frame.locator('#_f_dmz_enable')]},
                'mac_ip_bundling': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_mac'),
                    'visible_locator': [self.frame.locator('#bs-grid')],
                    'wait_locator': [self.frame.locator('#bs-grid')]},
                'nat': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#fw_nat'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text='NAT')],
                    'wait_locator': [self.page.locator('#content-window_top', has_text='NAT')]},
            },
            'qos': {
                'default': 'ip_bw_limit',
                'menu': [self.qos_menu],
                'ip_bw_limit': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#qos_ratelimit'),
                    # 'visible_locator': [self.frame.locator('#_f_qos_enable')],
                    'wait_locator': [self.frame.locator('#_f_qos_enable')]}},
            'vpn': {
                'default': 'ipsec_settings',
                'menu': [self.vpn_menu],
                'ipsec_settings': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#ipsec_basic'),
                    # 'visible_locator': [self.frame.locator('#_f_ipsec_debug')],
                    'wait_locator': [self.frame.locator('#_f_ipsec_debug')]},
                'ipsec_tunnels': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#ipsec_tunnels'),
                    'visible_locator': [self.frame.locator('#ipsec-grid')],
                    'wait_locator': [self.frame.locator('#ipsec-grid')]},
                'gre_tunnels': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#gre_tunnels'),
                    'visible_locator': [self.frame.locator('#gre-grid')],
                    'wait_locator': [self.frame.locator('#gre-grid')]},
                'l2tp_clients': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#l2tpc_tunnels'),
                    'visible_locator': [self.frame.locator('#l2tpc-grid')],
                    'wait_locator': [self.frame.locator('#l2tpc-grid')]},
                'pptp_clients': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#pptpc_tunnels'),
                    'visible_locator': [self.frame.locator('#pptpc-grid')],
                    'wait_locator': [self.frame.locator('#pptpc-grid')]},
                'openvpn_tunnels': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#openvpn_tunnels'),
                    'visible_locator': [self.frame.locator('#openvpn-grid')],
                    'wait_locator': [self.frame.locator('#openvpn-grid')]},
                'openvpn_advanced': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#openvpn_advanced'),
                    'visible_locator': [self.frame.locator('#muser-grid')],
                    'wait_locator': [self.frame.locator('#muser-grid')]},
                'certificate_management': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#cert_mgr'),
                    'visible_locator': [self.frame.locator('#_f_scep_enable')],
                    'wait_locator': [self.frame.locator('#_f_scep_enable')]},
                'wireguard_tunnels': {      # IR305 、IR615有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#wireguard_tunnels'),
                    'visible_locator': [self.frame.locator('#wireguard-grid')],
                    'wait_locator': [self.frame.locator('#wireguard-grid')]},
                'zerotier_vpn': {      # IR305 、IR615有该菜单
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#zerotier_tunnels'),
                    'visible_locator': [self.frame.locator('#_f_zerotier_enable')],
                    'wait_locator': [self.frame.locator('#_f_zerotier_enable')]},
            },
            'tools': {
                'default': 'ping',
                'menu': [self.tools_menu],
                'ping': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#tools_ping'),
                    # 'visible_locator': [self.frame.locator('#pingb')],
                    'wait_locator': [self.frame.locator('#pingb')]},
                'traceroute': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#tools_trace'),
                    'visible_locator': [self.frame.locator('#traceb')],
                    'wait_locator': [self.frame.locator('#traceb')]},
                'link_speed_test': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#tools_speed'),
                    'visible_locator': [self.frame.locator('#speed-up-button')],
                    'wait_locator': [self.frame.locator('#speed-up-button')]},
                'tcpdump': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#tools_tcpdump'),
                    'visible_locator': [self.frame.locator('#tcpdumpb')],
                    'wait_locator': [self.frame.locator('#tcpdumpb')]},
            },
            'application': {
                'default': 'smart_atm',
                'menu': [self.application_menu],
                'smart_atm': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_atm'),
                    # 'visible_locator': [self.frame.locator('#mserver-grid')],
                    'wait_locator': [self.frame.locator('#mserver-grid')]},
                'status_report': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_rmon'),
                    'visible_locator': [self.frame.locator('#_f_rmon_enable')],
                    'wait_locator': [self.frame.locator('#_f_rmon_enable')]},
                'smart_ems': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#service_dls'),
                    'visible_locator': [self.frame.locator('#_dls_url')],
                    'wait_locator': [self.frame.locator('#_dls_url')]}},
            'status': {
                'default': 'system',
                'menu': [self.status_menu],
                'system': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_system'),
                    # 'visible_locator': [self.frame.locator('#memory')],
                    'wait_locator': [self.frame.locator('#memory')]},
                'modem': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_modem'),
                    'visible_locator': [self.page.locator('#content-window_top', has_text=self.__locale.get('modem'))],
                    'wait_locator': [self.page.locator('#content-window_top', has_text=self.__locale.get('modem'))]},
                'traffic_statistics': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_traffic'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('traffic_statistics'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('traffic_statistics'))]},
                'alarm': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_alarm'),
                    'visible_locator': [self.frame.locator('#alarmlog-grid')],
                    'wait_locator': [self.frame.locator('#alarmlog-grid')]},
                'wlan': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_sta'),
                    'visible_locator': [self.frame.locator('#ap-grid')],
                    'wait_locator': [self.frame.locator('#ap-grid')]},
                'network_connections': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_networks'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('network_connections'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('network_connections'))]},
                'device_manager': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_mqtt'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('device_manager'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('device_manager'))]},
                'route_table': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_route'),
                    'visible_locator': [self.frame.locator('#route-grid')],
                    'wait_locator': [self.frame.locator('#route-grid')]},
                'device_list': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_devices'),
                    'visible_locator': [self.frame.locator('#dev-grid')],
                    'wait_locator': [self.frame.locator('#dev-grid')]},
                'log': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#status_log'),
                    'visible_locator': [self.frame.locator('#_f_lines')],
                    'wait_locator': [self.frame.locator('#_f_lines')]},
                'third_party_software_notices': {
                    'mouse_move': (300, 0),
                    'menu': self.page.locator('#opensource'),
                    'visible_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('third_party'))],
                    'wait_locator': [
                        self.page.locator('#content-window_top', has_text=self.__locale.get('third_party'))]},

            }}
