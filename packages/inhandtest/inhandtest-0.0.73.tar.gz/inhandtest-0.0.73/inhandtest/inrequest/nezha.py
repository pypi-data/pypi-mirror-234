# -*- coding: utf-8 -*-
# @Time    : 2023/7/5 13:28:22
# @Author  : Pane Li
# @File    : nezha.py
"""
nezha

"""
import logging
import random
import re
import time
import allure
from inhandtest.exception import TimeOutError, ResourceNotFoundError, UpgradeFailedError
from inhandtest.tools import generate_string, get_time_stamp, dict_in, loop_inspector, dict_merge, time_delta
from inhandtest.inrequest.inrequest import InRequest
from urllib.parse import urlparse, urlunparse
from inhandtest import expect


class Base:
    def __init__(self, api: InRequest, email: str, host: str):
        self.api = api
        self.host = host
        self.email = email

    @property
    def me(self) -> dict:
        """ 获取me的各种信息 包括oid

        :return:
        """
        return self.api.send_request('/api/v1/users/me', method='get', param={"expand": 'org'}).json().get('result')

    @allure.step("位置查询")
    def location_suggestion(self, q: str, provider, expect=None):
        """位置查询

        :param q: 位置
        :param provider: 服务商 baidu|google
        :param expect: 每个返回的地址都包含的字段
        :return:
        """
        address = self.api.send_request('/api/v1/places/suggestion', method='get',
                                        param={'q': q, 'provider': provider}).json().get('result')
        if address:
            if expect:
                for item in address:
                    assert expect in item.get('address')
        else:
            raise ResourceNotFoundError(f'the {q} address not found')

    # 递归删除字典里面的None值


