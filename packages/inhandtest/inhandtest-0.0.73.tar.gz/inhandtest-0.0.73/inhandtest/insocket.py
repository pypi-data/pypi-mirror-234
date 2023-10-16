# -*- coding: utf-8 -*-
# @Time    : 2023/4/4 17:15:10
# @Author  : Pane Li
# @File    : insocket.py
"""
insocket

"""

import threading
import time
import socket
import logging


def tcp_server_data(host, port, recv_content: dict = None, connect_time=10,
                    send_msg_to_server: str or list = None, function=None, accept_timeout=5, **kwargs):
    """ 开启tcp_server, 并且接收数据，对数据做验证, 该连接为阻塞式，所以要确保客户端能正常连接过来，还要确保防火墙是关闭的
        该连接使用with，所以不管是客户端还是服务端，还是在异常状态下都会正常关闭

    :param host:  server地址 ex: 10.5.24.224
    :param port:  server端口 ex: 3001
    :param recv_content: {('10.5.24.224', 3002): "hello world"} 判断客户端('10.5.24.224', 3002) 在接收到的内容里面是否包含"hello world",  value可以是list，判断多个内容
                         {'content': "hello world"}, 判断连接过来的客户端在接收到的内容里面是否包含"hello world"
    :param connect_time:  服务器和客户端建立连接后，需要连接的时间
    :param send_msg_to_server: 当客户端连接成功后，已连接客户端向服务端发送的内容
    :param function: tcp_server 连接上后做的操作
    :param accept_timeout: 接收数据的或连接的超时时间
    :param kwargs:  function接入的参数
    :return: AssertionError or None
    """
    all_datas = {}
    socket.setdefaulttimeout(accept_timeout)

    def client_send_msg_to_server(conn, addr, msg: str or list):
        if msg is not None:
            msg = [msg] if isinstance(msg, str) else [msg_ for msg_ in msg]
            for msg_ in msg:
                conn.send(msg_.encode('utf-8'))
                logging.debug(f'tcp client {addr} send msg {msg_} to server {host}: {port}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # 使用with， 不用担心没有关闭server
        s.bind((host, port))  # 绑定服务器IP地址和端口号
        s.listen()  # 等待客户端连接
        try:
            for i_ in range(0, 4):  # 有些端口错误的客户端会连接上来，导致收到的消息始终为空，需要过滤掉
                client = True
                logging.debug(f'tcp server {host}:{port} start wait client connect')
                __conn, __addr = s.accept()
                if function is not None:
                    threading.Thread(target=function, kwargs=kwargs).start()
                with __conn:
                    logging.info(f'tcp server {host}:{port} connect from client {__addr}')
                    datas = b''
                    now_time = int(time.time())
                    send_msg_status = False
                    while int(time.time()) <= now_time + connect_time:
                        # 接收客户端数据
                        recv_data = __conn.recv(1024)
                        if not recv_data:
                            client = False
                            __conn.close()
                            logging.debug(f'client {__addr} is a error client')
                            break
                        if not send_msg_status:
                            threading.Thread(target=client_send_msg_to_server,
                                             args=(__conn, __addr, send_msg_to_server)).start()
                            send_msg_status = True
                        logging.debug(f'tcp server {host}:{port} recv client {__addr} data {recv_data}')
                        datas = datas + recv_data
                        all_datas.update({__addr: datas})
                    else:
                        __conn.close()
                if client:
                    break
        except socket.timeout:
            logging.error(f'tcp server {host}:{port} connect timeout or reva data timeout')
    # 数据校验
    if recv_content is not None:
        if all_datas:
            for k, v in recv_content.items():
                if k == 'content':
                    datas = b''.join([v_ for v_ in all_datas.values()])
                    contents = [v.encode('utf-8')] if isinstance(v, str) else [c_.encode('utf-8') for c_ in v]
                    # 校验数据内容
                    if list(filter(lambda x: x not in datas, contents)):
                        logging.exception(f'tcp server {host}:{port} all clients not recv  content {v}')
                        raise AssertionError(f'tcp server {host}:{port} all clients not recv  content {v}')
                    else:
                        logging.info(f'tcp server {host}:{port} all clients recv content {v} success')
                else:
                    datas = all_datas.get(k)
                    if datas is not None:
                        contents = [v.encode('utf-8')] if isinstance(v, str) else [c_.encode('utf-8') for c_ in v]
                        # 校验数据内容
                        if list(filter(lambda x: x not in datas, contents)):
                            logging.exception(f'tcp server {host}:{port} client {k} not recv content {v}')
                            raise AssertionError(f'tcp server {host}:{port} client {k} not recv content {v}')
                        else:
                            logging.info(f'tcp server {host}:{port} client {k} recv content {v} success')
                    else:
                        logging.exception(f'tcp server {host}:{port} client {k} not connected')
                        raise AssertionError(f'tcp server {host}:{port} client {k} not connected')
        else:
            logging.exception(f'tcp server {host}:{port} client not connected')
            raise AssertionError(f'tcp server {host}:{port} client not connected')


def tcp_client_data(server: tuple, client: tuple = None, recv_content: str or list = None, connect_time=10,
                    send_msg_to_server: str or list = None, function=None, socket_timeout=5, **kwargs):
    """ 开启tcp_client, 并且接收数据，对数据做验证
        该连接使用with，所以不管是客户端还是服务端，还是在异常状态下都会正常关闭

    :param server: ($host, $port), 客户端需要连接的服务器地址和端口，使用元组，必填('192.168.2.1', 502)
    :param client:  ($host, $port) 绑定指定地址和端口，如果为None ，本机直接开启一个， 跟server参数一样
    :param recv_content: 判断客户端 在接收到的内容里面包含recv_content 也可以不做校验
    :param connect_time:  服务器和客户端建立连接后，需要连接的时间
    :param send_msg_to_server: 当客户端连接成功后，客户端向服务端发送的内容
    :param function: 当客户端 连接上后做的操作
    :param socket_timeout: 接收数据的或连接的超时时间
    :param kwargs:  function接入的参数
    :return: AssertionError or None
    """
    socket.setdefaulttimeout(socket_timeout)
    datas = b''

    def client_send_msg_to_server(client_, msg: str or list):
        if msg is not None:
            msg = [msg] if isinstance(msg, str) else [msg_ for msg_ in msg]
            for msg_ in msg:
                client_.send(msg_.encode("utf-8"))
                logging.debug(f'tcp client send msg {msg_} to server {server}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # 使用with， 不用担心没有关闭server
        if client:
            s.bind(client)  # 绑定客户端IP地址和端口号
        try:
            s.connect(server)  # 客户端连接服务端
            threading.Thread(target=client_send_msg_to_server, args=(s, send_msg_to_server)).start()
            threading.Thread(target=function, kwargs=kwargs).start()
            now_time = int(time.time())
            while int(time.time()) <= now_time + connect_time:
                # 接收客户端数据
                recv_data = s.recv(1024)
                logging.info(f'tcp client recv data from server {server}: {recv_data}')
                datas = datas + recv_data
                time.sleep(0.5)
        except socket.timeout:
            logging.warning(f'tcp client {client} connect timeout or reva data timeout')

    if recv_content is not None:
        if datas:
            contents = [recv_content.encode('utf-8')] if isinstance(recv_content, str) else [c_.encode('utf-8') for
                                                                                             c_ in recv_content]
            # 校验数据内容
            if list(filter(lambda x: x not in datas, contents)):
                logging.exception(f'tcp client {client} not recv content {recv_content}')
                raise AssertionError(f'tcp client {client} not recv content {recv_content}')
            else:
                logging.info(f'tcp client {client} recv content {recv_content} success')
        else:
            logging.exception(f'tcp client {client} not connected')
            raise AssertionError(f'tcp client {client} not connected')


def udp_server_data(host, port, recv_content: str or list = None, connect_time=10, send_msg_to_client: dict = None,
                    function=None, **kwargs):
    """ 开启udp_server, 并且接收数据，对数据做验证, udp 校验数据时未区分客户端，所以保证接入时只有一个客户端
        该连接使用with，所以不管是客户端还是服务端，还是在异常状态下都会正常关闭

    :param host:  server地址
    :param port:  server端口
    :param recv_content: 判断recv_content 在接收到的内容里面 也可以不做校验
    :param connect_time:  服务器和客户端建立连接后，需要连接的时间
    :param send_msg_to_client: 开启udp server后， 向客户端发送的内容{($host, $port): $msg}
                               总体内容为字典， key值为元组类型， 总共长度为2位，第一位是客户端的地址， 第二位是端口
                               字典的value为需要给对应客户端发送的内容，可以是str 或list，
                               如需要给客户端192.168.3.2:6541 发送两条内容 'hello', 'word', 可以这样写
                               {('192.168.3.2', 6541): ['hello', 'word']}
                               端口可以为None, 但是地址必须要有， 也就是说，如果需要给客户端
                               确保对端服务和端口正常开启，不然要出问题
    :param function: 当客户端 连接上后做的操作
    :return: AssertionError or None
    """
    own_port_client = None
    not_port_client = None
    if send_msg_to_client is not None:
        own_port_client = {key: value for key, value in send_msg_to_client.items() if key[1] is not None}
        not_port_client = {key[0]: value for key, value in send_msg_to_client.items() if key[1] is None}

    def server_send_msg_to_client(server, msg: dict):
        if msg:
            for key, value in msg.items():
                msg = [value] if isinstance(value, str) else value
                for msg_ in msg:
                    server.sendto(msg_.encode('utf-8'), key)
                    logging.info(f'udp server {host}: {port} send msg {msg_} to client {key}')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # 使用with， 不用担心没有关闭server
        s.bind((host, port))  # 绑定服务器IP地址和端口号
        logging.debug(f'udp server {host}:{port} enable')
        send_msg_thread = threading.Thread(target=server_send_msg_to_client, args=(s, own_port_client))
        send_msg_thread.start()
        if function is not None:
            threading.Thread(target=function, kwargs=kwargs).start()
        datas = b''
        now_time = int(time.time())
        if not_port_client or recv_content:  # 始终要去接收客户端
            send_client = {}
            while int(time.time()) <= now_time + connect_time:
                # 接收客户端数据
                data, addr = s.recvfrom(5024)
                logging.debug(f'udp server {host}:{port} recv data from {addr}: {data}')
                if addr not in send_client.keys() and addr[0] in not_port_client.keys():
                    msg = [not_port_client.get(addr[0])] if isinstance(not_port_client.get(addr[0]),
                                                                       str) else not_port_client.get(addr[0])
                    for msg_ in msg:
                        s.sendto(msg_.encode('utf-8'), addr)
                        logging.info(f'udp server {host}: {port} send msg {msg_} to client {addr}')
                datas = datas + data
            if recv_content:
                contents = [recv_content.encode()] if isinstance(recv_content, str) else [c_.encode() for c_ in
                                                                                          recv_content]
                # 校验数据内容
                if list(filter(lambda x: x not in datas, contents)):
                    logging.exception(f'recv all data is {datas}')
                    raise AssertionError('recv data error')


def udp_client_data(server: tuple, client: tuple = None, recv_content: str or list = None, connect_time=10,
                    send_msg_to_server: str or list = None):
    """ 开启udp_client, 并且接收数据，对数据做验证
        该连接使用with，所以不管是客户端还是服务端，还是在异常状态下都会正常关闭

    :param server: ($host, $port), 客户端需要连接的服务器地址和端口，使用元组，必填('192.168.2.1', 502)
    :param client:  ($host, $port) 绑定指定地址和端口，如果为None ，本机直接开启一个， 跟server参数一样
    :param recv_content: 判断客户端 在接收到的内容里面包含recv_content 也可以不做校验
    :param connect_time:  服务器和客户端建立连接后，需要连接的时间
    :param send_msg_to_server: 当客户端连接成功后，客户端向服务端发送的内容
    :return: AssertionError or None
    """

    def client_send_msg_to_server(client_, msg: str or list):
        if msg is not None:
            msg = [msg] if isinstance(msg, str) else [msg_ for msg_ in msg]
            for msg_ in msg:
                client_.sendto(msg_.encode("utf-8"), server)
                logging.info(f'udp client send msg {msg_} to server {server}')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  # 使用with， 不用担心没有关闭server
        if client:
            s.bind(client)  # 绑定客户端IP地址和端口号
        threading.Thread(target=client_send_msg_to_server, args=(s, send_msg_to_server)).start()
        now_time = int(time.time())
        datas = b''
        while int(time.time()) <= now_time + connect_time:
            # 接收服务端数据
            data, server_addr = s.recvfrom(5024)
            logging.debug(f'upd client recv data from server {server_addr}: {data}')
            datas = datas + data
            if recv_content is not None:
                contents = [recv_content.encode('utf-8')] if isinstance(recv_content, str) else [c_.encode('utf-8') for
                                                                                                 c_ in recv_content]
                # 校验数据内容
                if not list(filter(lambda x: x not in datas, contents)):
                    break
        else:
            if recv_content is not None:
                logging.exception(f'recv all data is {datas}')
                raise AssertionError('recv data error')


if __name__ == '__main__':
    import sys

    pass
