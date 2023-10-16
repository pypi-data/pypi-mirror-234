# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 15:58:25
# @Author  : Pane Li
# @File    : edge_computing_locators.py
"""
edge_computing_locators

"""
from playwright.sync_api import Page, Locator


class DockerManagerLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def docker_manager_status_locator(self) -> list:
        return [
            ('docker_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('docker_version',
             {'locator': self.page.locator('//label', has_text=self.locale.docker_version).locator(
                 '../../div[2]/div/span/div/span[1]'),
                 'type': 'text'}),
            ('portainer_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('username',
             {'locator': self.page.locator('//label', has_text=self.locale.user_name).locator('../../div[2]').nth(0),
              'type': 'text'}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'fill'}),
            ('port', {'locator': self.page.locator('#port'), 'type': 'fill'}),
        ]

    @property
    def docker_manager_locator(self) -> list:
        return [
            ('docker_manager', {'locator': self.page.locator('#enable').nth(0), 'type': 'switch_button'}),
            ('docker_upgrade', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('docker_upgrade_confirm',
             {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary').nth(0), 'type': 'button',
              'wait_for': [{'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000},  # 文件大时间就长
                           {'type': 'timeout', 'timeout': 3 * 1000}]}),
            ('docker_upgrade_tip', {'type': 'tip_messages'}),
            ('submit_docker_manager',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary').nth(1), 'type': 'button'}),
            ('portainer_manager', {'locator': self.page.locator('#enable').nth(1), 'type': 'switch_button'}),
            ('password', {'locator': self.page.locator('#password'), 'type': 'text', }),
            ('port', {'locator': self.page.locator('#port'), 'type': 'text', }),
            ('submit_portainer_manager',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]',
                                           has_text=self.locale.submit).nth(1),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]').nth(1),
                       'type': 'button', "always_do": True}),
        ]


class PythonEdgeComputingLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def app_status_table(self) -> Locator:
        return self.page.locator(
            '.ant-table.ant-table-default.ant-table-bordered.ant-table-scroll-position-left').nth(0)

    @property
    def python_engine_status_locator(self) -> list:
        return [
            ('python_engine', {'locator': self.page.locator('//button').nth(0), 'type': 'switch_button'}),
            ('sdk_version',
             {'locator': self.page.locator('//span', has_text=self.locale.sdk_version).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('python_version',
             {'locator': self.page.locator('//span', has_text=self.locale.python_version).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('username',
             {'locator': self.page.locator('//span', has_text=self.locale.username).locator('../span[2]').nth(0),
              'type': 'text'}),
            ('used_user_storage',
             {'locator': self.page.locator('//span', has_text=self.locale.used_user_storage).locator('../div').nth(0),
              'type': 'text'}),
            ('password', {'locator': self.page.locator('.anticon.anticon-copy'), 'type': 'clipboard'}),
        ]

    @property
    def python_edge_computing_locator(self) -> list:
        return [
            ('python_engine', {'locator': self.page.locator('//button').nth(0), 'type': 'switch_button'}),
            ('sdk_upgrade', {'locator': self.page.locator('//button').nth(1), 'type': 'upload_file',
                             'relation': [('python_engine', 'enable')]}),
            ('sdk_upgrade_confirm',
             {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary').nth(0), 'type': 'button'}),
            ('sdk_upgrade_tip', {'type': 'tip_messages'}),
            ('edit_password', {'locator': self.page.locator('.anticon.anticon-form').nth(0), 'type': 'button',
                               'relation': [('python_engine', 'enable')]}),
            ('password',
             {'locator': self.page.locator('.ant-input'), 'type': 'text', 'relation': [('python_engine', 'enable')]}),
            ('submit_password', {'locator': self.page.locator('.anticon.anticon-check').nth(1), 'type': 'button'}),
            ('start_all_app', {'locator': [self.page.locator('.anticon.anticon-play-circle').nth(0),
                                           self.page.locator('.ant-popover-inner-content').locator(
                                               '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                               'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('stop_all_app', {'locator': [self.page.locator('.anticon.anticon-pause-circle').nth(0),
                                          self.page.locator('.ant-popover-inner-content').locator(
                                              '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                              'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('restart_all_app', {'locator': [self.page.locator('.anticon.anticon-undo').nth(0),
                                             self.page.locator('.ant-popover-inner-content').locator(
                                                 '.ant-btn.ant-btn-primary.ant-btn-sm').first],
                                 'type': 'button', 'relation': [('python_engine', 'enable')]}),
            ('app_list',
             {'locator': {
                 'locator': self.page.locator('.antd-pro-components-in-gateway-editable-table-index-outerBox').nth(0),
                 'pop_up_locator': self.pop_up,
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                 "columns": [
                     ('app_package',
                      {'locator': self.pop_up.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
                     ('log_file_size', {'locator': self.pop_up.locator('#log_size'), 'type': 'text'}),
                     ('number_of_log', {'locator': self.pop_up.locator('#log_file_num'), 'type': 'text'}),
                     ('start_args', {'locator': self.pop_up.locator('#start_args'), 'type': 'text'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                 "always_do": True}),
                 ]},
                 'type': 'table_tr', 'relation': [('python_engine', 'enable')]}),
            ('app_status',
             {'locator': {
                 'locator': self.app_status_table,
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
             },
                 'type': 'table_tr', 'relation': [('python_engine', 'enable')]}),
            ('submit',
             {'locator': self.page.locator('//button[@class="ant-btn ant-btn-primary"]', has_text=self.locale.submit),
              'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('reset', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'),
                       'type': 'button', "always_do": True}),
            ('cancel', {'locator': self.page.locator('//button[@class="ant-btn" and @type="reset"]'), 'type': 'button',
                        "always_do": True}),
        ]


class DeviceSupervisorLocators:
    def __init__(self, page: Page, locale: dict):
        self.page = page
        self.locale = locale
        self.pop_up = self.page.locator('.ant-modal-content')

    @property
    def controller_operation(self) -> list:
        return [('add', {'locator': self.page.locator('//button').first, 'type': 'button'}),
                ('delete_bulk', {'locator': self.page.locator('//button').nth(1), 'type': 'button'}),
                ('delete_bulk_confirm',
                 {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn-primary'), 'type': 'button',
                  'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                ('apply_template', {'locator': self.page.locator('//i[@class="anticon"]'), 'type': 'button'}),
                ]

    @property
    def page_father(self) -> dict:
        return {'controller': self.page.locator('//ul[@class="ant-pagination"]'),
                'measure': self.page.locator('//ul[@class="ant-pagination ant-table-pagination"]')}

    @property
    def add_controller_all(self) -> list:
        return [('template_name',
                 {'locator': self.pop_up.locator('.ant-select.ant-select-enabled').first, 'type': 'select'}),
                ('name', {'locator': self.page.locator('#name'), 'type': 'text'}),
                ('protocol', {'locator': self.pop_up.locator('.ant-cascader-picker'), 'type': 'select_multi',
                              'param': {'modbus.modbus tcp': 'Modbus.Modbus Tcp',
                                        'Siemens PLC': self.locale.siemens_plc,
                                        'modbus.modbus rtu': 'Modbus.Modbus Rtu'}}),
                # opc ua
                ('servers_url', {'locator': self.pop_up.locator('#endpoint'), 'type': 'text'}),

                # modbus tcp or rtu
                ('ip_address', {'locator': self.page.locator('#point\.ip'), 'type': 'text'}),
                ('port', {'locator': self.page.locator('#point\.port'), 'type': 'text'}),
                # ISO-on-TCP
                ('mode', {'locator': self.pop_up.locator('#args\.mode'), 'type': 'radio_select'}),
                ('rack', {'locator': self.page.locator('#args\.rack'), 'type': 'text'}),
                ('slot', {'locator': self.page.locator('#args\.slot'), 'type': 'text'}),
                ('client_tsap', {'locator': self.page.locator('#args\.localTsap'), 'type': 'text'}),
                ('server_tsap', {'locator': self.page.locator('#args\.remoteTsap'), 'type': 'text'}),

                ('slave', {'locator': self.page.locator('#args\.slaveAddr'), 'type': 'text'}),
                ('endpoint', {'locator': self.page.locator('#endpoint'), 'type': 'select'}),
                ('polling_interval', {'locator': self.page.locator('#samplePeriod'), 'type': 'text'}),
                ('multiple_polling_interval',
                 {'locator': self.page.locator('#enablepollCycle'), 'type': 'switch_button'}),
                ('polling_interval2', {'locator': self.page.locator('#samplePeriod2'), 'type': 'text',
                                       'relation': [('multiple_polling_interval', 'enable')]}),
                # opc ua
                ('auth', {'locator': self.pop_up.locator('#args\.auth'), 'type': 'select',
                          'param': {'anonymous': self.locale.anonymous,
                                    'username_password': self.locale.username_password,
                                    'certificate_auth': self.locale.certificate_auth}}),
                ('username', {'locator': self.pop_up.locator('#args\.username'), 'type': 'text'}),
                ('password', {'locator': self.pop_up.locator('#args\.password'), 'type': 'text'}),
                ('certificate',
                 {'locator': self.pop_up.locator('.anticon.anticon-upload').nth(0), 'type': 'upload_file'}),
                ('private_key',
                 {'locator': self.pop_up.locator('.anticon.anticon-upload').nth(1), 'type': 'upload_file'}),
                ('security_policy', {'locator': self.pop_up.locator('#args\.securityPolicy'), 'type': 'select',
                                     'param': {'Automatic detection': self.locale.automatic_detection}}),
                ('security_mode', {'locator': self.pop_up.locator('#args\.securityMode'), 'type': 'select',
                                   'param': {'sign': self.locale.sign, 'sign_encrypt': self.locale.sign_encrypt}}),
                # modbus tcp or rtu
                ('description', {'locator': self.pop_up.locator('#desc'), 'type': 'text'}),
                ('advanced_settings', {'locator': self.locale.advanced_settings, 'type': 'expand'}),
                ('byte_order_16int', {'locator': self.page.locator('#args\.int16Ord'), 'type': 'select',
                                      'relation': [('advanced_settings', 'expand')]}),
                ('byte_order_32int', {'locator': self.page.locator('#args\.int32Ord'), 'type': 'select',
                                      'relation': [('advanced_settings', 'expand')]}),
                ('byte_order_32float', {'locator': self.page.locator('#args\.float32Ord'), 'type': 'select',
                                        'relation': [('advanced_settings', 'expand')]}),
                ('byte_order_64int', {'locator': self.page.locator('#args\.int64Ord'), 'type': 'select',
                                      'relation': [('advanced_settings', 'expand')]}),
                ('byte_order_64float', {'locator': self.page.locator('#args\.float64Ord'), 'type': 'select',
                                        'relation': [('advanced_settings', 'expand')]}),

                ('package_reporting', {'locator': self.page.locator('#args\.enableMsecSample'), 'type': 'switch_button',
                                       'relation': [('advanced_settings', 'expand')]}),
                ('packet_data_polling_interval', {'locator': self.page.locator('#args\.msecSamplePeriod'),
                                                  'type': 'text', 'relation': [('advanced_settings', 'expand'),
                                                                               ('package_reporting', 'enable')]}),
                ('mi_data_uploading', {'locator': self.page.locator('#args\.msecPackage'), 'type': 'text',
                                       'relation': [('advanced_settings', 'expand'),
                                                    ('package_reporting', 'enable')]}),
                ('continuous_collection',
                 {'locator': self.page.locator('#args\.continuousAcquisition'), 'type': 'switch_button',
                  'relation': [('advanced_settings', 'expand')]}),
                ('continuous_collection_address',
                 {'locator': self.page.locator('#args\.maxContinuousNumber'), 'type': 'text',
                  'relation': [('advanced_settings', 'expand'),
                               ('continuous_collection', 'enable')]}),
                ('timeout', {'locator': self.page.locator('#expired'), 'type': 'text',
                             'relation': [('advanced_settings', 'expand')]}),
                ('connect_timeout', {'locator': self.page.locator('#args\.connectTimeOut'), 'type': 'text',
                                     'relation': [('advanced_settings', 'expand')]}),
                ('periodically_upload_onchange_data',
                 {'locator': self.page.locator('#enablePerOnchange'), 'type': 'switch_button',
                  'relation': [('advanced_settings', 'expand')]}),
                ('onchange_uploading_interval',
                 {'locator': self.page.locator('#onchangePeriod'), 'type': 'text',
                  'relation': [('advanced_settings', 'expand'), ('periodically_upload_onchange_data', 'enable')]}),
                ('communication_interval_time',
                 {'locator': self.page.locator('#args\.communicationInterval'), 'type': 'text',
                  'relation': [('advanced_settings', 'expand')]}),
                ('coil_outputs_write_function_code',
                 {'locator': self.page.locator('#args\.writeCoilFunction'), 'type': 'select',
                  'relation': [('advanced_settings', 'expand')]}),
                ('holding_register_write_function_code',
                 {'locator': self.page.locator('#args\.writeRegisterFunction'), 'type': 'select',
                  'relation': [('advanced_settings', 'expand')]}),
                ('store_communication_message',
                 {'locator': self.pop_up.locator('#enableDebug'), 'type': 'switch_button',
                  'relation': [('advanced_settings', 'expand')]}),
                ('submit', {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                            'type': 'button'}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]

    @property
    def set_as_template(self) -> list:
        return [
            ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
            ('description', {'locator': self.pop_up.locator('#desc'), 'type': 'text'}),
            ('submit', {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                        'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('cancel',
             {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
        ]

    def controller_card(self, name) -> list:
        controller_name = f'//div[@class="ant-list-item"]//div[text()="{name}"]'
        controllers = [('select', {'locator': self.page.locator(controller_name), 'type': 'button'}),
                       ('check', {'locator': self.page.locator(f'{controller_name}/../../../../div[1]/label/span'),
                                  'type': 'check'}),
                       ('expand', {'locator': self.page.locator(f'{controller_name}/../../../../div[3]').locator(
                           '//i[@class="anticon anticon-ellipsis"]'), 'type': 'button'}),
                       ('edit', {'locator': self.page.get_by_text(self.locale.edit, exact=True).locator("visible=true"),
                                 'type': 'button', 'wait_for': {'type': 'timeout', 'timeout': 1000}}),
                       ('set_as_template', {
                           'locator': self.page.get_by_text(self.locale.set_as_template, exact=True).locator(
                               "visible=true"), 'type': 'button'}),
                       ('delete',
                        {'locator': self.page.get_by_text(self.locale.delete, exact=True).locator("visible=true"),
                         'type': 'button'}),
                       ('delete_confirm',
                        {'locator': self.page.locator('.ant-modal-content').locator('.ant-btn.ant-btn-primary'),
                         'type': 'button', 'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                       ('disable',
                        {'locator': self.page.get_by_text(self.locale.disable_2, exact=True).locator("visible=true"),
                         'type': 'button', 'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                       ('enable',
                        {'locator': self.page.get_by_text(self.locale.enable, exact=True).locator("visible=true"),
                         'type': 'button', 'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                       ('realtime_communication_message',
                        {'locator': self.page.get_by_text(self.locale.realtime_communication_message,
                                                          exact=True).locator("visible=true"),
                         'type': 'button', }),
                       ]
        return controllers

    def controller_card_status(self, name) -> list:
        controller_name = f'//div[@class="ant-list-item"]//div[text()="{name}"]'
        controllers = [
            ('online_', {'locator': self.page.locator(f'{controller_name}/../../span/span[1]'), 'type': 'class'}),
            ('protocol', {'locator': self.page.locator(f'{controller_name}/../../../div[2]/div'), 'type': 'text'}),
            ('address', {'locator': self.page.locator(f'{controller_name}/../../../div[3]/div'), 'type': 'text'}),
            ('description', {'locator': self.page.locator(f'{controller_name}/../../../div[4]/div'), 'type': 'text'}),
            ('status_', {'locator': self.page.locator(f'{controller_name}/../../../../../div[1]'), 'type': 'class'}),
        ]
        return controllers

    @property
    def measure_operation(self) -> list:
        return [
            ('search_name', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::input[1]'),
                             'type': 'text'}),
            ('search', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::button[1]'),
                        'type': 'button'}),
            ('add', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::button[2]'),
                     'type': 'button'}),
            ('import', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::button[3]'),
                        'type': 'upload_file'}),
            ('export', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::button[4]'),
                        'type': 'download_file'}),
            ('delete_bulk', {'locator': self.page.locator('(//div[@class="ant-card-body"])[2]/descendant::button[5]'),
                             'type': 'button'}),
            ('delete_bulk_confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn-primary'), 'type': 'button',
              'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
            ('check_all', {'locator': self.page.locator('.ant-table-thead >> .ant-checkbox-input'), 'type': 'check'}),
            ('add_to_group', {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
        ]

    def measure_add_to_group(self, name) -> list:
        return [
            ('group_name',
             {'locator': self.page.locator(f'//div[@class="ant-modal-body"]//td[text()="{name}"]/../td[1]').locator(
                 '//input[@type="radio"]'),
                 'type': 'radio'}),
            ('submit', {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                        'type': 'button'}),
        ]

    def measure_table(self, name) -> list:
        measure_name = f'//div[@class="ant-table-body"]//div[text()="{name}"]'
        return [
            ('name', {'locator': self.page.locator(f'{measure_name}'), 'type': 'button'}),
            ('check', {'locator': self.page.locator(f'{measure_name}/../../../..//span[@class="ant-checkbox"]'),
                       'type': 'check'}),
            ('edit', {'locator': self.page.locator(f'{measure_name}/../../../../td[9]//button[1]'),
                      'type': 'button', 'wait_for': {'type': 'timeout', 'timeout': 1000}}),
            ('delete', {'locator': self.page.locator(f'{measure_name}/../../../../td[9]//button[2]'),
                        'type': 'button'}),
            ('delete_confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary'),
              'type': 'button', 'wait_for': {'type': 'tip_messages', 'messages': self.locale.submit_success}}),
            ('value_edit', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//button'),
                            'type': 'button'}),
            ('value', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//input'),
                       'type': 'text'}),
            ('value_select', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]').locator(
                '.ant-select.ant-select-enabled'), 'type': 'select'}),
            ('submit', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//i[2]'),
                        'type': 'button'}),
            ('text_messages', {'type': 'text_messages'}),
            ('tip_messages', {'type': 'tip_messages'}),
            ('cancel', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//i[1]'), 'type': 'button',
                        "always_do": True}),
        ]

    def measure_card_status(self, name) -> list:
        measure_name = f'//div[@class="ant-table-body"]//div[text()="{name}"]'
        measures = [
            ('online_', {'locator': self.page.locator(f'{measure_name}/../../span/span[1]'), 'type': 'class'}),
            ('group', {'locator': self.page.locator(f'{measure_name}/../../../../td[3]'), 'type': 'text'}),
            ('datatype', {'locator': self.page.locator(f'{measure_name}/../../../../td[4]'), 'type': 'text'}),
            ('address', {'locator': self.page.locator(f'{measure_name}/../../../../td[5]'), 'type': 'text'}),
            ('value', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//span[1]'), 'type': 'text'}),
            ('unit', {'locator': self.page.locator(f'{measure_name}/../../../../td[6]//span[2]'), 'type': 'text'}),
            ('description', {'locator': self.page.locator(f'{measure_name}/../../../../td[7]'), 'type': 'text'}),
            ('time', {'locator': self.page.locator(f'{measure_name}/../../../../td[8]'), 'type': 'text'}),
        ]
        return measures

    @property
    def add_measure_all(self):
        return [('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                # OPC-UA
                ('namespace', {'locator': self.pop_up.locator('#index'), 'type': 'text'}),
                ('address_type', {'locator': self.pop_up.locator('#idType'), 'type': 'select'}),
                ('identifier', {'locator': self.pop_up.locator('#identifier'), 'type': 'text'}),
                # ISO-on-TCP
                ('register_type', {'locator': self.pop_up.locator('#regType'), 'type': 'select'}),
                ('dbnumber', {'locator': self.pop_up.locator('#dbnumber'), 'type': 'text'}),
                ('modbus_register_address', [{'locator': self.pop_up.locator(
                    '.antd-pro-components-app-reg-addr-input-index-wrapper >> .ant-input-group-addon'),
                    'type': 'select'},
                    {'locator': self.pop_up.locator(
                        '.antd-pro-components-app-reg-addr-input-index-wrapper >> .ant-input'), 'type': 'text'}]),
                ('register_address', {'locator': self.pop_up.locator('#regAddr'), 'type': 'text'}),
                ('data_type', {'locator': self.pop_up.locator('#dataType'), 'type': 'select',
                               'param': {'bit': self.locale.get('bit'), 'word': self.locale.get('word'),
                                         'sint': self.locale.get('sint'), 'byte': self.locale.get('byte'),
                                         'int': self.locale.get('int'), 'dword': self.locale.get('dword'),
                                         'dint': self.locale.get('dint'), 'bcd32': self.locale.get('bcd32'),
                                         'float': self.locale.get('float'), 'double': self.locale.get('double'),
                                         'string': self.locale.get('string'), 'bcd16': self.locale.get('bcd16'),
                                         'ulong': self.locale.get('ulong'), 'long': self.locale.get('long')}}),
                ('decimal_places', {'locator': self.pop_up.locator('#decimal'), 'type': 'text'}),
                ('read_bit_data', {'locator': self.pop_up.locator('#enableBit'), 'type': 'switch_button'}),
                ('register_bit', {'locator': self.pop_up.locator('#regBit'), 'type': 'text'}),
                ('data_register_bit', {'locator': self.pop_up.locator('#bitIndex'), 'type': 'text'}),
                ('negative_value', {'locator': self.pop_up.locator('#reverseBit'), 'type': 'switch_button'}),
                ('size', {'locator': self.pop_up.locator('#len'), 'type': 'text'}),
                ('encoding_format', {'locator': self.pop_up.locator('#codeType'), 'type': 'select',
                                     'param': {'ascii': 'ASCII', 'utf-8': 'UTF-8', 'utf-16': 'UTF-16',
                                               'utf-16-big': 'UTF-16-BIG', 'gb2312': 'GB2312'}}),
                ('is_array', {'locator': self.pop_up.locator('#isArr'), 'type': 'switch_button'}),
                ('read_write', {'locator': self.pop_up.locator('#readWrite'), 'type': 'select',
                                'param': {'read': 'Read', 'read/write': 'Read/Write', 'write': 'Write'}}),
                ('mode', {'locator': self.pop_up.locator('#uploadType'), 'type': 'select',
                          'param': {'periodic': 'Periodic', 'onchange': 'Onchange', 'never': 'Never'}}),
                ('onchange_deadzone', {'locator': self.pop_up.locator('#deadZonePercent'), 'type': 'text'}),
                ('unit', {'locator': self.pop_up.locator('#unit'), 'type': 'text'}),
                ('description', {'locator': self.pop_up.locator('#desc'), 'type': 'text'}),
                ('group', {'locator': self.pop_up.locator('#group'), 'type': 'select'}),
                ('storage_lwtsdb', {'locator': self.pop_up.locator('#storageLwTSDB'), 'type': 'switch_button'}),
                ('polling_interval', {'locator': self.pop_up.locator('#pollCycle'), 'type': 'select',
                                      'param': {'polling_interval': self.locale.polling_interval,
                                                'polling_interval_2': self.locale.polling_interval_2}}),
                ('numerical_mapping', {'locator': self.pop_up.locator('#bitMap'), 'type': 'switch_button'}),
                ('data_calculation', {'locator': self.pop_up.locator('#transformType'), 'type': 'select',
                                      'param': {'no': self.locale.get('no'),
                                                'ratio conversion': self.locale.get('ratio_conversion'),
                                                'offset and zoom': self.locale.get('offset_and_zoom'),
                                                'bit truncation': self.locale.get('bit_truncation'),
                                                'pt/ct': self.locale.get('pt/ct'),
                                                'value mapping': self.locale.get('value_mapping'), }}),
                ('trans_decimal', {'locator': self.pop_up.locator('#transDecimal'), 'type': 'text'}),
                ('data_high_limit', {'locator': self.pop_up.locator('#maxValue'), 'type': 'text'}),
                ('data_lower_limit', {'locator': self.pop_up.locator('#minValue'), 'type': 'text'}),
                ('high_limit_of_proportion', {'locator': self.pop_up.locator('#maxScaleValue'), 'type': 'text'}),
                ('lower_limit_of_proportion', {'locator': self.pop_up.locator('#minScaleValue'), 'type': 'text'}),
                ('magnification', {'locator': self.pop_up.locator('#gain'), 'type': 'text'}),
                ('offset', {'locator': self.pop_up.locator('#offset'), 'type': 'text'}),
                ('start_bit', {'locator': self.pop_up.locator('#startBit'), 'type': 'text'}),
                ('end_bit', {'locator': self.pop_up.locator('#endBit'), 'type': 'text'}),
                ('pt', {'locator': self.pop_up.locator('#pt'), 'type': 'text'}),
                ('ct', {'locator': self.pop_up.locator('#ct'), 'type': 'text'}),
                ('package_reporting', {'locator': self.pop_up.locator('#msecSample'), 'type': 'switch_button'}),
                ('value_mapping', {'locator': self.value_mapping, 'type': 'value_mapping'}),
                ('submit', {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                            'type': 'button'}),
                ('text_messages', {'type': 'text_messages'}),
                ('tip_messages', {'type': 'tip_messages'}),
                ('cancel',
                 {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button', "always_do": True}),
                ]

    @property
    def value_mapping(self) -> dict:
        return {'add': self.pop_up.locator('.ant-btn.ant-btn-primary.ant-btn-background-ghost.ant-btn-block'),
                'table': self.pop_up.locator('//table'),
                'ok': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm')}

    @property
    def group_locator(self) -> list:
        return [
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('import_confirm', {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download').first, 'type': 'download_file'}),
            ('check_all', {'locator': self.page.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('table',
             {'locator': {
                 'locator': self.page.locator('.ant-table-content').nth(0),
                 'pop_up_locator': self.pop_up,
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                 "columns": [
                     ('add', {'locator': self.page.locator('.anticon.anticon-plus-circle').first, 'type': 'button'}),
                     ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                     ('reporting_interval', {'locator': self.pop_up.locator('#uploadInterval'), 'type': 'text'}),
                     ('onchange_data', {'locator': self.pop_up.locator('#enablePerOnchange'), 'type': 'switch_button'}),
                     ('onchange_uploading_interval', {'locator': self.pop_up.locator('#onchangePeriod'), 'type': 'text',
                                                      'relation': [('onchange_data', 'enable')]}),
                     ('max_number', {'locator': self.pop_up.locator('#LwTSDBSize'), 'type': 'text'}),
                     ('storage_policy', {'locator': self.pop_up.locator('#strategy'), 'type': 'select',
                                         'param': {'same_as_reporting_interval': self.locale.same_as_reporting_interval,
                                                   'independent_storage_interval': self.locale.independent_storage_interval}}),
                     ('storage_interval', {'locator': self.pop_up.locator('#storagePeriod'), 'type': 'text'}),
                     ('storage_method', {'locator': self.pop_up.locator('#historyDataPath'), 'type': 'select',
                                         'param': {'gateway': self.locale.gateway_store, 'usb': self.locale.usb,
                                                   'sd_card': self.locale.sd_card, }}),
                     ('storage_path', {'locator': self.pop_up.locator('#dataPath'), 'type': 'text'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'hidden', 'locator': self.pop_up, 'timeout': 300 * 1000}}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                 "always_do": True}),
                 ]},
                 'type': 'table_tr', }),
            ('delete_bulk', {'locator': self.page.locator('.anticon.anticon-delete').first,
                             'type': 'button'}),
            ('delete_bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm').first, 'type': 'button'}),
        ]

    @property
    def controller_template_locator(self) -> list:
        return [
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download').first, 'type': 'download_file'}),
            ('check_all', {'locator': self.page.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('table',
             {'locator': {
                 'locator': self.page.locator('.ant-table-content').nth(0),
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                 "columns": [
                     ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                     ('description', {'locator': self.pop_up.locator('#desc'), 'type': 'text'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                 "always_do": True}),
                 ]},
                 'type': 'table_tr', }),
            ('delete_bulk', {'locator': self.page.locator('.anticon.anticon-delete').first, 'type': 'button',
                             'mouse_move': (-100, 0)}),  # 鼠标移动开，防止遮挡
            ('delete_bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
        ]

    @property
    def alarm_rules_locator(self) -> list:
        return [
            ('page_number', {'locator': self.page.locator('.ant-pagination-options-size-changer'), 'type': 'select',
                             'param': {'page': f' {self.locale.page_}'}}),
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('import_confirm', {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download').first, 'type': 'download_file'}),
            ('check_all', {'locator': self.page.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('table',
             {'locator': {
                 'locator': self.page.locator('.ant-table-content').nth(0),
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                 "columns": [
                     ('add', {'locator': self.page.locator('.anticon.anticon-plus-circle').first, 'type': 'button'}),
                     ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                     ('controller', {'locator': self.pop_up.locator('#ctrlName'), 'type': 'select'}),
                     ('measure', {
                         'locator': self.pop_up.locator('.ant-select-selection.ant-select-selection--single').nth(
                             1).locator('../div'),
                         'type': 'select'}),
                     ('level', {'locator': self.pop_up.locator('#alarmLevel'), 'type': 'select',
                                'param': {"remind": self.locale.remind, 'warning': self.locale.warning,
                                          'secondary': self.locale.secondary, 'important': self.locale.important,
                                          'serious': self.locale.serious}}),
                     ('condition',
                      [{'locator': self.pop_up.locator('.ant-select.ant-select-enabled').nth(3), 'type': 'select'},
                       {'locator': self.pop_up.locator('.ant-input').nth(1), 'type': 'text'},
                       {'locator': self.pop_up.locator('.ant-select.ant-select-enabled').nth(4), 'type': 'select'},
                       {'locator': self.pop_up.locator('.ant-select.ant-select-enabled').nth(5), 'type': 'select'},
                       {'locator': self.pop_up.locator('.ant-input').nth(2), 'type': 'text'}]),
                     ('content', {'locator': self.pop_up.locator('#content'), 'type': 'text'}),
                     ('label', {'locator': self.pop_up.locator('#alarmLable'), 'type': 'select'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                 "always_do": True}),
                 ]},
                 'type': 'table_tr', }),

            ('delete_bulk', {'locator': self.page.locator('.anticon.anticon-delete').first,
                             'type': 'button', 'mouse_move': (-100, 0)}),  # 鼠标移动开，防止遮挡
            ('delete_bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
            ('add_to_label', {'locator': self.page.locator('.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
        ]

    def alarm_add_to_label(self, name) -> list:
        return [
            ('label_name',
             {'locator': self.page.locator(f'//div[@class="ant-modal-body"]//td[text()="{name}"]/../td[1]').locator(
                 '//input[@type="radio"]'),
                 'type': 'radio'}),
            ('submit', {'locator': self.pop_up.locator('//button[@class="ant-btn ant-btn-primary"]'),
                        'type': 'button',
                        'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
        ]

    @property
    def alarm_label_locator(self) -> list:
        return [
            ('page_number', {'locator': self.page.locator('.ant-pagination-options-size-changer'), 'type': 'select',
                             'param': {'page': f' {self.locale.page_}'}}),
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('import_confirm', {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download').first, 'type': 'download_file'}),
            ('check_all', {'locator': self.page.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('table',
             {'locator': {
                 'locator': self.page.locator('.ant-table-content').nth(0),
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').locator('visible=true'),
                 "columns": [
                     ('add', {'locator': self.page.locator('.anticon.anticon-plus-circle').first, 'type': 'button'}),
                     ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                     ('save', {'locator': self.pop_up.locator(
                         '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                         'wait_for': {'type': 'timeout', 'timeout': 3 * 1000}}),
                     ('text_messages', {'type': 'text_messages'}),
                     ('tip_messages', {'type': 'tip_messages'}),
                     ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                 "always_do": True}),
                 ]}, 'type': 'table_tr'}),
            ('delete_bulk', {'locator': self.page.locator('.anticon.anticon-delete').first,
                             'type': 'button', 'mouse_move': (-100, 0)}),  # 鼠标移动开，防止遮挡
            ('delete_bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
        ]

    @property
    def alarm_realtime_locator(self) -> list:
        return [
            ('page_number', {'locator': self.page.locator('.ant-pagination-options-size-changer'), 'type': 'select',
                             'param': {'page': f' {self.locale.page_}'}})]

    @property
    def alarm_realtime_table(self) -> Locator:
        return self.page.locator('.ant-table-content')

    @property
    def alarm_history_locator(self) -> list:
        return [
            ('page_number', {'locator': self.page.locator('.ant-pagination-options-size-changer'), 'type': 'select',
                             'param': {'page': f' {self.locale.page_}'}}),
            ('name', {'locator': self.page.locator('#name'), 'type': 'text'}),
            ('start_time', {'locator': self.page.locator('.ant-calendar-picker').nth(0), 'type': 'fill_date'}),
            ('end_time', {'locator': self.page.locator('.ant-calendar-picker').nth(1), 'type': 'fill_date'}),
            ('search', {'locator': self.page.locator('.anticon.anticon-search'), 'type': 'button'}),
            ('check_all', {'locator': self.page.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('table',
             {'locator': {
                 'locator': self.page.locator('.ant-table-content').nth(0),
                 'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                     '.ant-btn.ant-btn-primary.ant-btn-sm').first, }, 'type': 'table_tr'}),
            ('delete_bulk', {'locator': self.page.locator('.anticon.anticon-delete').first,
                             'type': 'button', 'mouse_move': (-100, 0)}),  # 鼠标移动开，防止遮挡
            ('delete_bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm'), 'type': 'button'}),
        ]

    @property
    def alarm_history_table(self) -> Locator:
        return self.page.locator('.ant-table-content').nth(0)

    @property
    def parameter_locator(self) -> list:
        return [
            ('band_485', {'locator': self.page.locator('#rs485\.baud'), 'type': 'select'}),
            ('band_232', {'locator': self.page.locator('#rs232\.baud'), 'type': 'select'}),
            ('data_bits_485', {'locator': self.page.locator('#rs485\.bits'), 'type': 'select'}),
            ('data_bits_232', {'locator': self.page.locator('#rs232\.bits'), 'type': 'select'}),
            ('parity_485', {'locator': self.page.locator('#rs485\.parityChk'), 'type': 'select',
                            'param': {'none': self.locale.none, 'odd': self.locale.odd, 'even': self.locale.even}}),
            ('parity_232', {'locator': self.page.locator('#rs232\.parityChk'), 'type': 'select',
                            'param': {'none': self.locale.none, 'odd': self.locale.odd, 'even': self.locale.even}}),
            ('stop_bits_485', {'locator': self.page.locator('#rs485\.stopbits'), 'type': 'select'}),
            ('stop_bits_232', {'locator': self.page.locator('#rs232\.stopbits'), 'type': 'select'}),
            ('submit_serial', {'locator': self.page.locator('.ant-btn.ant-btn-primary').nth(0), 'type': 'button'}),

            ('log_level', {'locator': self.pop_up.locator('#logLvl'), 'type': 'select',
                           'param': {'info': self.locale.info.upper(), 'debug': self.locale.debug.upper(),
                                     'error': self.locale.error.upper(), 'warning': self.locale.warning.upper()}}),
            ('historical_alarm_max', {'locator': self.page.locator('#maxAlarmRecordSz'), 'type': 'text'}),
            ('cache_data_storage_method', {'locator': self.page.locator('#cachePath'), 'type': 'select',
                                           'param': {'usb': self.locale.usb, 'sd_card': self.locale.sd_card,
                                                     'gateway': self.locale.gateway}}),
            ('cache_data_storage_path', {'locator': self.page.locator('#folder'), 'type': 'text'}),
            ('cache_data_max', {'locator': self.page.locator('#cacheSize'), 'type': 'text'}),
            ('communication_storage_method', {'locator': self.page.locator('#debugLogPath'), 'type': 'select',
                                              'param': {'usb': self.locale.usb, 'sd_card': self.locale.sd_card,
                                                        'gateway': self.locale.gateway}}),
            ('communication_storage_path', {'locator': self.page.locator('#footer'), 'type': 'text'}),
            ('communication_max', {'locator': self.page.locator('#debugLogSize'), 'type': 'text'}),
            ('submit_default_parameter',
             {'locator': self.page.locator('.ant-btn.ant-btn-primary').nth(1), 'type': 'button'}),
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('import_confirm', {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download'), 'type': 'download_file'}),
            ('parameter', {'locator': {
                'locator': self.page.locator('//div[@class="antd-pro-pages-measure-monitor-index-wrapper"]/div[2]'),
                'pop_up_locator': self.pop_up,
                'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                "columns": [
                    ('key', {'locator': self.pop_up.locator('#key'), 'type': 'text'}),
                    ('value', {'locator': self.pop_up.locator('#value'), 'type': 'text'}),
                    ('save', {'locator': self.pop_up.locator(
                        '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button',
                        'wait_for': {'type': 'hidden', 'locator': self.pop_up,
                                     'timeout': 30 * 1000}}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                "always_do": True}),
                ]}, 'type': 'table_tr', })
        ]

    @property
    def cloud_status_locator(self) -> list:
        return [
            ('status', {'locator': self.page.locator('//div').get_by_text(self.locale.cloud_status, exact=True).locator(
                '../div[2]'), 'type': 'text',
                'param': {'not_enable': self.locale.not_enable, 'connecting': self.locale.connecting,
                          'connection_successful': self.locale.connection_successful,
                          'unknown_error': self.locale.unknown_error,
                          'registering': self.locale.registering_, 'registered': self.locale.registered}}),
            ('connection_time', {'locator': self.page.locator('//div').get_by_text(self.locale.connection_time,
                                                                                   exact=True).locator(
                '../div[2]'), 'type': 'text', 'param': {'day': self.locale.day}}),
        ]

    @property
    def cloud_locator(self) -> list:
        return [
            ('enable', {'locator': self.page.locator('#enable'), 'type': 'switch_button'}),
            ('clear_offline_cache',
             {'locator': self.page.locator('.ant-btn.ant-btn-danger.ant-btn-sm'), 'type': 'button',
              'relation': [('enable', True)]}),
            ('cache_confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary.ant-btn-sm'),
              'type': 'button', 'relation': [('enable', True)]}),
            ('import', {'locator': self.page.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('import_confirm', {'locator': self.pop_up.locator('.ant-btn.ant-btn-primary'), 'type': 'button'}),
            ('export', {'locator': self.page.locator('.anticon.anticon-download'), 'type': 'download_file'}),
            ('cloud_type', {'locator': self.page.locator('#type'), 'type': 'select', 'relation': [('enable', True)],
                            'param': {'mqtt': self.locale.mqtt, 'alibaba_cloud': self.locale.alibaba_cloud}}),
            # ics
            ('ics_local_configuration',
             {'locator': self.page.locator('#args\.force'), 'type': 'switch_button', 'relation': [('enable', True)]}),
            ('ics_server', [{'locator': self.page.locator('.ant-select.ant-select-enabled').nth(1), 'type': 'select',
                             'param': {"custom": self.locale.custom}, 'relation': [('enable', True)]},
                            {'locator': self.page.locator('//input[@class="ant-input"]').nth(0), 'type': 'text',
                             'relation': [('enable', True)]}]),
            ('ics_keepalive',
             {'locator': self.page.locator('#args\.keepalive'), 'type': 'text', 'relation': [('enable', True)]}),
            # aibaba
            ('alibaba_region_id',
             {'locator': self.page.locator('#args\.host'), 'type': 'text', 'relation': [('enable', True)]}),
            ('alibaba_auth_method',
             {'locator': self.page.locator('#args\.connType'), 'type': 'radio', 'relation': [('enable', True)],
              'param': {'unique_certificate_per_device': self.locale.unique_certificate_per_device,
                        'unique_certificate_per_product': self.locale.unique_certificate_per_product}}),
            ('alibaba_product_key',
             {'locator': self.page.locator('#args\.productKey'), 'type': 'text', 'relation': [('enable', True)]}),
            ('alibaba_device_name',
             {'locator': self.page.locator('#args\.deviceName'), 'type': 'text', 'relation': [('enable', True)]}),
            ('alibaba_device_secret',
             {'locator': self.page.locator('#args\.deviceSecret'), 'type': 'text', 'relation': [('enable', True)]}),
            ('alibaba_tls_model',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(1), 'type': 'upload_file',
              'relation': [('enable', True)]}),
            # aws
            ('aws_endpoint',
             {'locator': self.page.locator('#args\.endPoint'), 'type': 'text', 'relation': [('enable', True)]}),
            ('aws_client_id',
             {'locator': self.page.locator('#args\.clientId'), 'type': 'text', 'relation': [('enable', True)]}),
            ('aws_certificate',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(1), 'type': 'upload_file',
              'relation': [('enable', True)]}),
            ('aws_private_key', {'locator': self.page.locator('.anticon.anticon-upload').nth(2), 'type': 'upload_file',
                                 'relation': [('enable', True)]}),
            ('aws_root_ca', {'locator': self.page.locator('.anticon.anticon-upload').nth(3), 'type': 'upload_file',
                             'relation': [('enable', True)]}),
            # azure
            ('azure_auth_method',
             {'locator': self.page.locator('#args\.authType'), 'type': 'select', 'relation': [('enable', True)]}),
            ('azure_connection_string',
             {'locator': self.page.locator('#args\.connectionString'), 'type': 'text', 'relation': [('enable', True)]}),
            ('azure_hub_name',
             {'locator': self.page.locator('#args\.iotHubName'), 'type': 'text', 'relation': [('enable', True)]}),
            ('azure_device_id',
             {'locator': self.page.locator('#args\.deviceID'), 'type': 'text', 'relation': [('enable', True)]}),
            ('azure_device_certificate',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(1), 'type': 'upload_file',
              'relation': [('enable', True)]}),
            ('azure_device_key',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(2), 'type': 'upload_file',
              'relation': [('enable', True)]}),
            # mqtt

            ('mqtt_server',
             {'locator': self.page.locator('#args\.host'), 'type': 'text', 'relation': [('enable', True)]}),
            ('mqtt_client_id',
             {'locator': self.page.locator('#args\.clientId'), 'type': 'text', 'relation': [('enable', True)]}),
            ('mqtt_auth',
             {'locator': self.page.locator('#args\.auth'), 'type': 'switch_button', 'relation': [('enable', True)]}),
            ('mqtt_user', {'locator': self.page.locator('#args\.username'), 'type': 'text',
                           'relation': [('enable', True), ('mqtt_auth', True)]}),
            ('mqtt_password', {'locator': self.page.locator('#args\.passwd'), 'type': 'text',
                               'relation': [('enable', True), ('mqtt_auth', True)]}),
            ('mqtt_advanced_settings',
             {'locator': self.locale.advanced_settings, 'type': 'expand', 'relation': [('enable', True)]}),
            ('port', {'locator': self.page.locator('#args\.port'), 'type': 'text',
                      'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('keep_alive', {'locator': self.page.locator('#args\.keepalive'), 'type': 'text',
                            'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('tls', {'locator': self.page.locator('#args\.tls'), 'type': 'select',
                     'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')],
                     'param': {'symmetric': self.locale.symmetric, 'disable': self.locale.disable_,
                               'asymmetric': self.locale.asymmetric}}),
            ('verify_method', {'locator': self.page.locator('#args\.tlsAuth'), 'type': 'select',
                               'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')],
                               'param': {'verify_client_ca': self.locale.verify_client_ca,
                                         'verify_client_certificate_and_key': self.locale.verify_client_certificate_and_key}}),
            ('verify_server_certificate',
             {'locator': self.page.locator('#args\.verifyServer'), 'type': 'switch_button',
              'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('root_ca', {'locator': self.page.locator('.anticon.anticon-upload').nth(1), 'type': 'upload_file',
                         'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('client_private_key',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(2), 'type': 'upload_file',
              'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('client_certificate',
             {'locator': self.page.locator('.anticon.anticon-upload').nth(3), 'type': 'upload_file',
              'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('clean_session', {'locator': self.page.locator('#args\.cleanSession'), 'type': 'radio_select',
                               'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')],
                               'param': {'no': self.locale.no.upper(), 'yes': self.locale.yes.upper()}}),
            ('mqtt_version', {'locator': self.page.locator('#args\.mqttVersion'), 'type': 'radio_select',
                              'relation': [('enable', True), ('mqtt_advanced_settings', 'expand')]}),
            ('mqtt_last_will', {'locator': self.locale.last_will, 'type': 'expand',
                                'relation': [('enable', True), ]}),
            ('mqtt_last_will_topic', {'locator': self.page.locator('#args\.willTopic'), 'type': 'text',
                                      'relation': [('enable', True), ('mqtt_last_will', 'expand')]}),
            ('mqtt_last_will_qos', {'locator': self.page.locator('#args\.willQos'), 'type': 'select',
                                    'relation': [('enable', True), ('mqtt_last_will', 'expand')]}),
            ('mqtt_last_will_retain', {'locator': self.page.locator('#args\.willRetain'), 'type': 'select',
                                       'relation': [('enable', True), ('mqtt_last_will', 'expand')],
                                       'param': {'true': self.locale.true, 'false': self.locale.false}}),
            ('mqtt_last_will_payload', {'locator': self.page.locator('#args\.willPayload'), 'type': 'text',
                                        'relation': [('enable', True), ('mqtt_last_will', 'expand')]}),
            ('submit', {'locator': self.page.locator('.ant-btn.ant-btn-primary').last,
                        'type': 'button'}),
            ('publish', {'locator': {
                'locator': self.page.locator('.antd-pro-pages-cloud-service-message-index-addButton').nth(0).locator(
                    '..'),
                'pop_up_locator': self.pop_up,
                'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('trigger', {'locator': self.pop_up.locator('#trigger'), 'type': 'radio_select',
                                 'param': {'measuring_point': self.locale.measuring_point,
                                           'alarm_message': self.locale.alarm_message}}),
                    ('label',
                     {'locator': self.pop_up.locator('.ant-select.ant-select-enabled').nth(0), 'type': 'select_more'}),
                    ('topic', {'locator': self.pop_up.locator('#topic'), 'type': 'text'}),
                    ('qos', {'locator': self.pop_up.locator('#qos'), 'type': 'select'}),
                    ('entry_function', {'locator': self.pop_up.locator('#funcName'), 'type': 'text'}),
                    ('quick_function',
                     {'locator': self.pop_up.locator('.react-monaco-editor-container'), 'type': 'monaco'}),
                    ('save', {'locator': self.pop_up.locator(
                        '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('enable', True)]}),
            ('subscribe', {'locator': {
                'locator': self.page.locator('.antd-pro-pages-cloud-service-message-index-addButton').nth(1).locator(
                    '..'),
                'pop_up_locator': self.pop_up,
                'action_confirm': self.page.locator('.ant-popover-inner-content').locator(
                    '.ant-btn.ant-btn-primary.ant-btn-sm').first,
                "columns": [
                    ('name', {'locator': self.pop_up.locator('#name'), 'type': 'text'}),
                    ('topic', {'locator': self.pop_up.locator('#topic'), 'type': 'text'}),
                    ('qos', {'locator': self.pop_up.locator('#qos'), 'type': 'select'}),
                    ('entry_function', {'locator': self.pop_up.locator('#funcName'), 'type': 'text'}),
                    ('payload_type', {'locator': self.pop_up.locator('#payload_type'), 'type': 'select', }),
                    ('quick_function',
                     {'locator': self.pop_up.locator('.react-monaco-editor-container'), 'type': 'monaco'}),
                    ('save', {'locator': self.pop_up.locator(
                        '//button[@class="ant-btn ant-btn-primary"]'), 'type': 'button'}),
                    ('text_messages', {'type': 'text_messages'}),
                    ('tip_messages', {'type': 'tip_messages'}),
                    ('cancel', {'locator': self.pop_up.locator('//button[@class="ant-btn"]'), 'type': 'button',
                                "always_do": True}),
                ]}, 'type': 'table_tr', 'relation': [('enable', True)]})
        ]

    @property
    def cloud_measuring_point(self) -> list:
        return [
            ('page_number', {'locator': self.pop_up.locator('.ant-pagination-options-size-changer'), 'type': 'select',
                             'param': {'page': f' {self.locale.page_}'}}),
            ('search', [{'locator': self.pop_up.locator('.ant-select.ant-select-enabled').nth(0), 'type': 'select',
                         'param': {'point_name': self.locale.collection_measuring_point_name,
                                   'controller_name': self.locale.controller_name,
                                   'group_name': self.locale.group_name}},
                        {'locator': self.pop_up.locator('//input[@class="ant-input"]'), 'type': 'text'}]),
            ('is_search', {'locator': self.pop_up.locator('.anticon.anticon-search'), 'type': 'button'}),
            ('import', {'locator': self.pop_up.locator('.anticon.anticon-upload'), 'type': 'upload_file'}),
            ('export', {'locator': self.pop_up.locator('.anticon.anticon-download').first, 'type': 'download_file'}),
            ('check_all', {'locator': self.pop_up.locator('.ant-checkbox-input').first, 'type': 'check'}),
            ('measure_check_all', {'locator': self.pop_up.locator('.ant-checkbox-input').last, 'type': 'check'}),
            ('mute_bulk', {'locator': self.pop_up.locator('//button[@class="ant-btn"]').first, 'type': 'button'}),
            ('add_bulk', {'locator': self.pop_up.locator('//button[@class="ant-btn"]').last, 'type': 'button'}),
            ('bulk_confirm', {'locator': self.page.locator('.ant-popover-content').locator(
                '.ant-btn.ant-btn-primary.ant-btn-sm').locator('visible=true'), 'type': 'button',
                              'wait_for': {'type': 'tip_messages', 'messages': self.locale.submit_success}}),
            ('close', {'locator': self.pop_up.locator('.ant-modal-close-icon'), 'type': 'button'}),
        ]

    def cloud_measuring_point_table(self, name, type_='cloud') -> list:
        measure_tr = self.pop_up.locator('//tbody[@class="ant-table-tbody"]/tr/td[2]').get_by_text(name, exact=True)
        if type_ == 'cloud':
            measure_tr = measure_tr.locator('../..')
        else:
            measure_tr = measure_tr.locator('..')
        return [
            ('check', {'locator': measure_tr.locator('.ant-checkbox-input'), 'type': 'button'}),
            ('mute', {'locator': measure_tr.locator('//td[7]/a'), 'type': 'button'}),
            ('add', {'locator': measure_tr.locator('//td[7]/a'), 'type': 'button'}),
            ('confirm',
             {'locator': self.page.locator('.ant-popover-content').locator('.ant-btn.ant-btn-primary').locator(
                 'visible=true'),
              'type': 'button', 'wait_for': {'type': 'tip_messages', 'messages': self.locale.submit_success}}),
            ('name_edit', {'locator': measure_tr.locator('//button'), 'type': 'button'}),
            ('value', {'locator': self.pop_up.locator('//tbody[@class="ant-table-tbody"]/tr/td').locator(
                '//input[@class="ant-input"]'),
                'type': 'text'}),
            ('submit', {'locator': self.pop_up.locator('//tbody[@class="ant-table-tbody"]/tr/td').locator(
                '//i[@class="anticon anticon-check"]'), 'type': 'button'}),
        ]


class EdgeComputingLocators(PythonEdgeComputingLocators, DockerManagerLocators, DeviceSupervisorLocators):
    pass
