# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/9/20 14:41
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : contents_locators.py
@IDE     : PyCharm
------------------------------------
"""
import os
import dynaconf
from inhandtest.exception import ModelError
from playwright.sync_api import Locator, Page

contents = dynaconf.Dynaconf(
    settings_files=[os.path.join(os.path.dirname(__file__), 'contents_locale.yaml')])


class ContentsLocators:

    def __init__(self, page: Page, language='en', model='EAP600'):
        """

        :param page:
        :param language:
        """
        self.page = page
        self.model = model.upper()
        self.locale = contents.get(language)

    @property
    def __er(self) -> dict:
        return {"user_info_button": self.page.locator('.ant-dropdown-trigger.action___LP4_P.account___6HXOq'),
                "logout_button": self.page.locator('.anticon.anticon-logout'),
                "language_button": self.page.locator('i svg'),
                "dashboard_menu": self.page.locator(f'a:has-text("{self.locale.get("dashboard")}")'),
                "status_menu": self.page.locator(f'a:has-text("{self.locale.get("status")}")'),
                "internet_menu": self.page.locator(f'a:has-text("Internet")'),
                "local_network_menu": self.page.locator(f'a:has-text("{self.locale.get("local_network")}")'),
                "wifi_menu": self.page.locator(f'a:has-text("Wi-Fi")'),
                "vpn_menu": self.page.locator(f'a:has-text("VPN")'),
                "security_menu": self.page.locator(f'a:has-text("{self.locale.get("security")}")'),
                "services_menu": self.page.locator(f'a:has-text("{self.locale.get("services")}")'),
                "system_menu": self.page.locator(f'a:has-text("{self.locale.get("system")}")'),
                "config_menu": self.page.locator(f'a:has-text("{self.locale.get("config")}")'),
                "china_option": self.page.locator(f'text=🇨🇳简体中文'),
                "english_option": self.page.locator(f'text=🇺🇸English'),
                }

    @property
    def __ig(self) -> dict:
        return {"overview_menu": self.page.locator('//a[@href="/overview"]'),
                'network_menu': self.page.locator('//a[@href="/network"]'),
                'edge_menu': self.page.locator('//li[@role="menuitem"]/a[@href="/edge-computing"]'),
                'system_menu': self.page.locator('//li[@role="menuitem"]/a[@href="/system"]'),
                'network_interface_menu': self.page.locator(f'div:text-is("{self.locale.get("network_interface")}")'),
                'cellular_menu': self.page.locator(f'a:has-text("{self.locale.get("cellular")}")'),
                'ethernet_menu': self.page.locator(f'a:has-text("{self.locale.get("ethernet")}")'),
                'bridge_menu': self.page.locator(f'a:has-text("{self.locale.get("bridge")}")'),
                'wlan_menu': self.page.locator('a:has-text("WLAN")'),
                'loopback_menu': self.page.locator(f'a:has-text("{self.locale.get("loopback")}")'),
                'wan_menu_502': self.page.locator('a:has-text("WAN")'),
                'lan_menu_502': self.page.locator('a:has-text("LAN")'),
                'network_service_menu': self.page.locator(f'div:text-is("{self.locale.get("network_service")}")'),
                'dhcp_menu': self.page.locator(f'a:has-text("{self.locale.get("dhcp")}")'),
                'dns_menu': self.page.locator(f'a:has-text("{self.locale.get("dns")}")'),
                'gps_menu': self.page.locator('a:has-text("GPS")'),
                'host_list_menu': self.page.locator(f'a:has-text("{self.locale.get("host_list")}")'),
                'routing_menu': self.page.locator(f'div:text-is("{self.locale.get("routing")}")'),
                'routing_status_menu': self.page.locator(f'a:has-text("{self.locale.get("routing_status")}")'),
                'routing_static_menu': self.page.locator(f'a:has-text("{self.locale.get("routing_static")}")'),
                'firewall_menu': self.page.locator(f'div:text-is("{self.locale.get("firewall")}")'),
                'acl_menu': self.page.locator(f'a:has-text("{self.locale.get("acl")}")'),
                'nat_menu': self.page.locator(f'a:has-text("{self.locale.get("nat")}")'),
                'vpn_menu': self.page.locator('div:text-is("VPN")'),
                'l2tp_menu': self.page.locator('a:has-text("L2TP")'),
                'python_edge_menu': self.page.locator(f'a:has-text("{self.locale.get("python_edge")}")'),
                'docker_manager_menu': self.page.locator(f'a:has-text("{self.locale.get("docker_manager")}")'),
                'cloud_edge_computing_menu': self.page.locator(
                    f'a:has-text("{self.locale.get("cloud_edge_computing")}")'),
                'azure_iot_edge_menu': self.page.locator('div:text-is("Azure IoT Edge")'),
                'aws_iot_greengrass_menu': self.page.locator('div:text-is("AWS IoT Greengrass")'),
                'device_supervisor_menu': self.page.locator(f'div:text-is("{self.locale.get("device_supervisor")}")'),
                'measure_monitor_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("measure_monitor")}")'),
                'alarm_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("alarm")}")'),
                'cloud_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("cloud")}")'),
                'protocol_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("protocol")}")'),
                'parameter_settings_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("parameter_settings")}")'),
                'custom_quickfunctions_menu': self.page.locator(
                    f'.ant-menu.ant-menu-sub.ant-menu-inline >> a:has-text("{self.locale.get("custom_quickfunctions")}")'),
                'system_time_menu': self.page.locator(f'a:has-text("{self.locale.get("system_time")}")'),
                'system_log_menu': self.page.locator(f'a:has-text("{self.locale.get("system_log")}")'),
                'system_config_menu': self.page.locator(f'a:has-text("{self.locale.get("system_config")}")'),
                'system_cloud_menu': self.page.locator(f'a:has-text("{self.locale.get("system_cloud")}")'),
                'system_firmware_menu': self.page.locator(f'a:has-text("{self.locale.get("system_firmware")}")'),
                'system_tools_menu': self.page.locator(f'a:has-text("{self.locale.get("system_tools")}")'),
                'system_user_management_menu': self.page.locator(
                    f'a:has-text("{self.locale.get("system_user_management")}")'),
                'system_reboot_menu': self.page.locator(f'a:has-text("{self.locale.get("system_reboot")}")'),
                'system_network_tools_menu': self.page.locator(
                    f'a:has-text("{self.locale.get("system_network_tools")}")'),
                'system_3rd_party_menu': self.page.locator(f'a:has-text("{self.locale.get("system_3rd_party")}")')
                }

    def content_target(self, locale) -> Locator:
        if self.locale.get(locale):
            locale = self.locale.get(locale)
        return self.page.locator(f'//span[@class="ant-breadcrumb-link"]/span[text()="{locale}"]')

    @property
    def tags_menu(self) -> dict:
        if self.model in ('ER805', 'ER605', 'EAP600', 'ODU2002'):
            return {
                'dashboard': {
                    'menu': self.__er.get('dashboard_menu'),
                    'visible_locator': [
                        self.page.locator(f'//div[text()="{self.locale.get("device_information")}"]')],
                    'wait_locator': [self.page.locator(f'//div[text()="{self.locale.get("device_information")}"]')]},
                'status': {
                    'menu': self.__er.get('status_menu'),
                    'link_monitor': {
                        'menu': self.page.locator(
                            f'div[role="tab"]:text-is("{self.locale.get("link_monitoring")}")')},
                    'cell_signal': {
                        'menu': self.page.locator(
                            f'div[role="tab"]:text-is("{self.locale.get("cellular_signal")}")')},
                    'clients': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("clients")}")')},
                    'vpn_status': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("VPN")'),
                        'ipsec_status': {
                            'menu': self.page.locator(f'div[role="tab"]:text-is("IPsec")')},
                        'l2tp_status': {
                            'menu': self.page.locator(f'div[role="tab"]:text-is("L2TP")')}},
                    'events': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("events")}")')},
                    'logs': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("logs")}")')}},
                'internet': {
                    'menu': self.__er.get('internet_menu'),
                    'visible_locator': [self.page.locator(f'//span[text()="{self.locale.get("uplink_table")}"]')],
                    'wait_locator': [self.page.locator(f'//span[text()="{self.locale.get("uplink_table")}"]')]},
                'local_network': {'menu': self.__er.get('local_network_menu')},
                'wifi': {
                    'menu': self.__er.get('wifi_menu'),
                    'ssids': {'menu': self.page.locator(f'div[role="tab"]:text-is("SSIDs")')},
                    'portal': {'menu': self.page.locator(f'div[role="tab"]:text-is("Portal")')},
                    'ssid_24g': {'menu': self.page.locator(f'div[role="tab"]:text-is("2.4G SSID")')},
                    'ssid_5g': {'menu': self.page.locator(f'div[role="tab"]:text-is("5G SSID")')}},
                'config': {
                    'menu': self.__er.get('config_menu'),
                    'wan': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("WAN")'),
                        'visible_locator': [self.page.locator("#ip")],
                        'wait_locator': [self.page.locator("#ip")]},
                    'lan': {'menu': self.page.locator(f'div[role="tab"]:text-is("LAN")')},
                    'radio': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("radio")}")'),
                        'visible_locator': [
                            self.page.locator(f'//div[text()="{self.locale.get("radio_setting")}"]')],
                        'wait_locator': [self.page.locator(f'//div[text()="{self.locale.get("radio_setting")}"]')]}},
                'vpn': {
                    'menu': self.__er.get('vpn_menu'),
                    'ipsec': {'menu': self.page.locator(f'div[role="tab"]:text-is("IPsec")')},
                    'l2tp': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("L2TP")'),
                        'visible_locator': [self.page.locator('#enabled')],
                        'wait_locator': [self.page.locator('#enabled')],
                        'l2tp_server': {
                            'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("server")}")'),
                            'visible_locator': [self.page.locator('#enabled')],
                            'wait_locator': [self.page.locator('#enabled')]},
                        'l2tp_client': {
                            'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("client")}")')}},
                    'vxlan': {'menu': self.page.locator(f'div[role="tab"]:text-is("VXLAN VPN")')}},
                'security': {
                    'menu': self.__er.get('security_menu'),
                    'visible_locator': [self.page.locator('//div[text()="Default"]')],
                    'wait_locator': [self.page.locator('//div[text()="Default"]')],
                    'firewall': {
                        'menu': self.page.locator(f'div[role="tab"]:text-is("{self.locale.get("firewall")}")'),
                        'visible_locator': [self.page.locator('//div[text()="Default"]')],
                        'wait_locator': [self.page.locator('//div[text()="Default"]')],
                        'inbound': {
                            'menu': self.page.locator(
                                f'div[role="tab"]:text-is("{self.locale.get("inbound_rules")}")'),
                            'visible_locator': [self.page.locator('//div[text()="Default"]')],
                            'wait_locator': [self.page.locator('//div[text()="Default"]')]},
                        'outbound': {
                            'menu': self.page.locator(
                                f'div[role="tab"]:text-is("{self.locale.get("outbound_rules")}")'),
                            'visible_locator': [self.page.locator('//div[text()="Default"]')],
                            'wait_locator': [self.page.locator('//div[text()="Default"]')]},
                        'port_forwarding': {
                            'menu': self.page.locator(
                                f'div[role="tab"]:text-is("{self.locale.get("port_forwarding")}")')},
                        'mac_filter': {
                            'menu': self.page.locator(
                                f'div[role="tab"]:text-is("{self.locale.get("mac_address_filter")}")')}},
                    'policy_routing': {
                        'menu': self.page.locator(
                            f'div[role="tab"]:text-is("{self.locale.get("policy_base_routing")}")')},
                    'traffic_shaping': {
                        'menu': self.page.locator(
                            f'div[role="tab"]:text-is("{self.locale.get("traffic_shaping")}")')}},
                'services': {
                    'menu': self.__er.get('services_menu')},
                'system': {
                    'menu': self.__er.get('system_menu')}
            }
        elif self.model in ('IG902', 'IG502'):
            return {
                'overview': {
                    'default': 'flow_usage_monitoring(day)',
                    'menu': self.__ig.get('overview_menu'),
                    'visible_locator': [self.page.locator(f'//div[text()="{self.locale.get("performance")}"]')],
                    'wait_locator': [self.page.locator(f'//div[text()="{self.locale.get("performance")}"]')],
                    'flow_usage_monitoring(day)': {
                        'menu': self.page.locator(f'div:text-is("{self.locale.get("flow_usage_day")}")'),
                        'attributes': {
                            self.page.locator(f'div:text-is("{self.locale.get("flow_usage_day")}")'): {
                                'aria-selected': 'true'}},
                    },
                    'flow_usage_monitoring(month)': {
                        'menu': self.page.locator(f'div:text-is("{self.locale.get("flow_usage_month")}")'),
                        'attributes': {
                            self.page.locator(f'div:text-is("{self.locale.get("flow_usage_month")}")'): {
                                'aria-selected': 'true'}},
                    }
                },
                'network': {
                    'default': 'network_interface.cellular',
                    'menu': self.__ig.get('network_menu'),
                    'visible_locator': [self.page.locator('//span[@class="ant-breadcrumb-link"]/a[@href="/network"]')],
                    'wait_locator': [self.content_target('cellular')],
                    'network_interface': {
                        'default': 'cellular',
                        'menu': self.__ig.get('network_interface_menu'),
                        'visible_locator': [self.__ig.get('cellular_menu')],
                        'wait_locator': [self.__ig.get('cellular_menu')],
                        'cellular': {
                            'menu': self.__ig.get('cellular_menu'),
                            'visible_locator': [self.content_target('cellular')],
                            'wait_locator': [self.content_target('cellular')]},
                        'ethernet': {
                            'default': 'gigabitethernet_0/1',
                            'menu': self.__ig.get('ethernet_menu'),
                            'visible_locator': [self.content_target('ethernet')],
                            'wait_locator': [self.content_target('ethernet')],
                            'gigabitethernet_0/1': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("gigabitethernet")} 0/1")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("gigabitethernet")} 0/1")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('#internet')],
                            },
                            'gigabitethernet_0/2': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("gigabitethernet")} 0/2")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("gigabitethernet")} 0/2")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [
                                    self.page.locator('.antd-pro-components-description-list-index-term').first],
                            }
                        },
                        'bridge': {
                            'menu': self.__ig.get('bridge_menu'),
                            'visible_locator': [self.content_target('bridge')],
                            'wait_locator': [self.content_target('bridge')]},
                        'wlan': {
                            'menu': self.__ig.get('wlan_menu'),
                            'visible_locator': [self.content_target('WLAN')],
                            'wait_locator': [self.content_target('WLAN')]},
                        'wan': {
                            'menu': self.__ig.get('wan_menu_502'),
                            'visible_locator': [self.content_target('WAN')],
                            'wait_locator': [self.content_target('WAN')]},
                        'lan': {
                            'menu': self.__ig.get('lan_menu_502'),
                            'visible_locator': [self.content_target('LAN')],
                            'wait_locator': [self.content_target('LAN')]},
                        'loopback': {
                            'menu': self.__ig.get('loopback_menu'),
                            'visible_locator': [self.content_target('loopback')],
                            'wait_locator': [self.content_target('loopback')]}},
                    # Network Services
                    'network_services': {
                        'menu': self.__ig.get('network_service_menu'),
                        'visible_locator': [self.__ig.get('dhcp_menu')],
                        'wait_locator': [self.__ig.get('dhcp_menu')],
                        'dhcp': {
                            'menu': self.__ig.get('dhcp_menu'),
                            'visible_locator': [self.content_target('dhcp')],
                            'wait_locator': [self.content_target('dhcp')]},
                        'dns': {
                            'menu': self.__ig.get('dns_menu'),
                            'visible_locator': [self.content_target('dns')],
                            'wait_locator': [self.content_target('dns')]},
                        'gps': {
                            'default': 'gps_configure',
                            'menu': self.__ig.get('gps_menu'),
                            'visible_locator': [self.content_target('gps')],
                            'wait_locator': [self.content_target('gps')],
                            'gps_configure': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("gps_configure")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("gps_configure")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-form-item-no-colon')],
                            },
                            'gps_ip_forwarding': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("gps_ip_forwarding")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("gps_ip_forwarding")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('#enable')],
                            },
                            'gps_serial_forwarding': {
                                'menu': self.page.locator(
                                    f'div:text-is("{self.locale.get("gps_serial_forwarding")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("gps_serial_forwarding")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('#enable')],
                            },
                        },
                        'host_list': {
                            'menu': self.__ig.get('host_list_menu'),
                            'visible_locator': [self.content_target('host_list')],
                            'wait_locator': [self.content_target('host_list')]}},
                    # Routing
                    'routing': {
                        'menu': self.__ig.get('routing_menu'),
                        'visible_locator': [self.__ig.get('routing_status_menu')],
                        'wait_locator': [self.__ig.get('routing_status_menu')],
                        'routing_status': {
                            'menu': self.__ig.get('routing_status_menu'),
                            'visible_locator': [self.content_target('routing_status')],
                            'wait_locator': [self.content_target('routing_status')]},
                        'static_routing': {
                            'menu': self.__ig.get('routing_static_menu'),
                            'visible_locator': [self.content_target('routing_static')],
                            'wait_locator': [self.content_target('routing_static')]}},
                    # Firewall
                    'firewall': {
                        'menu': self.__ig.get('firewall_menu'),
                        'visible_locator': [self.__ig.get('acl_menu')],
                        'wait_locator': [self.__ig.get('acl_menu')],
                        'acl': {
                            'menu': self.__ig.get('acl_menu'),
                            'visible_locator': [self.content_target('acl')],
                            'wait_locator': [self.content_target('acl')]},
                        'nat': {
                            'menu': self.__ig.get('nat_menu'),
                            'visible_locator': [self.content_target('nat')],
                            'wait_locator': [self.content_target('nat')]}},
                    # VPN
                    'vpn': {
                        'menu': self.__ig.get('vpn_menu'),
                        'visible_locator': [self.__ig.get('l2tp_menu')],
                        'wait_locator': [self.__ig.get('l2tp_menu')],
                        'l2tp': {
                            'default': 'status',
                            'menu': self.__ig.get('l2tp_menu'),
                            'status': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("status")}")'),
                                'attributes': {self.page.locator(f'div:text-is("{self.locale.get("status")}")'): {
                                    'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-spin-container').first],
                            },
                            'l2tp_client': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("l2tp_client")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("l2tp_client")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-spin-container').first]
                            },
                            'l2tp_service': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("l2tp_service")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("l2tp_service")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-spin-container').first]}
                        }
                    }
                },
                'edge_computing': {
                    'default': 'python_edge_computing',
                    'menu': self.__ig.get('edge_menu'),
                    'visible_locator': [
                        self.page.locator('//span[@class="ant-breadcrumb-link"]/a[@href="/edge-computing"]').last],
                    'wait_locator': [self.content_target('python_edge').last],
                    'python_edge_computing': {
                        'menu': self.__ig.get('python_edge_menu'),
                        'visible_locator': [self.content_target('python_edge').last],
                        'wait_locator': [self.content_target('python_edge').last]
                    },
                    'docker_manager': {
                        'menu': self.__ig.get('docker_manager_menu'),
                        'visible_locator': [self.content_target('docker_manager').nth(1)],
                        'wait_locator': [self.content_target('docker_manager').nth(1)]
                    },
                    'cloud_edge_computing': {
                        'default': 'azure_iot_edge',
                        'menu': self.__ig.get('cloud_edge_computing_menu'),
                        'visible_locator': [self.content_target('cloud_edge_computing').nth(1)],
                        'wait_locator': [self.content_target('cloud_edge_computing').nth(1)],
                        'azure_iot_edge': {
                            'menu': self.__ig.get('azure_iot_edge_menu'),
                            'attributes': {self.__ig.get('azure_iot_edge_menu'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@id="enable"]').first],
                        },
                        'aws_iot_greengrass': {
                            'menu': self.__ig.get('aws_iot_greengrass_menu'),
                            'attributes': {
                                self.__ig.get('aws_iot_greengrass_menu'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@id="enable"]').first],
                        }
                    },
                    # Device Supervisor
                    'device_supervisor': {
                        'default': 'measure_monitor.monitoring_list',
                        'menu': self.__ig.get('device_supervisor_menu'),
                        'visible_locator': [self.__ig.get('measure_monitor_menu')],
                        'wait_locator': [self.__ig.get('measure_monitor_menu')],
                        'measure_monitor': {
                            'default': 'monitoring_list',
                            'menu': self.__ig.get('measure_monitor_menu'),
                            'visible_locator': [self.content_target('measure_monitor')],
                            'monitoring_list': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("monitoring_list")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("monitoring_list")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-input-search-button').first],
                            },
                            'group': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("group")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("group")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('//i[@class="anticon anticon-plus-circle"]')],
                            },
                            'controller_template': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("controller_template")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("controller_template")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-table-header.ant-table-hide-scrollbar')],
                            },
                        },
                        'alarm': {
                            'default': 'realtime_alarms',
                            'menu': self.__ig.get('alarm_menu'),
                            'visible_locator': [self.content_target('alarm')],
                            'wait_locator': [self.content_target('alarm')],
                            'realtime_alarms': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("realtime_alarms")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("realtime_alarms")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-table-header.ant-table-hide-scrollbar')]
                            },
                            'alarm_rules': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("alarm_rules")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("alarm_rules")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [
                                    self.page.locator(f'span:text-is("{self.locale.get("trigger_condition")}")')]
                            },
                            'history_alarms': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("history_alarms")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("history_alarms")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('span:text-is("~")')]
                            },
                            'alarm_label': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("alarm_label")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("alarm_label")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('.ant-table-selection-column >> nth=0')]
                            },
                        },
                        'cloud': {
                            'default': 'mqtt_cloud_service',
                            'menu': self.__ig.get('cloud_menu'),
                            'visible_locator': [self.content_target('cloud')],
                            'wait_locator': [self.content_target('cloud')],
                            'mqtt_cloud_service': {
                                'menu': self.page.locator(f'div:text-is("{self.locale.get("mqtt_cloud_service")}")'),
                                'attributes': {
                                    self.page.locator(f'div:text-is("{self.locale.get("mqtt_cloud_service")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('//label[@for="enable.form"]')],
                                'cloud_measuring_setting': {
                                    'menu': self.page.locator('//i[contains(@class, "anticon")][@tabindex="-1"]').first,
                                    'visible_locator': [
                                        self.page.locator('.ant-modal-title', has_text=self.locale.get(
                                            'cloud_measuring_point_setting'))],
                                    'wait_locator': [
                                        self.page.locator('.ant-modal-content').locator('.ant-table-content')],
                                    'cloud': {
                                        'menu': self.page.locator(
                                            f'div:text-is("{self.locale.get("cloud_measuring_point")}")'),
                                        'attributes': {
                                            self.page.locator(
                                                f'div:text-is("{self.locale.get("cloud_measuring_point")}")'): {
                                                'aria-selected': 'true'}}
                                    },
                                    'muting': {
                                        'menu': self.page.locator(
                                            f'div:text-is("{self.locale.get("Muting_measuring_point")}")'),
                                        'attributes': {
                                            self.page.locator(
                                                f'div:text-is("{self.locale.get("Muting_measuring_point")}")'): {
                                                'aria-selected': 'true'}}
                                    },

                                }
                            },
                            'whiteeagle_energy_manager': {
                                'menu': self.page.locator(
                                    f'div:text-is("{self.locale.get("whiteeagle_energy_manager")}")'),
                                'attributes': {
                                    self.page.locator(
                                        f'div:text-is("{self.locale.get("whiteeagle_energy_manager")}")'): {
                                        'aria-selected': 'true'}},
                                'wait_locator': [self.page.locator('//label[@for="enable.form"]')]
                            }
                        },
                        'protocol': {
                            'default': 'modbus_tcp_slave',
                            'menu': self.__ig.get('protocol_menu'),
                            'visible_locator': [self.content_target('protocol')],
                            'wait_locator': [self.content_target('protocol')],
                            'modbus_tcp_slave': {
                                'menu': self.page.locator(f'div:text-is("Modbus TCP Slave")'),
                                'visible_locator': [
                                    self.page.locator(f'text=Modbus TCP Slave{self.locale.get("configuration")}')],
                                'wait_locator': [
                                    self.page.locator(f'text=Modbus TCP Slave{self.locale.get("configuration")}')],
                            },
                            'iec_104_server': {
                                'menu': self.page.locator(f'div:text-is("IEC 104 Server")'),
                                'visible_locator': [
                                    self.page.locator(f'text=IEC 104 Server{self.locale.get("configuration")}')],
                                'wait_locator': [
                                    self.page.locator(f'text=IEC 104 Server{self.locale.get("configuration")}')],
                            },
                            'opcua_server': {
                                'menu': self.page.locator(f'div:text-is("OPCUA Server")'),
                                'visible_locator': [
                                    self.page.locator(f'text=OPCUA Server{self.locale.get("configuration")}')],
                                'wait_locator': [
                                    self.page.locator(f'text=OPCUA Server{self.locale.get("configuration")}')],
                            },
                            'modbus_rtu_slave': {
                                'menu': self.page.locator(f'div:text-is("Modbus RTU Slave")'),
                                'visible_locator': [
                                    self.page.locator(f'text=Modbus RTU Slave{self.locale.get("configuration")}')],
                                'wait_locator': [
                                    self.page.locator(f'text=Modbus RTU Slave{self.locale.get("configuration")}')],
                            },
                        },
                        'parameter_settings': {
                            'menu': self.__ig.get('parameter_settings_menu'),
                            'visible_locator': [self.content_target('parameter_settings')],
                            'wait_locator': [self.page.locator('.ant-table-content')]
                        },
                        'custom_quickfunctions': {
                            'menu': self.__ig.get('custom_quickfunctions_menu'),
                            'visible_locator': [self.content_target('custom_quickfunctions')],
                            'wait_locator': [self.content_target('custom_quickfunctions')]}
                    }
                },
                'system': {
                    'default': 'system_time',
                    'menu': self.__ig.get('system_menu'),
                    'visible_locator': [self.page.locator('//span[@class="ant-breadcrumb-link"]/a[@href="/system"]')],
                    'wait_locator': [self.content_target('system_time')],
                    'system_time': {
                        'menu': self.__ig.get('system_time_menu'),
                        'visible_locator': [self.content_target('system_time')],
                        'wait_locator': [self.content_target('system_time')],
                    },
                    'log': {
                        'default': 'log',
                        'menu': self.__ig.get('system_log_menu'),
                        'visible_locator': [self.content_target('system_log')],
                        'wait_locator': [self.content_target('system_log')],
                        'log': {
                            'menu': self.page.locator('.ant-tabs-tab >> nth=0'),
                            'visible_locator': [
                                self.page.locator('//button', has_text=self.locale.get('clear_history_log'))],
                            'attributes': {
                                self.page.locator('.ant-tabs-tab >> nth=0'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@class="ant-btn"]').first],
                        },
                        'configure': {
                            'menu': self.page.locator('.ant-tabs-tab >> nth=1'),
                            'visible_locator': [self.page.locator('#log_to_remote_enable')],
                            'attributes': {
                                self.page.locator('.ant-tabs-tab >> nth=1'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('#log_to_remote_enable')],
                        }
                    },
                    'configuration_management': {
                        'menu': self.__ig.get('system_config_menu'),
                        'visible_locator': [self.page.locator('.ant-btn.ant-btn-danger')],
                        'wait_locator': [self.content_target('system_config')],
                    },
                    'inhand_cloud': {
                        'default': 'inhand_connect_service',
                        'menu': self.__ig.get('system_cloud_menu'),
                        'visible_locator': [self.content_target('system_cloud')],
                        'wait_locator': [self.content_target('system_cloud')],
                        'inhand_connect_service': {
                            'menu': self.page.locator(f'div:text-is("InHand Connect Service")'),
                            'attributes': {
                                self.page.locator(f'div:text-is("InHand Connect Service")'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@id="enable"]')],
                        },
                        'inhand_device_manager': {
                            'menu': self.page.locator(f'div:text-is("InHand Device Manager")'),
                            'attributes': {
                                self.page.locator(f'div:text-is("InHand Device Manager")'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@id="enable"]')],
                        },
                        'inhand_iscada_cloud': {
                            'menu': self.page.locator(f'div:text-is("InHand iSCADA Cloud")'),
                            'attributes': {
                                self.page.locator(f'div:text-is("InHand iSCADA Cloud")'): {'aria-selected': 'true'}},
                            'wait_locator': [self.page.locator('//button[@id="mode"]')],
                        }
                    },
                    'firmware_upgrade': {
                        'menu': self.__ig.get('system_firmware_menu'),
                        'visible_locator': [self.content_target('system_firmware')],
                        'wait_locator': [self.content_target('system_firmware')],
                    },
                    'access_tools': {
                        'menu': self.__ig.get('system_tools_menu'),
                        'visible_locator': [self.content_target('system_tools')],
                        'wait_locator': [self.content_target('system_tools')],
                    },
                    'user_management': {
                        'menu': self.__ig.get('system_user_management_menu'),
                        'visible_locator': [self.content_target('system_user_management')],
                        'wait_locator': [self.content_target('system_user_management')],
                    },
                    'reboot': {
                        'menu': self.__ig.get('system_reboot_menu'),
                        'visible_locator': [self.content_target('system_reboot')],
                        'wait_locator': [self.content_target('system_reboot')],
                    },
                    'network_tools': {
                        'menu': self.__ig.get('system_network_tools_menu'),
                        'visible_locator': [self.content_target('system_network_tools')],
                        'wait_locator': [self.content_target('system_network_tools')],
                    },
                    '3rd_party_notification': {
                        'menu': self.__ig.get('system_3rd_party_menu'),
                        'attributes': {
                            self.__ig.get('system_3rd_party_menu').locator('..'): {'class': 'ant-menu-item-selected'}},
                        'wait_locator': [self.content_target('system_3rd_party')],
                    }
                },
            }
        else:
            raise ModelError(f'not support this mode {self.model} device access menu')
