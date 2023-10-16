# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 10:10:43
# @Author  : Pane Li
# @File    : mail.py
"""
mail

"""
import datetime
import subprocess
import re
import typing

import emails
import os
import json
import imaplib
import email
from email.header import decode_header
from lxml import etree
from inhandtest.tools import kill_windows_port, loop_inspector
import logging


def pytest_send_report_mail(mail_to: str or list, mail_from: tuple or list, render: dict):
    """使用已配置好的邮件模板，发送邮件内容, 且使用node.js anywhere启动一个本地服务，用于分享报告,

    :param mail_to:  发送给谁
    :param mail_from: 元组($email, $password)
    :param render: 字典类型，需要将报告的内容传入 key值如下：
                             model：必填 测试设备型号， 如VG710
                             fun: 必填 测试功能
                             version: 必填 测试的版本, 如 VG7-V209bfd4(test)-2023-03-31-14-52-02.bin
                             host: 必填 测试主机， 10.5.24.107
                             port： 必填 分享报告端口， 63330
                             allure_results_path: 必填 报告中的/allure-results 路径

    :return:
    """
    port = render.get('port') if render.get('port') else 63330
    # 杀掉端口, 防止端口占用
    kill_windows_port(render.get('host'), [port, port + 1])  # port+1 是https端口
    # 启动本地服务，分享报告
    p = subprocess.Popen(f'npx anywhere -h {render.get("host")} -p {port}', cwd=render.get('allure_results_path'),
                         shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
    while True:
        output = p.stdout.readline()
        logging.debug(output)
        if len(re.findall(r'Running at (.*)/', output)) < 1:  # 无论是否启动成功，都会退出循环
            break
    # 读取报告中的summary.json文件，获取测试结果
    summary = json.load(
        open(os.path.join(render.get('allure_results_path'), 'widgets', 'summary.json'), 'r', encoding='utf-8'))
    html_file_path = os.path.join(os.path.dirname(__file__), 'pytest_email.html')
    from emails.template import JinjaTemplate as Te

    message = emails.html(html=Te(open(html_file_path, encoding='utf-8').read()),
                          subject=f'{render.get("model")}测试已完成',
                          mail_from=('映翰通网络测试', mail_from[0]))
    render.update(summary.get('statistic'))
    start = datetime.datetime.fromtimestamp(summary.get('time').get("start") / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
    stop = datetime.datetime.fromtimestamp(summary.get('time').get("stop") / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
    render.update({'start': start, 'stop': stop})
    render.update({'report_url': f'http://{render.get("host")}:{port}'})
    # 发送邮件
    if mail_to:
        r = message.send(mail_to, smtp={'host': 'smtp.exmail.qq.com', 'port': 465, 'user': mail_from[0], 'ssl': True,
                                        'password': mail_from[1]},
                         render=render)
        assert r.status_code == 250, 'send email failed'
        logging.info(f'send {mail_to} result success!')


def start_test_notice(mail_to: str or list, mail_from: tuple or list, render: dict):
    """使用已配置好的邮件模板，发送邮件内容, 且使用node.js anywhere启动一个本地服务，用于分享报告,

    :param mail_to:  发送给谁
    :param mail_from: 元组($email, $password)
    :param render: 字典类型，需要将报告的内容传入 key值如下：
                             model：必填 测试设备型号， 如VG710
                             version: 必填 测试的版本, 如 VG7-V209bfd4(test)-2023-03-31-14-52-02.bin
                             host: 必填 测试主机， 10.5.24.107
                             port： 必填 分享报告端口， 63330

    :return:
    """
    port = render.get('port') if render.get('port') else 63330
    # 杀掉端口, 防止端口占用
    html_file_path = os.path.join(os.path.dirname(__file__), 'notice_email.html')
    kill_windows_port(render.get('host'), [port, port + 1])  # port+1 是https端口
    # 启动本地服务，分享报告
    p = subprocess.Popen(f'npx anywhere -s -h {render.get("host")} -p {port}', cwd=render.get('allure_results_path'),
                         shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk')
    while True:
        output = p.stdout.readline()
        logging.debug(output)
        if len(re.findall(r'Running at (.*)/', output)) < 1:  # 无论是否启动成功，都会退出循环
            break
    from emails.template import JinjaTemplate as Te

    message = emails.html(html=Te(open(html_file_path, encoding='utf-8').read()),
                          subject=f'{render.get("model")}测试已开始',
                          mail_from=('映翰通网络测试', mail_from[0]))
    render.update({'report_url': f'http://{render.get("host")}:{port}'})
    # 发送邮件
    if mail_to:
        r = message.send(mail_to, smtp={'host': 'smtp.exmail.qq.com', 'port': 465, 'user': mail_from[0], 'ssl': True,
                                        'password': mail_from[1]},
                         render=render)
        assert r.status_code == 250, 'send email failed'
        logging.info(f'send {mail_to} result success!')


@loop_inspector('receive last email', 120, 5)
def receive_last_mail(receiver: tuple, mail_from: tuple, subject: str, **kwargs):
    """收取符合条件的邮件做校验，如果匹配到多个邮件，只校验最近的一封邮件
       当邮箱中邮件较多时，会耗时很长，所以建议匹配未读的邮件进行分析，分析完后，将邮件标记为已读

    :param receiver: 接收者('test@inhand.com.cn', '1111124') email, password
    :param mail_from: 发送者('映翰通网络', 'iot_console@inhand.com.cn') name, email
    :param subject: 邮件主题， 如：'VG710自动化测试'
    :param kwargs:
                  before_date: 匹配发送日期早于指定日期的邮件，格式：'2021-03-12 10:10:43' 本地时间
                  after_date: 匹配发送日期晚于或等于指定日期的邮件，格式：'2021-04-12 10:10:43'  本地时间
                  unseen: True| False 匹配未读邮件
                  seen_flag: True| False 对匹配到的所有邮件设置已读标记
                  assert_body: str or list 对匹配到的邮件内容做校验，整个邮件的内容是text形式, 判断邮件内容是否包含body中的内容, 且html_body和body只能有一个
                  assert_html_attr: dict or list, {'xpath': '', 'attr': 'src', 'value':''}对匹配到的邮件内容做校验，整个邮件的内容是html形式，
                                       xpath: str,  attr: text|src|href|value|id|class|name   value: str
                  get_html_attr: dict {'xpath': $xpath, 'attr': $attr}对匹配到的邮件内容做校验，整个邮件的内容是html形式，example: ('//td[@align="center"]/a', 'href')
                                   xpath: str,
                                   attr： str只能匹配一个属性  需要获取文本时 就传text  text|src|href|value|id|class|name
                                   return str
                  timeout: 超时时间，单位秒
                  interval: 每隔多久检查一次，单位秒
    :return:
    """

    def decode_str(s):
        """解码邮件标题"""
        values = ''
        for content in decode_header(s):
            try:
                if content[1]:
                    try:
                        values = values + content[0].decode('utf-8')  # 大部分邮件标题都是utf-8编码
                    except UnicodeDecodeError:
                        values = values + content[0].decode('gbk')  # 少部分邮件标题是gbk编码
                else:
                    values = values + str(content[0])  # 如果邮件标题没有编码信息，直接转成str
            except IndexError:
                values = values + str(content[0])
        return values

    # 连接到 IMAP 服务器
    imap_server = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
    imap_server.login(receiver[0], receiver[1])
    logging.info(f'login in email {receiver[0]}')
    imap_server.select('INBOX')
    type_ = 'UNSEEN' if kwargs.get('unseen') else 'ALL'
    # 搜索邮件
    status, data = imap_server.search(None, type_)
    result = False
    # 循环处理每个邮件
    if status == 'OK':
        all_email = data[0].split()
        all_email.reverse()  # 从最新的邮件开始处理
        for num in all_email:
            logging.info(f'查询第{all_email.index(num) + 1}封邮件')
            # 获取邮件内容
            if kwargs.get('seen_flag'):
                imap_server.store(num, '+FLAGS', '\\Seen')
            status_, data = imap_server.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # 解析邮件头
            receiver_time = str(decode_header(email_message['Date'])[0][0])
            receiver_time = datetime.datetime.strptime(receiver_time,
                                                       f'%a, %d %b %Y %H:%M:%S {receiver_time.split(" ", 5)[-1]}')
            if kwargs.get('before_date'):
                if receiver_time <= datetime.datetime.strptime(kwargs.get('before_date'), '%Y-%m-%d %H:%M:%S'):
                    break  # 邮件是按照时间倒序排列的，如果匹配到的邮件时间早于指定时间，就不用再匹配了
            if kwargs.get('after_date'):
                if receiver_time >= datetime.datetime.strptime(kwargs.get('after_date'), '%Y-%m-%d %H:%M:%S'):
                    continue  # 不符合条件的邮件，直接跳过
            subject_ = decode_str(email_message['Subject'])
            sender_from = decode_str(email_message['From'])
            if not ((subject in subject_) and (mail_from[0] in sender_from and mail_from[1] in sender_from)):
                continue
            else:
                logging.debug(f'get email success! subject: {subject_}, sender: {sender_from}')
            # 解析邮件正文
            if not kwargs.get('assert_body') and not kwargs.get('assert_html_attr') and not kwargs.get('get_html_attr'):
                result = True
                break
            else:
                body = html_body = None
                if email_message.is_multipart():
                    for part in email_message.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == 'text/plain' and 'attachment' not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode('utf-8')
                            except UnicodeDecodeError:
                                body = part.get_payload(decode=True).decode('gbk')
                        elif content_type == 'text/html' and 'attachment' not in content_disposition:
                            html_body = part.get_payload(decode=True).decode('utf-8')
                else:
                    try:
                        body = email_message.get_payload(decode=True).decode('utf-8')
                    except UnicodeDecodeError:
                        body = email_message.get_payload(decode=True).decode('gbk')
                if kwargs.get('assert_body'):
                    if not body:
                        break
                    else:
                        expect_body = kwargs.get('assert_body') if isinstance(kwargs.get('assert_body'), list) else [
                            kwargs.get('assert_body')]
                        for expect_ in expect_body:
                            if isinstance(expect_, str):
                                if expect_ not in body:
                                    logging.warning(f'assert email body failed!')
                                    break
                            elif isinstance(expect_, typing.Pattern):
                                if not expect_.search(body):
                                    logging.warning(f'assert email body failed!')
                                    break
                        else:
                            result = True
                            logging.debug(f'assert email body success!')
                        if result:
                            break
                if kwargs.get('assert_html_attr'):
                    if not html_body:
                        break
                    else:
                        html_body = etree.HTML(html_body)
                        assert_html = [kwargs.get('assert_html_attr')] if isinstance(kwargs.get('assert_html_attr'), dict) else kwargs.get('assert_html_attr')
                        for html_ in assert_html:
                            if html_.get('attr') is None or html_.get('attr') == 'text':
                                text = html_body.xpath(html_.get('xpath'))[0].text
                            else:
                                text = html_body.xpath(html_.get('xpath'))[0].get(html_.get('attr'))
                            try:
                                if '${value}' in html_.get('value'):
                                    expression = html_.get('value').replace('${value}', text).replace('\n', ' ')
                                else:
                                    ex_ = html_.get('value').replace("'", "\'")
                                    value = text.replace("'", "\'")
                                    expression = f'"""{ex_}""" == """{value}"""'  # 默认使用等于判断
                                if eval(expression):
                                    logging.info(f'Check {html_.get("xpath")} , {expression} is success')
                                else:
                                    logging.info(f'Check {html_.get("xpath")} , {expression} is failed')
                                    return False
                            except TypeError:
                                logging.error(f'get {html_.get("xpath")} value failed')
                                return False
                        else:
                            result = True
                        break
                if kwargs.get('get_html_attr'):
                    if not html_body:
                        break
                    else:
                        html_body = etree.HTML(html_body)
                        if isinstance(kwargs.get('get_html_attr'), dict):
                            try:
                                if kwargs.get('get_html_attr').get('attr') == 'text':
                                    return html_body.xpath(kwargs.get('get_html_attr').get('xpath'))[0].text
                                else:
                                    return html_body.xpath(kwargs.get('get_html_attr').get('xpath'))[0].get(
                                        kwargs.get('get_html_attr').get('attr'))
                            except IndexError:
                                logging.warning(f'not found html_attribute failed!')
                                pass
        else:
            logging.debug(f'not found {subject} email')
    else:
        logging.error(f'get email failed: {status}')
    # 关闭 IMAP 连接
    imap_server.close()
    imap_server.logout()
    return result


# 邮箱删除收件箱
def delete_all_mail(receiver: tuple):
    """邮箱删除收件箱

    :param receiver: 接收者('test@inhand.com.cn', '1111124') email, password
    :return:
    """
    imap_server = imaplib.IMAP4_SSL('imap.exmail.qq.com', 993)
    imap_server.login(receiver[0], receiver[1])
    logging.debug(f'login in email {receiver[0]}')
    # 选择收件箱
    imap_server.select('inbox')
    # 检索所有邮件的ID
    status, data = imap_server.search(None, 'ALL')
    if status == 'OK':
        # 将每个邮件标记为删除

        for num in data[0].split():
            imap_server.store(num, '+FLAGS', '\\Deleted')
        # 执行删除操作
        imap_server.expunge()

    # 关闭连接
    logging.info('delete all emails')
    imap_server.close()
    imap_server.logout()


if __name__ == '__main__':
    from inhandtest.log import enable_log
    enable_log(console_level='debug')
    import re
    # 设置日志
    a = receive_last_mail(receiver=('test@inhand.com.cn', 'ABc124'),
                          before_date='2023-09-06 10:00:00',
                          after_date='2023-09-06 11:00:00',
                          mail_from=('', 'test@inhand.com.cn'), subject='VG710 alarm!!!',
                          assert_body=['state  : raise', 'level  : WARN', 'content: Interface dot11radio 2, changed state to down'])

