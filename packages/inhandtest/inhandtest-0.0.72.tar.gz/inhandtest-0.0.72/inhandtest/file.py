# -*- coding: utf-8 -*-
# @Time    : 2023/2/23 16:48:50
# @Author  : Pane Li
# @File    : file.py
"""
file

"""
import os
import random
import string
import logging

import yaml


def del_file(file_path: str) -> None:
    """删除指定路径下的所有文件或单个文件

    :param file_path:
    :return:
    """
    if os.path.isdir(file_path):
        for i in os.listdir(file_path):
            c_path = os.path.join(file_path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
    elif os.path.isfile(file_path):
        os.remove(file_path)
    else:
        logging.debug(f"parameter file_path {file_path} is not exist")


def del_file_by_key(file_dir: str, name_contain: str) -> None:
    """根据文件名包含的关键字删除文件

    :param file_dir: 需要删除的文件目录
    :param name_contain: 文件名包含的关键字
    :return:
    """
    if os.path.isdir(file_dir):
        for i in os.listdir(file_dir):
            c_path = os.path.join(file_dir, i)
            if name_contain in i:
                os.remove(c_path)
                logging.info(f"delete {i} file")


def check_file(file_path) -> None:
    """校验文件是否存在

    :param file_path: 文件夹路径或者文件路径
    :return:  检查到文件不存在时就抛异常FileNotFoundError
    """
    if not os.path.isfile(file_path) or not os.path.exists(file_path):
        logging.exception(f"this file {file_path} not exist")
        raise FileNotFoundError(f"this file {file_path} not exist")
    else:
        logging.debug(f"check file {file_path} ok")


def check_dir(dir_path, create_dir=True) -> None:
    """

    :param dir_path:  问价夹路径
    :param create_dir:
    :return:
    """
    if os.path.exists(dir_path):
        logging.debug(f"check dir {dir_path} ok")
    else:
        if create_dir:
            os.makedirs(dir_path)
            logging.debug(f"create dir {dir_path} ok")
        else:
            logging.exception(f"this dir {dir_path} not exist")
            raise FileNotFoundError(f"this file {dir_path} not exist")


def generate_str_or_file(size: int or str = '48KB', file_path=None) -> str:
    """生成指定大小字符串或文件 1024KB=1MB  1024MB=1GB  1024GB=1TB

    :param size: int or str, int时单位为字节， str可带单位'KB'|'MB'|'GB', e.g: 49152|'48KB'...
    :param file_path: 文件全路径，ex: /$file_path/test.txt 将内容写道文件中
    :return: 返回文件内容, 即指定大小的字符串
    """
    str_ = ''

    if isinstance(size, str):
        if 'KB' in size:
            size = int(float(size.replace('KB', '')) * 1024)
        elif 'MB' in size:
            size = int(float(size.replace('MB', '')) * 1024 * 1024)
        elif 'GB' in size:
            size = int(float(size.replace('GB', '')) * 1024 * 1024 * 1024)
    elif isinstance(size, int):
        pass
    else:
        logging.exception(f'param {size} type {type(size)} error, only can be str or int!')
        raise Exception(f'param {size} type {type(size)} error, only can be str or int!')
    if size:  # 都已经转换为byte
        str_ = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
        if file_path:  # 生成文件
            with open(file_path, 'w') as file:
                file.write(str_)
            logging.debug(
                f"file {file_path} success create.Size is {os.path.getsize(file_path)}" + 'Byte')
    return str_


def file_hash(file_path_or_msg, hash_type='md5') -> str:
    """

    :param file_path_or_msg:  文件全路径 | 或者加密文件内容
    :param hash_type: 'md5'|'sha1'|'sha256'
    :return:
    """
    from hashlib import md5, sha1, sha256
    if hash_type.lower() == 'md5':
        obj = md5()
    elif hash_type.lower() == 'sha1':
        obj = sha1()
    elif hash_type.lower() == 'sha256':
        obj = sha256()
    else:
        logging.exception(f'Not support this hash_type {hash_type}')
        raise Exception(f'Not support this hash_type {hash_type}')
    if os.path.isfile(file_path_or_msg):
        with open(file_path_or_msg, 'rb') as f:
            obj.update(f.read())
    else:
        obj.update(file_path_or_msg.encode('utf-8'))
    return obj.hexdigest().upper()


def create_size_file(file_path, size='48KB'):
    """创建一个指定大小的文件，文件内容是乱码

    :param file_path:  文件路径包括文件名称
    :param size:   KB  MB  GB  TB生成指定大小文件
    :return:
    """
    size, unit = int(size[:-2]), size[-2:].lower()
    sm = {'b': 1, 'kb': 1024, 'mb': 1024 * 1024, 'gb': 1024 * 1024 * 1024, 'tb': 1024 * 1024 * 1024 * 1024}
    size = size * sm[unit]
    with open(file_path, 'wb') as f:
        f.write(os.urandom(size))
    logging.info("file create done")


def create_file(file_path, content: str, mode='w', encoding='utf-8'):
    """创建一个文件，将内容写入文件

    :param file_path:  文件路径包括文件名称
    :param content: 文件内容
    :param mode:  w | a  w:覆盖写入  a:追加写入
    :param encoding:  文件编码
    :return:
    """
    if not os.path.isfile(file_path):
        with open(file_path, 'w'):
            pass
    with open(file_path, mode, encoding=encoding) as f:
        f.write(content)
        logging.info(f"{file_path} file create and write done")


def file_to_csv(content: dict, file_path, header=False, mode='w'):
    """ 将字典内容写入csv文件

    :param content: {'id': ['i1', 'i2'], 'key': ['k1', 'k2']}
    :param file_path: './test.csv'
    :param header: 是否写入表头
    :param mode, w|a  覆盖或者追加内容
    :return:
    """
    import pandas
    df = pandas.DataFrame(content)
    df.to_csv(file_path, index=False, header=header, mode=mode)
    logging.info('file to csv success')


def file_content_read(file_path):
    """
    读取文件内容，返回列表
    :param file_path: 文件路径
    :return: 返回的文件内容，list
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        str_file_content = f.read()
    return str_file_content.split('\n')


def read_yaml_file(file_path) -> dict or list or None:
    if os.path.isfile(file_path):
        fr = open(file_path, 'r', encoding='utf-8')
        yaml_info = yaml.safe_load(fr)
        fr.close()
        return yaml_info
    else:
        return None


def create_yaml_file(content: dict or list, file_path, mode='w+'):
    if content:
        with open(file_path, mode, encoding='utf-8') as f:
            f.write(yaml.dump(content, allow_unicode=True))


if __name__ == '__main__':
    create_yaml_file({'a': 1, 'b': '中過人'}, './test.yaml')
    print(read_yaml_file('./test.yaml'))
