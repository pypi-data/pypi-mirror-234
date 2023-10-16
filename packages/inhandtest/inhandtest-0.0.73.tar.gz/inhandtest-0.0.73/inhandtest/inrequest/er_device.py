# -*- coding: utf-8 -*-
# @Time    : 2023/7/6 18:26:55
# @Author  : Pane Li
# @File    : er_device.py
"""
er_device

"""
import random
import re
import time
from typing import List
from inhandtest.inrequest.er_default_config import *
from inhandtest.inrequest.inrequest import *
from inhandtest.exception import ResourceNotFoundError, TimeOutError
from inhandtest.tools import dict_flatten


class ErRequest(InRequest):

    def send_request(self, path, method, param=None, body=None, expect=None, file_path=None,
                     params_type='json', header=None, code=200, auth=True, url=None):

        def switch_config(in_payload: dict) -> dict:
            """转换配置，当配置中的key是随机id时， 可使用$id, 然后该函数会自动替换成随机id并返回

            :param in_payload: 需要修正的配置项，其中需要更新的key 使用$id来替换
            :return:
            """

            def _uuid():
                def _random():
                    result = hex(random.randint(0, 16 ** 4)).replace('0x', '')
                    if len(result) < 4:
                        result = '0' * (4 - len(result)) + result
                    return result

                return '0' + _random()[1:] + hex(int(time.time())).replace('0x', '') + _random()

            in_payload = str(in_payload)
            for i in range(0, len(re.findall('\$id', in_payload))):
                in_payload = in_payload.replace('$id', _uuid(), 1)
            return eval(in_payload)

        body = switch_config(body) if body else body
        return super().send_request(path, method, param, body, expect, file_path, params_type, header, code, auth)


