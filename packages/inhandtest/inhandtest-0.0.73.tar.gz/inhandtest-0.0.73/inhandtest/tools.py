# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 16:42:40
# @Author  : Pane Li
# @File    : tools.py
"""
tools

"""
import os.path
import random
import re
import string
import subprocess
import time
import datetime
import typing
from functools import wraps
from typing import List
import pytz
import requests
import speedtest

from inhandtest.file import file_hash
from inhandtest.exception import ResourceNotFoundError
import logging


def loop_inspector(flag='status', timeout=90, interval=5, assertion=True):
    """装饰器，期望接收函数返回的值为True，如果为False时进行轮询，直至超时失败，如果正确就退出

    :param flag:  功能名称，用以输出日志，如果不填  默认为’状态’二字
    :param timeout:  循环检测超时时间
    :param interval:  循环检测时间间隔
    :param assertion: 默认期望断言，如果为False时 返回值
    :return:  assertion为False时，返回函数的值
    """

    def timeout_(func):
        @wraps(func)
        def inspector(*args, **kwargs):
            nonlocal timeout, interval
            timeout = kwargs.get('timeout') if kwargs.get('timeout') else timeout
            interval = kwargs.get('interval') if kwargs.get('interval') else interval
            for i in range(0, timeout, interval):
                result = func(*args, **kwargs)
                if result or result is None:
                    logging.info(f'{flag} assert success')
                    return result
                else:
                    logging.info(f'{flag} assert failure, wait for {interval}s inspection')
                    time.sleep(interval)
                    continue
            else:
                if assertion:
                    logging.exception(f'{flag} assert timeout failure')
                    raise AssertionError(f'{flag} assert timeout failure')

        return inspector

    return timeout_


def check_device_product(support_product: list):
    """设备型号装饰器: 用于判断即将使用某方法或类的设备是否支持使用该方法或类
        需保证类有属性product

    :param support_product: 方法或类 支持的设备型号 list, 如：['ir302', 'ir305'], 不区分大小写
    :return:
    """
    support_product = [product.lower() for product in support_product]

    def wrapper(obj):
        if isinstance(obj, type):
            @wraps(obj, updated=())
            class Inner(obj):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    if self.product.lower() not in support_product:
                        logging.exception(f"This class not support this device that product is {self.product}")
                        raise Exception(f"This class not support this device that product is {self.product}")

            return Inner
        else:
            @wraps(obj)
            def inner(self, *args, **kwargs):
                if self.product.lower() in support_product:
                    return obj(self, *args, **kwargs)
                else:
                    logging.exception(f"This method not support this device that product is {self.product}")
                    raise Exception(f"This method not support this device that product is {self.product}")

            return inner

    return wrapper


def dict_merge(*dicts) -> dict:
    """合并多个字典

    :param dicts:
    :return:
    """
    result = {}
    for dict_ in dicts:
        if dict_ is not None:
            result.update(dict_)
    return result


def dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None) -> dict:
    """ 平铺字典

    :param in_dict: 输入的字典
    :param separator: 连接符号
    :param dict_out:
    :param parent_key:
    :return: dict
    """
    if dict_out is None:
        dict_out = {}

    for k, v in in_dict.items():
        k = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            dict_flatten(in_dict=v, dict_out=dict_out, parent_key=k)
            continue

        dict_out[k] = v

    return dict_out


def timezone_change(time_str, src_timezone, dst_timezone=None, time_format=None) -> str:
    """
    将任一时区的时间转换成指定时区的时间
    如果没有指定目的时区，则默认转换成当地时区  时区参考https://www.beijing-time.org/shiqu/

    :param time_str:
    :param src_timezone: 要转换的源时区，如"Asia/Shanghai" 即东八区， 'Europe/London' 零时区  'Canada/Eastern' 西五区 UTC-5
    :param dst_timezone: 要转换的目的时区，如"Asia/Shanghai", 如果没有指定目的时区，则默认转换成当地时区
    :param time_format: 默认格式"%Y-%m-%d %H:%M:%S"
    :return: str, 字符串时间格式
    """
    if not time_format:
        time_format = "%Y-%m-%d %H:%M:%S"

    # 将字符串时间格式转换成datetime形式
    old_dt = datetime.datetime.strptime(time_str, time_format)

    # 将源时区的datetime形式转换成GMT时区(UTC+0)的datetime形式
    dt = pytz.timezone(src_timezone).localize(old_dt)
    utc_dt = pytz.utc.normalize(dt.astimezone(pytz.utc))

    # 将GMT时区的datetime形式转换成指定的目的时区的datetime形式
    if dst_timezone:
        _timezone = pytz.timezone(dst_timezone)
        new_dt = _timezone.normalize(utc_dt.astimezone(_timezone))
    else:
        # 未指定目的时间，默认转换成当地时区
        new_dt = utc_dt.astimezone()
    # 转换成字符串时间格式
    return new_dt.strftime(time_format)


