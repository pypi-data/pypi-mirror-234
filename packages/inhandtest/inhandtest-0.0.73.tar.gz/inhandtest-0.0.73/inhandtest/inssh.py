# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 13:26:52
# @Author  : Pane Li
# @File    : inssh.py
"""
inssh

"""
import functools
import os.path

import paramiko
from paramiko.ssh_exception import *
import logging


class InSsh:
    def __init__(self, host: str, username: str, password: str, port=22, sftp=True):
        """

        :param host: ssh 连接主机地址
        :param username: ssh 连接主机用户名
        :param password: ssh 连接主机密码
        :param port: 端口， 默认22
        :param sftp: 是否开启sftp 服务
        """
        self.__host = host
        self.__username = username
        self.__password = password
        self.__port = port
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.transport = paramiko.Transport((host, port))
        self.__connect()
        self.transport.connect(username=username, password=password)
        if sftp:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        else:
            self.sftp = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __connect(self):
        try:
            logging.info(f"ssh connect {self.__host} by {self.__username}:{self.__password}")
            self.ssh.connect(self.__host, self.__port, self.__username, self.__password, timeout=5)
        except AuthenticationException:
            logging.exception(f"ssh connect {self.__host} Username or Password error")
            raise AuthenticationException(f"ssh connect {self.__host} Username or Password error")
        except Exception:
            logging.exception(f"ssh connect {self.__host} connect error")
            raise ConnectionError(f"ssh connect {self.__host} connect error")

    def __auto_connect(function):
        """自动重连, 只能当装饰器使用， 不对外使用

        :param function:
        :return:
        """

        def auto_connect(self, *args, **kwargs):
            try:
                res = function(self, *args, **kwargs)
            except (ConnectionResetError, ConnectionAbortedError):
                logging.debug(f"ssh connect {self.__host} error, reconnect")
                self.__connect()
                res = function(self, *args, **kwargs)
            return res

        return auto_connect

    def enable_sftp(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.sftp is None:
                logging.exception("please set sftp=True when init InSsh")
                raise Exception("please set sftp=True when init InSsh")
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    @__auto_connect
    def exec_command(self, command: str) -> str:
        """执行命令并返回结果

        :param command: 执行命令, 多条时使用分号隔开
        :return: 返回所有命令执行后的结果
        """
        result = None
        if command:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            logging.info(f'exec command 【{command}】')
            result = stdout.read().decode("utf-8")
            logging.debug(f'command result 【{result}】')
        return result

    def ping(self, host, package=4, assert_lost_package=True, max_delay=100):
        """

        :param host: ip or host
        :param package:  默认ping4个包
        :param assert_lost_package: 判断是否存在丢包
        :param max_delay:  最大延迟，单位ms
        :return:
        """
        result = self.exec_command(f'ping -c {package} {host}')
        if not result:
            logging.exception('未建立openvpn连接')
            raise AssertionError('未建立openvpn连接')
        else:
            if len(result) >= 2:
                if assert_lost_package:
                    assert package == int(result[-2].split(' ')[3]), '存在丢包'
                if max_delay:
                    assert float(max_delay) >= float(result[-1].split('/')[-2]), '延迟过大'
            else:
                logging.exception('ping 包失败')
                raise AssertionError('ping 包失败')

    @enable_sftp
    def download_file(self, remote_file, local_file) -> None:
        """
        从服务器上下载文件
        :param remote_file: 远端文件路径
        :param local_file: 本地文件路径
        :return:
        """

        try:
            self.sftp.get(remote_file, local_file)
            logging.info(f'{remote_file} download success')
        except Exception as e:
            logging.error(f'{remote_file} download failed, {e}')

    @enable_sftp
    def upload_file(self, remote_file, local_file) -> None:
        """
        文件上传
        :param remote_file: 远端文件路径
        :param local_file: 本地文件路径
        :return:
        """
        try:
            self.sftp.put(local_file, remote_file)
            logging.info(f'{local_file} upload success')
        except Exception as e:
            logging.error(f'{remote_file} upload failed, {e}')

    @enable_sftp
    def clear_dir_or_remove_file(self, dir_name_or_file_path: str) -> None:
        """ 清除远端目录下所有文件，或单个文件

        :param dir_name_or_file_path: 目录或者文件路径
        :return:
        """

        def remove_file(file_path):
            try:
                self.sftp.remove(file_path)
                logging.info(f'{file_path} remove success！')
            except Exception as e:
                logging.error(f'{file_path} remove failed! {e}')

        if os.path.isdir(dir_name_or_file_path):
            files = self.sftp.listdir(dir_name_or_file_path)
            [remove_file(os.path.join(dir_name_or_file_path, i)) for i in files]
        else:
            remove_file(dir_name_or_file_path)

    @enable_sftp
    def get_file_content(self, file_path: str) -> str:
        """获取文件内容

        :param file_path:  文件路径  ex： 'D:\ecoer\sdf.sh'
        :return:
        """
        self.sftp.chdir(os.path.dirname(file_path))
        logging.debug(f'read {file_path} content success')
        return self.sftp.file(os.path.basename(file_path), 'r').read().decode(encoding='utf-8')

    @enable_sftp
    def write_file_content(self, file_path: str, content: str, mode='w') -> None:
        """像文件写入数据

        :param file_path: 文件全路径 ex: 'D:\ecoer\sdf.sh'
        :param content: 写入的文件内容，多行内容使用\n 连接
        :param mode: 'w' 替换文件内容写入， 'a' 追加内容
        :return:
        """
        self.sftp.chdir(os.path.dirname(file_path))
        with self.sftp.open(os.path.basename(file_path), mode) as f:
            f.write(content)
        logging.debug(f'write {file_path} content success')

    @enable_sftp
    def chmod(self, file_path: str, mode) -> None:
        """更改文件权限

        :param file_path:
        :param mode:
        :return:
        """
        self.sftp.chmod(file_path, mode)
        logging.debug(f'chmod {file_path} success')

    @enable_sftp
    def mkdir(self, path, mode=511) -> None:
        """创建文件夹

        :param path: 路径
        :param mode:  511 即 o777 权限，最大的
        :return:
        """
        self.sftp.mkdir(path, mode)
        logging.debug(f'mkdir {path} success')

    @enable_sftp
    def rmdir(self, path) -> None:
        """删除文件夹

        :param path: 路径
        :return:
        """
        self.sftp.rmdir(path)
        logging.debug(f'remove {path} success')

    @enable_sftp
    def rename(self, old_path, new_path) -> None:
        """文件重命名

        :param old_path:
        :param new_path:
        :return:
        """
        self.sftp.rename(old_path, new_path)
        logging.debug(f'{old_path} rename success')

    def close(self) -> None:
        """断开连接

        :return:
        """
        self.ssh.close()
        if self.sftp:
            self.sftp.close()
        self.transport.close()


if __name__ == '__main__':
    import sys

    pass