class Overview(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__device = Device(api, email, host)

    @allure.step("概览地图位置验证")
    def map(self, sn: str, expect=None):
        """对概览的地图进行验证

        :param sn: 设备序列号
        :param expect: 期望值  字典 {'location': {'source': 'gps'}}
        :return:
        """
        if expect:
            name = self.__device.info(sn).get('name')
            devices = self.api.send_request('/api/v1/devices/locations', method='get').json().get('result')
            for device in devices:
                if device.get('name') == name:
                    dict_in(device, expect)
                    break

    @allure.step("概览上行链路验证")
    def uplink_status(self, expect: dict, param: dict = None):
        """

        :param expect:  {"result":{"connected":518,"disconnected":167,"disabled":154,"exception":54}}
        :param param:  {"org": "5f0f1e9b9d6b4e0001a3e2b0"}
        :return:
        """
        self.api.send_request('/api/v1/uplinks/status', method='get', expect=expect, param=param)

    @allure.step("概览上行链路列表验证")
    def assert_uplinks_list(self, sn: str, interfaces: list, param=None, expect=None):
        """

        :param sn: 当sn为空时就对整体列表做验证
        :param interfaces:
        :param param: 查询参数
        :param expect: 期望值
        :return:
        """

        param = dict_merge({'limit': 100, 'page': 0}, param) if param else {'limit': 100, 'page': 0}
        if interfaces and sn:
            result = self.api.send_request('/api/v1/uplinks', 'get', param).json().get('result')
            _id = self.__device.info(sn).get('_id')
            for interface in interfaces:
                for device in result:
                    if device.get('deviceId') == _id and device.get('name') == interface.get('name'):
                        dict_in(device, interface)
                        break
                else:
                    raise ResourceNotFoundError(f'the {sn} not found in uplinks list')
        else:
            self.api.send_request('/api/v1/uplinks', 'get', param, expect=expect)


class Clients(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__device = Device(api, email, host)

    def info(self, name: str, type_='list') -> dict:
        """name 转换属性 属性值有：  connectedAt
                                    connectedSeconds
                                       ip:
                                       mac:
                                       name
                                       oid:
                                       online
                                       ssid
                                       type:
        :param name: 客户端名称 在查询info时 名称应唯一
        :param type_:  list|detail,  分别为客户端列表或者客户端详情返回该客户端的信息
        :return: {'name': name, 'ssid': 1}
        """
        try:
            response = self.api.send_request('/api/v1/network/clients', method='get',
                                             param={'name': name, 'expand': 'device', 'page': 0, 'limit': 100}).json()
            info = response.get('result')[0]
        except IndexError:
            raise ResourceNotFoundError(f'the network client {name} not exist')
        if type_ == 'list':
            return info
        else:
            return self.api.send_request(f'/api/v1/network/clients/{info["_id"]}', method='get',
                                         param={'expand': 'device'}).json().get('result')

    @allure.step("客户端验证")
    def assert_device_info_network_client(self, sn: str, clients: list):
        """

        :param sn:
        :param clients:
        :return:
        """
        if clients:
            _id = self.__device.info(sn).get('_id')
            result = self.api.send_request(f'/api/v1/network/devices/{_id}/clients', 'get', ).json().get('result').get(
                'clients')
            for client in clients:
                for device_ in result:
                    if device_.get('name') == client.get('name'):
                        dict_in(device_, client)
                        break
                else:
                    raise ResourceNotFoundError(f'the {sn} not found in client list')

    @allure.step("验证客户端属性")
    def assert_state(self, name: str, state: dict, timeout=30, interval=5, type_='list') -> None:
        """校验设备基本状态

        :param name: 序列号
        :param state:
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :param type_: list|detail, 分别是列表和详情返回的具体信息
        :return: True or False
        """
        if state:
            for i in range(0, timeout, interval):
                try:
                    result = self.info(name, type_)
                    dict_in(result, state)
                    break
                except (ResourceNotFoundError, AssertionError):
                    time.sleep(interval)
            else:
                logging.exception(f"the client {name} state {state} check failed")
                raise TimeOutError(f"the client {name} state {state} check failed")

    @allure.step("查询客户端")
    def find(self, param: dict = None, statistics: dict = None) -> list:
        """

        :param param:
        :param statistics:
        :return:
        """
        result = []
        if statistics:
            self.api.send_request('/api/v1/network/clients/statistics', method='get', expect=statistics)
        for i in range(0, 1000):
            response = self.api.send_request('/api/v1/network/clients', method='get',
                                             param=dict_merge(param,
                                                              {"limit": 100, 'page': i, 'expand': 'device'})).json()
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result

    @allure.step("客户端在线事件")
    def online_event(self, name: str, params: dict = None, type_='chart') -> list:
        """

        :param name: 客戶端名称
        :param params: 查询参数, 如：'after'| 'before'
        :param type_: 'chart'|'list'
        :return:
        """
        if type_ == 'chart':
            return self.api.send_request(
                f'/api/v1/network/clients/{self.info(name).get("_id")}/online-events-chart/statistics',
                method='get',
                param=dict_merge(params, {'expand': 'device'})).json().get('result').get('list')
        else:
            return self.api.send_request(
                f'/api/v1/network/clients/{self.info(name).get("_id")}/online-events-list',
                method='get',
                param=dict_merge(params, {'expand': 'device'})).json().get('result')

    @allure.step("客户端流量")
    def data_usage(self, name: str, params: dict = None, type_='hourly') -> dict:
        """

        :param name: 客户端名称
        :param params: 客户端参数， 如：'after'| 'before'
        :param type_:
        :return:  {"overview" : {"total": 0, "tx": 0, "rx": 0}, "values": [["2023-08-31T16:00:00Z", 0, 0, 0]]}
        """
        if type_ == 'hourly':
            result = self.api.send_request(
                f'/api/v1/network/clients/{self.info(name).get("_id")}/datausage-hourly', method='get',
                param=params).json().get('result')
            return {"overview": result.get('overview'), "values": result.get('series')[0].get('values')}

        else:
            result = self.api.send_request(
                f'/api/v1/network/clients/{self.info(name).get("_id")}/datausage-daily',
                method='get', param=params).json().get('result')
            return {"overview": result.get('overview'), "values": result.get('series')[0].get('values')}

    @allure.step("客户端历史数据")
    def history(self, name: str, params: dict = None, data_interval: int = None, data_type='throughput') -> list:
        """["time", "throughputUp", "throughputDown"]

        :param name:  客户端名称
        :param params: 客户端参数， 如：'after'| 'before'
        :param data_interval: 数据间隔时间 5
        :param data_type:  throughput| rssi|sinr
        :return:
        """
        series = self.api.send_request(
            f'/api/v1/network/clients/{self.info(name).get("_id")}/{data_type}', method='get',
            param=params).json().get('result').get('series')[0].get('values')
        if data_interval is not None:
            timestamp_ls = [i[0] for i in series]
            time_delta(timestamp_ls, delta=data_interval)
        return series


class Device(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__firmware = Firmware(api, email, host)

    def info(self, sn: str, type_='list') -> dict:
        """根据sn 转换属性 属性值有：  online: 在线|离线   True|False
                                       iccid:
                                       imei:
                                       imsi:
                                       version: 固件版本
                                       licenseStatus: 'licensed'
                                       sn: 序列号
                                       address
                                       _id: 设备_id
                                       name: 设备名字
                                       org:  {'_id': oid, 'name': 'org_name', 'email': 'org_email'}
        :param sn: 设备序列号
        :param type_:  list|detail,  分别为设备列表或者设备详情返回该设备的信息
        :return: {'sn': $sn, 'online': 1, 'iccid': '', 'imei'}
        """
        try:
            response = self.api.send_request('/api/v1/devices', method='get', param={'serialNumber': sn,
                                                                                     'expand': 'firmwareUpgradeStatus,compatibilities,org'}).json()
            info = response.get('result')[0]
        except Exception:
            raise ResourceNotFoundError(f'the device {sn} not exist')
        if type_ == 'list':
            return info
        else:
            return self.api.send_request(f'/api/v1/devices/{info["_id"]}', method='get',
                                         param={'expand': 'firmwareUpgradeStatus,compatibilities,org'}).json().get(
                'result')

    @allure.step("添加设备")
    def add(self, sn: str, mac_or_imei: str, name=None) -> None:
        """添加设备，

        :param sn: 设备序列号
        :param mac_or_imei: 添加设备时需要依赖设备的mac地址或者IMEI号，去生产库查询该设备是否是映翰通设备
        :param name: 设备名字
        :return:
        """
        try:
            validated_field = self.api.send_request(f'api/v1/serialnumber/{sn}/validate', method='post').json().get(
                'result').get('validatedField')
        except Exception:
            raise Exception(f'the {sn} validate failed')
        if name is None:
            name = sn + str(int(time.time()))
        self.api.send_request('api/v1/devices', 'post',
                              body={"name": name, "serialNumber": sn, 'oid': self.me.get('oid'),
                                    validated_field: mac_or_imei})
        logging.info(f"the {sn} device add success")

    @allure.step("编辑设备")
    def update(self, sn: str, name: str = None, description: str = None) -> None:
        """编辑设备

        :param sn: 设备序列号
        :param name: 设备名字
        :param description: 设备描述
        :return:
        """
        _id = self.info(sn).get('_id')
        self.api.send_request(f'/api/v1/devices/{_id}', method='put',
                              body={'name': name, 'description': description})

    @allure.step("验证设备属性")
    def assert_state(self, sn: str, state: dict, timeout=30, interval=5, type_='list') -> None:
        """校验设备基本状态

        :param sn: 序列号
        :param state:
                        online: 在线|离线   True|False
                        iccid:
                        imei:
                        imsi:
                        version: 固件版本
                        licenseStatus: 'licensed'
                        sn: 序列号
                        address
        :param timeout: 校验信息，最大超时时间
        :param interval: 校验信息，校验间隔时间
        :param type_: list|detail, 分别是列表和详情返回的具体信息
        :return: True or False
        """
        if state:
            for i in range(0, timeout, interval):
                try:
                    result = self.info(sn, type_)
                    dict_in(result, state)
                    break
                except (ResourceNotFoundError, AssertionError):
                    time.sleep(interval)
            else:
                logging.exception(f"the {sn} state {state} check failed")
                raise TimeOutError(f"the {sn} state {state} check failed")

    @allure.step("删除设备")
    def delete(self, sn: str or list, type_='sn') -> None:
        """

        :param sn: 设备序列号，一个或多个, sn='all' 时，删除所有设备
        :param type_: sn|id,  sn: 设备序列号， id: 设备id
        :return:
        """

        def delete(ids: list):
            if ids:
                for _id in ids:
                    self.api.send_request(f'api/v1/devices/{_id}', 'delete')
                    logging.debug(f'{_id} device delete success')

        if sn == 'all':
            while True:
                devices = self.api.send_request(f'api/v1/devices', 'get', {'limit': 100, 'page': 0}).json().get(
                    'result')
                if devices:
                    delete([device.get('_id') for device in devices])
                else:
                    break
                logging.info(f'{self.email} user delete all device success')
        else:
            sn = [sn] if isinstance(sn, str) else sn
            if type_ == 'sn':
                delete([self.info(sn_).get('_id') for sn_ in sn])
            else:
                delete(sn)

    @allure.step("查询设备")
    def find_device(self, expect, param: dict) -> list:
        """

        :param expect:
        :param param:
        :return:
        """
        result = []
        for i in range(0, 1000):
            response = self.api.send_request('/api/v1/devices', method='get',
                                             param=dict_merge(param, {"limit": 100, 'page': i})).json()
            if i == 0:
                dict_in(response, expect)
            if response.get('result'):
                for res in response.get('result'):
                    result.append(res)
            if len(response.get('result')) < 100:
                break
        return result

    @allure.step("设备绑定license")
    def bind_license(self, sn: list, licenses: dict):
        """ 绑定license

        :param sn
        :param licenses: {'slug': 'star_pro'}
        """
        licenses_ = []
        for sn_ in sn:
            info = self.info(sn_)
            if info.get('licenseStatus') == 'licensed':
                sn.remove(sn_)
        org_license = self.api.send_request('/api/v1/billing/licenses', 'get',
                                            param={'expand': 'org,device,type', 'limit': 200, 'page': 0},
                                            code=200).json().get('result')
        if org_license:
            for org in org_license:
                if org['status'] != 'expired' and org.get('device') is None and org['type']['slug'] == licenses.get(
                        'slug'):
                    licenses_.append(org['_id'])
        if sn:
            if len(licenses_) < len(sn):
                logging.error(f'licenses not enough, please check the licenses')
            else:
                device_ids = [self.info(sn_).get('_id') for sn_ in sn]
                for license_, _id in zip(licenses_, device_ids):
                    self.api.send_request(f'/api/v1/billing/licenses/{license_}/device', 'put',
                                          body={'deviceId': _id},
                                          code=200)
                logging.info(f'bind license success')

    @allure.step("设备取消license")
    def unbind_license(self, sn: list):
        """ 取消license

        :param sn
        """
        for sn_ in sn:
            info = self.info(sn_)
            if info.get('licenseStatus') == 'unlicensed':
                sn.remove(sn_)
        if sn:
            license_ids = [self.info(sn_).get('license').get('_id') for sn_ in sn]
            self.api.send_request(f'/api/v1/billing/licenses/bulk-detach', 'POST',
                                  body={'ids': license_ids},
                                  code=200)
        logging.info(f'unbind license success')

    @allure.step("设备位置")
    def location(self, sn: str, type_='sync', location=None, address=None) -> None:
        """对设备位置做操作

        :param sn:
        :param type_: sync|manually
        :param location:  {"latitude":30.588423465204404,"longitude":104.0541738405845}  仅手动方式有用
        :param address: "成都市-武侯区-府城大道西段399号"  仅手动方式有用
        :return:  None
        """
        if type_ == 'sync':
            body = {'pinned': False}
        else:
            body = {"pinned": True, "location": location, "address": address}
        self.api.send_request(f'/api/v1/devices/{self.info(sn).get("_id")}/location', 'put', body=body)

    @allure.step("设备升级")
    def upgrade_firmware(self, sn: str or list, version: str, schedule=None) -> str:
        """ 升级任务

        :param sn: 设备序列号 一个或多个，他们需要都是同一个产品型号
        :param version: 版本号
        :param schedule: 计划升级时间， int， 单位分钟
        :return str， job_id
        """
        if isinstance(sn, str):
            product = self.info(sn).get('product')
            _id = [self.info(sn).get('_id')]
        else:
            product = self.info(sn[0]).get('product')
            _id = [self.info(sn_).get('_id') for sn_ in sn]
        firmware_id = self.__firmware.info(product, version).get('_id')
        payload = {"jobs": [{"targets": _id, "firmware": firmware_id}], "targetType": "device"}
        if schedule:
            payload["scheduledAt"] = get_time_stamp(delta=schedule, delta_type='m')
        try:
            return self.api.send_request('/api/v1/firmwares/batch/jobs', 'post', body=payload).json().get('result')[0][
                '_id']
        except (IndexError, KeyError):
            logging.exception(f'firmware upgrade failed')
            raise UpgradeFailedError(f'firmware upgrade failed')

    @allure.step("设备取消最近固件升级任务")
    def cancel_latest_task(self, sn: str):
        detail = self.info(sn, 'detail')
        if detail.get('firmwareUpgradeStatus'):
            if detail.get('firmwareUpgradeStatus').get('status') == 'queued':
                self.api.send_request(
                    f'/api/v1/job/executions/{detail.get("firmwareUpgradeStatus").get("jobExecutionId")}/cancel',
                    'put')

    @allure.step("设备下发实时命令")
    def commands_online(self, sn: str or list, method='nezha_reboot'):
        """

        :param sn:
        :param method: nezha_reboot|nezha_restore_to_defaults
        :return:
        """
        sn = [sn] if isinstance(sn, str) else sn
        ids = [self.info(sn_).get('_id') for sn_ in sn]
        body = {"deviceIds": ids, "method": method}
        self.api.send_request('/api/v1/devices/bulk-invoke-methods', 'post', body=body, expect={'result': 'ok'})

    @allure.step("在线下载日志")
    def download_log_online(self, sn: str, type_='diagnostic', expect_file=None, expect_content=None):
        """

        :param sn:
        :param type_:diagnostic|syslog
        :param expect_file: 期望下载的文件路径
        :param expect_content: 期望下载的文件内容,
                                1.支持写表达式"AES in '${text}'"(${text}指代下载的文件内容)
                                2.当传入的值中没有${text}则校验下载的文件内容是否与传入的值相等
        :return:
        """
        _id = self.info(sn).get('_id')
        result = self.api.send_request(f'/api/v1/devices/{_id}/logs/download', 'get', {'type': type_},
                                       expect=f'"downloadUrl"').json().get('result')
        time.sleep(3)
        lines = self.api.send_request('', 'get', url=result.get('downloadUrl'), auth=False).text
        lines = lines.replace('\r', '')
        if expect_file:
            with open(expect_file, 'r', encoding='utf-8') as f:
                expect_lines = ''.join(f.readlines())
            assert lines == expect_lines, f'文件下载失败'
        if expect_content:
            lines = lines.replace('\n', '')
            logging.info(f'lines: {lines}')
            logging.info(f'expect_content: {expect_content}')
            if '${text}' not in expect_content:
                assert lines == expect_content, f'文件下载失败'
            else:
                lines = lines.replace('\"', '').replace('\'', '')
                if not eval(expect_content.replace('${text}', lines)):
                    raise AssertionError(f'文件下载失败')

    @allure.step("设备蜂窝历史数据")
    def assert_cellular_history(self, sn: str, state, delta_day=-1, data_interval=None):
        """

        :param sn:
        :param state:
        :param delta_day: 查询开始时间的起点， 默认晚一天时间
        :param data_interval: 当查询的时间越长时，返回的数据会少，防止页面在渲染时卡顿，所以返回的数据间隔增大，可以对间隔做判断， 单位秒
        :return:
        """
        time.sleep(2)
        payload = {
            "after": get_time_stamp(delta=delta_day, delta_type='d', time_format='%Y-%m-%dT16:00:00.000Z'),
            "before": get_time_stamp(time_format='%Y-%m-%dT16:00:00.000Z')
        }
        resp = self.api.send_request(f'/api/v1/devices/{self.info(sn).get("_id")}/signal', 'get',
                                     param=payload, code=200).json().get('result').get('series')
        fields = resp[0]['fields']
        cellular_state = []
        if state:
            for each_type in resp:
                for data in each_type["data"]:
                    temp = {"name": "signal", "tags": {"type": each_type["type"]}, "fields": {}}
                    if data[1]:
                        temp["timestamp"] = data[0]
                        for i in range(1, len(data)):
                            if data[i] != 0:
                                if data[i]:
                                    if i == 5:
                                        temp["fields"]["level"] = data[i] - 1
                                    temp["fields"][fields[i]] = data[i]
                            elif data[i] == 0:
                                temp["fields"][fields[i]] = 0
                        temp["fields"].pop("strength")
                        cellular_state.append(temp)
                        assert temp in state, '查询结果不对'
            assert len(cellular_state) == len(state), '查询结果不对'
        if data_interval is not None:
            cellular_type = []
            for each_type in resp:
                cellular_type.append(each_type['type'])
                timestamp_ls = [i[0] for i in each_type['data']]
                time_delta(timestamp_ls, delta=data_interval)
            assert len(cellular_type) == len(set(cellular_type)), '蜂窝历史返回数据不对'

    @allure.step("设备上线链路数据")
    def assert_uplink_history(self, sn: str, name: str, param: dict = None, value: list = None,
                              interval: int = None):
        """

        :param sn: 序列号
        :param name: 上行链路接口名称 wan  cellular
        :param param: {'name': 'cellular1', 'after': '2023-07-24T16:00:00.000Z'}
        :param value: 期望返回的值，
        :param interval: 期望返回的数据间隔， 单位秒
        :return:
        """
        _id = self.info(sn).get('_id')
        param = {'name': name} if param is None else dict_merge({'name': name}, param)
        resp = self.api.send_request(f'/api/v1/devices/{_id}/uplinks/perf-trend', 'get', param=param)
        if interval:
            timestamp_ls = [i[0] for i in resp.json().get('result').get('series')[0].get('values')]
            time_delta(timestamp_ls, delta=interval)
        if value:
            expect(resp.json().get('result').get('series')[0].get('values')).to_contain(value)

    @allure.step("设备流量数据")
    def assert_traffic(self, sn: str, date_='hourly', type_='overview', expect=None, **kwargs):
        """

        :param sn: 设备序列号
        :param date_: hourly|daily|monthly
        :param expect: 期望返回的内容
        :param type_: overview|detail
        :param kwargs: after|before|month|year|param
                       after: int数, 在type_为hourly 时必传， 过期时间为天， 传0表示今天，传-1 表示昨天
                       before: int数, 在type_为hourly 时必传， 过期时间为天， 传0表示今天，传-1 表示昨天
                       month: 2023-07
                       year: 查询今年传0， 过去一年 传-1， 依次类推
        :return:
        """
        if date_ == 'hourly':
            param = {'after': get_time_stamp('', kwargs.get('after'), 'd', '%Y-%m-%dT16:00:00.000Z'),
                     'before': get_time_stamp('', kwargs.get('before'), 'd', '%Y-%m-%dT16:00:00.000Z')}
        elif date_ == 'daily':
            param = {'month': kwargs.get('month')}
        else:
            param = {'year': kwargs.get('year')}
        if kwargs.get('param'):
            param.update(kwargs.get('param'))
        if type_ == 'overview':
            self.api.send_request(f'/api/v1/devices/{self.info(sn).get("_id")}/datausage-{date_}/overview', 'get',
                                  param=param, expect=expect, )
        else:
            self.api.send_request(f'/api/v1/devices/{self.info(sn).get("_id")}/datausage-{date_}', 'get',
                                  param=param, expect=expect, )

    @allure.step("设备在线事件")
    @loop_inspector('device_online_event', timeout=20, interval=4)
    def assert_online_event(self, sn: str, time_from=get_time_stamp('', -1, 'd', '%Y-%m-%dT16:00:00Z'),
                            time_to=get_time_stamp('', 0, 'd', '%Y-%m-%dT16:00:00Z'), **kwargs):
        """ 对在线图和在线统计表做验证

        :param sn: 设备序列号
        :param time_from: 查询开始时间
        :param time_to: 查询结束时间
        :param kwargs:
            online: int 表示在线几次
            offline: int 表示离线几次
            event： list or dict {timestamp: "2023-06-14T16:00:00Z", online: false} 查询有该事件，多个使用列表传入
        :return:
        """
        _id = self.info(sn).get('_id')
        # 去除首尾两条记录，是时间戳划线时会自动补齐
        online_statis = self.api.send_request(f'/api/v1/devices/{_id}/online-events-chart/statistics', 'get',
                                              {'from': time_from, 'to': time_to}).json().get('result').get('list')[1:-1]
        online_event = self.api.send_request(f'/api/v1/devices/{_id}/online-events-list', 'get',
                                             {'from': time_from, 'to': time_to, 'limit': 100,
                                              'page': 0}).json().get('result')
        if kwargs.get('online'):
            if not (len(list(filter(lambda x: x.get('online'), online_statis))) == len(
                    list(filter(lambda x: x.get('eventType') == 'connected', online_event))) == kwargs.get('online')):
                return False
        if kwargs.get('offline'):
            if not (len(list(filter(lambda x: not x.get('online'), online_statis))) == len(
                    list(filter(lambda x: x.get('eventType') == 'disconnected', online_event))) == kwargs.get(
                'offline')):
                return False
        if kwargs.get('event'):
            events = [kwargs.get('event')] if isinstance(kwargs.get('event'), dict) else kwargs.get('event')
            for event in events:
                if event not in online_statis:
                    return False
                for _ in online_event:
                    if event.get('timestamp') == _.get('timestamp'):
                        if event.get('online') and _.get('eventType') == 'connected':
                            break
                        if (not event.get('online')) and _.get('eventType') == 'disconnected':
                            break
                else:
                    return False

    @allure.step("上行链路列表验证")
    def assert_uplinks_list(self, sn: str, interfaces: list):
        """

        :param sn:
        :param interfaces:
        :return:
        """
        if interfaces:
            _id = self.info(sn).get('_id')
            result = self.api.send_request(f'/api/v1/devices/{_id}/uplinks', 'get', ).json().get('result')
            for interface in interfaces:
                for device in result:
                    if device.get('name') == interface.get('name'):
                        dict_in(device, interface)
                        break
                else:
                    raise ResourceNotFoundError(f'the {sn} not found in uplinks list')

    @allure.step("客户端验证")
    def assert_client(self, sn: str, clients: list):
        """

        :param sn:
        :param clients:
        :return:
        """
        if clients:
            _id = self.info(sn).get('_id')
            result = self.api.send_request(f'/api/v1/devices/{_id}/clients', 'get', ).json().get('result').get(
                'clients')
            for client in clients:
                for device in result:
                    if device.get('name') == client.get('name'):
                        dict_in(device, client)
                        break
                else:
                    raise ResourceNotFoundError(f'the {sn} not found in cient list')

    @allure.step("获取设备interface")
    def get_interface(self, sn: str):
        """

        :param sn:
        :return:
        """
        _id = self.info(sn).get('_id')
        try:
            self.api.send_request(f'/api/v1/devices/{_id}/interfaces/refresh', 'post')
        except Exception as e:
            logging.exception(e)
            raise e

    @allure.step("验证设备interface")
    def assert_interface(self, sn: str, publish_info: dict):
        """只验证设备interface 名称以及状态

        :param sn:
        :param publish_info:
        :return:
        """
        _id = self.info(sn).get('_id')
        interfaces = self.api.send_request(f'/api/v1/devices/{_id}/interfaces', 'get').json().get('result')

        def switch_payload(payload: dict):
            for key, value in payload.items():
                if key == 'wifiSta':
                    payload[key] = {'name': value.get('name'), 'state': value.get('status'),
                                    'priority': value.get('priority')}
                elif 'cellular' in key:
                    new_v = [{'name': v_.get('name'), 'card': v_.get('card'), 'state': v_.get('status'),
                              'priority': v_.get('priority')} for v_ in value]
                    payload[key] = new_v
                else:
                    new_v = [{'name': v_.get('name'), 'state': v_.get('status'), 'priority': v_.get('priority')} for v_
                             in value]
                    payload[key] = new_v
            return payload

        if not publish_info:
            assert not interfaces, "设备interface不为空"
        else:
            assert switch_payload(interfaces) == switch_payload(publish_info), '设备interface不一致'

    @allure.step("下载批量导入模板")
    def download_import_model(self, locale='en'):
        """

        :param locale: en or zh
        :return:
        """
        param = {'local': 'us_EN'} if locale == 'en' else {'local': 'zh_CN'}
        self.api.send_request('/api/v1/devices/template/download', 'get', param)

    @allure.step("批量导入设备")
    def import_devices(self, file_path) -> str:
        """

        :param file_path:
        :return:
        """
        # 文件内容校验
        try:
            _id = self.api.send_request('api/v1/devices/imports', 'post', params_type='form',
                                        file_path=file_path).json().get('result')
            self.api.send_request(f'api/v1/devices/imports/{_id}', 'post', )
            return _id
        except Exception as e:
            logging.exception(e)
            raise e

    @allure.step("导出设备")
    def export_devices(self, param) -> str:
        """

        :param param:
        :return:
        """
        return self.api.send_request('api/v1/devices/export', 'get', param).content.decode('UTF-8-sig')

    @allure.step("批量导入设备任务状态查询")
    @loop_inspector('import devices', timeout=10, interval=2)
    def assert_import_devices_status(self, _id: str, expect: dict):
        """

        :param _id: 批量导入任务id
        :param expect: 期望结果
        :return: AssertionError
        """
        result = self.api.send_request('/api/v1/devices/imports?limit=100&page=0', 'get').json().get('result')
        for i_ in result:
            if i_.get('_id') == _id:
                try:
                    dict_in(i_, expect)
                    return True
                except AssertionError:
                    return False

    @allure.step("设备拥有功能校验")
    def function_validate(self, sn: str, function: dict):
        """

        :param sn:
        :param function: {'nezha_device_config': True, 'nezha_cellular_signal': False}
        :return:
        """
        if function:
            _id = self.info(sn).get('_id')
            compatibilities = list(function.keys())
            body = {"ids": [_id], "compatibilities": compatibilities, "type": "device"}
            result = self.api.send_request(f'/api/v1/product-compatibilities/bulk-validate', 'post',
                                           body=body).json().get('result')[0]
            contain_ = {key: {"support": value} for key, value in function.items()}
            dict_in(result, {"compatibilities": contain_})


class Config(Base):

    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__device = Device(api, email, host)
        self.__group = Group(api, email, host)

    @allure.step("下发配置")
    def send(self, sn_or_group: str, payload: dict, commit=True, type_='device') -> dict:
        """下发设备配置

        :param sn_or_group: 设备序列号 或分组的名称
        :param commit: 是否提交, 在云端可以保存配置，默认是提交
        :param payload: 配置内容，当配置中的key是随机id时， 可使用$id，下发时会自动替换成随机id
        :param type_: device | group 通过sn或者分组名称下发配置
        :return:
        """

        def switch_config(in_payload: dict) -> dict:
            """转换配置，当配置中的key是随机id时， 可使用$id, 然后该函数会自动替换成随机id并返回

            :param in_payload: 需要修正的配置项，其中需要更新的key 使用$id来替换
            :return:
            """
            local_time = str(hex(int(time.time())))[2:]
            start = f'000{random.randint(1, 9)}{local_time}'
            in_payload = str(in_payload)
            for i in range(0, len(re.findall('\$id', in_payload))):
                in_payload = in_payload.replace('$id',
                                                f'{start}{generate_string(4, uppercase=False, special_chars=False)}',
                                                1)
            return eval(in_payload)

        payload = switch_config(payload)
        param = {'groupId': self.__group.info(sn_or_group).get('_id')} if type_ == 'group' else {
            'deviceId': self.__device.info(sn_or_group).get('_id')}
        session_id = self.api.send_request('/api/v1/config/init', 'post', param=param).json().get('result').get('_id')
        header = {'x-session-id': session_id}
        resp = self.api.send_request('/api/v1/config', 'put', body=payload, header=header).json()
        assert resp == {'result': 'ok'}, 'save config failed'
        if commit:
            resp = self.api.send_request('/api/v1/config/commit', 'post', header=header).json()
            assert resp == {'result': 'ok'}, 'commit config failed'
            logging.info(f'the {type_} {sn_or_group} config commit success')
        return payload

    @allure.step("获取配置")
    def get(self, sn_or_group: str, expect: dict = None, config_type='actual', type_='device') -> dict or None:
        """获取校验备配置

        :param sn_or_group: 设备序列号或者分组的名称
        :param expect: 配置内容，完整的配置路径，如{'lan': {'type': 'dhcp'}}
        :param config_type: actual 实际设备上传的配置
                      group 设备所在组的配置
                      pending 正在下发的配置
                      target 目标配置
                      individual 个性化配置
                      none
        :param type_: device | group 通过sn或者分组名称获取配置
        :return: 如果 expect 为None 就返回设备当前实际的配置
        """
        if type_ != 'group':
            path = f'/api/v1/devices/{self.__device.info(sn_or_group).get("_id")}/config'
        else:
            path = f'/api/v1/config/layer/group/{self.__group.info(sn_or_group).get("_id")}'
        if expect is not None:
            expect = {'result': {config_type: expect}}
            self.api.send_request(path, 'get', expect=expect)
        else:
            return self.api.send_request(path, 'get').json().get('result').get(config_type)

    def get_uuid_config(self, sn: str, fields: str, condition: dict, not_none=False) -> list or None:
        """根据条件返回当前配置的uuid

        :param sn: 设备序列号
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
        config = self.get(sn, None)
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
                logging.info('not find key, return $id')
            else:
                raise ResourceNotFoundError('not find key, please check the fields')
        if not not_none:
            logging.info(f'find the matched uuid: {id_}')
        return [id_, config_]

    @allure.step("清除配置")
    def clear_config(self, sn: str):
        """清除设备配置

        :param sn:
        :return:
        """
        self.api.send_request(f'/api/v1/config/layer/device/{self.__device.info(sn).get("_id")}', 'delete',
                              expect={
                                  "result": 'ok'})
        self.get(sn, expect={}, type_='individual')

    @allure.step("复制配置")
    def copy_config(self, source_sn: str, target_sns: list = None, target_group: list = None,
                    target_group_id: list = None):
        """清除设备配置

        :param source_sn: 源设备sn
        :param target_sns: 目标设备sn
        :param target_group: 目标分组名称
        :param target_group_id: 目标分组id
        :return:
        """
        if target_sns:
            body = {"sourceDeviceId": self.__device.info(source_sn).get("_id"),
                    "targetDeviceIds": [self.__device.info(device).get('_id') for device in target_sns]}
            self.api.send_request(f'/api/v1/config/layer/bulk-copy', 'post', body=body, expect={"result": 'ok'})
        if target_group or target_group_id:
            if not target_group_id:
                target_group_id = [self.__group.info(name).get('_id') for name in target_group]
            body = {"sourceDeviceId": self.__device.info(source_sn).get("_id"),
                    "targetGroupIds": target_group_id}
            self.api.send_request(f'/api/v1/config/layer/bulk-copy', 'post', body=body, expect={"result": 'ok'})


class Org(Base):

    def org_info(self, name=None, **kwargs) -> dict:
        """
        获取组织信息
        :param name: 根据组织名称返回信息
        :param kwargs:
               如果有_id: 就直接返回该组织的信息
               如果有org_admin: 就返回该组织的管理员信息
        :return:
        """
        _id = org_admin = None
        if kwargs.get('_id'):
            _id = kwargs.get('_id')
        if kwargs.get('org_admin'):
            org_admin = True
        for i in range(0, 20):  # 20次查询，如果组织数量超过100，就需要多次查询
            orgs = self.api.send_request('/api/v1/orgs', 'get', param={'depth': 5, 'limit': 100, 'page': i}).json()
            for org in orgs.get('result'):
                if _id:
                    if org.get('_id') == _id:
                        return org
                elif org_admin:
                    if org.get('level') == 1:
                        return org
                else:
                    if org.get('name') == name:
                        return org
            if len(orgs.get('result')) <= 100:
                raise ResourceNotFoundError(f'org not found')

    def role_info(self, type_='admin') -> dict:
        """
        获取角色信息
        :param type_: admin|orgAdmin|device_manager|readonly
        :return:
        """
        roles = self.api.send_request('/api/v1/roles', 'get', param={'app': 'nezha', 'sort': 'index,desc'}).json()
        for role in roles.get('result'):
            if role.get('name') == type_:
                return role
        else:
            raise ResourceNotFoundError(f'role not found')

    def user_info(self, email: str) -> dict:
        """
        获取用户信息
        :param email:
        :return:
        """
        users = self.api.send_request('/api/v1/users', 'get',
                                      param={'email': email, 'limit': 100, 'page': 0, 'expand': 'roles,mfa,org'}).json()
        for user in users.get('result'):
            if user.get('email') == email:
                return user
        else:
            raise ResourceNotFoundError(f'user not found')

    @allure.step("SaaS创建组织机构")
    def create(self, name: str, parent_name: str = None, level=2, email='', phone='', **kwargs) -> str:
        """创建组织, 创建2级组织时，parent_name和parent_id可以不传

        :param name: 组织名称 (在实现自动化时可让名称唯一，来实现创建组织的唯一性)
        :param parent_name: 父组织名称，如果组织名称唯一，可以传入，如果不唯一就拿第一个创建
        :param level: 组织层级，2 二级组织，3 三级组织 4 四级组织 5 五级组织
        :param email: 组织邮箱
        :param phone: 组织电话
        :param kwargs: 组织信息
               parent_id: 父组织id，唯一id，传入它时可以不用传入parent_name
               description: 组织描述
               force: 是否强制创建，如果组织已存在，是否强制创建
        :return: 组织id
        """
        if level in (2, 3, 4, 5):
            org_admin = True if level - 1 == 1 else False
            parent_id = self.org_info(name=parent_name, _id=kwargs.get('parent_id'), org_admin=org_admin).get('_id')
            body = {'name': name, 'parent': parent_id, 'phone': phone, 'email': email,
                    'description': kwargs.get('description')}
            logging.info(f'create org {name} success')
            return self.api.send_request('/api/v1/orgs', 'post', body=body).json().get('result').get('_id')
        else:
            raise ValueError('level must be in (2, 3, 4, 5)')

    @allure.step("SaaS删除组织机构")
    def delete(self, name: str, _id=None, ):
        """删除组织, 不能删除一级组织

        :param name: 组织名称, _id 为None时，使用名称删除，搜索到名称一致的组织就全部删除
        :param _id: 组织id, 使用id删除，精确删除
        :return:
        """
        id_ = self.org_info(name=name, _id=_id).get('_id')
        self.api.send_request(f'/api/v1/orgs/{id_}', 'delete')
        logging.info(f'delete org success')

    @allure.step("SaaS外部机构查询验证")
    def external_org(self, info: dict or list):
        """SaaS外部机构查询

        :param info: dict: {'oid': $oid, 'roleName': $roleName, 'orgName': $orgName} 可以是多个
        :return:
        """

        def _ex_one_org(info_: dict, result_):
            role_id = self.role_info(info_.get('roleName')).get('_id')
            user_oid = self.me.get('oid')
            for result_one in result_:
                if result_one.get('oid') == info_.get('oid'):
                    dict_in(result_one, dict_merge(info_, {'userOid': user_oid, 'roleId': role_id}))

        result = self.api.send_request('/api/v1/user/identities', 'get').json().get('result')
        if isinstance(info, dict):
            _ex_one_org(info, result)
        else:
            for _info in info:
                _ex_one_org(_info, result)

    @allure.step("SaaS添加用户")
    def add_user(self, email: str, org_name=None, role='admin', type_='internal', **kwargs):
        """

        :param email: 用户邮箱
        :param org_name: 添加组织的名称
        :param role: admin|orgAdmin|device_manager|readonly， 只有加入到一级组织时，才可以设置admin角色
        :param type_: internal 内部用户，external 外部用户，invite 邀请用户, invite_link 获取邀请链接用户
        :param kwargs:
               name: 用户名称,  internal，invite 用户必填
               password: 密码，internal，invite 用户必填
               org_id: 组织机构id
               org_admin: True 一级组织管理员，False 级组织管理员
               reset_invite_link, 重置邀请链接 默认False
        :return:
        """
        org_id = self.org_info(name=org_name, _id=kwargs.get('org_id'), org_admin=kwargs.get('org_admin', False)).get(
            '_id')
        role_id = self.role_info(role).get('_id')
        if type_ == 'internal':
            body = {'email': email, 'oid': org_id, 'roleId': role_id, 'type': type_, 'name': kwargs.get('name'),
                    'password': kwargs.get('password')}
            self.api.send_request('/api/v1/users', 'post', body=body)
        elif type_ == 'external':
            body = {'email': email, 'oid': org_id, 'roleId': role_id, 'type': type_, 'app': 'nezha'}
            self.api.send_request('/api/v1/users/invite', 'post', body=body)  # 邀请外部用户， 只发出了邀请邮件
        else:
            body = {'oid': org_id, 'roleId': role_id}
            url = self.api.send_request('/api/v1/users/invitations', 'post', body=body).json().get('result').get('url')
            if kwargs.get('reset_invite_link'):
                self.api.send_request(f'/api/v1/users/invitations/reset', 'put', body=body)
            parsed_url = urlparse(url)
            new_url = parsed_url._replace(path='/api/v1/users/invitations/' + url.split('/')[-1] + '/register')
            self.api.send_request(None, 'post',
                                  body={'email': email, 'name': kwargs.get('name'), 'password': kwargs.get('password')},
                                  auth=False, url=urlunparse(new_url))

    @allure.step("SaaS外部用户重发邀请邮件")
    def resend_external(self, email: str):
        """

        :param email:
        :return:
        """
        _user_id = self.user_info(email).get('_id')
        self.api.send_request(f'/api/v1/users/{_user_id}/resend-invite', 'get', param={'app': 'nezha'})

    @allure.step("SaaS锁定用户")
    def lock_user(self, email: str):
        """

        :param email:
        :return:
        """
        _user_id = self.user_info(email).get('_id')
        self.api.send_request(f'/api/v1/users/{_user_id}/lock', 'put')

    @allure.step("SaaS解锁用户")
    def unlock_user(self, email: str):
        """

        :param email:
        :return:
        """
        _user_id = self.user_info(email).get('_id')
        self.api.send_request(f'/api/v1/users/{_user_id}/unlock', 'put')

    @allure.step("SaaS删除用户")
    def delete_user(self, email: str or list):
        """

        :param email:
        :return:
        """
        users = [self.user_info(email).get('_id')] if isinstance(email, str) else [self.user_info(e).get('_id') for e
                                                                                   in email]

        self.api.send_request(f'/api/v1/users/remove', 'post', body={"resourceIds": users})

    @allure.step("SaaS更新用户属性")
    def update_user(self, email: str, **kwargs):
        """更新用户

        :param email: 用户邮箱
        :param kwargs:
               password: 密码
               name: 用户名称
               role: admin|orgAdmin|device_manager|readonly
               org_name:
               org_id:
               org_admin:
        :return:
        """
        _user = self.user_info(email)
        if kwargs.get('password'):
            self.api.send_request(f'api/v1/users/{_user.get("_id")}/password', 'put',
                                  body={'password': kwargs.get('password')})
        logging.info(f'the {email} user update password success')
        if self.email == email:
            self.api = InRequest(self.host, email, kwargs.get('password'), 'star')  # 重新登录
        update_info = {}
        if kwargs.get('name'):
            if not _user.get('collaborator'):
                update_info['name'] = kwargs.get('name')
                update_info['type'] = 'internal'
            else:
                update_info['type'] = 'external'
        if kwargs.get('role'):
            update_info['roleId'] = self.role_info(kwargs.get('role')).get('_id')
        if kwargs.get('org_name') or kwargs.get('org_id') or kwargs.get('org_level'):
            org_id = self.org_info(name=kwargs.get('org_name'), _id=kwargs.get('org_id'),
                                   org_admin=kwargs.get('org_admin', False)).get('_id')
            update_info['oid'] = org_id
        if update_info:
            self.api.send_request(f'/api/v1/users/{_user.get("_id")}', 'put', body=update_info)


class Group(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__org = Org(api, email, host)
        self.__device = Device(api, email, host)

    def info(self, name, _id=None) -> dict:
        for i in range(0, 20):  # 20次查询，如果组织数量超过100，就需要多次查询
            groups = self.api.send_request('/api/v1/devicegroups', 'get', param={'page': i, 'limit': 100}).json()
            for group in groups.get('result'):
                if group.get('name') == name or group.get('_id') == _id:
                    return group
            if len(groups.get('result')) <= 100:
                raise ResourceNotFoundError(f'group not found')

    @allure.step("SaaS创建分组")
    def create(self, name: str, product: str, firmware: str, org_name: str, org_id=None, org_admin=False) -> str:
        """创建分组

        :param name: 分组名称(在实现自动化时可让名称唯一，来实现创建分组的唯一性)
        :param product: 产品名称
        :param firmware: 固件版本
        :param org_name: 所属组织名称
        :param org_id: 组织id，唯一id，传入它时可以不用传入org_name
        :param org_admin: 是否为组织管理员
        :return: 组织id
        """
        org_id = org_id if org_id else self.__org.org_info(name=org_name, org_id=org_id, org_admin=org_admin).get('_id')
        body = {"name": name, "product": product, "firmware": firmware, "oid": org_id}
        result = self.api.send_request('/api/v1/devicegroups', 'post', body=body).json()
        logging.info(f'create group {name} success')
        return result.get('result').get('_id')

    @allure.step("SaaS删除分组")
    def delete(self, name: str or list, _id: str or list = None, ):
        """删除分组

        :param name: 分组名称, _id 为None时，使用名称删除，搜索到名称一致的分组只删除第一个
        :param _id: 分组id, 使用id删除，精确删除
        :return:
        """
        if _id:
            if isinstance(_id, str):
                _id = [_id]
        else:
            if name:
                if isinstance(name, str):
                    _id = [self.info(name=name).get('_id')]
                else:
                    _id = [self.info(group_name).get('_id') for group_name in name]
        if _id:
            self.api.send_request('/api/v1/devicegroups/remove', 'post', body={'ids': _id})
        logging.info(f'delete groups success')

    @allure.step("SaaS分组移入或移出设备")
    def move(self, sn: list, group_name: str, group_id: str = None, type_='in'):
        """移动设备到分组

        :param sn: 设备sn列表
        :param group_name: 分组名称
        :param group_id: 分组id 二选一, 传入id时，不用传入group_name
        :param type_: 移动类型，in: 移入分组， out: 移出分组
        :return:
        """
        group = self.info(group_name, group_id)
        if type_ == 'in':
            items = [{"deviceId": info.get('_id'), "deviceGroupId": group.get('_id'), 'oid': group.get('oid')} for info
                     in [self.__device.info(sn_) for sn_ in sn]]
        else:
            items = [{"deviceId": info.get('_id'), 'oid': group.get('oid')} for info in
                     [self.__device.info(sn_) for sn_ in sn]]
        self.api.send_request('/api/v1/devices/move', 'put', body={'items': items})
        logging.info(f'move device {sn} {type_} group success')

    @allure.step("SaaS设备移动到子组织")
    def move_to_org(self, sn: list, org_name: str, org_id: str = None):
        """移动设备到移动到子组织

        :param sn: 设备sn列表
        :param org_name: 分组名称
        :param org_id: 分组id 二选一, 传入id时，不用传入group_name
        :return:
        """
        org_id = self.__org.org_info(org_name, _id=org_id).get('_id')
        items = [{"deviceId": info.get('_id'), 'oid': org_id} for info in
                 [self.__device.info(sn_) for sn_ in sn]]
        self.api.send_request('/api/v1/devices/move', 'put', body={'items': items})
        logging.info(f'move device {sn} to org {org_name} success')

    @allure.step("SaaS分组获取配置")
    def get_config(self, group_name: str, expect: dict, type_='actual', group_id: str = None) -> dict or None:
        """分组获取配置校验

        :param group_name: 设备序列号
        :param expect: 配置内容，完整的配置路径，如{'lan': {'type': 'dhcp'}}
        :param type_: actual 实际设备上传的配置
                      group 设备所在组的配置
                      pending 正在下发的配置
                      target 目标配置
                      individual 个性化配置
                      'none'
        :param group_id: 分组id 二选一, 传入id时，不用传入group_name
        :return: 如果 expect 为None 就返回分组当前实际的配置
        """
        if type_ == 'none':
            expect = {'result': expect}
        else:
            expect = {'result': {type_: expect}}
        _id = self.info(group_name, group_id).get('_id')
        if expect is not None:
            self.api.send_request(f'/api/v1/config/layer/group/{_id}', 'get', expect=expect)
        else:
            return self.api.send_request(f'/api/v1/config/layer/group/{_id}', 'get').json().get('result').get(type_)


class Alert(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__group = Group(api, email, host)
        self.__device = Device(api, email, host)
        self.__org = Org(api, email, host)

    @allure.step("创建告警规则")
    def create_rule(self, rules: dict or list, users: list, groups: list, channels=None, expect=None) -> str:
        """

        :param rules: {"type": "reboot"}, or [{"type": "connected", "param": {retention: 600}}]
        :param users:  用户邮箱列表
        :param channels: 通知渠道列表 ["email"]  sms app
        :param groups: 分组名列表, 需保障分组名唯一
        :param expect: 预期结果
        :return:  rule_id
        """
        rules = [rules] if isinstance(rules, dict) else rules
        user_ids = [self.__org.user_info(email=user).get('_id') for user in users]
        channels = ['email'] if channels is None else channels
        groups_id = [self.__group.info(name=group).get('_id') for group in groups]
        body = {"rules": rules, "notify": {"users": user_ids, "channels": channels},
                "groupIds": groups_id}
        return self.api.send_request('/api/v1/alerts/rules', 'post', body=body, expect=expect).json().get('result').get(
            '_id')

    @allure.step("编辑告警规则")
    def edit_rule(self, _id: str, rules: dict or list, users: list, groups: list, channels=None, expect=None):
        """

        :param _id: rule_id
        :param rules: {"type": "reboot"}, or [{"type": "connected", "param": {retention: 600}}]
        :param users:  用户邮箱列表
        :param channels: 通知渠道列表 ["email"]  sms app
        :param groups: 分组名列表, 需保障分组名唯一
        :param expect: 预期结果
        :return:  rule_id
        """
        rules = [rules] if isinstance(rules, dict) else rules
        user_ids = [self.__org.user_info(email=user).get('_id') for user in users]
        channels = ['email'] if channels is None else channels
        groups_id = [self.__group.info(name=group).get('_id') for group in groups]
        body = {"rules": rules, "notify": {"users": user_ids, "channels": channels},
                "groupIds": groups_id}
        self.api.send_request(f'/api/v1/alerts/rules/{_id}', 'put', body=body, expect=expect)

    @allure.step("删除告警规则")
    def delete_rule(self, ids: list, expect=None):
        self.api.send_request(f'/api/v1/alerts/rules/bulk-delete', 'post', body={"ids": ids}, expect=expect)

    @allure.step("查询告警规则")
    def find_rule(self, expect=None) -> list:
        """
        :param expect: 预期结果
        :return:  返回符合查询条件的所有告警规则id
        """
        result = self.api.send_request('/api/v1/alerts/rules', 'get', param={"limit": 100, "page": 0},
                                       expect=expect).json().get('result')
        if result:
            return [alert.get('_id') for alert in result]
        else:
            return []

    @allure.step("查询告警")
    def find_alert(self, params=None, expect=None) -> list:
        """
        :param expect: 预期结果
        :param params: 查询参数 ack=false
                                from=2023-08-02T16:00:00.000Z
                                to=2023-08-03T16:00:00.000Z
                                type=connected
                                deviceId=64c85ab3b51c32731f029155
                                deviceGroupId=64ba5b5e4718687c71936feb
                                expand=deviceGroup,org  默认
                                app=nezha 默认
                                limit=100 默认
                                page=0 默认
        :return:  返回符合查询条件的所有告警id
        """
        params = dict_merge({"expand": "deviceGroup,org", "app": "nezha", "limit": 100, "page": 0}, params)
        result = self.api.send_request('/api/v1/alerts', 'get', param=params, expect=expect).json().get('result')
        if result:
            return [alert.get('_id') for alert in result]
        else:
            return []

    @allure.step("确认告警")
    def ack_alert(self, ids: list, expect=None):
        """

        :param ids: 当list为空时，确认所有告警， 如果不为空时，确认指定告警
        :param expect:
        :return:
        """
        if ids:
            self.api.send_request('/api/v1/alerts/acknowledge', 'put', body={"ids": ids, "app": "nezha"}, expect=expect)
        else:
            self.api.send_request('/api/v1/alerts/acknowledge/all', 'put', body={"app": "nezha"}, expect=expect)


class Firmware(Base):

    def info(self, product: str, version=None) -> dict or list:
        """查询账号下对应产品 已发布版本

        :param product: ER805
        :param version: None 当版本为None返回所有的已发布版本
        :return:
        """
        param = {'fields': 'version,_id,latest,recommended', 'limit': 1000, 'status': 'published'}
        ver = self.api.send_request(f'/api/v1/products/{product.upper()}/firmwares', 'get', param).json().get('result')
        if version:
            for v in ver:
                if v.get('version') == version:
                    return v
            else:
                raise ResourceNotFoundError(f'{product} product version {version} not publish')
        else:
            return ver


class Log(Base):
    def __init__(self, api, email, host):
        super().__init__(api, email, host)
        self.__device = Device(api, email, host)

    @allure.step("SaaS验证job属性")
    def assert_job(self, job_id: str, **kwargs):
        """
        :param job_id: 任务id
        :param kwargs:
               status: canceled|
               type: firmware
               jobProcessDetails.total  总计下发的设备数
        :return:
        """
        param = {'jobId': job_id, 'expand': 'jobProcessDetails', 'limit': 20, 'page': 0}
        try:
            result = self.api.send_request(f'api/v1/jobs', 'get', param=param).json().get('result')[0]
        except IndexError:
            raise ResourceNotFoundError(f'job {job_id} not found')
        dict_in(result, kwargs)

    @allure.step("SaaS设备验证升级任务")
    def assert_device_task(self, sn: str, job_id: str, **kwargs):
        param = {'jobId': job_id, 'serialNumber': sn, 'limit': 20, 'page': 0}
        try:
            result = self.api.send_request('/api/v1/job/executions', 'get', param=param).json().get('result')[0]
        except IndexError:
            raise ResourceNotFoundError(f'job {job_id} not found')
        dict_in(result, kwargs)

    @allure.step("SaaS取消设备最新任务")
    def cancel_device_latest_task(self, sn: str):
        param = {'serialNumber': sn, 'limit': 20, 'page': 0}
        try:
            result = self.api.send_request('/api/v1/job/executions', 'get', param=param).json().get('result')[0]
            if result.get('status') == 'queued':
                self.api.send_request(f'/api/v1/job/executions/{result.get("_id")}/cancel', 'put')
            else:
                logging.warning(f'the {sn} latest task status is {result.get("status")}, can not cancel')
        except IndexError:
            raise ResourceNotFoundError(f'the {sn} not has task')

    @allure.step("SaaS取消任务")
    def cancel_job(self, job_id: str):
        """

        :param job_id: 任务id
        :return:
        """
        self.api.send_request(f'api/v1/jobs/{job_id}/cancel', 'put', expect={'result': 'ok'})

    @allure.step("SaaS 设备取消等待任务")
    def cancel_executions(self, job_id: str):
        """

        :param job_id: 任务id
        :return:
        """
        for i_ in range(0, 10):
            executions = self.api.send_request('api/v1/job/executions', 'get',
                                               {'jobId': job_id, 'status': 'queued', 'limit': 100, 'page': 0}).json()
            if executions.get('total') == 0:
                break
            else:
                for execution in executions.get('result'):
                    self.api.send_request(f'api/v1/job/executions/{execution.get("_id")}/cancel', 'put')


class Report(Base):

    @allure.step("创建报表")
    def create_policies(self, period: str, name: str, _format: str, schedule: dict, apply_to='all', templates='all',
                        recipient=None, description=None, expect=None):
        """
        :param templates: 模板列表    'all', TOTAL_DEVICES, DEVICE_DISTRIBUTION, FIRMWARE_STATUS,
                                    CONFIGURATION_STATUS, NETWORKING_METHOD, OFFLINE_TIMES_TOP_10,
                                    USAGE_SUMMARY, TOTAL_USAGE_TOP_10, USAGE_TOP_10_BY_CELLULAR,
                                    USAGE_TOP_10_BY_WIRED, USAGE_TOP_10_BY_WIRELESS, ALERTS_TOP_10_BY_DEVICE,
                                    ALERT_TOP_10_BY_TYPE
        :param apply_to: 适用对象，支持填入长度为1的字典   {"org": [ids]}, {"group": [ids]}
        :param period: 周期   LAST_1_DAY，LAST_3_DAYS，LAST_7_DAYS，LAST_30_DAYS
        :param name: 报表名称
        :param _format: 报表格式    PDF，XLSX
        :param schedule: 定时任务   定时任务字段：dayOfWeek, dayOfMonth, hourOfDay, minuteOfHour
        :param recipient: 收件人
        :param description: 描述
        :param expect: 预期结果
        :return:  report_id
        """
        tmp = {}
        if isinstance(apply_to, dict):
            for k, v in apply_to.items():
                tmp["type"] = k
                tmp["ids"] = v
        else:
            tmp["type"] = apply_to
        if isinstance(templates, list):
            templates = templates
        elif isinstance(templates, str):
            if templates == 'all':
                templates = ['TOTAL_DEVICES', 'DEVICE_DISTRIBUTION', 'FIRMWARE_STATUS', 'CONFIGURATION_STATUS',
                             'NETWORKING_METHOD', 'OFFLINE_TIMES_TOP_10', 'USAGE_SUMMARY', 'TOTAL_USAGE_TOP_10',
                             'USAGE_TOP_10_BY_CELLULAR', 'USAGE_TOP_10_BY_WIRED', 'USAGE_TOP_10_BY_WIRELESS',
                             'ALERTS_TOP_10_BY_DEVICE', 'ALERT_TOP_10_BY_TYPE']
        body = {"templates": templates, "applyTo": tmp, "period": period, "name": name, "format": _format,
                "scheduled": False, "recipient": recipient, "description": description}
        if schedule:
            body['scheduled'] = True
            body['schedule'] = schedule
        return self.api.send_request('/api/v1/incloud/report/policies', 'post', body=body, expect=expect).json().get(
            'result')

    @allure.step("获取历史报表")
    def history_list(self, name=None, date_from=None, date_to=None, expect=None):
        """
        :param name: 报表名称
        :param date_from: 开始时间
        :param date_to: 结束时间
        :param expect: 预期结果
        :return:
        """
        param = {
            "name": name,
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": 100,
            "page": 0
        }
        return self.api.send_request(f'/api/v1/incloud/reports', 'get', param=param, expect=expect).json().get('result')

    @allure.step("编辑报表规则")
    def edit_policies(self, report_id: str, period: str, name: str, _format: str, schedule: dict, apply_to='all',
                      templates='all', recipient=None, description=None, expect=None):
        tmp = {}
        if isinstance(apply_to, dict):
            for k, v in apply_to.items():
                tmp["type"] = k
                tmp["ids"] = v
        else:
            tmp["type"] = apply_to
        if isinstance(templates, list):
            templates = templates
        elif isinstance(templates, str):
            if templates == 'all':
                templates = ['TOTAL_DEVICES', 'DEVICE_DISTRIBUTION', 'FIRMWARE_STATUS', 'CONFIGURATION_STATUS',
                             'NETWORKING_METHOD', 'OFFLINE_TIMES_TOP_10', 'USAGE_SUMMARY', 'TOTAL_USAGE_TOP_10',
                             'USAGE_TOP_10_BY_CELLULAR', 'USAGE_TOP_10_BY_WIRED', 'USAGE_TOP_10_BY_WIRELESS',
                             'ALERTS_TOP_10_BY_DEVICE', 'ALERT_TOP_10_BY_TYPE']
        body = {"templates": templates, "applyTo": tmp, "period": period, "name": name, "format": _format,
                "scheduled": False, "recipient": recipient, "description": description}
        if schedule:
            body['scheduled'] = True
            body['schedule'] = schedule
        return self.api.send_request(f'/api/v1/incloud/report/policies/{report_id}', 'put', body=body,
                                     expect=expect).json().get('result')

    @allure.step("删除报表规则")
    def delete_policies(self, report_id: str, expect=None):
        return self.api.send_request(f'/api/v1/incloud/report/policies/{report_id}', 'delete', expect=expect).json()

    @allure.step("获取报表")
    def get_policies(self, _type="list", name=None, report_id=None, expect=None):
        param = {
            "name": name,
            "limit": 100,
            "page": 0
        }
        if _type == "list":
            return self.api.send_request(f'/api/v1/incloud/report/policies', 'get', param=param,
                                         expect=expect).json().get('result')
        elif _type == "detail" and report_id:
            return self.api.send_request(f'/api/v1/incloud/report/policies/{report_id}', 'get',
                                         expect=expect).json().get('result')

    @allure.step("删除报表")
    def delete(self, report_id: str, expect=None):
        return self.api.send_request(f'/api/v1/incloud/reports/{report_id}', 'delete', expect=expect).json()

    @allure.step("下载报表")
    def download(self, report_id: str, expect=None):
        return self.api.send_request(f'/api/v1/incloud/reports/{report_id}/download', 'get', expect=expect).json()

    @allure.step("重新生成报表")
    def recreate(self, report_id: str, expect=None):
        return self.api.send_request(f'/api/v1/incloud/reports/{report_id}/recreate', 'post', expect=expect).json()

    @allure.step("获取报表详情")
    def detail(self, report_id: str, expect=None):
        return self.api.send_request(f'/api/v1/incloud/reports/{report_id}', 'get', expect=expect).json().get('result')


class StarInterface:

    def __init__(self, email, password, host='star.inhandcloud.cn', proxy=False, **kwargs):
        """ 须确保用户关闭了多因素认证

        :param email  平台用户名
        :param password  平台密码
        :param host: 'star.inhandcloud.cn'|'star.inhandcloud.cn'|'star.nezha.inhand.dev'|'star.nezha.inhand.design' 平台是哪个环境,
        :param proxy: 是否使用代理
        :param kwargs:
            body_remove_none_key: 是否删除请求体中的空值
            param_remove_none_key: 是否删除请求参数中的空值
        """

        self.api = InRequest(host, email, password, 'star',
                             body_remove_none_key=kwargs.get('body_remove_none_key', True),
                             param_remove_none_key=kwargs.get('param_remove_none_key', True),
                             proxy=proxy)
        self.overview = Overview(self.api, email, host)
        self.device = Device(self.api, email, host)
        self.clients = Clients(self.api, email, host)
        self.firmware = Firmware(self.api, email, host)
        self.config = Config(self.api, email, host)
        self.org = Org(self.api, email, host)
        self.group = Group(self.api, email, host)
        self.log = Log(self.api, email, host)
        self.alert = Alert(self.api, email, host)
        self.report = Report(self.api, email, host)

    def set_x_api_oid(self, oid=None):
        if oid is None:
            self.api.headers = {}
        else:
            self.api.headers = {'X-Api-Oid': oid}


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log(console_level='debug')
    star = StarInterface('admin', '123456', 'star.nezha.inhand.design', proxy=False)
    device = star.device.find_device(expect=None, param={'serialNumber': 'MR80512345'})
    device_id = [device_.get('_id') for device_ in device]
    star.device.delete(device_id, 'id')
