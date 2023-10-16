# -*- coding: utf-8 -*-
# @Time    : 2023/3/21 10:13:10
# @Author  : Pane Li
# @File    : table_tr.py
"""
table_tr

"""
from typing import List
from inhandtest.tools import replace_str, loop_inspector
from playwright.sync_api import Locator, TimeoutError
import logging


class Table:

    def __init__(self, columns: list, table_locator: Locator, unique_columns: list, locale: dict = None, log_desc=None):
        """


        :param columns: [("acl_name", 'input'), ('action', 'select')] 说明列的表名以及 类型， 类型现在只支持三种('input'、'select'、'check')
                        eg:[("列名称变量","列字段对应类型"), ...]
                        在选择时只接收label, 不支持value选择， 因为查找时也使用的label，
                        在表格只有查找功能是时，只要列属性不定义为check 都可以
        :param table_locator: table_locator 定位
        :param unique_columns:  list, 确认唯一的列资源名称, eg: ["列名称变量1", "列名称变量2"...]， 当表只有查找功能时，该项为列的所有值。
        :param locale: dict, 国际化文件,
        """
        self.columns = columns  # 列名要与实际的列相对应，不能多也不能少 [("acl_name", 'input'), ('action', 'select')]
        self.table_locator = table_locator
        self.unique_columns = unique_columns  # 唯一的列资源名称
        self.tr = self.table_locator.locator('//tbody').locator('//tr')
        self.locale = locale
        self.log_desc = log_desc

    def __filter_td_index(self, contain_check=False, **kwargs):
        self.table_locator.wait_for(state='visible')
        expect_result = []
        for input_key, input_value in kwargs.items():
            if not contain_check:
                result = list(filter(lambda a: a[0] == input_key and a[1] != 'check' and a[0] in self.unique_columns,
                                     self.columns))  # 排除掉check
            else:
                result = list(filter(lambda a: a[0] == input_key and a[0] in self.unique_columns, self.columns))
            if len(result) == 1:
                expect_result.append((self.columns.index(result[0]), input_value, result[0][1]))  # 找出td是第几个，也及值, 以及类型
        return expect_result

    def __edit_add(self, **kwargs):
        for column in self.__filter_td_index(True, **kwargs):
            if column[1] is not None:
                if column[2] == 'input':
                    self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.clear()
                    self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.fill(str(column[1]))
                elif column[2] == 'select':
                    option = self.locale.get(
                        column[1]) if self.locale and self.locale.get(
                        column[1]) else str(column[1])
                    self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.select_option(option)
                elif column[2] == 'check':
                    if column[1] in ('check', 'Yes', '是', 'yes'):
                        self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.check()
                    else:
                        self.tr.locator('//td').locator(f'.fi{column[0] + 1}').first.uncheck()
                else:
                    logging.exception(f'not support this type {column[2]}')
                    raise Exception(f'not support this type {column[2]}')

    def exist(self, find_one=True, locale=None, **kwargs) -> int or None or List[int]:
        """ 传入的资源是否存在, 对于check 项是不计入重复选项的，因为勾选其实只是开启功能而已


        :param find_one: 是否只查询一个，当查询一个时返回的是int值，索引从0 开始， 当没查询到时返回的是None
                         当查询多个时，如果没有找到返回的是[], 如果找到了是列表包含了多个索引值
        :param locale: dict 国际化， 默认为类初始化的locale, 也可以单独传入
        :param kwargs: 支持传入表达式， 如 acl_name='${value} == '2''
        :return: int or list or None
        """
        search_tr = []
        one_tr = None
        expect_result = self.__filter_td_index(**kwargs)
        locale = self.locale if locale is None else locale
        if expect_result:
            for tr_nth in range(0, self.tr.count()):
                if self.tr.nth(tr_nth).locator('//td').count() == len(self.columns):  # 要求td里面的项跟最初定义的是一样的长度，不然就认为不是内容项
                    for result_ in expect_result:
                        text_n = self.tr.nth(tr_nth).locator('//td').nth(result_[0]).inner_text()  # 现在的值
                        if self.tr.nth(tr_nth).locator('//td').nth(result_[0]).locator('//select').count() == 1:
                            text_n = self.tr.nth(tr_nth).locator('//td').nth(result_[0]).locator(
                                '//select').evaluate('(element) => element.value')
                        elif self.tr.nth(tr_nth).locator('//td').nth(result_[0]).locator('//input').count() == 1:
                            text_n = self.tr.nth(tr_nth).locator('//td').nth(result_[0]).locator(
                                '//input').input_value()
                        text_e = replace_str(str(result_[1]), locale)  # 期望的值
                        if '${value}' in text_e:
                            text_e = text_e.replace('${value}', text_n)
                            try:
                                if not eval(text_e):
                                    break
                            except Exception as e:
                                logging.error(e)
                                break
                        else:
                            if text_n != text_e:
                                break
                    else:
                        search_tr.append(tr_nth)
                        if find_one:
                            one_tr = tr_nth
                            break
        if find_one:
            return one_tr
        else:
            return search_tr

    @loop_inspector('table tr')
    def assert_exist(self, timeout=90, interval=5, locale=None, **kwargs):
        """ 传入的资源是否存在, 对于check 项是不计入重复选项的，因为勾选其实只是开启功能而已

        :param locale: dict 国际化， 默认为类初始化的locale, 也可以单独传入
        :param timeout: 超时时间
        :param interval: 间隔时间
        :param kwargs: 支持传入表达式， 如 acl_name='${value} == '2''
               多增加参数：exist_number: 期望的数量， 默认为1, 可以是0 表示查找不到该项
        :return:
        """
        exist_number = kwargs.get('exist_number', 1)
        if exist_number == 0:
            if self.exist(find_one=True, locale=locale, **kwargs) is None:
                return True
            else:
                return False
        elif exist_number == 1:
            if self.exist(find_one=True, locale=locale, **kwargs) is not None:
                return True
            else:
                return False
        elif exist_number > 1:
            if len(self.exist(find_one=False, locale=locale, **kwargs)) == exist_number:
                return True
            else:
                return False
        else:
            return True

    def add(self, **kwargs) -> None:
        """ add 前是不查找是否存在的，直接加
        :param kwargs str, 待添加列 及对应值
        :return:
        """
        self.__edit_add(**kwargs)
        for i in range(0, self.tr.get_by_role('button').count()):
            action_attribute = self.tr.get_by_role('button').nth(i).get_attribute('onclick')
            if action_attribute in (
                    'TGO(this).onAdd()', 'TGO(this).footerAdd()', 'footerAdd()') and self.tr.get_by_role(
                'button').nth(i).is_enabled():
                self.tr.get_by_role('button').nth(i).click()
                if self.log_desc is not None:
                    logging.debug(f'add table {self.log_desc} success')
                break

    def delete(self, **kwargs) -> None:
        """
        :param kwargs str, 待删除列 及对应值
        :return:
        """
        find_tr = self.exist(find_one=True, **kwargs)
        if find_tr is not None:
            self.tr.nth(find_tr).locator('//td').nth(0).click()
            for i in range(0, self.tr.get_by_role('button').count()):
                action_attribute = self.tr.get_by_role('button').nth(i).get_attribute('onclick')
                if action_attribute in (
                        "TGO(this).onDelete()", "TGO(this).footerDel()", "footerDel()", 'delete_save(this)'):
                    if not self.tr.get_by_role('button').nth(i).is_disabled():
                        self.tr.get_by_role('button').nth(i).click()
                        if self.log_desc is not None:
                            logging.debug(f'delete table {self.log_desc} success')
                        break
                    else:
                        logging.error(f'the data in the row {find_tr} cannot be deleted')
        else:
            logging.warning(f'not found the resource {kwargs}')

    def delete_all(self) -> None:
        nth = 1
        while self.tr.count() >= nth + 2:
            self.tr.nth(nth).locator('//td').nth(0).click()
            try:
                for i in range(0, self.tr.get_by_role('button').count()):
                    action_attribute = self.tr.get_by_role('button').nth(i).get_attribute('onclick')
                    if action_attribute in (
                            "TGO(this).onDelete()", "TGO(this).footerDel()", 'footerDel()', 'delete_save(this)'):
                        if not self.tr.get_by_role('button').nth(i).is_disabled():
                            self.tr.get_by_role('button').nth(i).click()
                            break
                        else:
                            logging.exception(f'the data in the row {nth} cannot be deleted')
                            raise TimeoutError  # 第一行的数据不能删除，走到第二行去
                else:
                    break  # 所有行都走完了却没有删除按钮，也需要退出去
            except TimeoutError:
                nth = nth + 1
        logging.info('table resource all delete')

    def edit(self, old: dict, new: dict) -> None:
        """
        :param old ,dict, 待变更列数据
        :param new ,dict, 变更数据
        :return:
        """
        find_tr = self.exist(find_one=True, **old)
        if find_tr is not None:
            self.tr.nth(find_tr).locator('//td').nth(0).click()
            self.__edit_add(**new)
            for i in range(0, self.tr.get_by_role('button').count()):
                action_attribute = self.tr.get_by_role('button').nth(i).get_attribute('onclick')

                if action_attribute in ("TGO(this).onOK()", "TGO(this).footerOK()", 'footerOK()', 'footerModify()',
                                        "TGO(this).footerModify()",) and self.tr.get_by_role(
                    'button').nth(i).is_enabled():
                    self.tr.get_by_role('button').nth(i).click()
                    if self.log_desc is not None:
                        logging.info(f'edit table {self.log_desc} success')
                    break
        else:
            logging.warning(f'not found the resource {old}')

    def exists(self, value: list, find_one=True, locale=None) -> List[int] or List[list]:
        """查找多条记录

        :param value: list [{}, {}], 每组信息使用字典传输
        :param find_one: 是否只查询一个
        :param locale: 国际化，默认使用self.locale
        :return: 返回列表
        """
        result = []
        for value_ in value:
            result.append(self.exist(find_one, locale, **value_))
        return result

    def adds(self, value: list) -> None:
        """添加多列资源

        :param value: 列表， 套字典[{'acl_name': 'pl'}]
        :return:
        """
        if value:
            for value_ in value:
                self.add(**value_)

    def deletes(self, value: list) -> None:
        """删除多列资源

        :param value: 列表， 套字典[{'acl_name': 'pl'}]
        :return:
        """
        if value:
            for value_ in value:
                self.delete(**value_)

    def edits(self, value: list) -> None:
        """编辑多列资源

        :param value: 列表， 套字典[($old, $new)]  old 和new 都是字典
        :return:
        """
        if value:
            for value_ in value:
                self.edit(value_[0], value_[1])