def check_windows_process(process: str or int or list, kill=False) -> bool or List[bool]:
    """ 检测进程是否运行
    :param process: str|int|list, 进程名称或进程pid(不一定是应用程序名称！), eg:'3CDaemon'|'mosquitto'|49040 如果有多个时使用list传入
    :param kill: True|False 当为True时，将检测到的进程杀死
    :return: boolean
    """

    def _search(process_):
        if process_:
            if isinstance(process_, str) or isinstance(process_, int):
                command = f'tasklist |findstr {process_}'
            else:
                logging.exception("not support process type")
                raise Exception("not support process type")
            logging.info(command)
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
            task_result = p.communicate()[0].strip()
            logging.debug(f'find {process_} process is: {task_result}')
            try:
                task_result = re.sub('\s+', ' ', task_result).split(' ')
                if len(task_result) % 6 == 0:  # 判断是6的倍数 说明一个程序打开了一个或多个进程
                    server_name = list(set([task_result[i] for i in range(len(task_result)) if i % 6 == 0]))
                else:
                    server_name = False
            except Exception:
                server_name = False
            return server_name
        else:
            return False

    if not kill:
        if isinstance(process, list):
            return [_search(name_) for name_ in process]
        else:
            return _search(process)
    else:
        process = process if isinstance(process, list) else [process]
        for name_ in process:
            if isinstance(name_, str):
                pid = _search(name_)
                if pid:
                    for process_ in pid:
                        logging.debug(f'taskkill /F /IM {process_}')
                        p = subprocess.Popen(f'taskkill /F /IM {process_}', shell=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT, encoding='gbk')
                        logging.debug(p.communicate()[0])
                        time.sleep(3)  # 删除服务应等待几秒，服务完全退出
                else:
                    logging.debug(f'not found task {name_}')
            elif isinstance(name_, int):
                logging.debug(f'taskkill /pid {name_} /F')
                p = subprocess.Popen(f'taskkill /pid {name_} /F', shell=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, encoding='gbk')
                logging.debug(p.communicate()[0])
                time.sleep(3)  # 删除服务应等待几秒，服务完全退出
            else:
                logging.exception("not support process type")
                raise Exception("not support process type")


def kill_windows_port(ip_, port: int or list) -> None:
    """ 杀死windows 相关端口服务

    :param ip_: 本机IP地址
    :param port: int|list, 端口号，可以是多个
    """
    import psutil
    import socket
    close_port = []

    def kill_one_port(one_port: int):
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                conn_list = proc.connections()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            for conn in conn_list:
                if conn.status == psutil.CONN_LISTEN and conn.laddr.port == one_port:
                    logging.debug(f"process {proc.pid} already use port {one_port}")
                    # 终止进程
                    try:
                        proc.kill()
                    except psutil.NoSuchProcess:
                        pass
                    logging.info(f"kill process {proc.pid} success")
                    close_port.append(one_port)

    def port_is_close(one_port: int):  # 杀死后要一直等到进程完全退出才能继续执行，否则会报错
        for i in range(0, 5 * 60, 30):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    windows_cmd(f'netstat -ano | findstr {one_port}', '', )
                    break
                except AssertionError:
                    time.sleep(30)
                    logging.info(f"wait for port {one_port} not to be timewait...")
                    continue
        else:
            logging.exception(f"kill process {one_port} failed")
            raise Exception(f"kill process {one_port} failed")

    [kill_one_port(port_) for port_ in port] if isinstance(port, list) else kill_one_port(port)
    if close_port:
        [port_is_close(port_) for port_ in close_port]


