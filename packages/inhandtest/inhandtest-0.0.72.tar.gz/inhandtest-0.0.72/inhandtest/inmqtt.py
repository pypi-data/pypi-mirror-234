# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 16:48:50
# @Author  : HengYi Li
# @File    : inmqtt.py
"""
inmqtt

"""
import json
import os
import re
import subprocess
import uuid
import time
from paho.mqtt import client
from inhandtest.tools import dict_flatten, check_windows_process
from inhandtest.file import check_file
import logging


class MqttClient:
    __doc__ = "使用前需安装paho-mqtt  pip install paho-mqtt"

    def __init__(self, host: str, port: int = 1883, username=None, password=None, client_id=None, clean_session=True,
                 reconnect_on_failure=True, keepalive=120, tls=False, proxy=False):
        """MQTT客户端

        :param host: 服务器地址
        :param port: 服务器MQTT端口
        :param username: username
        :param password: password
        :param client_id: client_id, 如果为None时随机获取
        :param clean_session: 是否清除session， 默认为True
        :param reconnect_on_failure: 失败时重连，默认为True
        :param tls: 是否使用tls，默认为False
        :param proxy: 是否使用代理，默认为False
        :param keepalive: 心跳 默认120
        """

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client_id = 'inhand-' + str(uuid.uuid4()) if client_id is None else client_id
        self.keepalive = keepalive
        self.clean_session = clean_session
        self.reconnect_on_failure = reconnect_on_failure
        self.tls = tls
        self.proxy = proxy  # 是否使用代理
        self.connect_time = None
        self.client = self.__connect()
        self.recv_datas = []

    def __on_connect(self, client, userdata, flags, rc):
        """
        :param client:
        :param userdata: Client()或user_data_set()中设置的私有用户数据
        :param flags:
        :param rc: 连接结果
            0：连接成功                        1：连接被拒绝 - 协议版本
            2: 连接被拒绝 - 客户端标识符无效      3：连接被拒绝 - 服务器不可用
            4：连接被拒绝 - 用户名或密码错误      5：连接被拒绝 - 未授权
            6-255：当前未使用
        :return:
        """
        if rc == 0:
            logging.info(f"{client} Connection success, id: {self.client_id}")
            self.connect_time = int(time.time())
        else:
            logging.error(f'client {self.client_id} connect failed, code=%s' % rc)

    def __on_message(self, client, userdata, message):
        try:
            logging.debug(
                f"client {self.client_id} recv topic '{message.topic}', payload {json.loads(message.payload)}")
            self.recv_datas.append((message.topic, json.loads(message.payload), int(round(time.time() * 1000))))
        except Exception:
            logging.error(f'client {self.client_id} recv exception data: {message.payload}')

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        logging.debug(f'On Subscribed: mid={mid}, qos={granted_qos}')

    def __on_publish(self, client, userdata, mid):
        logging.debug(f'On onPublish: mid={mid}')

    def __on_log(self, client, userdata, level, buf):
        logging.debug(buf)
        if 'WinError 10054' in buf:
            self.disconnect()

    def __on_disconnect(self, client, userdata, rc):
        logging.info(f'client {self.client_id} On disconnected: rc={rc}')
        if not self.reconnect_on_failure:
            self.disconnect()

    def __connect(self) -> client.Client:
        """连接MQTT服务器
        """
        # 生成随机ID
        if self.proxy:
            import socket
            import socks
            socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "10.5.17.21", 8118)
            socket.socket = socks.socksocket
        mqtt_client = client.Client(self.client_id, self.clean_session, reconnect_on_failure=self.reconnect_on_failure)
        mqtt_client.username_pw_set(self.username, self.password)
        mqtt_client.on_connect = self.__on_connect
        mqtt_client.on_message = self.__on_message
        mqtt_client.on_subscribe = self.__on_subscribe
        mqtt_client.on_publish = self.__on_publish
        mqtt_client.on_log = self.__on_log
        mqtt_client.on_disconnect = self.__on_disconnect
        logging.info(f'client {self.client_id} start connection')
        if self.tls:
            mqtt_client.tls_set()
        mqtt_client.connect(self.host, self.port, self.keepalive)
        mqtt_client.loop_start()
        return mqtt_client

    def disconnect(self) -> None:
        """断开MQTT连接
        """
        self.client.disconnect()
        self.client.loop_stop()

    def sub(self, topic, qos=0, clear_recv_datas=False) -> None:
        """订阅主题
        :param topic:
        1. Simple string and integer: subscribe("my/topic", 2)
        2. String and integer tuple: subscribe(("my/topic", 1))
        3. List of string and integer tuples: subscribe([("my/topic", 0), ("another/topic", 2)])
        :param qos: 默认为0, 订阅时的qos值
        :param clear_recv_datas: 订阅前是否要清除掉已接收的消息
        """
        self.recv_datas = [] if clear_recv_datas else self.recv_datas
        if isinstance(topic, str):
            self.client.subscribe(topic=topic, qos=qos)
        elif isinstance(topic, tuple):
            self.client.subscribe(topic)
        elif isinstance(topic, list):
            self.client.subscribe(topic)
        logging.info(f'client {self.client_id}  subscribe topic {topic}')

    def un_sub(self, topic: str or list) -> None:
        """取消主题订阅
        :param topic: A single string, or list of strings that are the subscription
               topics to unsubscribe from.
        """
        self.client.unsubscribe(topic)
        logging.info(f'client {self.client_id} unsubscribe , topic is {topic}')

    def pub(self, topic: str, payload: str or dict, qos=0, clear_recv_datas=False) -> None:
        """发布主题
        :param topic: the topic that the message should be published on
        :param payload: the actual message to send. If not given, or set to None a zero length
                        message will be used.
                        Passing an int or float will result in the payload being converted to
                        a string representing that number.
        :param qos: the quality of service level to use
        :param clear_recv_datas: 订阅前是否要清除掉已接收的消息
        """
        self.recv_datas = [] if clear_recv_datas else self.recv_datas
        if isinstance(payload, str):
            self.client.publish(topic, payload, qos)
        else:
            self.client.publish(topic, json.dumps(payload), qos)

        logging.info("client {}  publish {} {}".format(self.client_id, topic, payload))

    def expect_data(self, expect_recv_rules: dict, timeout=10) -> None:
        """ 对收到的数据做处理, 不管数据是否正常处理都会消费掉

        :param expect_recv_rules: 元组()或字典 {}
                                为字典时: ex: {'v1/${client_id}/summary/refresh/resp': {'status': '${value}=="connected"', 'result':{"status": '${value}=="connected"'}, "number": (4, 5), "time_interval": (450, 550)}
                                          {"number": (100, 100)}, 表示收到的所有消息是100条
                                          {'v1/${client_id}/summary': {'result':{"status": '${value}=="connected"'}, "number": (100, 100), "time_interval": (450, 550)}},
                                           表示接收到topic为'v1/${client_id}/summary' 消息100条，且每两条消息的时间间隔是450-550毫秒， 且验证payload内容{'result':{"status": 'connected'}}
                                          {'v1/${client_id}/summary': True} 表示存在topic为'v1/${client_id}/summary' 的消息
                                          {'v1/${client_id}/summary': False} 表示不存在topic为'v1/${client_id}/summary' 的消息
                                      key 为具体的topic, value 为对应层次的表达式
                                      number: tuple|list, 且长度为2，(value1, value2)为特定字段，如果加上他就是代表该类消息的条数范围，(1, 2)表示接收的条数是在1和2条之间, 如果放在字典最外层表示，所有消息的数量
                                     time_interval: tuple, 且长度为2，(value1, value2)为特定字段，表示后一条消息与前一条消息的时间差范围，注意此处的单位是毫秒，(450, 550)表示大于等于450ms 小于等于550ms
                                    当判断payload中的value时输入完整表达式,当判断int型的关系时${value}和期望值不加"",而当需要调用str型的关系时${value}和期望值都要加"",
                                     例:（'${value}==1', '${value}!=1', '${value}>1', '${value}>=1', '${value}<1', '${value}<=1', "${value}"=="abc"
                                    '"${value}".startswith("123")', '"${value}".endswith("23")', '"${value}" in a', '"${value}" not in b',
                                    '"${value}".__contains__("234")', 'time.strptime("${value}", "%Y-%m-%d %H:%M:%S")', 'type(${value})==float',
                                    "len('${value}')==3"）
        :param timeout: 检测超时时间 单位秒
        :return:
        """
        time.sleep(timeout)
        logging.info(f'start analysis recv datas')
        try:
            if expect_recv_rules is not None:
                if isinstance(expect_recv_rules, dict):
                    for topic, assert_payload in expect_recv_rules.items():
                        if topic == 'number':
                            assert expect_recv_rules.get('number')[0] <= len(self.recv_datas) <= \
                                   expect_recv_rules.get('number')[1], f"all data count:{len(self.recv_datas)}"
                        else:
                            topic_payloads = list(filter(lambda x: x[0] == topic, self.recv_datas))
                            if isinstance(assert_payload, bool):
                                if assert_payload:
                                    assert topic_payloads, f'expect rule topic {topic} receive None'
                                else:
                                    assert not topic_payloads, f'expect rule topic {topic} receive {topic_payloads}'
                            elif isinstance(assert_payload, dict):
                                if assert_payload.get('number') is not None:
                                    assert assert_payload.get('number')[0] <= len(topic_payloads) <= \
                                           assert_payload.get('number')[
                                               1], f'expect rule topic {topic} receive {len(topic_payloads)} data error'
                                if assert_payload.get('time_interval') is not None:
                                    if len(topic_payloads) >= 2:
                                        fist_time = topic_payloads[0][2]  # 取第一条的第3个元素
                                        for time_payload in topic_payloads[1:]:
                                            if assert_payload.get('time_interval')[0] <= time_payload[2] - fist_time <= \
                                                    assert_payload.get('time_interval')[1]:
                                                fist_time = time_payload[2]
                                            else:
                                                logging.exception(
                                                    f"current data time is  {time_payload[2]},  last data time is {fist_time}")
                                                raise AssertionError(
                                                    f"current data time is  {time_payload[2]},  last data time is {fist_time}")
                                if assert_payload:
                                    def payload_verify(x):
                                        if x[0] == topic:
                                            expect_payload_ = dict_flatten(assert_payload)  # 平铺字典
                                            r_payload_ = dict_flatten(x[1])
                                            for expect_item_, expect_value_ in expect_payload_.items():
                                                if expect_item_ not in ('number', 'exist', 'time_interval'):
                                                    value_ = r_payload_.get(expect_item_)
                                                    expect_value_ = str(expect_value_).replace('${value}', str(value_))
                                                    if not eval(expect_value_):
                                                        logging.exception(expect_value_)
                                                        raise AssertionError(
                                                            f'payload error parm {expect_item_} value is {expect_value_} is False')

                                    [payload_verify(data_) for data_ in self.recv_datas]
                            else:
                                logging.exception('param expect_recv_rules topic value must be boolean or dict')
                                raise Exception('param expect_recv_rules topic value must be boolean or dict')
                else:
                    logging.exception('param expect_recv_rules must be dict')
                    raise Exception('param expect_recv_rules must be dict')
                logging.info("analysis data is ok")
        except Exception:
            logging.exception('analysis data is error')
            raise
        finally:
            self.recv_datas = []


