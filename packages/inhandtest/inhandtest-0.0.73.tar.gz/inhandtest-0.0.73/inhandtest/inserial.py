# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 9:24:33
# @Author  : Pane Li
# @File    : inserial.py
"""
inserial

"""
from threading import Thread
from inhandtest.tools import check_windows_process
from serial import *
from serial.tools import list_ports
from inhandtest.exception import *
import logging


class InSerial:

    def __init__(self, com='', baud_rate=115200, data_bits=8, parity='none', stop_bit=1, flow_control=False,
                 timeout=1, username='adm', password='123456'):
        """ 在使用串口做功能配置时需关闭日志服务器，避免影响功能，如果在接收日志时可不登录, 使用with 语句主动关闭串口

        :param com: com口，如不传系统自动查找, com1|com2
        :param baud_rate: 波特率
        :param data_bits: 8|7 只能是這兩個选项
        :param parity: none|even|odd
        :param stop_bit: 1|2
        :param flow_control: True|False
        :param timeout: 控制read函数读取超时时间
        :param username: 登录账号
        :param password: 登录密码
        """
        self.com = com.upper()
        self.baud_rate = baud_rate
        self.data_bits = data_bits
        self.parity = parity[0].upper()
        self.stop_bit = stop_bit
        self.flow_control = flow_control
        self.timeout = timeout
        self.username = username
        self.password = password
        self.__user_flag = 'Router#'
        self.__super_flag = '/www #'
        self.__config_flag = '(config)#'
        self.__normal_flag = 'Router>'
        self.serial = Serial()
        self.__auto_find_com()
        self.logs_number = []
        self.__open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __auto_find_com(self):
        if not self.com:
            port_list = list(list_ports.comports())
            logging.debug(port_list)
            if len(port_list) <= 0:
                logging.error("The Serial port can't find!")
            else:
                # 找到第一个可用的串口
                port_list_0 = list(port_list[0])
                self.com = port_list_0[0]

    def login(self, username=None, password=None):
        username = self.username if not username else username
        password = self.password if not password else password
        try:
            self.serial.write("\n".encode("gbk"))
            flag = self.serial.readlines(2)
            logging.debug(f'{flag[1].decode()}')
            flag = flag[1].decode("gbk").strip()
            if flag in (self.__config_flag, self.__super_flag, self.__normal_flag, self.__user_flag):
                pass
            elif 'login:' in flag:
                self.send_cli({username: ":"})
                self.serial.write((password + '\n').encode('gbk'))
                login_flag = self.serial.read_until('>'.encode("gbk")).decode("gbk")
                if ' \r\n' == login_flag:
                    logging.exception(f'Username Or Password Error')
                    raise UsernameOrPasswordError
                else:
                    tag = login_flag.split('\r\n')[-1].strip().replace('>', '')
                    self.__user_flag = f'{tag}#'
                    self.__normal_flag = f'{tag}>'
                    logging.debug(login_flag)
                    pass
            else:
                logging.exception(f'Serial Connect {self.com} Failed')
                raise ConnectionError
            logging.info(f'Serial Connect {self.com} Successful')
        except Exception:
            logging.exception(f'Serial Connect {self.com} Failed')
            raise ConnectionError

    def __open(self):
        try:
            check_windows_process(['sscom', 'MobaXterm'], True)
        except:
            pass
        self.serial.port = self.com
        self.serial.baudrate = self.baud_rate
        self.serial.bytesize = self.data_bits
        self.serial.parity = self.parity
        self.serial.stopbits = self.stop_bit
        self.serial.xonxoff = self.flow_control
        self.serial.timeout = self.timeout
        for i in range(0, 30, 3):
            if not self.serial.is_open:
                self.serial.open()
                logging.debug(f"open serial {self.com} success")
                break
            time.sleep(3)
        else:
            logging.exception(f"open serial {self.com} failed")
            raise SerialException(f'serial {self.com} already used')

    def receive_log(self, recv_timeout=20, logs_number=1):
        """接收日志

        :param recv_timeout: 接收超时时间
        :param logs_number
        :return:
        """
        self.serial.timeout = 1
        for i in range(0, recv_timeout, 1):
            try:
                data = self.serial.readline()  # 获取串口内容
            except AttributeError:
                break
            logging.debug(f'serial com {self.com} read str <{data.decode(errors="ignore")}>')
            if data:
                self.logs_number.append(data.decode(errors="ignore"))
            if logs_number == len(self.logs_number):
                break
            else:
                time.sleep(1)
        else:
            logging.exception(f'serial com {self.com} read log timeout')
            raise Exception('can not receive logs')

    def logout(self):
        self.send_cli({"exit": "[Y|N]", "y": "Press"})

    def send_cli(self, command: dict, encoding='gbk'):
        """发送命令，支持多条，

        @param command: 支持发送多条命令，命令为key，期望返回为value, 先执行的命令写前面
        {"first_command": "first_flag", "second_command": "second_flag"}
        @param encoding: 编码格式, 默认gbk, 支持 hex
        @return: 当发送一条命令时直接返回结果，发送多条时返回结果列表
        """
        flag_reacts = []
        if command:
            for com, flag in command.items():
                if encoding == 'hex':
                    self.serial.write(bytes.fromhex(com + "\r\n"))
                else:
                    self.serial.write(bytes((com + "\r\n").encode(encoding)))
                if not flag:
                    flag_react = None
                    time.sleep(1)
                else:
                    flag_react = self.serial.read_until(flag.encode("gbk")).decode("gbk").strip()
                logging.debug(flag_react)
                flag_reacts.append(flag_react)
        if len(flag_reacts) == 1:
            return flag_reacts[0]
        else:
            return flag_reacts

    def close(self):
        if self.serial.is_open:
            try:
                self.serial.close()
            except SerialException:
                logging.error(f'Serial Close {self.com} Failed')

    def assert_recv_data(self, action, length, timeout=10, content=None, **kwargs):
        """
        :param action: 操作函数
        :param length: 期望接受到的数据长度
        :param timeout: 最大超时时间
        :param content: 期望校验接受到的数据的内容
        """
        serial_thread = Thread(target=self.receive_log, args=(timeout, length))
        serial_thread.daemon = True
        serial_thread.start()
        time.sleep(1)
        action(**kwargs)
        for x in range(0, timeout, 1):
            result = True
            if length:
                if length != len(self.logs_number):
                    result = False
            if content and result:
                if isinstance(content, str):
                    if content not in ','.join(self.logs_number):
                        result = False
                else:
                    if [c for c in content if c not in ','.join(self.logs_number)]:
                        result = False
            if result:
                logging.info(f"assert data ok")
                break
            else:
                time.sleep(1)
                logging.debug(f"assert data failed, try again")
        else:
            logging.exception(f"assert data failed finally")
            raise Exception('serial not receive data')


if __name__ == '__main__':
    pass