def windows_cmd(command: str or list, expect: str or list or dict = None, last_read_replace: dict = None):
    """输入一条或多条命令, 且支持对执行时最后一条命令返回的结果做断言

    :param command: 输入的一条或多条命令，注意操作者的权限
    :param expect: str or list or dict, 一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}
                       同时校验时可以是{$expect1: True, $expect: False}, str或者list时都是判断存在
                       校验失败时就会抛出AssertionError 异常
    :param last_read_replace: 对最后一条命令读取的内容做替换
    :return:
    """
    command = [command] if isinstance(command, str) else command
    last_read_content = None
    for command_ in command:
        logging.info(f'windows cmd do {command_}')
        if expect is None and last_read_replace is None:
            subprocess.Popen(command_, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
        else:
            p = subprocess.Popen(command_, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
            last_read_content = p.communicate()[0].strip()
            logging.debug(last_read_content)
    if last_read_replace and last_read_content is not None:
        last_read_content = replace_str(last_read_content, last_read_replace)
    if expect is not None:
        if isinstance(expect, str):
            if expect and (expect not in last_read_content):
                logging.exception(f'{expect} not in last read content')
                raise AssertionError(f'{expect} not in last read content')
            else:
                assert last_read_content != '', 'last read content not null'
        elif isinstance(expect, list):
            if [expect_ for expect_ in expect if expect_ not in last_read_content]:
                logging.exception(f'{expect} not in last read content')
                raise AssertionError(f'{expect} not in last read content')
        elif isinstance(expect, dict):
            for k, v in expect.items():
                if v:
                    if k not in last_read_content:
                        logging.exception(f'{k} not in last read content')
                        raise AssertionError(f'{k} not in last read content')
                else:
                    if k in last_read_content:
                        logging.exception(f'{k} in last read content')
                        raise AssertionError(f'{k} in last read content')
        else:
            logging.exception('parameter expect is error')
            raise Exception('parameter expect is error')


def download_svn_package(svn: dict, file_path, check_package=True) -> None:
    """

    :param svn: dict {'url': $url, 'username': $username, 'password': $password} 固件全路径
    :param file_path: 本地存放固件文件夹路径
    :param check_package: True|False 支持下载完文件后校验文件正确性
    :return:
    """
    from requests.auth import HTTPBasicAuth
    from requests.adapters import HTTPAdapter

    if svn.get("url") and svn.get('username') and svn.get('password') and file_path:
        url_path = svn.get("url")
        firmware_name = url_path.split('/')[-1]
        local_firmware_path = os.path.join(file_path, firmware_name)
        svn_hash_file_path = url_path.replace(firmware_name, 'sha256.txt')
        auth = HTTPBasicAuth(svn.get('username'), svn.get('password'))
        if (not os.path.isfile(local_firmware_path)) and (not os.path.exists(local_firmware_path)):
            logging.info(f"download {local_firmware_path} from svn and wait for a moment!")
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))  # 本身请求失败会重试3次
            for i in range(3):  # 文件下载错误再继续下载
                r = s.get(url_path, auth=auth)
                if r.status_code == 401:
                    logging.exception("svn username or password error")
                    raise Exception("svn username or password error")
                elif r.status_code == 200:
                    with open(local_firmware_path, 'wb') as fi_:  # 覆盖写入
                        fi_.write(r.content)
                    r_hash_file = s.get(svn_hash_file_path, auth=auth)
                    if check_package:
                        for co_ in r_hash_file.content.split(b'\n'):
                            if co_.decode('utf-8').endswith(firmware_name):
                                hash_sha256_value = co_.decode('utf-8').split(' ')[0].upper()
                                break
                        else:
                            logging.exception(f'{svn_hash_file_path} not contain {firmware_name} hash_sha256 value')
                            raise Exception(f'{svn_hash_file_path} not contain {firmware_name} hash_sha256 value')
                        if file_hash(local_firmware_path, 'sha256') == hash_sha256_value:
                            logging.debug(f'{local_firmware_path} download success')
                            break
                        else:
                            logging.warning(f'download package failed, try {i + 1} time')
                    else:
                        break
                else:
                    logging.exception("svn server down error")
                    raise Exception("svn server down error")
            else:
                logging.exception("download package failed")
                raise Exception('download package failed')