class IgTable:
    __doc__ = """ 适配新产品架构，前端的表格，如IG
    """

    def __init__(self, columns: list, table_locator: Locator, locale: dict = None, log_desc=None, action_confirm=None,
                 pop_up_locator=None):
        """


        :param columns: [('name',{'locator': self.page.locator(''), 'type': 'fill'}),
                         ('model',{'locator': self.page.locator(''), 'type': 'radio', param: {'value': '1'}}),
                         ('save',{'locator': self.page.locator(''), 'type': 'button'}),]
                         说明列的表名以及类型， 必须定义"add"、"save" 按钮， 因为添加按钮和保存按钮的定位不能自动获取
                        eg:[("列名称变量","列字段对应类型"), ...]
                        在选择时只接收label, 不支持value选择， 因为查找时也使用的label，
                        在表格只有查找功能是时，只要列属性不定义为check 都可以
        :param table_locator: 添加按钮元素上面的div定位
        :param locale: dict, 国际化文件,
        :param log_desc: str, 日志描述
        :param action_confirm: Locator, 弹窗中的confirm 按钮定位 是否操作有确认弹窗， 如delete，
        :param pop_up_locator: Locator, 弹窗定位, 只有在操作表格操作时如果有弹窗需要给出该定位， 如edge import config
        """
        self.columns = columns  # 列名要与实际的列相对应，不能多也不能少
        self.table_locator = table_locator
        self.locale = locale
        self.log_desc = log_desc
        self.action_confirm = action_confirm
        self.pop_up_locator = pop_up_locator

    def exist(self, value: str, locale: dict) -> bool:
        """ 传入的资源是否存在, 对于check 项是不计入重复选项的，因为勾选其实只是开启功能而已

        :param value: str 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化 ex: 192.168.2.1255.255.255.0
        :param locale: dict 国际化， 默认为类初始化的locale, 也可以单独传入
        :return: True|False
        """
        locale = self.locale if locale is None else locale
        if value:
            value = replace_str(value, locale) if isinstance(value, str) else value
            exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
            if exist_tr.count() > 0:
                return True
        return False

    def add(self, agg_in, **kwargs, ) -> None:
        """ add 前是不查找是否存在的，直接加

        :param agg_in: function, 导致该方法不能单独使用
        :param kwargs str, 待添加列 及对应值
        :return:
        """
        if ('save' not in list(kwargs.keys())) and ('cancel' not in list(kwargs.keys())):
            kwargs['save'] = True
        try:
            add_button = list(filter(lambda x: x[0] == 'add', self.columns))[0][1].get('locator')
        except Exception:
            add_button = self.table_locator.locator('//button').first
        if kwargs.get('is_exists'):
            is_exists = kwargs.pop('is_exists')
            if not self.exist(is_exists, self.locale):
                add_button.click()
                agg_in(self.columns, kwargs)
                logging.debug(f'table resource {kwargs} add success')
            else:
                logging.debug(f'table resource {kwargs} exist')
        else:
            add_button.click()
            agg_in(self.columns, kwargs)
            logging.debug(f'table resource {kwargs} add success')

    def edit(self, agg_in, old_value, **kwargs) -> None:
        """ 只能编辑匹配到的第一条记录

        :param agg_in: function, 导致该方法不能单独使用
        :param old_value: str, 旧值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值
        :param kwargs str, 待添加列 及对应值
        :return:
        """
        old_value = replace_str(old_value, self.locale) if isinstance(old_value, str) else old_value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=old_value)
        if exist_tr.count() > 0:
            if exist_tr.first.locator('//i[@class="anticon anticon-form"]').count() == 1:
                exist_tr.first.locator('//i[@class="anticon anticon-form"]').click()
            else:
                exist_tr.first.locator('//i[@class="anticon anticon-edit"]').click()
            if ('save' not in list(kwargs.keys())) and ('cancel' not in list(kwargs.keys())):
                kwargs['save'] = True
            agg_in(self.columns, kwargs)
            logging.debug(f'table resource {kwargs} edit success')
        else:
            logging.debug(f'table resource {old_value} not exist')

    def delete(self, value: str) -> None:
        """
        :param value str, 待删除列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        exist_tr_number = exist_tr.count()
        for i in range(0, exist_tr_number):
            exist_tr.first.locator('//i[@class="anticon anticon-delete"]').click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
                self.table_locator.page.wait_for_timeout(3000)
            else:
                self.table_locator.page.wait_for_timeout(500)
        logging.debug(f'table resource {value} all delete')

    def associate_delete(self, value: str) -> None:
        """
        :param value str, 关联删除按钮，如VPN 中l2tp client表格中的删除按钮
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        while exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-close"]').click()
        logging.debug(f'table resource {value} all delete associate')

    def download(self, action, value: str, file_path: str, file_name: str = None):
        """
        :param action: function, 导致该方法不能单独使用
        :param value str,
        :param file_path: str, 下载文件存放路径
        :param file_name: str, 下载文件名
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            action(exist_tr.first.locator('//i[@class="anticon anticon-download"]').first, file_path,
                   file_name=file_name)
        logging.debug(f'table resource {value} download success')

    def upload(self, action, value, file_path):
        """
        :param action: function, 导致该方法不能单独使用
        :param value str, 待上传列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :param file_path: str, 上传文件全路径
        :return:
        """
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-upload"]').click()
            action(self.pop_up_locator.locator('.anticon.anticon-upload').nth(0), file_path)
            self.pop_up_locator.locator('.ant-btn.ant-btn-primary').nth(0).click()
        logging.debug(f'table resource {value}  click upload')

    def check(self, action, value, check_value):
        """
        :param action: function, 导致该方法不能单独使用
        :param value str, 待check 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :param check_value: str, 待check值
        :return:
        """
        tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr')
        for i in range(0, tr.count()):
            for x in range(0, tr.nth(i).locator('//td').count()):
                if tr.nth(i).locator('//td').nth(x).inner_text() == value:
                    return action(tr.nth(i).locator('//input[@type="checkbox"][@class="ant-checkbox-input"]').nth(0),
                                  check_value)
        else:
            exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
            if exist_tr.count() > 0:
                action(exist_tr.first.locator('//input[@type="checkbox"][@class="ant-checkbox-input"]').nth(0),
                       check_value)
        logging.debug(f'table resource {value}  {check_value}')

    def start(self, value: str) -> None:
        """
        :param value str, 待开始列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-play-circle"]').first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
        logging.debug(f'table resource {value} all start')

    def stop(self, value: str) -> None:
        """
        :param value str, 待停止列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-pause-circle"]').first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
        logging.debug(f'table resource {value} all stop')

    def restart(self, value: str) -> None:
        """
        :param value str, 待重启列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-undo"]').first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
        logging.debug(f'table resource {value} all restart')

    def clear_historical_data(self, value: str) -> None:
        """
        :param value str, 待重启列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon"]').first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
        logging.debug(f'table resource {value} all restart')

    def clear_log(self, value: str) -> None:
        """
        :param value str, 待开始列 及对应值 每列值可按顺序直接连接在一起传入，当然也可以传一列的值 自己国际化
        :return:
        """
        value = replace_str(value, self.locale) if isinstance(value, str) else value
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            exist_tr.first.locator('//i[@class="anticon anticon-delete"]').first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()  # 二次确认
        logging.debug(f'table resource {value} all clear log')

    def connect(self, value: str) -> None:
        """
        :param value str, WLAN 页面connect连接，每列值可按顺序直接连接在一起传入，当然也可以传一列的值
        :return:
        """
        exist_tr = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr', has_text=value)
        if exist_tr.count() > 0:
            if exist_tr.first.locator('//button[@class="ant-btn ant-btn-background-ghost"]').is_enabled():
                exist_tr.first.locator('//button[@class="ant-btn ant-btn-background-ghost"]').click()
                logging.info(f'table resource {value} connect success')
            else:
                logging.debug(f'table resource {value} already connected')

    def delete_all(self) -> None:
        tr_locators = self.table_locator.locator('//tbody[@class="ant-table-tbody"]/tr').locator(
            '//i[@class="anticon anticon-delete"]')
        exist_tr_number = tr_locators.count()
        for i in range(0, exist_tr_number):
            tr_locators.first.click()
            if isinstance(self.action_confirm, Locator):
                self.action_confirm.click()
                self.table_locator.page.wait_for_timeout(3000)
            else:
                self.table_locator.page.wait_for_timeout(500)
        logging.debug('table resource all delete')
