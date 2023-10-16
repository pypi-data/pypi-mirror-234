# -*- coding: utf-8 -*-
# @Time    : 2023/3/3 9:23:56
# @Author  : Pane Li
# @File    : inrequest.py
"""
封装request， 使设备和平台都能来正常调用，统一入口，token过期时也能自动更新

"""
from inhandtest.inrequest.inrequest import InRequest
from inhandtest.exception import ResourceNotFoundError
from inhandtest.tools import loop_inspector
import logging


class DnInterface:
    def __init__(self, username, password, host='c.inhand.com.cn'):
        """
        :param username  平台用户名
        :param password  平台密码
        :param host: 'c.inhand.com.cn'
        """
        self.host = host
        self.username = username
        self.api = InRequest(self.host, username, password, 'dn4')

    def add_device(self, sn: str, mac: str, model: str) -> None:
        """添加设备，

        :param sn: 设备序列号
        :param mac: 设备mac地址
        :param model: 设备型号 IR6XX_EVDO  IR300
        :return:
        """

        def get_model_id(model_name: str) -> str:
            models = self.api.send_request('api/models', method='get', param={'limit': 0, 'verbose': 1}).json().get(
                'result')
            for model_ in models:
                if model_.get('name').upper() == model_name.upper():
                    return model_.get('_id')
            else:
                logging.exception(f"the model {model_name} not found")
                raise ResourceNotFoundError(f"the model {model_name} not found")

        for i in range(3):
            response = self.api.send_request('api/devices', method='get',
                                             param={"verbose": 100, "limit": 10, "cursor": 0,
                                                    'serial_number': sn, 'plc_id': 0})
            if response.json().get('total') == 0:
                body = {"deviceConfig": {"maxHeartbeatLost": 6, "heartbeatInterval": 120, "heartbeatTimeout": 10,
                                         "resendLogin": 60}, "siteName": "", "siteId": None, "name": sn,
                        "businessState": "0", "modelId": get_model_id(model), "model": model.upper(),
                        "serialNumber": sn, "mac": mac.upper(), "mobileNumber": "", "plcId": 0,
                        "config": {"timeout": "300000", "ackTimeout": "120000", "ackRetries": "3", "sync": "2"}}
                self.api.send_request('api/devices', 'post', param={"create_site": 0}, body=body)
                logging.info(f"the {sn} device add success")
            else:
                break

    @loop_inspector('device online')
    def assert_device_online(self, sn: str, timeout=120, interval=5) -> int:
        """ 校验设备基本状态

        :param sn: 序列号
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :return: True or False
        """
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn, 'plc_id': 0})
        if response.json().get('total') == 1:
            device_id = response.json().get('result')[0].get('_id')
            response = self.api.send_request(f'api/devices/{device_id}', method='get', param={"verbose": 100}).json()
            return response.get('result').get('online')
        else:
            return 0

    def delete_device(self, sn):
        response = self.api.send_request('api/devices', method='get',
                                         param={"verbose": 100, "limit": 10, "cursor": 0,
                                                'serial_number': sn, 'plc_id': 0}).json()
        if response.get('total') == 1:
            self.api.send_request(f'api/devices/{response.get("result")[0].get("_id")}', method='delete')
            logging.info(f"the {sn} device delete success")