class ErDevice:
    def __init__(self, username, password, host, protocol='https', port='443', model='ER805'):
        """
        :param username: 设备用户名
        :param password: 设备密码
        :param protocol: http|https
        :param host: 设备IP
        :param model: 设备型号, 默认ER805
        """
        self.username = username
        self.password = password
        self.protocol = protocol
        self.host = host
        self.port = port
        self.model = model
        self.api = ErRequest(host=self.host, username=self.username, password=self.password, type_='device',
                             protocol=self.protocol, port=self.port, device_model=self.model)
        self.default_config = er_default_config

    @property
    def path_url(self) -> dict:
        """
        :return: 返回设备的url
        """
        return {'import_firmware': '/api/v1/import/firmware',
                'import_config': '/api/v1/config/import',
                'upgrade_config': '/api/v1/config/update',
                'upgrade_firmware': '/api/v1/upgrade',
                'config_backup': '/api/v1/config/backup',
                'config_url': '/api/v1/config',
                'status_url': '/api/v1/status/',
                'login': '/api/v1/user/login',
                'basic': '/api/v1/basic',
                'diagnose': '/api/v1/diagnose',
                'download': '/api/v1/syslog/download',
                'events_url': '/api/v1/events/get',
                'adjust_url': '/api/v1/data_usage/adjust'}

    @property
    def basic(self) -> dict:
        """获取设备基本信息

            "language": "English",
            "model": "EAP600-LITE",
            "hostname": "EAP600",
            "oem": "inhand",
            "features": [
                "wlan"
            ],
            "firmware": "V2.0.2-beta.2",
            "modem_version": "",
            "bootloader": "1.0.0",
            "serial_number": "AL6002325WH5ROZ",
            "mac": "00:18:05:2B:5D:03",
            "firm_size_max": 52428800

        :return: 返回设备基本信息

        """
        return self.api.send_request(self.path_url.get('basic'), method='get').json().get('result')

    def get_config(self, fields: str, expect: dict = None) -> dict:
        """

        :param expect: 对期望的内容做判断，以字典形式传入，注意匹配大小写并保证key和value的值需完全匹配
        :param fields: cellular| wlan_ap| lan| switch_port| data_usage| wan| clients| system| ntp| data_usage| l2tp| ipsec|
                         可根据配置层级使用.来获取，例'cellular.modem'，
                         也可使用逗号分隔获取多个状态，例'wlan_ap,lan,wlan_sta'
        """
        return self.api.send_request(self.path_url.get('config_url'), method='get',
                                     param={'fields': fields}, expect=expect).json().get('result').get('config')

    def get_status(self, path: str):
        """获取设备状态

        :param path: cellular| wlan_ap| lan| wan| system| signal_history_info| data_usage| ipsec| l2tp|
        """
        return self.api.send_request(f"{self.path_url.get('status_url')}{path}", method='get').json().get('result')

    def assert_status(self, path: str, expect: dict, timeout=30, interval=5):
        """校验设备状态

        :param path: cellular| wlan_ap| lan| wan| system| signal_history_info| data_usage| ipsec| l2tp|
        :param expect: 期望的状态，以字典形式传入，注意匹配大小写并保证key和value的值需完全匹配
        :param timeout: 超时时间
        :param interval: 检查间隔
        """
        if expect:
            device_status = ''
            for i in range(0, timeout, interval):
                try:
                    device_status = self.get_status(path).get(path)
                    dict_in(device_status, expect)
                    break
                except AssertionError:
                    time.sleep(interval)
            else:
                logging.exception(f"the device status {expect} check failed, real status: {device_status}")
                raise TimeOutError(f"the device status {expect} check failed")

    def get_uuid_config(self, fields: str, condition: dict, not_none=False) -> List or None:
        """根据条件返回当前配置的uuid


        :param fields: cellular| wlan_ap| lan| static_route4| uplink| wan| admin| system| ntp| data_usage| record| alerts|
                         ipsec| email| ippt| l2tp| link_quality| uplink| dhcp| admin_access| firewall| policy_route| qos|
                         port_mapping| wlan_sta| switch_port
                         可根据配置层级使用.来获取，例'cellular.modem'，不可获取多个配置项
                         传参时需写到uuid前一级
        :param condition: 查找uuid的条件，以字典形式传入，注意匹配大小写并保证key和value的值需完全匹配
                            例当需要查找ssid=test且band=2.4G的wifi时可传入{'ssid': 'test', 'band': '2.4G'}
                例当需要匹配qos中interface=wan1的uuid时
                         "qos": {"uplink_rules":
                         {"0000f0804da7846f": {
                         "interface": "wan1",
                         "egress_rate": "0Mbps",
                         "ingress_rate": "0Mbps"}
                         fields传参为'qos.uplink_rules'，condition传参为{'interface': 'wan1'}
        :param not_none: True| False, 为True如果匹配不到uuid则返回['$id', {}], 为False如果匹配不到则返回None
        :return: 如存在uuid则返回uuid及匹配的config，否则返回None
        """
        config = self.get_config(fields)
        con = (fields, condition)
        try:
            for k in con[0].split('.'):
                config = config.get(k)
            for uuid_, v in config.items():
                for ex_k, ex_v in con[1].items():
                    if v.get(ex_k) != ex_v:
                        break
                else:
                    id_ = uuid_
                    config_ = v
                    break
            else:
                if not_none:
                    id_ = '$id'
                    config_ = None
                    logging.info('not find uuid, return $id')
                else:
                    raise ResourceNotFoundError('not find uuid, please check the condition')
        except Exception:
            if not_none:
                id_ = '$id'
                config_ = None
                logging.info('not find uuid, return $id')
            else:
                raise ResourceNotFoundError('not find key, please check the fields')
        if not not_none:
            logging.info(f'find the matched uuid: {id_}')
        return [id_, config_]

    def wifi_ap(self, ssid: str, band: str, action: str, **kwargs):
        """编辑wifi ap

        :param ssid: 编辑和删除时填入操作前的ssid, 添加时填入新的ssid
        :param band: '2.4g'| '5g' 频段 编辑和删除时填入操作前的频段, 添加时填入新的频段
        :param action: 'edit'| 'add'| 'delete' 编辑\添加\删除, 添加和删除只对副wifi有效
        :param kwargs: ssid|enabled|auth|key|encrypt|ap_isolate|vlan|channel
                        new_ssid: 新的ssid, 添加和删除时不需要填写
                        enabled: True| False 启用或者禁用
                        key: 密码, 添加ap时密码为必填项, 8-63 characters,support letters, numbers, special characters
                        auth: 'WPA2-PSK'|'OPEN'|'WPA-PSK'|'WPA-PSK/WPA2-PSK' 安全方式,只支持大写
                        encrypt: 'CCMP'|'CCMP/TKIP' 加密方式,只支持大写
                        vlan: int, 默认为1
                        channel: 信道，只能在主wifi中编辑 'Auto'或数字
                        ap_isolate: True| False 启用或者禁用
        :return:
        """
        wlan_ap = self.get_config('wlan_ap').get('wlan_ap')
        band = band.upper()
        is_primary = False
        body = {}
        if kwargs.get('new_ssid'):
            kwargs.update({'ssid': kwargs.pop('new_ssid')})
        if action in ('edit', 'delete'):
            try:
                config_ap = self.get_uuid_config('wlan_ap', {'ssid': ssid, 'band': band})
                if config_ap[1].get('channel'):
                    is_primary = True
                if action == 'edit':
                    config_ap[1].update(kwargs)
                    body = {'wlan_ap': {config_ap[0]: config_ap[1]}}
                elif action == 'delete':
                    config_ap[1] = None
                    body = {'wlan_ap': {config_ap[0]: config_ap[1]}}
                    if is_primary:
                        raise ParameterValueError('the primary wifi can not be deleted')
                else:
                    pass
            except Exception:
                raise ParameterValueError(f'the ssid:{ssid} and band:{band} is not exist')
        else:
            # 添加时先获取已有ap的name
            list_2_4 = [v.get('name') for k, v in wlan_ap.items() if 'wlan1' in v.get('name')]
            list_5 = [v.get('name') for k, v in wlan_ap.items() if 'wlan2' in v.get('name')]
            try:
                if band == '2.4G':
                    name = [un_name for un_name in ('wlan1.1', 'wlan1.2', 'wlan1.3') if un_name not in list_2_4][0]
                else:
                    name = [un_name for un_name in ('wlan2.1', 'wlan2.2', 'wlan2.3') if un_name not in list_5][0]
            except IndexError:
                raise ParameterValueError(f'the {band} wifi is full')
            config_ap = self.default_config.get('wlan_ap').get(band)
            config_ap.update(kwargs)
            config_ap.update({'ssid': ssid, 'band': band, 'name': name})
            body = {'wlan_ap': {'$id': config_ap}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body,
                              expect={'result': 'ok'})
        logging.info(f'{action} wifi {band} {ssid}  ap success')

    def config_wan(self, interface='wan1', status='enable', **kwargs):
        """
        :param interface: 'wan1'|'wan2'
        :param status: 'enable'|'disable'|'delete'
        :kwargs: dict
                nat: True| False
                mtu: int
                ipv4:
                    dhcpc: True | False
                    ip: str
                    prefix_len: int, 0-32, 掩码长度
                    gateway: str
                    dns1: str
                    dns2: str
                pppoe:
                    enabled: True| False
                    username: str
                    password: str
                    local_ip: str
                    remote_ip: str
        """
        try:
            config_wan = self.get_uuid_config('wan', {'name': interface})
        except ResourceNotFoundError:
            config_wan = ['$id', self.default_config.get('wan').get(interface)]
        if status == 'enable':
            kwargs.update({'enabled': True})
            if kwargs.get('ipv4'):  # 改为ipv4时  清除原来的pppoe配置
                kwargs.update({'pppoe': {'enabled': False}})
            config_wan[1].update(kwargs)
            body = {'wan': {config_wan[0]: config_wan[1]}}
        elif status in ('disable', 'delete'):
            if config_wan[0] == '$id':
                raise ParameterValueError(f'wan {interface} is not exist')
            else:
                if status == 'disable':
                    body = {'wan': {config_wan[0]: {'enabled': False}}}
                else:
                    body = {'wan': {config_wan[0]: None}}
        else:
            raise ParameterValueError(f'status:{status} is not support')
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{status} wan {interface} success')

    def config_wifi_sta(self, status='enable', **kwargs):
        """编辑wifi_sta

        :param status: 'enable'|'disable'|'delete'
        :param kwargs: dict
                    band: '2.4G'|'5G'
                    ssid: str
                    mtu: int
                    nat: True| False
                    auth: 'OPEN'|'WPA-PSK'|'WPA2-PSK'|'WPAWPA2-PSK'
                    encrypt: 'CCMP'|'CCMP-TKIP'
                    key: str, 密码
                    ipv4:
                        dhcpc: True | False
                        ip: str
                        prefix_len: int, 0-32, 掩码长度
                        gateway: str
                        dns1: str
                        dns2: str
        """
        config_wlan = ['wlan_sta', self.get_config('wlan_sta').get('wlan_sta')] if self.get_config('wlan_sta').get(
            'wlan_sta') else ['$id', self.default_config.get('wlan_sta')]
        if status == 'enable':
            kwargs.update({'enabled': True})
            config_wlan[1].update(kwargs)
            body = {config_wlan[0].replace('$id', 'wlan_sta'): config_wlan[1]}
        elif status in ('disable', 'delete'):
            if config_wlan[0] == '$id':
                raise ParameterValueError(f'wlan_sta is not exist')
            else:
                if status == 'disable':
                    body = {config_wlan[0].replace('$id', 'wlan_sta'): {'enabled': False}}
                else:
                    body = {config_wlan[0].replace('$id', 'wlan_sta'): None}
        else:
            raise ParameterValueError(f'status:{status} is not support')
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{status} wlan_ap success')

    def mac_filter(self, mac: str = None, action: str = None, **kwargs):
        """编辑mac地址过滤

        :param mac: str, 新增和删除时必填, 只变更过滤模式可为None
        :param action: 'edit'|'add'|'delete', 只变更过滤模式可为None
        :param kwargs: new_mac| action| mode| desc
                        new_mac: str, 编辑时填入新的mac地址,新增和删除时不填
                        mode: 'none'|'blacklist'| 'whitelist', 过滤模式, 无限制|黑名单|白名单, 支持只变更过滤模式,
                        desc: str, 描述
        """
        body = {}
        if mac and action and action in ('edit', 'delete'):
            config_mac_filter = self.get_uuid_config('mac_filter.mac_list', {'mac': mac})
            if action == 'edit':
                info = {'mac': kwargs.get('new_mac') if kwargs.get('new_mac') else '',
                        'desc': kwargs.get('desc') if kwargs.get('desc') else ''}
                config_mac_filter[1].update(info)
                body = {'mac_filter': {'mac_list': {config_mac_filter[0]: config_mac_filter[1]}}}
            elif mac and action and action == 'delete':
                config_mac_filter[1] = None
                body = {'mac_filter': {'mac_list': {config_mac_filter[0]: config_mac_filter[1]}}}
            else:
                raise ParameterValueError(f'action:{action} is not support')
        else:
            if mac and action and action == 'add':
                config_mac_filter = {'mac': mac, 'desc': kwargs.get('desc') if kwargs.get('desc') else ''}
                body = {'mac_filter': {'mac_list': {'$id': config_mac_filter}}}
        if 'mode' in kwargs.keys():
            if body:
                body.get('mac_filter').update({'mode': kwargs.get('mode')})
                action = 'change_mode'
            else:
                body = {'mac_filter': {'mode': kwargs.get('mode')}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body,
                              expect={'result': 'ok'})
        logging.info(f'{action} mac_filter success')

    def config_cellular(self, **kwargs):
        """
        :param kwargs: dict
                    cellular: dict, cellular配置
                        modem:dict
                            enabled: True| False, 使能
                            dual_sim:dict 双卡策略
                                enabled: True| False
                                main_sim: 'sim1'|'sim2'
                            sim1:dict sim1模式配置
                                profile: 策略配置, 'auto'|0, 当不为auto时就传0
                                network_type: 'auto'|'g2'|'g3'|'g4'|'g5'|'g5_g4', 网络类型, 自动|2G|3G|4G|5G|4G及5G
                                nr5g_mode: 'sa'|'nsa'|'sa-nsa', 5G模式, sa|nsa|sa-nsa
                                pin_code: str, 四位PIN码
                                pdp_type: 'ipv4'|'ipv6'|'ipv4v6', PDP范围: ipv4,ipv6,ipv4v6
                                ims: 'auto'|'enable'|'disable'
                            sim2:dict sim2模式配置
                                profile: 策略配置, 'auto'|1, 当不为auto时就传1
                                network_type: 'auto'|'g2'|'g3'|'g4'|'g5'|'g5_g4', 网络类型, 自动|2G|3G|4G|5G|4G及5G
                                nr5g_mode: 'sa'|'nsa'|'sa-nsa', 5G模式, sa|nsa|sa-nsa
                                pin_code: str, 四位PIN码
                                pdp_type: 'ipv4'|'ipv6'|'ipv4v6', PDP范围: ipv4,ipv6,ipv4v6
                                ims: 'auto'|'enable'|'disable'
                            ipv4:dict 掩码配置
                                prefix_len: int, 0-32, 掩码长度
                            mtu: int
                            nat: True| False
                            profile:dict
                                0:dict sim1的策略配置
                                    type: str, 'ipv4'
                                    apn: str
                                    access_num: str, "*99***1#"
                                    auth: auto|pap|chap|ms-chap|ms-chapv2
                                    username: str, 用户名
                                    password: str, 密码
                                1:dict sim2的策略配置
                                    type: str, 'ipv4'
                                    apn: str
                                    access_num: str, "*99***1#"
                                    auth: auto|pap|chap|ms-chap|ms-chapv2
                                    username: str, 用户名
                                    password: str, 密码
                    data_usage:dict 流量策略配置
                        sim1:dict sim1流量策略配置
                            monthly_data_plan:dict
                                enabled: True| False
                                threshold: int, 阈值
                                threshold_unit: 单位, 'GB'|'MB'|'KB'
                                start_date: int, 计算流量起始日期, 1-31
                                over_threshold_oper: 'alert'|'switch-sim'|'cloud', 超过阈值操作, 通知|切换卡|仅保持云管理功能
                        sim2:dict sim2流量策略配置
                            monthly_data_plan:
                                enabled: True| False
                                threshold: int, 阈值
                                threshold_unit: 单位, 'GB'|'MB'|'KB'
                                start_date: int, 计算流量起始日期, 1-31
                                over_threshold_oper: 'alert'|'switch-sim'|'cloud', 超过阈值操作, 通知|切换卡|仅保持云管理功能
                    adjust_usage:dict 流量使用调整
                        sim1:dict, sim1流量使用调整
                            adjust_usage_unit: 'GB'|'MB'|'KB'
                            adjust_usage: int
                        sim2:dict sim2流量使用调整
                            adjust_usage_unit: 'GB'|'MB'|'KB'
                            adjust_usage: str

        """

        if 'adjust_usage' in kwargs.keys():
            config_adjust_usage = kwargs.get('adjust_usage')
            self.api.send_request(self.path_url.get('adjust_url'), method='post', body=config_adjust_usage,
                                  expect={'result': 'ok'})
            logging.info(f'config adjust usage success')
        if kwargs.get('cellular'):
            config_cellular = kwargs.get('cellular')
        else:
            config_cellular = {}
        if 'cellular:modem:dual_sim:enabled' in dict_flatten(kwargs).keys():
            if dict_flatten(kwargs).get('cellular:modem:dual_sim:enabled'):
                config_data_usage = {
                    'sim1': {'monthly_data_plan': {'over_threshold_oper': 'switch-sim'}},
                    'sim2': {'monthly_data_plan': {'over_threshold_oper': 'switch-sim'}}}
            else:
                config_data_usage = {
                    'sim1': {'monthly_data_plan': {'over_threshold_oper': 'alert'}},
                    'sim2': {'monthly_data_plan': {'over_threshold_oper': 'alert'}}}
        else:
            config_data_usage = {}
        if kwargs.get('data_usage'):
            config_data_usage.update(kwargs.get('data_usage'))
        body = {'cellular': config_cellular, 'data_usage': config_data_usage}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'config cellular success')

    def config_uplink(self, **kwargs):
        """

        :param kwargs: dict
                    mode: 'failover'|'load-balance', 链路备份|负载均衡
                    down_delay: int, -1, 0, 5-60, 延迟切换, 默认0s(立即切换)，-1表示不切换
                    link_detect: 探测地址
                        target: str, 探测地址
                        target2: str, 探测地址
                    interface: dict, 链路优先级
                        wan1:dict
                            priority: int
                        cellular1:dict
                            priority: int
                        wan2:dict
                            priority: int
                        wlan-sta:dict
                            priority: int

        """
        uplink = {}
        if kwargs.get('interface'):
            interface = {}
            for k, v in kwargs.get('interface').items():
                try:
                    config_interface_ = self.get_uuid_config('uplink.interface', {'name': k})
                    interface.update({config_interface_[0]: {'name': k, 'priority': v.get('priority')}})
                except ResourceNotFoundError:
                    logging.info(f'interface {k} not found')
            uplink.update({'interface': interface})
            kwargs.pop('interface')
        uplink.update(kwargs)
        body = {'uplink': uplink}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'config uplink success')

    def config_lan(self, alias: str, action: str, **kwargs):
        """配置lan

        :param alias: str, lan名称
        :param action: str, 'edit'|'add'|'delete'
        :param kwargs: dict
                    lan:dict
                        new_alias: 新的lan名称, action为edit时需要
                        vlan: int, vlan id, 1-4094
                        mtu: int
                        l3_vlan: bool, True|False, IP Mode|vlan only mode
                        guest: bool, True|False, guest|standard
                        ipv4:dict
                            ip: str
                            prefix_len: int, 0-32, 掩码长度
                    dhcp:dict
                        server:dict
                            enabled: bool, True|False
                            lease: int, 租期, 1-86400
                            ip_pool:dict
                                start_ip: str
                                end_ip: str
                            option:dict
                                dns_type: 'auto'|'manual', 自动获取|手动配置
                                dns1: str
                                dns2: str
                    当只传dhcp且action为edit时，可只修改dhcp配置, dhcp配置的alias与lan的alias一致, 且不可修改, dhcp配置只能修改不能添加或删除
        """
        is_default = False
        body = {}
        if kwargs.get('lan'):
            if 'new_alias' in kwargs.get('lan').keys():
                kwargs.get('lan').update({'alias': kwargs.get('lan').pop('new_alias')})
                kwargs.get('dhcp').get('server').update({'alias': kwargs.get('lan').get('alias')}) if kwargs.get(
                    'dhcp') else kwargs.update({'dhcp': {'server': {'alias': kwargs.get('lan').get('alias')}}})
            if 'vlan' in kwargs.get('lan').keys():
                kwargs.get('lan').update({'name': f'vlan{kwargs.get("lan").get("vlan")}'})
                kwargs.get('dhcp').get('server').update(
                    {'interface': f'vlan{kwargs.get("lan").get("vlan")}'}) if kwargs.get('dhcp') else kwargs.update(
                    {'dhcp': {'server': {'interface': f'vlan{kwargs.get("lan").get("vlan")}'}}})
        if action in ('edit', 'delete'):
            try:
                lan_config = self.get_uuid_config('lan', {'alias': alias})
                dhcp_config = self.get_uuid_config('dhcp.server', {'alias': alias})
                if lan_config[1].get('vlan') == 1:
                    is_default = True
                if action == 'edit':
                    if kwargs.get('lan'):
                        lan_config[1].update(kwargs.get('lan'))
                    if kwargs.get('dhcp'):
                        dhcp_config[1].update(kwargs.get('dhcp').get('server'))
                    body = {'lan': {lan_config[0]: lan_config[1]}, 'dhcp': {'server': {dhcp_config[0]: dhcp_config[1]}}}
                elif action == 'delete':
                    body = {'lan': {lan_config[0]: None}, 'dhcp': {'server': {dhcp_config[0]: None}}}
                    if is_default:
                        raise ParameterValueError('default lan can not be deleted')
                else:
                    pass
            except ResourceNotFoundError:
                raise ResourceNotFoundError(f'lan {alias} not found')
        else:
            lan_config = self.default_config.get('lan')
            lan_config.update({'alias': alias})
            lan_config.update(kwargs.get('lan'))
            dhcp_config = self.default_config.get('dhcp').get('server')
            dhcp_config.update({'alias': alias})
            dhcp_config.update(kwargs.get('dhcp').get('server'))
            body = {'lan': {'$id': lan_config}, 'dhcp': {'server': {'$id': dhcp_config}}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{action} lan {alias} success')

    def config_route(self, destination: str, next_hop: dict, action: str, **kwargs):
        """配置静态路由

        :param destination: str, 目的地址, 格式'0.0.0.0/0'
        :param next_hop: dict
                        type: str
                        distance: int
                        interface: str, 下一跳接口, type为gateway时不填
                        gateway: str, 下一跳网关, type为interface时不填
        :param action: str, 'edit'|'add'|'delete'
        :param kwargs: dict
                    new_destination: str, 新目的地址, 格式'0.0.0.0/0'
                    desc: str, 描述
                    new_next_hop: dict
                        type: str, 'interface'|'gateway', 新下一跳类型
                        distance: int, 1-255
                        interface: None or str, 下一跳接口, type为gateway时传None, None|wan1|wan2|cellular1|wlan-sta|l2tp接口
                        gateway: None or str, 下一跳网关, type为interface时传None
        """
        body = {}
        if kwargs.get('new_destination'):
            kwargs.update({'destination': kwargs.pop('new_destination')})
        if kwargs.get('new_next_hop'):
            kwargs.update({'next_hop': kwargs.pop('new_next_hop')})
        if action in ('edit', 'delete'):
            try:
                route_config = self.get_uuid_config('static_route4',
                                                    {'destination': destination, 'next_hop': next_hop})
                if action == 'edit':
                    route_config[1].update(kwargs)
                    body = {'static_route4': {route_config[0]: route_config[1]}}
                elif action == 'delete':
                    body = {'static_route4': {route_config[0]: None}}
                else:
                    pass
            except ResourceNotFoundError:
                raise ResourceNotFoundError(f'route {destination} not found')
        else:
            route_config = self.default_config.get('static_route4')
            route_config.update({'destination': destination, 'next_hop': next_hop})
            route_config.update(kwargs)
            body = {'static_route4': {'$id': route_config}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{action} route {destination} success')

    def config_ipsec(self, name: str, action: str, **kwargs):
        """配置ipsec

        :param name: str, ipsec名称
        :param action: str, 'edit'|'add'|'delete'
        :param kwargs:
                    new_name: str, 新ipsec名称
                    ike_version: str, 'ikev1'|'ikev2'
                    enabled: bool, True|False
                    key: str, psk
                    interface: str, 接口, 'wan1'|'wan2'|'cellular1'|'wlan-sta'
                    peeraddr: str, 对端地址
                    mode: str, 'tunnel'|'transport'
                    local_subnet: list, ['0.0.0.0/0'], 本地网段, 最大支持4个
                    remote_subnet: list, ['0.0.0.0/0'], 对端网段, 最大支持4个
                    ike_policy: dict
                            encrypt: str, 'aes128'|'aes256'|'3des'|'des'|'aes192'
                            auth: str, 'md5'|'sha1'|'sha256'|'sha384'|'sha512'
                            dh: int, 1|2|5|14|15|16|19|20|21|24
                            lifetime: int, 1200-86400
                    ipsec_policy: dict
                            sec_protocol: str, 'esp'|'ah'
                            encrypt: str, 'aes128'|'aes256'|'3des'|'des'|'aes192'
                            auth: str, 'md5'|'sha1'|'sha256'|'sha384'|'sha512'
                            pfs: str, 'none'|'1'|'2'|'5'|'14'|'15'|'16'|'19'|'20'|'21'|'24'
                            lifetime: int, 1200-86400
        """
        body = {}
        if kwargs.get('new_name'):
            kwargs.update({'name': kwargs.pop('new_name')})
        if action in ('edit', 'delete'):
            try:
                ipsec_config = self.get_uuid_config('ipsec', {'name': name})
                if action == 'edit':
                    ipsec_config[1].update(kwargs)
                    body = {'ipsec': {ipsec_config[0]: ipsec_config[1]}}
                elif action == 'delete':
                    body = {'ipsec': {ipsec_config[0]: None}}
                else:
                    pass
            except ResourceNotFoundError:
                raise ResourceNotFoundError(f'ipsec {name} not found')
        else:
            ipsec_config = self.default_config.get('ipsec')
            ipsec_config.update({'name': name})
            ipsec_config.update(kwargs)
            body = {'ipsec': {'$id': ipsec_config}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'{action} ipsec {name} success')

    def config_l2tp(self, character: str, **kwargs):
        """配置l2tp

        :param character: str, 'server'|'client'
        :param kwargs: dict
                当character为server时传如下参数:
                    enabled: bool, True|False
                    ip: str, vpn连接虚拟地址
                    start_ip:str, 开始ip
                    end_ip: str, 结束ip
                    interface: str, 接口, 'any'|'wan1'|'wan2'|'cellular1'|'wlan-sta'
                    username: str, 用户名
                    password: str, 密码
                    ppp_auth: str, 'auto'|'pap'|'chap'
                    tunnel_auth: dict
                        enabled: bool, True|False
                        server: str, 认证服务器地址
                        password: str, 密码
                当character为client时传如下参数:
                    alias: str, 隧道名称
                    action:str, 'add'|'edit'|'delete'
                    clients:dict
                        new_alias: str, 新隧道名称, 新增和删除时不传, 编辑时选传
                        enabled: bool, True|False
                        nat: bool, True|False
                        interface: str, 接口, 'any'|'wan1'|'wan2'|'cellular1'|'wlan-sta'
                        server_ip: str, 连接的服务器IP
                        username: str, 用户名
                        password: str, 密码
                        ppp_auth: str, 'auto'|'pap'|'chap'
                        tunnel_auth: dict
                            enabled: bool, True|False
                            server: str, 认证服务器地址
                            password: str, 密码
        """
        body = None
        if character == 'server':
            l2tp_server = self.default_config.get('l2tp').get('server')
            l2tp_server.update(kwargs)
            body = {'l2tp': {'server': l2tp_server}}
        else:
            if kwargs.get('alias') and kwargs.get('action'):
                if kwargs.get('clients') and 'new_alias' in kwargs.get('clients'):
                    kwargs.get('clients').update({'alias': kwargs.get('clients').pop('new_alias')})
                if kwargs.get('action') in ('edit', 'delete'):
                    try:
                        l2tp_client = self.get_uuid_config('l2tp.clients', {'alias': kwargs.get('alias')})
                        if kwargs.get('action') == 'edit':
                            l2tp_client[1].update(kwargs.get('clients'))
                            body = {'l2tp': {'clients': {l2tp_client[0]: l2tp_client[1]}}}
                        elif kwargs.get('action') == 'delete':
                            body = {'l2tp': {'clients': {l2tp_client[0]: None}}}
                        else:
                            pass
                    except ResourceNotFoundError:
                        raise ResourceNotFoundError(f'l2tp client {kwargs.get("alias")} not found')
                else:
                    l2tp_now = self.get_config('l2tp.clients').get('l2tp').get('clients')
                    l2tp_list = [v.get('name') for k, v in l2tp_now.items() if 'l2tp' in v.get('name')]
                    un_name = \
                        [un_name_ for un_name_ in [f'l2tp{i}' for i in range(1, 10)] if un_name_ not in l2tp_list][0]
                    l2tp_client = self.default_config.get('l2tp').get('clients')
                    l2tp_client.update(kwargs.get('clients'))
                    l2tp_client.update({'alias': kwargs.get('alias'), 'name': un_name})
                    body = {'l2tp': {'clients': {'$id': l2tp_client}}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'config l2tp {character} success')

    def config_inbound_default(self, action: str):
        """配置防火墙入站默认规则

        :param action: str, 'permit'|'deny'
        """
        body = {'firewall': {'inbound_default': {'action': action}}}
        self.api.send_request(self.path_url.get('config_url'), method='put', body=body, expect={'result': 'ok'})
        logging.info(f'config inbound default {action} success')


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    device = ErDevice('adm', '123456', '192.168.2.1')
    # device.config_l2tp(character='server', enabled=True, ip='2.2.2.2', start_ip='2.2.2.1', end_ip='2.2.2.254',
    #                    interface='cellular1', username='adm', password='123456', ppp_auth='chap',
    #                    tunnel_auth={'enabled': True, 'server':'3.3.3.3', 'password':'123456'})
    a = device.get_uuid_config(fields='ltp.client', condition={'interface': 'any'}, not_none=True)
    print(a)

    # device.config_l2tp(character='client', alias='test4', action='edit',
    #                    clients={'enabled': False, 'nat': False, 'server_ip': '5.5.5.5', 'username': 'test',
    #                             'password': '789456', 'new_alias': 'test5', 'interface': 'wan1', 'ppp_auth': 'pap',
    #                             'tunnel_auth': {'enabled': True, 'server': '6.6.6.6', 'password': '789456'}})
    # print(device.get_status('wlan_sta'))
