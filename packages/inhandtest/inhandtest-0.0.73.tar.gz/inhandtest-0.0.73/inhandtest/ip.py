# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 14:41:08
# @Author  : Pane Li
# @File    : ip.py
"""
ip

"""
import ipaddress
import random
import re
import socket

import xeger


def ip_range(ip: str = '192.168.2.3', start_ip: str = '192.168.2.1', end_ip: str = '192.168.2.254',
             assertion=True) -> bool:
    """验证IP地址是否在约定的范围

    :param ip: 验证的IP地址
    :param start_ip: IP地址起始
    :param end_ip: IP地址结束
    :param assertion: 为True 时直接断言，为False时返回判断结果
    :return:
    """
    if ip and start_ip and end_ip:
        start_address = ipaddress.ip_address(start_ip)
        end_address = ipaddress.ip_address(end_ip)
        ip_address = ipaddress.ip_address(ip)
        if assertion:
            assert end_address >= ip_address >= start_address, 'ip is not in the specified range'
        else:
            return end_address >= ip_address >= start_address


def validate_mac(mac) -> None:
    assert re.match(r"^\s*([0-9a-fA-F]{2,2}:){5,5}[0-9a-fA-F]{2,2}\s*$", mac), f'"{mac}" is not mac'


def is_private_ip(ip) -> bool:
    return ipaddress.ip_address(ip).is_private


def get_ip(domain, protocol) -> list:
    my_addr = socket.getaddrinfo(domain, protocol)
    return [addr[4][0] for addr in my_addr]


def get_mac_by_ip(ip_addr: str) -> str:
    from psutil import net_if_addrs
    mac = None
    for k, v in net_if_addrs().items():
        y = [v for item in v if item[1] == ip_addr]
        if len(y) == 1:
            mac = y[0][0][1]
    return mac


def create_ip() -> str:
    base_ip = '{}.{}.{}.{}'.format(random.randint(1, 255), random.randint(0, 255), random.randint(0, 255),
                                   random.randint(0, 255))
    return base_ip


def create_mac() -> str:
    mac = []
    for i in range(1, 7):
        str_ = "".join(random.sample("0123456789abcdef", 2))
        mac.append(str_.upper())
    mac_list = ":".join(mac)
    return mac_list
