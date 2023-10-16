#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/2/15 17:56
# @Author   : chengfeng
# @Email    : chengfeng@inhand.com.cn
# @File     : modbus.py


import modbus_tk
import modbus_tk.defines as cst
import serial
import math
import struct
import ctypes
import re
from modbus_tk import modbus_rtu, modbus_tcp, utils
import logging


class ModbusMaster:
    __doc__ = "使用前需安装pyserial, modbus-tk"

    def __init__(self, protocol: str, host: str, port=502, slave_id=1, baud_rate=9600, bytesize=8, parity='N',
                 stop_bits=1):
        """
        创建modbus master
        :param protocol: 协议类型| TCP| RTU
        :param host: 当协议为TCP时，填入IP地址，当协议为RTU时，填入串口号
        :param port: 端口号
        :param slave_id: 从站地址
        :param baud_rate: 串口波特率
        :param bytesize: 数据位
        :param parity: 校验位 N| O| E
        :param stop_bits: 停止位
        """
        self.logging = utils.create_logger("console", level=logging.DEBUG)
        try:
            if protocol.upper() == 'TCP':
                self.master = modbus_tcp.TcpMaster(host=host, port=port)
            else:
                self.uart = serial.Serial(host, baudrate=baud_rate, bytesize=bytesize, parity=parity,
                                          stopbits=stop_bits)
                self.master = modbus_rtu.RtuMaster(self.uart)
            self.master.set_timeout(5.0)
            self.master.set_verbose(True)
            self.logging.info("connected")
        except modbus_tk.modbus_rtu.ModbusInvalidResponseError as err:
            logging.exception("ModbusInvalidResponseError")
            raise err
        self.slave_id = slave_id

    def read_data(self, addr: str, datatype: str, length=0, decimal=0):
        """
        根据数据类型读指定寄存器地址
        :param addr: 寄存器地址
        :param datatype: 数据类型
        :param length: datatype为string类型时，必填项
        :param decimal: datatype为float类型时，必填项
        :return:
        """
        function_code_dict = {'0': cst.READ_COILS, '1': cst.READ_DISCRETE_INPUTS, '3': cst.READ_INPUT_REGISTERS,
                              '4': cst.READ_HOLDING_REGISTERS}
        addr = str(addr)
        function_code = function_code_dict[addr[0]]
        # print('function code is %s' % function_code)
        self.logging.info('PLC address function code is %s.' % function_code)
        type_ = datatype.upper()
        data = None
        if function_code in [1, 2] and type_ == 'BIT':
            return self.master.execute(self.slave_id, function_code, int(addr[1:]) - 1, 1)[0]
        elif function_code in [3, 4] and type_ in \
                ['INT', 'WORD', 'DINT', 'DWORD', 'LONG', 'ULONG', 'BCD16', 'BCD32', 'FLOAT', 'DOUBLE', 'STRING']:
            if type_ == 'INT':
                data = self.read_holding_registers(addr, function_code, 1, symbol=True)[0]
            elif type_ == 'WORD':
                data = self.read_holding_registers(addr, function_code, 1, symbol=False)[0]
            elif type_ == 'BCD16':
                data = int('{:x}'.format(self.read_holding_registers(addr, function_code, 1, symbol=False)[0]))
            elif type_ == 'FLOAT':
                data = self.read_float_data(addr, function_code)
            elif type_ in ['DINT', 'DWORD', 'BCD32']:
                data_tuple = self.read_holding_registers(addr, function_code, 2, symbol=False)
                if type_ == 'DINT':
                    data = self.read_not_16int_data(data_tuple, datatype=type_)
                elif type_ == 'DWORD':
                    data = ctypes.c_uint32(self.read_not_16int_data(data_tuple, datatype='DINT')).value
                else:
                    data = int(
                        '{:x}'.format(ctypes.c_uint32(self.read_not_16int_data(data_tuple, datatype='DINT')).value))
            elif type_ in ['LONG', 'ULONG', 'DOUBLE']:
                data_tuple = self.read_holding_registers(addr, function_code, 4, symbol=False)
                print(data_tuple)
                if type_ == 'ULONG':
                    data = ctypes.c_uint64(self.read_not_16int_data(data_tuple, datatype='LONG')).value
                else:
                    data = self.read_not_16int_data(data_tuple, datatype=type_)
            elif type_ == 'STRING':
                data_tuple = self.read_holding_registers(addr, function_code, (length + 1) // 2, symbol=False)
                data = self.read_not_16int_data(data_tuple, datatype=type_)[:length]
            else:
                pass
            if type_ in ['FLOAT', 'DOUBLE']:
                data = round(data, decimal)
            self.logging.info(f'PLC address {addr} read data is {data}')
            return data
        else:
            self.logging.exception(f'Datatype Error')
            raise Exception('The current register address does not match the data type.')

    def write_data(self, addr: str, datatype: str, write_value):
        """
        都指定寄存器地址写入值
        :param addr: 寄存器地址
        :param datatype: datatype
        :param write_value: 写入值
        :return:
        """
        type_ = datatype.upper()
        address = int(str(addr)[1:]) - 1
        addr = str(addr)
        if isinstance(write_value, str) and type_ != 'STRING':
            write_value = int(write_value)
        if addr[0] == '0':
            if write_value not in [0, 1, True, False]:
                logging.exception('This address type does not support writing such values.')
                raise Exception('This address type does not support writing such values.')
            else:
                self.master.execute(self.slave_id, cst.WRITE_MULTIPLE_COILS, address, output_value=[write_value])
        elif addr[0] == '4':
            if type_ == 'FLOAT':
                self.write_float_data(addr, write_value)
            elif type_ == 'INT':
                self.master.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, address, output_value=[write_value],
                                    data_format=">" + (1 * "h"))
            elif type_ in ['WORD', 'BCD16']:
                if type_ == 'BCD16':
                    write_value = self.bcd_to_decimal(write_value)
                self.master.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, address, output_value=[write_value])
            elif type_ in ['DINT', 'LONG', 'DOUBLE', 'DWORD', 'ULONG', 'STRING', 'BCD32']:
                if type_ in ['DWORD', 'BCD32']:
                    if type_ == 'BCD32':
                        write_value = self.bcd_to_decimal(write_value)
                    value = ctypes.c_int32(write_value).value
                    type_ = 'DINT'
                elif type_ in ['ULONG']:
                    value = ctypes.c_int64(write_value).value
                    type_ = 'LONG'
                elif type_ == 'STRING':
                    value = write_value.ljust(math.ceil(len(write_value) / 2) * 2)
                else:
                    value = write_value
                value_list = self.write_not_int16_data(value, type_)
                self.master.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, address, output_value=value_list)
        else:
            logging.exception('This address type does not support write operations.')
            raise Exception('This address type does not support write operations.')

    def read_holding_registers(self, addr, function_code, number, symbol=True):
        """
        读取寄存器
        if start==42,读取x轴坐标，需要除以1000
        :param addr:
        :param function_code: 功能码
        :param number:
        :param symbol: True | False
        :return:
        """
        start = int(addr[1:]) - 1
        if symbol:
            data_format = ">" + (number * "h")
            data = self.master.execute(self.slave_id, function_code, start, number, data_format=data_format)
        else:
            data = self.master.execute(self.slave_id, function_code, start, number)
        self.logging.info(f'PLC address {addr} read tuple is {data}')
        return data

    def read_float_data(self, addr, function_code):
        """
        读取单精度类型浮点数
        :param addr: 地址
        :param function_code: 功能码
        :return:
        """
        return self.master.execute(self.slave_id, function_code, int(addr[1:]) - 1, 2, data_format='>f')[0]

    def write_float_data(self, addr, value):
        """
        给单精度浮点数写值
        :param addr: 地址
        :param value: 值
        :return:
        """
        self.master.execute(self.slave_id, cst.WRITE_MULTIPLE_REGISTERS, int(addr[1:]) - 1, output_value=[value],
                            data_format='>f')

    @staticmethod
    def read_not_16int_data(*args, datatype):
        """
        读非16位整数和float类型以外的数据类型
        :param args: 传入参数
        :param datatype：数据类型 DINT| LONG| DOUBLE| STRING
        :return:
        """
        sum_v = ''
        for val in args[0]:
            value = '%04x' % val
            sum_v += value
        # print(sum_v)
        if datatype == 'STRING':
            string = ''
            str_list = re.findall(r'.{2}', sum_v)
            # print(str_list)
            for i in str_list:
                # print(chr(int(i, 16)))
                string += chr(int(i, 16))
            return string
        else:
            data_bytes = bytes.fromhex(sum_v)
            # print('data_bytes is %s' % data_bytes)
            if datatype == 'DINT':
                struct_format = '!i'
            elif datatype == 'LONG':
                struct_format = '!q'
            elif datatype == 'DOUBLE':
                struct_format = '!d'
            # elif datatype == 'STRING':
            #     struct_format = '!p'
            else:
                logging.exception('NonsupportDataType')
                raise Exception('NonsupportDataType')
            data = struct.unpack(struct_format, data_bytes)[0]
            return data

    @staticmethod
    def write_not_int16_data(value, datatype):
        """
        写入非16位整数和float类型以外的数据类型
        :param value:
        :param datatype: STRING| DINT| LONG| DOUBLE
        :return:
        """
        if datatype == 'STRING':
            lin = ['%02X' % ord(i) for i in value]
            y_bytes = ''.join(lin)
            eval_val = re.findall(r'.{4}', y_bytes)
        else:
            if datatype == 'DINT':
                struct_format = '!i'
            elif datatype == 'LONG':
                struct_format = '!q'
            elif datatype == 'DOUBLE':
                struct_format = '!d'
            else:
                logging.exception('NonsupportDataType')
                raise Exception('NonsupportDataType')
            y_bytes = struct.pack(struct_format, value)
            # print(y_bytes)
            # y_hex = bytes.hex(y_bytes)
            y_hex = ''.join(['%02x' % i for i in y_bytes])
            eval_val = re.findall(r'.{4}', y_hex)
        value_list = []
        for val in eval_val:
            val = int(val, 16)
            # print(val)
            value_list.append(val)
        return value_list

    def bcd_to_decimal(self, bcd):
        """
        BCD码转换为十进制
        :param bcd: BCD码
        :return: 十进制
        """
        string = ''
        if isinstance(bcd, int):
            bcd = str(bcd)
        for i in bcd:
            string += '{0:b}'.format(int(i)).zfill(4)
        decimal = int(string, 2)
        return decimal

    def decimal_to_bcd(self, decimal):
        """
        十进制转换为BCD码
        :param decimal: 十进制
        :return: BCD码
        """
        bcd = 0
        for i in range(4):
            bcd += (decimal // 10 ** i % 10) << (i * 4)
        return bcd