class MosquittoBrokerWindows:
    __doc__ = "使用mosquitto 搭建mqtt server, 使用前需要确保mosquitto 正确安装到windows上面"

    def __init__(self, mosquitto_path='D:\Program Files\mosquitto', port=1883):
        """

        :param mosquitto_path:
        :param port:
        """
        self.mosquitto_path = mosquitto_path
        self.broker_log_file = os.path.join(self.mosquitto_path, 'mosquitto.log')
        self.sub_log_file = os.path.join(self.mosquitto_path, 'mosquitto_sub.log')
        self.mosquitto_exe = os.path.join(self.mosquitto_path, 'mosquitto.exe')
        self.mosquitto_sub = os.path.join(self.mosquitto_path, 'mosquitto_sub.exe')
        self.mosquitto_pub = os.path.join(self.mosquitto_path, 'mosquitto_pub.exe')
        self.port = port
        logging.info("check the mosquitto server is correct install")
        [check_file(file_) for file_ in (self.mosquitto_exe, self.mosquitto_sub, self.mosquitto_pub)]
        [os.chmod(file_, 0o777) for file_ in (self.broker_log_file, self.sub_log_file) if os.path.isfile(file_)]

    def start_mosquitto_broker(self, config='mosquitto.conf', clear_log=True) -> None:
        """

        :param config: 启动时的配置文件，可以根据不同的配置文件设置不同server的功能
        :param clear_log: 是否清除broker 日志
        :return:
        """
        if check_windows_process('mosquitto.exe'):
            logging.info(f"mosquitto broker server already start")
            self.close()
        if clear_log:
            open(self.broker_log_file, 'w').close()
        log = open(self.broker_log_file, 'a')
        cnf_file = os.path.join(self.mosquitto_path, config)
        subprocess.Popen(f'"{self.mosquitto_exe}" -c "{cnf_file}" -p {self.port} -v', stdout=log, stderr=log)
        logging.debug(f"start mosquitto broker server success")
        logging.debug(f"mosquitto broker log is {self.broker_log_file}")

    def broker_user(self, username, password, type_='add', filename='pwfile.example') -> None:
        """ 添加删除更新服务的用户

        :param username: 用户名
        :param password: 密码
        :param filename: 存储文件密码文件
        :param type_: 'add'|'delete'
        :return:
        """
        password_file = os.path.join(self.mosquitto_path, filename)
        password_exe = os.path.join(self.mosquitto_path, 'mosquitto_passwd.exe')
        check_file(password_exe)
        if type_ in ('add',):
            subprocess.Popen(f'"{password_exe}" -b "{password_file}" {username} {password}')
        else:
            subprocess.Popen(f'"{password_exe}" -D "{password_file}" {username} {password}')
        logging.info(f"{password_file} file {type_} user {username} success")

    def broker_psk(self, username, password, type_='add', filename='pskfile.example') -> None:
        """ 添加删除更新服务的PSK

        :param username: 用户名
        :param password: 密码
        :param filename: 存储文件密码文件
        :param type_: 'add'|'delete'
        :return:
        """
        psk_file = os.path.join(self.mosquitto_path, filename)
        contents = []
        if os.path.isfile(psk_file):
            with open(psk_file, 'r', encoding='utf-8') as f:
                contents = f.readlines()
        if contents:
            contents = [user.replace('\n', '') for user in contents]
            if type_ == 'add':
                contents = [user for user in contents if f'{username}:' not in user] + [f'{username}:{password}']
            else:
                contents = [user for user in contents if f'{username}:' not in user]
        else:
            contents = [f'{username}:{password}'] if type_ == 'add' else []
        contents = '' if not contents else '\n'.join(contents)
        with open(psk_file, 'w', encoding='utf-8') as f:
            f.write(contents)
        logging.info(f"{psk_file} file {type_} user {username} success")

    def sub(self, param: str, clear_log=True) -> int:
        """ 订阅Topic

        :param param: '-h 10.5.24.224 -p 1883 -t v1/VG7102022101801/# -u admin -P 123456'
        :param clear_log: 是否清除sub 日志
        :return: Popen
        """
        if clear_log:
            open(self.sub_log_file, 'w').close()
        log = open(self.sub_log_file, 'a')
        param = param + ' -v' if '-v' not in param else param
        p = subprocess.Popen(f'"{self.mosquitto_sub}" {param}', stdout=log, stderr=log)
        logging.info(f"mosquitto sub {param} success")
        logging.debug(f"mosquitto sub log path is {log}")
        return p.pid

    def pub(self, param: str) -> None:
        """ 发布Topic

        :param param: '-h 10.5.24.224 -p 1883 -t v1/VG7102022101801/# -u admin -P 123456 -m message'
        :return:
        """
        subprocess.Popen(f'"{self.mosquitto_pub}" {param}')
        logging.info(f"mosquitto pub {param} success")

    @staticmethod
    def close(server: str or int = 'mosquitto') -> None:
        """ 删除服务

        :param server: 'mosquitto'|'mosquitto_sub'| pid
                     如果为 'mosquitto_sub' 关闭所有sub任务， 如果为pid 则只关闭对应的服务
        :return:
        """

        if server == 'mosquitto':
            check_windows_process('mosquitto.exe', kill=True)
        elif server == 'mosquitto_sub':
            check_windows_process('mosquitto_sub.exe', kill=True)
        elif isinstance(server, int):
            check_windows_process(server, kill=True)
        else:
            logging.error(f"not support the {server} server close")

    def close_server_and_expect_log(self, broker_log_rules: dict = None, sub_log_rules: dict = None, timeout=10,
                                    clear_log=True) -> None:
        """ 关闭broker 或者 sub server 然后对收到的数据做处理

        :param broker_log_rules: ex : broker_log_rules = {'v1/${client_id}/summary': True, 'v1/${client_id}/info': (1, 10)},
                                      True or False 代表是否存在，元组(1, 10), 代表出现次数
        :param sub_log_rules: ex: sub_log_rules = {'v1/${client_id}/summary': True, 'v1/${client_id}/info': (1, 10)}}
                                  True or False 代表是否存在，元组(1, 10), 代表出现次数
        :param timeout: 数据校验超时时间
        :param clear_log: 检测完数据后是否清除日志
        :return:
        """
        time.sleep(timeout)
        for log_rule, log in zip((broker_log_rules, sub_log_rules), ('mosquitto', 'mosquitto_sub')):
            if log_rule:
                self.close(log)  # 关闭对应服务
                logging.info(f'start analysis {log} log')
                log_file = self.broker_log_file if log == 'mosquitto' else self.sub_log_file
                logs = ''
                if os.path.isfile(log_file) and os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        logs = ''.join([line.replace('\n', '') for line in f.readlines()])
                try:
                    for key, value in log_rule.items():
                        if isinstance(value, bool):
                            if value:
                                assert re.findall(key, logs), f"expect rule message {key} receive None"
                            else:
                                assert not re.findall(key, logs), f"expect rule message {key} receive any"
                        elif (isinstance(value, tuple) or isinstance(value, list)) and len(value) == 2:
                            assert value[0] <= len(re.findall(key, logs)) <= value[
                                1], f"expect rule message {key} number is error"
                        else:
                            logging.exception(f"param rules error")
                            raise Exception('param rules error')
                except Exception:
                    logging.exception(f"analysis {log} log is error")
                    raise
                finally:
                    if clear_log:
                        open(self.broker_log_file, 'w').close()
                logging.info(f"analysis {log} log is ok")