def get_time_stamp(time_='', delta=0, delta_type='h', time_format='%Y-%m-%dT%H:%M:%SZ') -> str:
    """获取时间戳

    :param time_: 默认获取当前时间
    :param delta: 要增加或者减少的时间
    :param delta_type: 单位 d:天 h:小时 m:分钟 s:秒
    :param time_format: 显示格式 ,为空时返回对应时间的时间戳
    :return:
    """
    delta_type = delta_type.lower()
    if delta_type == 'h':
        delta_time = datetime.timedelta(hours=delta)
    elif delta_type == 'm':
        delta_time = datetime.timedelta(minutes=delta)
    elif delta_type == 's':
        delta_time = datetime.timedelta(seconds=delta)
    elif delta_type == 'd':
        delta_time = datetime.timedelta(days=delta)
    else:
        delta_time = 0
    if not time_:
        time_stamp = datetime.datetime.utcnow() + delta_time
    else:
        time_stamp = datetime.datetime.strptime(time_, time_format) + delta_time
    res = time_stamp.strftime(time_format) if time_format else time_stamp.timestamp()
    return res


def get_nearest_minute_time(near_time=5) -> typing.Tuple[str, str]:
    """按照最近的整数倍时间点获取时间戳， 如默认5分钟，当前时间为 2020-05-20T10:23:00Z
       当start为True时，返回 2020-05-20T10:15:00Z, 当start为False时，返回 2020-05-20T10:20:00Z


    :param near_time:
    :param start:
    :return:
    """
    from datetime import timedelta
    current_time = datetime.datetime.utcnow()
    minutes = current_time.minute
    remainder = minutes % near_time
    if remainder == 0:
        return (current_time - timedelta(minutes=near_time)).strftime('%Y-%m-%dT%H:%M:00Z'), current_time.strftime(
            '%Y-%m-%dT%H:%M:00Z')
    else:
        nearest_multiple = minutes - remainder
        return (current_time - timedelta(minutes=minutes - nearest_multiple + near_time)).strftime(
            '%Y-%m-%dT%H:%M:00Z'), (current_time - timedelta(minutes=minutes - nearest_multiple)).strftime(
            '%Y-%m-%dT%H:%M:00Z')


def time_delta(time_list, delta, diff=0, time_format='%Y-%m-%dT%H:%M:%SZ', order_by=True):
    """校验连续数据时间差

    :param time_list: list of timestamp
    :param delta: int 单位秒 两个数据点之间的时间差10s 正整数
    :param diff: int 允许的误差 more为0  正整数
    :param time_format: str 时间格式
    :param order_by: bool True 传入的时间列表是按时间从小到大排列， False 传入的时间列表是按时间从大到小排列
    :return:
    """
    tmp = []
    for each in time_list:
        if isinstance(each, int):
            tmp.append(each)
        else:
            each = time.strptime(each, time_format)
            tmp.append(int(time.mktime(each)))
    t0 = tmp[0]
    for i_ in tmp[1:]:
        if not order_by:
            assert delta - diff <= t0 - i_ <= delta + diff, f'The time error between {t0} and {i_} is large'
        else:
            assert delta - diff <= i_ - t0 <= delta + diff, f'The time error between {t0} and {i_} is large'
        t0 = i_


def dict_in(expect_dict: dict, contain: dict) -> None:
    """验证字典包含关系

    :param expect_dict: dict {key: value}
    :param contain: dict,  支持${value} 表达式判断
    :return: AssertionError
    """
    if expect_dict and contain:
        contain_flatten = dict_flatten(contain)  # 平铺字典
        expect_dict_flatten = dict_flatten(expect_dict)  # 平铺字典
        for contain_item, contain_value in contain_flatten.items():
            value = expect_dict_flatten.get(contain_item)
            if isinstance(contain_value, str) and '${value}' in contain_value:
                expect_value = contain_value.replace('${value}', str(value))
                if not eval(expect_value):
                    logging.exception(f'expect_item {contain_item} value is {expect_value} is False')
                    raise AssertionError(f'expect_item {contain_item} value is {expect_value} is False')
            else:
                assert value == contain_value, f'expect_item {contain_item} value is {contain_value} is False'

        else:
            logging.info(f'{contain} in {expect_dict} assert ok')


