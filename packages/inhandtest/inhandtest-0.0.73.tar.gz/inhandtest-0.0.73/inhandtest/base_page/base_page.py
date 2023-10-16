# -*- coding: utf-8 -*-
# @Time    : 2023/3/8 17:54:32
# @Author  : Pane Li
# @File    : base_page.py
"""
base_page

"""
import os
import time
import allure
import logging
import base64
from inhandtest.base_page._contents_locators import ContentsLocators
from inhandtest.exception import ModelError
from inhandtest.base_page.page import Page_
from inhandtest.inrequest import ErDevice
from inhandtest.tools import replace_str
from playwright.sync_api import Page, Locator, TimeoutError, sync_playwright
from inhandtest.file import read_yaml_file

login_yaml = read_yaml_file(os.path.join(os.path.dirname(__file__), 'login_config.yaml'))


class BasePage(Page_):

    def __init__(self, host: str, username: str, password: str, protocol='https',
                 port=443, model='VG710', language='en', page: Page = None, **kwargs):
        """

        :param host:  设备主机地址
        :param username: 用户名
        :param password: 密码
        :param protocol: 协议
        :param port: 端口
        :param model: 'VG710'|'ER805'|'ER605'|'IR302'|'IG502'|'IG902'|'IR305'|'IR615'|'EAP600'
        :param page: 当page为None时，自动打开浏览器及页面，否则使用传入的page
        :param kwargs:
                      browser: 当没有传入page时，可以选择浏览器
                      locale: dict 国际化
                      bring_to_front: bool 是否将浏览器窗口置顶
                      viewport: {'width': 1366, 'height': 768}  浏览器窗口大小
                      web_login_timeout: int  登录超时时间 默认300， 单位秒 即5分钟， 监测到登录超时后，会自动重新登录
                      version: str  设备版本号
        """
        self.page = page
        self.host = host
        self.model = model.upper()
        self.protocol = protocol
        self.port = port
        self.username = username
        self.password = password
        self.language = language
        self.bring_to_front = kwargs.get('bring_to_front', False)
        self.__browser_type = kwargs.get('browser')
        self.__web_login_timeout = kwargs.get('web_login_timeout', 300)
        self.__logout_time = None
        self.viewport = kwargs.get('viewport', {'width': 1366, 'height': 768})
        self.__login_ = login_yaml.get(self.model)
        if self.__login_ is None:
            raise ModelError(f'not support this model {self.model} login')
        if self.page is None:
            self.__new_page()
        self.content_locator = ContentsLocators(self.page, language, self.model).tags_menu
        if self.model in ('ER805', 'ER605', 'EAP600', 'ODU2002'):
            self.api = ErDevice(username, password, host, protocol, port, model)
        self.locale = kwargs.get('locale').get(language) if kwargs.get('locale') else None
        super().__init__(self.page, self.host, self.model, self.locale)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def version(self):
        try:
            return self.api.basic.get('firmware')
        except Exception:
            raise Exception('Please use the api to initialize the version')

    def _get_locator(self, value: dict):
        """ 对于定义的locator做转换，需找出对应型号及版本的locator

        :param value:
        """
        if value and isinstance(value, dict):
            value = {key.upper(): value for key, value in value.items()}
            try:
                return value.get(list(filter(lambda x: self.model in x and self.version.upper() in x, value.keys()))[0])
            except Exception:
                if value.get(self.model):
                    return value.get(self.model)
                else:
                    if value.get('DEFAULT'):
                        return value.get('DEFAULT')
                    else:
                        return list(value.values())[0]
        elif value and isinstance(value, list):
            return [self._get_locator(value_) for value_ in value]
        else:
            return value

    def call_web_login_timeout(self, response):
        if response.status == 401:
            # 当页面的token过期时，可能会连续几个API返回401，这里只处理一次，避免重复登录
            if self.__logout_time is None or (int(time.time()) - self.__logout_time) > self.__web_login_timeout:
                logging.warning(f'login timeout, try to login again')
                self.__logout_time = int(time.time())
                self.login(self.username, self.password)

    def __new_page(self):
        def dialog_(dialog):
            logging.debug(f'dialog message is {dialog.message}, accepted')
            dialog.accept()

        self.__playwright = sync_playwright().start()
        if self.__browser_type == 'firefox':
            browser = self.__playwright.firefox
        elif self.__browser_type == 'webkit':
            browser = self.__playwright.webkit
        else:
            browser = self.__playwright.chromium
        self.__browser = browser.launch(headless=False)
        if self.__login_.get('type') != 'auth':
            http_credentials = {'username': self.username, 'password': self.password}
        else:
            http_credentials = None
        self.__context = self.__browser.new_context(ignore_https_errors=True, http_credentials=http_credentials,
                                                    viewport=self.viewport, permissions=['clipboard-read'])
        logging.info('Start your journey browser is chrome')
        self.page = self.__context.new_page()
        self.page.on("dialog", dialog_)

    @allure.step("用户登录")
    def login(self, username=None, password=None, status='success') -> None:
        """

        :param username:  如果不传使用默认的用户名
        :param password:  如果不传使用默认的密码
        :param status: 登录状态 'success'|'fail' 期望登录的状态是成功还是失败，失败了就会停留在登录页面，不做任何操作
        :return:
        """
        username = self.username if not username else username
        password = self.password if not password else password

        def goto_router():
            device = "{}://{}:{}".format(self.protocol, self.host, self.port)
            try:
                self.page.goto(device, timeout=120 * 1000)
            except Exception:
                logging.exception(f'Open {self.host} device address {device} timeout')
                raise
            if self.bring_to_front:
                self.page.bring_to_front()
            self.page.wait_for_timeout(500)
            logging.info(f'Open {self.host} device address {device}')

        def auth_login():
            if self.__login_.get('type') == 'auth':
                self.page.locator(self.__login_.get('username')).fill(username)
                logging.debug('Device %s fill username %s' % (self.host, username))
                self.page.locator(self.__login_.get('password')).fill(password)
                logging.debug('Device %s fill password %s' % (self.host, password))
                self.page.locator(self.__login_.get('submit')).click()
                logging.info("Device %s login" % self.host)
                if status == 'success':
                    self.page.locator(self.__login_.get('wait_locator')).wait_for(state='visible', timeout=10 * 1000)
                    self.page.wait_for_timeout(500)

        self.page.wait_for_load_state('domcontentloaded', timeout=15 * 1000)
        try:
            if self.page.url == 'about:blank':
                goto_router()
                auth_login()
            elif self.__login_.get('type') == 'auth' and self.page.locator(
                    self.__login_.get('username')).is_visible() and self.page.locator(
                self.__login_.get('wait_locator')).is_hidden():
                auth_login()
            elif self.page.locator(self.__login_.get('wait_locator')).is_visible():
                pass
            else:
                self.page.reload()
            self.page.locator(self.__login_.get('wait_locator')).wait_for(state='visible', timeout=10 * 1000)
        except TimeoutError:
            logging.error(f"Device {self.host} page is error")
            goto_router()
            auth_login()

    @allure.step('进入菜单')
    def access_menu(self, menu: str, wait_time=None) -> None:
        """进入菜单，多个菜单使用点号隔开，不限多少层级   menu_locator 存放在 base_locators 里面，
            定义menu = {'system': {'locator': '#menu_id', 'wait_locator': '#wait_locator_id'},
                               'status':{'locator': '#status_id', 'wait_locator': '#wait_locator_id'}}
            定义菜单时所有菜单的点号都需要省略，如2.4g 写成24g；空格写成下划线，如wi-fi 2.4g 写成wi-fi_24g
            中划线写成下划线，如wi-fi-2.4g 写成wi_fi_24g


        :param menu: 'system'| 'system.status' 菜单名称全部来自与设备的英文版本，点号需要省略不写， 其他不变，大小写均可以
                     菜单中原有的点号都需要忽略，如wi-fi 2.4g 需要传入wi-fi_24g 或 wi-fi 2.4g 或 wi-fi_2.4g
        :param wait_time: 当操作完菜单后是否需要等待时间 单位毫秒
        :return:
        """

        def in_current_menu(locators: dict) -> bool:
            _in_current_menu = False
            if locators.get('visible_locator'):
                _in_current_menu = True
                for visible_locator in locators.get('visible_locator'):
                    if not visible_locator.is_visible():
                        _in_current_menu = False
                        break
            if _in_current_menu:
                if locators.get('attributes'):
                    for locator, value in locators.get('attributes').items():
                        if locator.is_visible():
                            for attr, expect_value in value.items():
                                if expect_value not in locator.get_attribute(attr):
                                    _in_current_menu = False
                                    break
                            else:
                                _in_current_menu = True
                                continue
                            break
                        else:
                            _in_current_menu = False
                            break
            return _in_current_menu

        def access_one_menu(menu_one: str, locators: dict, level: int):  # 进入某一个菜单
            if not in_current_menu(locators):
                menus = locators.get('menu') if isinstance(locators.get('menu'), list) else [locators.get('menu')]
                for menu_1 in menus:
                    self.click(menu_1)
                logging.info(f'select {level} level menu {menu_one}')
                if locators.get('mouse_move'):
                    self.page.mouse.move(locators.get('mouse_move')[0], locators.get('mouse_move')[1])
                if locators.get('wait_locator'):
                    for wait_locator in locators.get('wait_locator'):
                        wait_locator.wait_for(state='visible')
                    self.page.wait_for_timeout(500)  # 多等500ms
                else:
                    self.page.wait_for_timeout(1000)

        def access(menus):  # 递归进入菜单
            new_menus = []
            click_menus = []
            menu_content = self.content_locator
            # 把菜单名、菜单的元素信息、以及菜单等级依次放入列表中
            for menu_s, level_ in zip(menus, range(1, len(menus) + 1)):
                menu_content = menu_content.get(menu_s)
                new_menus.append([menu_s, menu_content, level_])
            new_menus.reverse()  # 逆序查看是否在当前这个菜单的页面
            for menu_one, locators, level_ in new_menus:
                if not in_current_menu(locators):
                    # 找出需要点击的菜单
                    click_menus.append((menu_one, locators, level_))
                else:
                    break
            if click_menus:
                click_menus.reverse()  # 回归原来的顺序
                for menu_one, locators, level_ in click_menus:
                    access_one_menu(menu_one, locators, level_)
            else:
                logging.debug(f'already in {".".join(menu)} menu')

        def default_change(menu_old, locators: dict) -> str:
            menu_old_s = menu_old.split('.')
            for menu_old_ in menu_old_s:
                locators = locators.get(menu_old_)
            default = locators.get('default')
            menu_new = menu_old + '.' + default if default else menu_old
            return menu_new

        if menu:
            if self.bring_to_front:
                self.page.bring_to_front()
            self.login()
            try:
                menu = menu.replace(' ', '_').replace('-', '_').lower()
                menu = default_change(menu, self.content_locator).split('.')
                access(menu)
            except Exception:
                logging.exception(f'not support this menu {menu}')
                raise f'not support this menu {menu}'
            if wait_time:
                self.page.wait_for_timeout(wait_time)

    def agg_in(self, locators: list, action_dict: dict) -> None:
        """封装公共的整合输入操作
                :param locators:  列表 嵌套 长度为2的元组，元组的第一项为操作项名称， 第二项为对应的一个字典
                    [($param1, {"locator": $locator1, "type": $type1, "relation": [($param2, $value2)], "param": {$key1: $value1}}),
                    ($param2, {"locator": $locator2, "type": $type2, "relation": [($param3, $value3),……], "param": {$key2: $value2}}),
                    ($param3, {"locator": $locator2, "type": 'table_tr', "relation": [($param3, $value3),……], "param": {$key2: $value2},
                                "columns": list, 'unique_columns': list}),]
                    $param: 操作项的名称，如 'language'|'sim'|'status'
                    $locator: 操作项的元素定位， locator or [locator,locator,...]
                    $type: 操作项的类型 text|select|select_multi|select_more|button|check|upload_file|download_file|tip_messages|text_messages|title_messages|fill_date|
                                     multi_select|multi_check|multi_fill|table_tr|switch_button|radio_select|expand|monaco|value_mapping
                            select value值可以是label|Value
                            multi_select指一个参数有多个select, 对应操作项的多个locator及value用[]传入
                    "relation":[($param, $value)]: 操作项的关联项，若有多个则首个为最先操作的关联项，其中$param为关联项的名称，$value为关联项的预期值
                    "param":{$key, $value}: 参数转换，如大小写转换{"ab":"AB"} {"wan":"Wan"}等.
                    "always_do": True|False: 操作项是否必须操作, 哪怕是报异常也会做
                :param action_dict: 要做操作的参数名称与对应的值{$param1: $value1, $param2: $value2}
                :return:
                """
        relations = []

        def operation(param, param_locator, value):
            # param  传过来的参数名称
            # param_locator {'locator': self.page.locator('.ant-modal-content'), 'type': 'button', "always_do": True}  元素定位信息
            param_locator.update({'locator': self._get_locator(param_locator.get('locator'))})
            if param_locator.get('type') in ('text', 'fill'):
                value, force = value, False
                if isinstance(value, dict):
                    value, force = value.get('value'), value.get('force', False)
                self.fill(param_locator.get('locator'), value, param, force)
            elif param_locator.get('type') == 'monaco':
                self.monaco(param_locator.get('locator'), value, param)
            elif param_locator.get('type') in ('select', 'select_option'):
                self.select_option(param_locator.get('locator'), value, param, param_locator.get('param'))
            elif param_locator.get('type') == 'select_more':
                self.select_more(param_locator.get('locator'), value, param, param_locator.get('param'))
            elif param_locator.get('type') == 'select_multi':
                self.select_multi(param_locator.get('locator'), value, param, param_locator.get('param'))
            elif param_locator.get('type') == 'radio_select':
                self.radio_select(param_locator.get('locator'), value, param, param_locator.get('param'))
            elif param_locator.get('type') == 'radio':
                self.radio(param_locator.get('locator'), value, param, param_locator.get('param'))
            elif param_locator.get('type') == 'switch_button':
                self.switch_button(param_locator.get('locator'), value, param)
            elif param_locator.get('type') == 'expand':
                self.expand(param_locator.get('locator'), value)  # 此处获取到的locator 是一个str
            elif param_locator.get('type') in ('button', 'click'):
                if value:
                    dialog_message, tip_messages, wait_for_time, text_messages, tip_messages_timeout = None, None, None, None, 30
                    if isinstance(value, dict):
                        dialog_message = value.get('dialog_message')
                        tip_messages = value.get('tip_messages')
                        wait_for_time = value.get('wait_for_time')
                        text_messages = value.get('text_messages')
                        tip_messages_timeout = value.get('tip_messages_timeout', 30)
                    self.click(param_locator.get('locator'), param, dialog_message, tip_messages, text_messages,
                               wait_for_time, tip_messages_timeout)
            elif param_locator.get('type') == 'check':
                if value is not None:
                    value_, tip_messages = value, None
                    if isinstance(value, dict):
                        value_ = value.get('value')
                        tip_messages = value.get('tip_messages')
                    self.check(param_locator.get('locator'), value_, param, tip_messages)
            elif param_locator.get('type') == 'table_tr':
                if isinstance(value, list):  # value按照table_tr()的传参方式传参,
                    self.table_tr(param_locator.get('locator'), value, self.agg_in, param)
                else:
                    logging.error(f'value {value} should be a list, not {type(value)}')
            elif param_locator.get('type').startswith('multi_'):  # 多次连续选择或输入或勾选
                if len(param_locator.get('locator')) == len(value):
                    for locator_, value_ in dict(zip(param_locator.get('locator'), value)):
                        if 'select' in param_locator.get('type'):
                            self.select_option(locator_, value_, param, param_locator.get('param'))
                        elif param_locator.get('type').endswith('check'):
                            self.check(locator_, value_, param)
                        elif param_locator.get('type').endswith('fill'):
                            self.fill(locator_, value_, param)
                        else:
                            logging.error(f"not support this param type {param_locator.get('type')}")
                else:
                    logging.error('Wrong length or type of locator or value!')
            elif param_locator.get('type') == 'upload_file':
                file_path, dialog_message, tip_message = value, None, None
                if isinstance(value, dict):
                    file_path, dialog_message, tip_message = value.get('file_path'), value.get(
                        'dialog_message'), value.get('tip_messages')
                self.upload_file(param_locator.get('locator'), file_path, dialog_message, tip_message)
            elif param_locator.get('type') == 'download_file':
                file_path, file_name = value, None
                if isinstance(value, dict):
                    file_path, file_name = value.get('file_path'), value.get('file_name')
                self.download_file(param_locator.get('locator'), file_path, file_name)
            elif param_locator.get('type') in ('tip_messages', 'text_messages', 'title_messages'):
                messages, timeout = value, 10
                if isinstance(value, dict):
                    timeout, messages = value.get('timeout', 10), value.get('messages')
                if param_locator.get('type') == 'tip_messages':
                    self.tip_messages(messages, timeout)
                elif param_locator.get('type') == 'text_messages':
                    self.text_messages(messages, timeout)
                elif param_locator.get('type') == 'title_messages':
                    self.title_messages(messages, timeout)
            elif param_locator.get('type') == 'fill_date':
                self.fill_date(param_locator.get('locator'), value)
            elif param_locator.get('type') == 'value_mapping':
                self.value_mapping(param_locator.get('locator'), value)
            else:
                logging.exception(f"not support this param type {param_locator.get('type')}")
                raise Exception(f"not support this param type {param_locator.get('type')}")
            if param_locator.get('wait_for'):
                wait_for = [param_locator.get('wait_for')] if isinstance(param_locator.get('wait_for'),
                                                                         dict) else param_locator.get('wait_for')
                for wait_for_ in wait_for:
                    if wait_for_.get('type') == 'timeout':
                        self.page.wait_for_timeout(wait_for_.get('timeout'))
                    elif wait_for_.get('type') == 'visible':
                        wait_for_.get('locator').wait_for(state='visible', timeout=wait_for_.get('timeout'))
                    elif wait_for_.get('type') == 'hidden':
                        wait_for_.get('locator').wait_for(state='hidden', timeout=wait_for_.get('timeout'))
                    elif wait_for_.get('type') == 'tip_messages':
                        timeout = wait_for_.get('timeout') if wait_for_.get('timeout') else 30
                        self.tip_messages(wait_for_.get('messages'), timeout)
            if param_locator.get('mouse_move'):
                self.page.mouse.move(param_locator.get('mouse_move')[0], param_locator.get('mouse_move')[1])

        if action_dict:
            always_do_value = None
            always_do_all = [(option[0], option[1]) for option in locators if
                             isinstance(option[1], dict) and option[1].get("always_do")]
            if len(always_do_all) >= 1 and action_dict.get(always_do_all[0][0]) is not None:  # always_do 始终要做的操作
                always_do_value = action_dict.pop(always_do_all[0][0])
            try:
                for option in locators:
                    assert type(option) in (tuple, list) and len(option) == 2, "type of option is incorrect"
                    if option[0] in [key for key, value in action_dict.items() if value is not None]:
                        if isinstance(option[1], dict):  # 'relation': [('cellular_enable', 'enable')]
                            if option[1].get("relation") and option[1].get("relation") not in relations:
                                # 对关系项操作之前检查关系项
                                for relation_ in option[1].get("relation"):
                                    relation_locator = [i[1] for i in locators if i[0] == relation_[0]][0]
                                    operation(relation_[0], relation_locator, relation_[1])  # 关系项操作
                                relations.append(option[1].get("relation"))
                            operation(option[0], option[1], action_dict.get(option[0]))  # 本身操作
                        elif isinstance(option[1], list) and isinstance(action_dict.get(option[0]),
                                                                        list):  # 当使用一个变量传多个元素的值时
                            for option_, action_value in zip(option[1], action_dict.get(option[0])):
                                if option_.get("relation") and option_.get("relation") not in relations:
                                    # 对关系项操作之前检查关系项
                                    for relation_ in option_.get("relation"):
                                        relation_locator = [i[1] for i in locators if i[0] == relation_[0]][0]
                                        operation(relation_[0], relation_locator, relation_[1])  # 关系项操作
                                    relations.append(option_.get("relation"))
                                operation(option[0], option_, action_value)  # 本身操作
                        else:
                            logging.exception("type of option is incorrect")
                            raise Exception("type of option is incorrect")
            except Exception as e:
                raise e
            finally:
                if always_do_value is not None:
                    operation(always_do_all[0][0], always_do_all[0][1], always_do_value)

    @allure.step("计算元素表达式")
    def eval_locator_attribute(self, expect_: dict, locators: list) -> bool:
        """对页面特定元素值做判断

        :param expect_: {$status: $expressions}
                        status: 状态名称， 比如可以传定义好的 current_sim
                        expressions: 完整表达式, 当判断int型的关系时${value}和期望值可加"",而当需要调用str型的关系时${value}和期望值都要加"",
                         例:（'${value}==1', '${value}!=1', '${value}>1', '${value}>=1', '${value}<1', '${value}<=1', "${value}"=="abc"
                        '"${value}".startswith("123")', '"${value}".endswith("23")', '"${value}" in a', '"${value}" not in b',
                        '"${value}".__contains__("234")', 'time.strptime("${value}}", "%Y-%m-%d %H:%M:%S")'）
                        ex: '${value}==8' 多个使用元组或者列表，注意期望值是字符串时需要带上引号， 如'${value}=="sim1"'
        :param locators: [($param1, {"locator": $locator1, "type": $type1, "relation": [($param2, $value2)], "param": {$key1: $value1}}),
                          ($param2, {"locator": $locator2, "type": $type2, "relation": [($param3, $value3),……], "param": {$key2: $value2}}),
                          ($param3, {"locator": $locator2, "type": 'table_tr', "relation": [($param3, $value3),……], "param": {$key2: $value2},
                                "columns": list, 'unique_columns': list}),]
                          type:  text, switch_button, fill

        :return: 只返回True or False 不做断言
        """
        if expect_:
            for key in expect_.keys():
                filter_key = list(filter(lambda x: x[0] == key, locators))
                if len(filter_key) == 1:
                    option = filter_key[0]
                    locator = self._get_locator(option[1].get('locator'))
                    if isinstance(locator, Locator):
                        if locator.count() != 0:
                            if option[1].get('type') == 'switch_button':
                                if 'ant-switch-checked' in locator.first.get_attribute('class'):
                                    value = 'enable'
                                else:
                                    value = 'disable'
                            elif option[1].get('type') == 'fill':
                                value = locator.first.input_value()
                            elif option[1].get('type') == 'class':
                                value = locator.first.get_attribute('class')
                            else:  # type is text
                                value = locator.first.inner_text()
                        else:
                            value = None
                    else:
                        value = str(locator)
                    try:
                        if isinstance(expect_.get(key), str) and '${value}' in expect_.get(key):
                            expression = expect_.get(key).replace('${value}', value).replace('\n', ' ')
                            if option[1].get('param'):
                                expression = replace_str(expression, option[1].get('param'))
                            log_expression = expression
                            logging.info(f'assert {expression}')
                        else:
                            ex_ = expect_.get(key)
                            if option[1].get('param') and isinstance(ex_, str):
                                ex_ = replace_str(expect_.get(key), option[1].get('param'))
                            log_expression = f'{ex_} == {value}'  # 默认使用等于判断
                            ex_ = f'"{base64.b64encode(ex_.encode())}"' if isinstance(ex_, str) else ex_
                            value = f'"{base64.b64encode(value.encode())}"' if isinstance(value, str) else value
                            expression = f'{ex_} == {value}'
                        if eval(expression):
                            logging.info(f'assert {log_expression} is success')
                        else:
                            logging.info(f'assert {log_expression} is failed')
                            return False
                    except TypeError:
                        logging.error(f'get {key} inner_text failed')
                        return False
        return True

    @allure.step("获取页面元素文本值")
    def get_text(self, keys: str or list or tuple, locators: list) -> str or dict or None:
        """获取页面元素文本值

        :param keys: None or str or list or tuple, 需要获取对应文本的元素的关键字
        :param locators: [($param1, {"locator": $locator1, "type": $type1}),
                         type: 支持的类型有：'text'|'fill'|'select'|'clipboard'|'switch_button'
                         该select 为select标签的文本值， ER805 和ER605 直接使用text
        :return: 当key为None时，返回None
                 当key为str时，只能获取某一个字段的信息，同时使用str返回
                 当key为列表或者元组时， 使用字典返回相关关键字的信息
        """
        result = {}
        if keys:
            keys = [keys] if isinstance(keys, str) else keys
            for key in keys:
                filter_key = list(filter(lambda x: x[0] == key, locators))
                if len(filter_key) == 1:
                    option = filter_key[0]
                    locator = self._get_locator(option[1].get('locator'))
                    if isinstance(locator, Locator):
                        if locator.count() != 0:
                            if option[1].get('type') == 'select':
                                value = locator.first.text_content()
                            elif option[1].get('type') == 'fill':
                                value = locator.first.input_value()
                            elif option[1].get('type') == 'clipboard':
                                locator.first.click()
                                value = self.page.evaluate('navigator.clipboard.readText()')
                            elif option[1].get('type') == 'switch_button':
                                if 'ant-switch-checked' in locator.first.get_attribute('class'):
                                    value = 'enable'
                                else:
                                    value = 'disable'
                            elif option[1].get('type') == 'class':
                                value = locator.first.get_attribute('class')
                            else:
                                value = locator.first.inner_text()
                        else:
                            value = None
                    else:
                        value = str(locator)
                    result[key] = value
                else:
                    logging.exception(f'not support the key {key}')
                    raise KeyError(f'not support the key {key}')
        if result:
            if len(result.keys()) == 1:
                return result.get(keys[0])
            else:
                return result
        else:
            return None

    @allure.step("PC Ping")
    def pc_ping(self, host_or_ip: str or list or tuple = 'www.baidu.com', number: int = 4, src=None,
                lost_packets=False, assert_result=True, timeout=120, interval=10) -> None:
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
        from inhandtest.tools import pc_ping
        pc_ping(host_or_ip, number, src, lost_packets, assert_result, timeout, interval)

    def close(self) -> None:
        if self.__context and self.__browser and self.__playwright:
            self.__context.close()
            self.__browser.close()
            self.__playwright.stop()
            logging.info('close browser and playwright')


if __name__ == '__main__':
    a = BasePage('10.5.31.96', 'adm', '123456', model='IG902')
    a.login()
    # print(a.version)
