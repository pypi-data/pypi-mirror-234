# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 9:23:56
# @Author  : Pane Li
# @File    : inrequest.py
"""
封装request， 使设备和平台都能来正常调用，统一入口，token过期时也能自动更新

"""
from typing import List
from inhandtest.tools import replace_str
from inhandtest.exception import TimeOutError, ResourceNotFoundError, UpgradeFailedError
from inhandtest.inrequest.inrequest import InRequest
import logging
import time
import os
import re


class DmInterface:

    def __init__(self, username, password, host='iot.inhand.com.cn', proxy=False, headers=None):
        """
        :param username  平台用户名
        :param password  平台密码
        :param host: 'iot.inhand.com.cn'|'iot.inhandnetworks.com' 平台是哪个环境,
        """
        self.host = host
        self.username = username
        type_ = 'iot' if ('iot' in self.host) or ('elms' in self.host) else 'ics'
        self.api = InRequest(self.host, username, password, type_, proxy=proxy, headers=headers)

    def me(self) -> dict:
        """获取用户信息

        :return:
        """
        response = self.api.send_request('/api2/users/this', method='get', param={'verbose': 100})
        return response.json().get('result')

    def get_model_id(self, model: str) -> str or None:
        result = self.api.send_request('api/models', method='get', param={"verbose": 15, "limit": 0}).json()
        for model_info in result.get('result'):
            if model_info.get('name') == model:
                return model_info.get('_id')
        else:
            return None

    def device_exist(self, sn: str, timeout=120, interval=5) -> None:
        """检查设备在平台账号下存在，如果超时都不存在就抛异常

        :param sn:
        :param timeout:
        :param interval:
        :return:
        """
        for i in range(0, timeout, interval):
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn})
            if response.json().get('total') == 1:
                logging.debug(f'check {sn} device exist')
                break
            logging.info(f'check {sn} device is not exist, please wait for {interval}s')
            time.sleep(interval)
        else:
            logging.exception(f'{self.host} {self.username} account not found device {sn}')
            raise TimeOutError(f'{self.host} {self.username} account not found device {sn}')

    def device_state(self, sn: list) -> List[dict]:
        """根据sn 转换属性 属性值有：  online: 在线|离线   1|0
                                       iccid:
                                       imei:
                                       imsi:
                                       model: 设备型号
                                       version: 固件版本
                                       hwVersion: 硬件版本 'V1.0'
                                       bootVersion:  Bootloader版本  '1.1.3.r4956'
                                       sn: 序列号
                                       address
                                       id: 设备id
                                       name: 设备名字
                                       ip: 设备连接平台的ip地址
                                       protocol: 设备连接平台的协议
                                       config_sync: 设备配置同步状态
        :param sn: 列表
        :return: [{'sn': $sn, 'online': 1, 'iccid': '', 'imei'}]
        """
        result = []
        for sn_ in sn:
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn_}).json()
            if response.get('total') == 1:
                res = response.get('result')[0]
                config_sync = res.get('config').get('sync') if res.get('config') else None
                result.append(
                    {'sn': sn_, 'online': res.get('online'), 'iccid': res.get('info').get('iccid'),
                     'imei': res.get('info').get('imei'), 'imsi': res.get('info').get('imsi'),
                     'version': res.get('info').get('swVersion'), 'hwVersion': res.get('info').get('hwVersion'),
                     'bootVersion': res.get('info').get('bootVersion'), 'address': res.get('address'),
                     'id': res.get('_id'), 'name': res.get('name'), 'ip': res.get('pubIp'),
                     'protocol': res.get('protocol'), 'config_sync': config_sync, 'model': res.get('model')})
            else:
                result.append(
                    {'sn': sn_, 'online': None, 'iccid': None, 'imei': None, 'imsi': None, 'version': None,
                     'hwVersion': None, 'bootVersion': None, 'address': None, 'id': None, 'name': None, 'ip': None,
                     'protocol': None, 'config_sync': None, 'model': None})
        return result

    def add_device(self, sn: str) -> None:
        """添加设备，

        :param sn: 设备序列号
        :return:
        """
        for i in range(5):
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn})
            if response.json().get('total') == 0:
                self.api.send_request('api/devices', 'post',
                                      body={"name": sn + str(int(time.time())), "serialNumber": sn})
                logging.info(f"the {sn} device add success")
            else:
                break

    def assert_device_state(self, sn: str, state: dict, timeout=120, interval=5) -> None:
        """校验设备基本状态

        :param sn: 序列号
        :param state:   支持表达式${value} ex: {'version': "'${value}' in 'V1.1.3.r4956'"}
                        online: 在线|离线   1|0
                        connected: true 只有ics 有该参数
                        model: 设备型号
                        iccid:
                        imei:
                        imsi:
                        version: 固件版本
                        hwVersion: 硬件版本 'V1.0'
                        bootVersion:  Bootloader版本  '1.1.3.r4956'
                        sn: 序列号
                        address
                        vip:  只能在ics里面使用
                        ip: 设备连接平台的ip地址
                        protocol: 设备连接平台的协议 ex: 'mqtt' or 'ovdp'
                        config_sync: 设备配置同步状态 ex: 2  同成功
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :return: True or False
        """
        if state:
            import ipaddress
            for i in range(0, timeout, interval):
                result = self.device_state([sn])[0]
                for key, value in state.items():
                    if '${value}' in value:
                        value = replace_str(value, {'${value}': result.get(key)})
                        logging.debug(f'start assert {sn} state {key} {value}')
                        try:
                            if not eval(value, {'ipaddress': ipaddress}):
                                logging.debug(f'the {sn} device {key} info eval {value} is false')
                                break
                        except Exception as e:
                            logging.error(e)
                            break
                    else:
                        logging.debug(f'start assert {sn} state {key} {value}')
                        if result.get(key) != value:
                            logging.debug(f'the {sn} device {key} info value is {result.get(key)} not {value}')
                            break
                else:
                    logging.info(f"check {sn} device all state success")
                    break
                logging.info(f"check {sn} device state failed, please wait for {interval}s")
                time.sleep(interval)
            else:
                logging.exception(f"the {sn} state {state} check failed")
                raise TimeOutError(f"the {sn} state {state} check failed")

    def send_config_online(self, sn: str or list, config: str) -> List[str]:
        """下发配置， 多台时仍然是一台一台下发的， 注意逻辑 设备必须是在线的才能下发

        :param config: 配置命令，多个配置用'\n'隔开
        :param sn: 一台设备或多台设备
        :return: list 返回未成功下发配置的设备sn
        """
        body = {
            "deviceType": 0,
            "deviceContent": config,
            "deviceDesc": 'set running config'
        }
        sn = [sn] if isinstance(sn, str) else sn
        online_devices = list(filter(lambda x: x.get('online'), self.device_state(sn)))
        offline_devices = list(filter(lambda x: not x.get('online'), self.device_state(sn)))
        if online_devices:
            for on_device in online_devices:
                logging.info(f'the {on_device.get("sn")} device send config')
                self.api.send_request(f'/api/devices/{on_device.get("id")}/config/set', 'post', param={'timeout': 30},
                                      body=body)
        else:
            logging.warning(f"the {sn} all offline")
        return [offline_.get('sn') for offline_ in offline_devices]

    def get_config_online(self, sn: str, config: str = None) -> None:
        """平台获取配置 设备需要在线

        :param sn: 序列号
        :param config: 对获取到的配置做校验 多条配置使用'\n'隔开， 为None时仅获取
        """
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            device_name = response.json().get('result')[0].get('name')
            for i in range(0, 3):
                try:
                    task_state = self.api.send_request('api2/tasks/run', 'post',
                                                       body={'name': "GET RUNNING CONFIG", 'objectId': device_id,
                                                             'priority': 30, 'objectName': device_name,
                                                             'timeout': 30000,
                                                             'type': "4"}).json().get('result').get('state')
                    assert task_state == 3, "GET RUNNING CONFIG task status error!"
                    break
                except Exception as e:
                    logging.error(f'get running config task status reason is {e}, try {i + 2} again')
            else:
                logging.exception(f'device {sn} get running config task status failed')
                raise Exception(f'device {sn} get running config task status failed')
            config_content = self.api.send_request(f'api/devices/{device_id}/config', 'get').json().get('result').get(
                'content')
            if config:
                assert set(config.split('\n')).issubset(set(config_content.split('\n'))), f'config {config} not exist'
        else:
            logging.exception(f'the {sn} device not exist or offline')
            raise ResourceNotFoundError(f'the {sn} device not exist or offline')

    def upgrade_firmware_online(self, sn: str, firmware: str, timeout=20 * 60, interval=10) -> None:
        """ 升级固件， 保障升级成功不然就会报错

        :param sn: 设备序列号
        :param firmware: 升级的固件，本地全路径
        :param timeout: 下发升级任务后，总体的升级超时时间， 单位秒 至少5分鐘， 10， 20， 30
        :param interval: 升级任务检测间隔， 单位秒
        :return None or TimeOutError， 升级失败就报TimeOutError
        """

        def model(name):
            models = self.api.send_request('api/models', 'get',
                                           {'gateway': True, 'verbose': 100, 'limit': 0}).json().get('result')
            for model_ in models:
                if len(re.findall(model_.get('firmwareNamePattern'), name)) == 1:
                    return model_.get('name')

        def version(name):
            return 'V' + re.findall('V(.*).bin', name)[0]

        online_devices = list(filter(lambda x: x.get('online'), self.device_state([sn])))
        if online_devices:
            device_id = online_devices[0].get('id')
            device_name = online_devices[0].get('name')
            file_name = os.path.basename(firmware)
            if os.path.isfile(firmware):  # 只要升级文件存在就升级
                get_firmware = self.api.send_request('api/firmware', 'get', {'name': file_name}).json()
                if get_firmware.get('total') == 0:
                    if os.path.exists(firmware):
                        param = {'filename': firmware, 'oid': 'undefined'}
                        upload_file = self.api.send_request('api/file/form', method='post', param=param,
                                                            params_type='form', file_path=firmware).json().get('result')
                        body = {'fid': upload_file['_id'], 'jobTimeout': int(timeout / 60), 'model': model(file_name),
                                'name': file_name,
                                'version': version(file_name), 'desc': 'auto test upload firmware'}
                        firmware_id = self.api.send_request('api/firmware', 'post', body=body, ).json().get(
                            'result').get(
                            '_id')
                    else:
                        logging.exception(f'{firmware} not exist')
                        raise FileNotFoundError(f'{firmware} not exist')
                else:
                    logging.debug(f'This file {firmware} already exists on the cloud {self.host} {self.username}')
                    firmware_id = get_firmware.get('result')[0].get('_id')
                # 已完成固件上传
                job_id = self.api.send_request(f'api/device/{device_id}/upgrade', method='post',
                                               body={'deviceName': device_name, 'firmwareId': firmware_id,
                                                     'timeout': int(timeout / 60)}).json().get('result').get('_id')
                for i in range(0, timeout, interval):
                    time.sleep(interval)
                    job_response = self.api.send_request(f'/api2/tasks', method='get',
                                                         param={"verbose": 50, 'types': 6, 'object_id': device_id,
                                                                'limit': 100, 'cursor': 0}).json().get('result')
                    job = [job for job in job_response if job.get('_id') == job_id]
                    if len(job) == 1:
                        if job[0].get('_id') == job_id:
                            if job[0].get('state') == 3:
                                logging.info(f"upgrade to {file_name} success!")
                                break
                            elif job[0].get('state') == -1:
                                logging.exception(f'upgrade to {file_name} failed!')
                                raise UpgradeFailedError(f'upgrade to {file_name} failed!')
                    else:
                        logging.exception(f'upgrade to {file_name} failed!')
                        raise UpgradeFailedError('create upgrade task failed!')
                else:
                    logging.exception(f'upgrade to {file_name} timeout!')
                    raise TimeOutError('upgrade job check timeout')
                self.assert_device_state(sn, state={'version': '"${value}" in ' + f'"{file_name}"'}, timeout=300)
            else:
                logging.debug(f'{firmware} not is file or version of same ')
        else:
            logging.exception(f'the device {sn} is offline or not exist')
            raise Exception(f'the device {sn} is offline or not exist')

    def upgrade_firmware(self, sn: str or list, firmware: str) -> None:
        """ 升级固件，只管下发升级任务，不监督是否升级成功

        :param sn: 设备序列号
        :param firmware: 升级的固件，本地全路径
        :return None
        """

        def model(name):
            models = self.api.send_request('api/models', 'get',
                                           {'gateway': True, 'verbose': 100, 'limit': 0}).json().get('result')
            for model_ in models:
                if len(re.findall(model_.get('firmwareNamePattern'), name)) == 1:
                    return model_.get('name')

        def version(name):
            return 'V' + re.findall('V(.*).bin', name)[0]

        sn = [sn] if isinstance(sn, str) else sn
        devices = list(filter(lambda x: x.get('id'), self.device_state(sn)))
        if os.path.isfile(firmware) and devices:
            file_name = os.path.basename(firmware)
            get_firmware = self.api.send_request('api/firmware', 'get', {'name': file_name}).json()
            if get_firmware.get('total') == 0:
                if os.path.exists(firmware):
                    param = {'filename': firmware, 'oid': 'undefined'}
                    upload_file = self.api.send_request('api/file/form', method='post', param=param,
                                                        params_type='form', file_path=firmware).json().get('result')
                    body = {'fid': upload_file['_id'], 'jobTimeout': 30, 'model': model(file_name),
                            'name': file_name,
                            'version': version(file_name), 'desc': 'auto test upload firmware'}
                    firmware_id = self.api.send_request('api/firmware', 'post', body=body, ).json().get(
                        'result').get(
                        '_id')
                else:
                    logging.exception(f'{firmware} not exist')
                    raise FileNotFoundError(f'{firmware} not exist')
            else:
                logging.debug(f'This file {firmware} already exists on the cloud {self.host} {self.username}')
                firmware_id = get_firmware.get('result')[0].get('_id')
            self.api.send_request(f'api/firmware/{firmware_id}/devices', method='post',
                                  body={'deviceIds': [device.get('id') for device in devices], 'deviceGroupIds': [], })
        else:
            logging.debug(f'{firmware} not is file or device is not exist')

    def web_remote_online(self, sn: str) -> str:
        """封装远程web访问方法

        :param sn: str, 设备序列号
        :return: 远程web管理链接
        """
        if self.host == 'iot.inhand.com.cn':
            server = 'ngrok.iot.inhand.com.cn:4443'
        elif self.host == 'iot.inhandnetworks.com':
            server = 'iot.inhandnetworks.com:4443'
        elif self.host == 'ics.inhandiot.com':
            server = 'ics.inhandiot.com:4443'
        else:
            server = 'ngrok.ics.inhandnetworks.com:443'
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            device_name = response.json().get('result')[0].get('name')
            body = {"priority": 30, "timeout": 20000, "objectId": device_id, "objectName": device_name,
                    "name": "ngrok connect", "type": "23", "data": {"server": server, "proto": 'http', "port": 80}}
            for i in range(0, 3):
                try:
                    ngrok = self.api.send_request('api2/tasks/run', method='post', body=body).json()
                    if ngrok["result"]["data"]["response"]:
                        return ngrok["result"]["data"]["response"]
                except Exception as e:
                    logging.error(f"ngrok request failed reason is {e}, try {i + 2} again")
            else:
                logging.exception(f'Device {sn} get ngrok failed.')
                raise Exception(f'Device {sn} get ngrok failed.')
        else:
            logging.exception(f'the device {sn} is offline or not exist')
            raise ResourceNotFoundError(f'the {sn} is not exist or offline')

    def reboot_online(self, sn: str) -> None:
        """DM平台设备重启
        """
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn})
        if response.json().get('total') == 1 and response.json().get('result')[0].get('online') == 1:
            device_id = response.json().get('result')[0].get('_id')
            logging.debug(f'{self.host} send to {sn} reboot command')
            status = self.api.send_request(f'api/device/{device_id}/methods', 'post',
                                           body={'method': "reboot", 'timeout': 15000}).json().get('status')
            assert status == 'succeeded', 'reboot error!'
        else:
            logging.exception(f'the device {sn} is offline or not exist')
            raise ResourceNotFoundError(f'the {sn} is not exist or offline')

    def remote_maintenance_online(self, sn: str, protocol='http', port=80, local_host='192.168.2.1',
                                  action='connect') -> str or None:
        """封装dm远程维护方法

        :param sn，必须在线
        :param protocol: str, 本地主机服务的协议, 'http'| 'https'| 'tcp'
        :param port: 端口, 本地主机的端口
        :param local_host: str, 本地主机的ip地址
        :param action: str, 是否连接远程维护隧道, 'connect'| 'disconnect'| 'delete'| 当为connect 时如果隧道不存在则自动新增
        :return: 当action='connect' 时返回远程维护连接
        """
        device = list(filter(lambda x: x.get('id'), self.device_state([sn])))

        tunnel_des = f'{sn} tunnel {protocol}://{local_host}:{port} '

        def find_tunnel(device_id_):
            tunnels_ = self.api.send_request('/api/touch/tunnels', method='get',
                                             param={'verbose': 100, 'device_id': device_id_}).json().get('result')
            if tunnels_:
                for tunnel_ in tunnels_:
                    if tunnel_.get('proto') == protocol and tunnel_.get('localPort') == port and tunnel_.get(
                            'localAddress'):
                        return tunnel_.get('_id'), tunnel_.get('connected'), tunnel_.get('publicUrl')
            return None, None, None

        if device:
            device_id = device[0].get('id')
            add_tunnel_body = {'verbose': 100, 'proto': protocol, 'name': str(round(time.time() * 1000)),
                               'localAddress': local_host, 'localPort': port, 'deviceId': device_id}
            tunnel_id, tunnel_status, pub_url = find_tunnel(device_id)
            if action == 'connect' and device[0].get('online'):
                if not tunnel_id:
                    result = self.api.send_request('/api/touch/tunnels', method='post', body=add_tunnel_body).json()
                    tunnel_id = result.get('result').get('_id')
                    tunnel_status = False
                    logging.debug(f'Add {tunnel_des} success, tunnel name is {add_tunnel_body["name"]}')
                if not tunnel_status:
                    for i in range(0, 3):
                        connect = self.api.send_request(f'/api/touch/tunnels/{tunnel_id}/connect', 'put').json()
                        if connect.get('result').get('connected'):
                            pub_url = connect.get('result').get('publicUrl')
                            logging.info(f'tunnel {tunnel_des} connect success')
                            break
                    else:
                        logging.exception(f'tunnel {tunnel_des} connect failed')
                        raise ConnectionError(f'tunnel {tunnel_des} connect failed')
                else:
                    logging.debug(f'tunnel {tunnel_des} already connect')
                return pub_url
            elif action == 'disconnect' and device[0].get('online'):
                if tunnel_id and tunnel_status:
                    self.api.send_request(f'/api/touch/tunnels/{tunnel_id}/disconnect', 'put')
                    logging.info(f'tunnel {tunnel_des} disconnect success')
                else:
                    logging.debug(f'tunnel {tunnel_des} not exist or already disconnect')
            elif action == 'delete':
                if tunnel_id:
                    self.api.send_request(f'/api/touch/tunnels/{tunnel_id}', 'delete')
                    logging.info(f'tunnel {tunnel_des} delete success')
                else:
                    logging.debug(f'tunnel {tunnel_des} not exist')
        else:
            logging.error(f'the device {sn} not exist')

    def delete_device(self, sn: str or list) -> None:
        """

        :param sn: 设备序列号，一个或多个
        :return:
        """
        sn = [sn] if isinstance(sn, str) else sn
        device = list(filter(lambda x: x.get('id'), self.device_state(sn)))
        if device:
            for device_ in device:
                self.api.send_request(f'api/devices/{device_.get("id")}', 'delete')
                logging.info(f'the {device_.get("sn")} delete success')