def replace_str(old: str or list or dict, replace_value: dict) -> str:
    """深度替换字符串，避免替换重复出问题

    :param old:
    :param replace_value:
    :return:
    """
    new_old = old

    def replace_(replace_str_: str):
        for k_, i_ in zip(replace_value.keys(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace(k_, '${' + str(i_) + '}')
        for v_, i_ in zip(replace_value.values(), range(0, len(replace_value.keys()))):
            replace_str_ = replace_str_.replace('${' + str(i_) + '}', str(v_))
        return replace_str_

    if old and replace_value:
        replace_value = {k: v for k, v in replace_value.items() if v is not None}
        if replace_value:
            if isinstance(old, str):
                new_old = replace_(old)
            elif isinstance(old, list):
                new_old = [replace_(str(old_)) for old_ in old]
            elif isinstance(old, dict):
                new_old = {}
                for k, v in old.items():
                    new_old.update({replace_(str(k)): v})
            else:
                logging.exception('Not support this type')
                raise Exception('Not support this type')
    return new_old


def generate_string(length, digits=True, lowercase=True, uppercase=True, special_chars=True, chinese_chars=False,
                    peer_chinese_chars_len=1):
    """生成指定长度的密码，可以选择包含类型，如（数字、大小写字母、特殊字符、中文）

    :param length: 密码长度
    :param digits: 是否包含数字
    :param lowercase: 是否包含小写字母
    :param uppercase: 是否包含大写字母
    :param special_chars: 是否包含特殊字符
    :param chinese_chars: 是否包含中文字符
    :param peer_chinese_chars_len: 每个中文的长度算几，默认是1， 可以选择为2
    :return: 生成的密码
    """
    all_type = {'chinese_chars': chinese_chars, 'digits': digits, 'lowercase': lowercase, 'uppercase': uppercase,
                'special_chars': special_chars}

    def shuffle_string(string_):
        """
        将输入的字符串打乱顺序并返回
        """
        # 将字符串转换为列表
        chars = list(string_)
        # 使用random.shuffle函数打乱列表顺序
        random.shuffle(chars)
        # 将列表转换为字符串并返回
        return ''.join(chars)

    def random_chinese_character():
        return random.choice(
            '读取指定目录下的机内码与转换工具在没修改编码格式时无法正确打印汉字解决方法为只要在文件开头加入勉强你我他是姐妹兄弟任务简体字列表')

    def generate_random(length_, type_='digits'):
        if type_ == 'digits':
            return ''.join(str(random.randint(0, 9)) for _ in range(length_))
        elif type_ == 'lowercase':
            return ''.join(random.choice(string.ascii_lowercase) for _ in range(length_))
        elif type_ == 'uppercase':
            return ''.join(random.choice(string.ascii_uppercase) for _ in range(length_))
        elif type_ == 'special_chars':
            return ''.join(random.choice(string.punctuation) for _ in range(length_))
        elif type_ == 'chinese_chars':
            length_ = int(length_ / peer_chinese_chars_len) if peer_chinese_chars_len != 1 else length_
            return ''.join(random_chinese_character() for _ in range(length_))

    # 定义字符集
    def split_number(num, n, contain_even_=True):
        """
        将一个数字拆分成n个数字相加得来
        :param num: 要拆分的数字
        :param n: 拆分成n个数字相加
        :param contain_even_: 包含偶数
        :return: 拆分后的数字列表
        """
        value = []
        for i in range(n, 0, -1):
            if i != 1:
                if num - i > 0:
                    if contain_even_:
                        one = random.randrange(peer_chinese_chars_len, num - i, peer_chinese_chars_len)
                        contain_even_ = False
                    else:
                        one = random.randint(1, num - i)
                    num = num - one
                elif num - i == 0:
                    if contain_even_:
                        logging.exception('The minimum generated string does not support the inclusion of Chinese char')
                        raise Exception('The minimum generated string does not support the inclusion of Chinese char')
                    one = 1
                    num = num - one
                else:
                    logging.exception('the length of the generated string does not meet the kind requirement')
                    raise Exception('the length of the generated string does not meet the kind requirement')
            else:
                one = num
            value.append(one)
        return value

    contain_char = [type_ for type_, exist_ in all_type.items() if exist_]
    result = ''
    if contain_char:
        contain_even = False if peer_chinese_chars_len == 1 else True
        len_spilt = split_number(length, len(contain_char), contain_even)
        for char_, len_ in zip(contain_char, len_spilt):
            result = result + generate_random(len_, char_)

    return shuffle_string(result)


def pytest_report_save(file_path, days=60, report_file_start_with='Report') -> str:
    """ 按照最大保存时间清理过期报告文件，清理时只限Report_2023-04-03-17这种格式， 且返回当前时间的报告文件名

    :param file_path: Report 文件所在的上级目录，
    :param days: Report 文件要保存的时间
    :param report_file_start_with: 报告文件的开头
    :return: 返回当前报告的文件名称， ex：Report_2023-04-03-17
    """

    def report_expired(file_name: str) -> bool:
        expired = False
        try:
            if report_file_start_with in file_name and file_name != report_file_start_with:
                report_time = file_name.replace(report_file_start_with + '_', '')
                report_time = datetime.datetime.strptime(report_time, '%Y-%m-%d-%H')
                if (datetime.datetime.now() - report_time).days >= days:
                    expired = True
        except Exception:
            pass
        finally:
            return expired

    if os.path.isdir(file_path):
        for i in os.listdir(file_path):
            if report_expired(i):
                import shutil
                shutil.rmtree(os.path.join(file_path, i))
                logging.debug(f'{i} has expired days {days}, auto remove')

    return '_'.join([report_file_start_with, get_time_stamp(delta=+8, time_format='%Y-%m-%d-%H')])


def stop_thread(thread):
    """某些线程会在后台一直运行，当在外界满足一定条件时，是可以停掉的

    :param thread: 定义的线程
    :return:
    """
    import ctypes
    import inspect

    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            logging.exception('PyThreadState_SetAsyncExc failed')
            raise ValueError("invalid thread id or thread already stop")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            logging.exception('PyThreadState_SetAsyncExc failed')
            raise SystemError("PyThreadState_SetAsyncExc failed")
        else:
            logging.debug(f'threading {thread} stop success')

    try:
        _async_raise(thread.ident, SystemExit)
    except Exception as e:
        logging.exception(e)


def is_installed(name):
    """
    判断windows系统是否安装了某个软件
    :param name:
    :return: ResourceNotFoundError
    """
    import winreg
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
    all_installed = []
    for i in range(0, winreg.QueryInfoKey(key)[0]):
        skey_name = winreg.EnumKey(key, i)
        skey = winreg.OpenKey(key, skey_name)
        try:
            value = winreg.QueryValueEx(skey, 'DisplayName')[0]
            all_installed.append(value)
            if name in value:
                logging.debug(f'Found the software {name}')
                break
        except:
            pass
    else:
        logging.exception(f'all installed software is {all_installed}')
        raise ResourceNotFoundError(f'Not found the software {name}')


@loop_inspector('PC Ping', )
def pc_ping(host_or_ip: str or list or tuple = 'www.baidu.com', number: int = 4, src=None,
            lost_packets=False, assert_result=True, timeout=120, interval=10) -> bool:
    """ 验证在PC机上ping某个地址是否丢包， 仅判断丢包

    :param lost_packets:
    :param src: 验证的源IP地址 '192.168.2.100'
    :param host_or_ip: 验证的目的IP地址, 可使用元组或列表接收多个地址
    :param number: 包数量
    :param lost_packets: True|False 如果为True判断会丢包，如果为False判断不丢包
    :param assert_result: True|False 是否对 lost_packets 的结果做判断
    :param timeout: 超时时间
    :param interval: 间隔时间
    :return:
    """
    tag_result = True
    if host_or_ip:
        host_or_ip = [host_or_ip] if isinstance(host_or_ip, str) else host_or_ip
        for host in host_or_ip:
            command = f'ping {host} -n {number}' if src is None else f'ping -S {src} {host} -n {number}'
            logging.debug(command)
            if assert_result:
                result = os.popen(command).read()
                logging.debug(result)
                if lost_packets:  # 判断需要丢包
                    send = re.findall(r'已发送 = (.*?)，', result, re.S)[0]
                    accept = re.findall(r'已接收 = (.*?)，', result, re.S)[0]
                    if send == accept:
                        if '无法访问' not in result:
                            logging.info(f'PC {src} ping {host} does not loss packet')
                            tag_result = False
                else:  # 判断不丢包
                    if '丢失 = 0' not in result:
                        logging.info(f'PC {src} ping {host} loss packet')
                        tag_result = False
                    else:
                        if '无法访问' in result:
                            logging.info(f'PC {src} ping {host} loss packet')
                            tag_result = False
            else:
                os.popen(command)
            if not tag_result:
                break
    return tag_result


def speed_test(assert_download: tuple or None = None, assert_upload: tuple or None = None, unit: str = 'Mbps',
               max_retry_num: int = 3, timeout: int = 3):
    """进行网络测速, 并返回下载|上传速率
    :param assert_download: tuple or None,
        eg: (1, None): 校验 download_speed 是否大于 1
            (None, 2) 校验 download_speed 是否小于 2
            (1, 2) 校验 download_speed 是否大于 1 并且小于 2
    :param assert_upload: str or None, eg: (1, )|( , 2)|(1, 2)
    :param unit: str , 'bits'|'Kbps'|'Mbps'|'Gbps'
    默认为 None, 返回 (download_speed, upload_speed)
    :param max_retry_num: int , 最大测速次数，默认为 3
    :param timeout: int , 测速间隔，默认为 3s
    :return: float

    """

    def _get_sentence(speed: str, param: tuple):
        str_list = []
        if param[0] and param[1] is None:
            str_list = [speed, '>=', str(param[0])]
        elif param[1] and param[0] is None:
            str_list = [str(param[1]), '>=', speed]
        elif param[0] and param[1]:
            str_list = [str(param[1]), '>=', speed, '>=', str(param[0])]
        return eval(''.join(str_list))

    unit_dict = {'bits': 1, 'Kbps': 1000, 'Mbps': 1000 * 1000, 'Gbps': 1000 * 1000 * 1000}

    test = speedtest.Speedtest()
    servers = test.get_servers()
    logging.info(f"sponsor is {servers.get(min(servers))[0].get('sponsor')}")
    test.get_servers(servers=[servers.get(min(servers))[0].get('id')])
    test.get_best_server()
    logging.info("Testing in progress...")
    if isinstance(assert_download, tuple):
        for n in range(0, max_retry_num):
            download_speed = str(test.download() / (unit_dict.get(unit)))
            logging.info(f"download speed: {str(download_speed)} {unit}")
            if _get_sentence(download_speed, assert_download) is True:
                break
            else:
                time.sleep(timeout)
                continue
        else:
            raise Exception('download speed assert error')
    if isinstance(assert_upload, tuple):
        for n in range(0, max_retry_num):
            upload_speed = str(test.upload() / (unit_dict.get(unit)))
            logging.info(f"upload speed: {str(upload_speed)} {unit}")
            if _get_sentence(upload_speed, assert_upload) is True:
                break
            else:
                time.sleep(timeout)
                continue
        else:
            raise Exception('upload speed assert error')


class DotDict(dict):
    """使用点号深度获取字典key的值

    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            logging.exception(f'Not found the key {key}')
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


if __name__ == '__main__':
    from inhandtest.log import enable_log

    enable_log()
    kill_windows_port('10.5.24.112', 12313)
    # print(get_nearest_minute_time(30))
    # print(generate_string(20, chinese_chars=True, peer_chinese_chars_len=3))
    # speed_test(assert_download=(10, None), assert_upload=(1000, None))
