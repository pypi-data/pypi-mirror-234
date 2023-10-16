# 安装
    pip install inhandtest
	
	使用该项目时，日志都是输入到logging, 所以需要在main函数入口配置日志信息如下
    
```python
    if __name__ == '__main__':
        import sys
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                            stream=sys.stdout)
  
  ```
# tools 使用

- loop_inspector(flag='status', timeout=90, interval=5, assertion=True)

状态循环检测，当设备做完某个操作后，需要循环检测状态才能判定生效，作为函数装饰器使用

    - 参数解析
        + flag :  功能名称，用以输出日志，如果不填  默认为’status’
        + timeout : 检测超时时间 单位秒
        + interval ：检测时间间隔 单位秒
        + assertion ：断言，为True时，超时检测失败就报错，为False 超时检测失败不报错
    - 返回（return）

    返回被装饰函数返回的值

    - 实例

```python
    from inhandtest.tools import loop_inspector

    @loop_inspector(flag='status', timeout=90, interval=5, assertion=True)
    def assert_status():
        return True
               
   ```
- dict_merge(*dict)

字典合并，如果都为空

    - 参数解析
        + dict_a :  字典A
        + dict_b : 字典B
    - 返回（return）
        
    返回合并后的字典，
    
    - 实例

```python
   from inhandtest.tools import dict_merge
   
   if __name__ == '__main__':
       print(dict_merge({'key': 'value'}, {'key1': 'value1'}))
       
   {'key': 'value', 'key1': 'value1'}
        
  ```
- dict_flatten(in_dict, separator=":", dict_out=None, parent_key=None)

字典平铺，让多层级字典直接平铺，方便做字典的断言

    - 参数解析
        + in_dict :  需要平铺的字典
        + separator : 平铺字典时需要将多层级key连接，这是连接字符
        + dict_out ： 输出的字典， 一般为None
        + parent_key： 父辈的key， 一般为None
    - 返回（return）
        
    返回平铺后的字典，
    
    - 实例

```python
   from inhandtest.tools import dict_flatten
   
   if __name__ == '__main__':
       print(dict_flatten({'key': {'key1': 'value1'}, 'key2': [0, 1]}))
       
   {'key:key1': 'value1', 'key2': [0, 1]}
           
   ```
			
# Telnet 使用
- __init__(self, model: str, host: str, super_user: str, super_password: str, user='adm', password='123456', port=23, **kwargs)

初始化函数 设备Telnet操作封装，让测试同事更易用, 

    - 参数解析
        + model : 设备型号，VG710'|'IR302'|'ER805'|'ER605'，大小写无关
        + host : 设备lan ip， 192.168.2.1
        + super_user : 超级管理员的用户名称
        + super_password :  超级管理员的密码
        + user : 用户名
        + password : 用户密码
        + port : 端口
        + kwargs : interface_replace, 字典类型，只替换输入命令 {'wan': 'wan0', 'wifi_sta': 'wan2', 'cellular1': 'wwan0'}，在telnet里面接口名称转换，使得输入命令时接口名称统一。

    - 实例

```python
   from inhandtest.telnet import Telnet

   if __name__ == '__main__':
        import sys

        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO,
                            stream=sys.stdout)
        my_device = Telnet('VG710', '10.5.47.197', '*****', '******', interface_replace={'wifi': 'ath0'})
        my_device.super_mode()
                
   ```
- super_mode(self)

进入超级模式 /www

    - 参数解析
    - 返回（return）
    
    None
    
    - 实例

```python
   my_device.super_mode()
           
   ```
- config_mode(self)

进入配置模式 (config)#

    - 参数解析
    - 返回（return）
    
    None
    
    - 实例

```python
   my_device.config_mode()
           
   ```
- user_mode(self)

进入用户模式 f'{hostname}#'

    - 参数解析
    - 返回（return）
    
    None
    
    - 实例

```python
   my_device.user_mode()
           
   ```
- normal_mode(self)

进入普通模式 f'{hostname}>'

    - 参数解析
    - 返回（return）
    
    None
    
    - 实例

```python
   my_device.normal_mode()
           
   ```
- update_hostname(self, hostname: str)

更新主机名，在使用telnet时，因为读取命令要read_until, 所以一旦界面更改主机名后需要手动调用该方法更新主机名

    - 参数解析
        + hostname :  主机名
    - 返回（return）
        
    None
    
    - 实例

```python
   my_device.update_hostname('new_host_name')
           
   ```
        
- send_cli(self, command: list or str, read_until=None, type_=None, **kwargs) -> str:

发送命令，支持多条，返回最后一条命令输入后的结果

    - 参数解析
        + command : 支持发送多条命令["first_command", "second_command"] or 'command'
        + read_until: str or list, 直至返回结果终止， 与command相呼应，如None的情况表示输入命令后等待1s， ['/www', None]
        + type_: 'super'|'config'|'user'|'normal'|None 在什么模式下执行
        + kwargs : 
            + timeout: 当有read_until时， timeout参数生效， 读取超时时间 默认30秒
            + key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等
            + key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
                + 'cli': 仅替换发出去的命令
                + 'last_read': 仅替换最后读取到的内容
                + 'cli_last_read': 既要替换cli 也要替换最后读取到的内容
            + interface_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在interface_replace 有值时生效，默认cli
                + 'cli': 仅替换发出去的命令
                + 'last_read': 仅替换最后读取到的内容
                + 'cli_last_read': 既要替换cli 也要替换最后读取到的内容
                
    - 返回（return）
        
    读取超时时返回Exception， 如果命令执行正确，返回最后一条命令输入后的结果
    
    - 实例

```python
   my_device.send_cli('ifconfig ath0')
           
   ```
	
- assert_cli(self, cli=None, expect=None, timeout=120, interval=5, type_='super', key_replace=None, key_replace_type='last_read', interface_replace_type='cli'):

在某个模式下支持输入一条或多条命令, 且支持对执行时最后一条命令返回的结果做断言, 该方法对ping tcpdump命令 无效

    - 参数解析
        + cli : str or list, 发送的命令 一条或者多条
        + expect : str or list or dict, 一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False} 同时校验时可以是{$expect1: True, $expect: False}, str或者list时都是判断存在
        + timeout : 检测超时时间  秒
        + interval : 检测间隔时间 秒
        + type_ : 'super'|'config'|'user'|'normal'
        + key_replace: 字典, 需将固定字符替换为另一字符则填写该参数, 例: {'\r\n': '', ' ': ''}等 默认去掉换行
        + key_replace_type: 'cli'|'last_read'|'expect'，仅在key_replace 有值时生效，默认last_read
            + 'cli': 仅替换发出去的命令
            + 'last_read': 仅替换最后读取到的内容
            + 'expect': 仅替换期望校验的值
            + 'cli_last_read'|'cli_expect'|'last_read_expect' 任意两种组合
            + 'cli_expect_last_read': 既要替换cli 也要替换最后读取到的内容还有校验的值
        + interface_replace_type: 'cli'|'last_read'|'expect'，仅在interface_replace 有值时生效，默认cli
            + 'cli': 仅替换发出去的命令
            + 'last_read': 仅替换最后读取到的内容
            + 'expect': 仅替换期望校验的值
            + 'cli_last_read'|'cli_expect'|'last_read_expect' 任意两种组合
            + 'cli_expect_last_read': 既要替换cli 也要替换最后读取到的内容还有校验的值
                
    - 返回（return）
        
    None|Exception
    
    - 实例


```python
   my_device.assert_cli('ifconfig ath0', expect='HWaddr 00:18:05:A0:00:03')
           
   ```
 
- ping(self, address='www.baidu.com', packets_number=4, params='', key_replace=None, lost_packets=False):

设备里面ping地址

    - 参数解析
        + address: 域名或者IP
        + packets_number, ping 包的个数，默认都是4个
        + params: 参数 如'-I cellular1'、'-s 32'
        + key_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        + lost_packets: True|False 如果为True判断会丢包，如果为False判断不丢包
                
    - 返回（return）
        
    None|Exception
    
    - 实例

```python
   my_device.ping()
           
   ```
        
- tcpdump(self, expect: str or list or dict, key_replace=None, timeout=30, interval=5, **kwargs):

设备里面抓包

    - 参数解析
        + expect: str or list or dict, 一条或多条希望校验的存在的结果，如需要判断不存在时，可以使用字典{$expect: False}, str或者list时都是判断存在
        + key_replace: 字典类型， 传入的参数转换关系表{$old: $new}
        + timeout: 校验超时时间, 单位秒
        + interval: 检测时间间隔 单位秒
        + kwargs: 命令参数, str, interface| param| cat_num
            + interface: 接口名称, wan| wifi_24g| wifi_5g| lan| cellular1
            + param: 抓包过滤关键字, None, 'icmp', 'http', 'port 21', 'host 1.1.1.1 and icmp'
            + catch_num: 抓包数量, int
                
    - 返回（return）
        
    None|Exception
    
    - 实例

```python
   my_device.tcpdump()
           
   ```
        
- re_match(self, command: str or list, regular: str or list, type_='super', key_replace=None, key_replace_type='last_read') -> str or list:

根据表达式获取最后一次执行命令的匹配值

    - 参数解析
        + command: 发送命令，可以是一条或多条
        + regular: 正则表达式，对执行的最后一次命令返回内容进行正则查询，必须要查询到，
            + 如果查不到，直至查询超时并报错
            + 如果查到不止一个，返回每个正则表达式的第一个
            + 列子：硬件地址 r'HWaddr(.*)inet6'， '(([0-9a-fA-F]{2}[:]){5}([0-9a-fA-F]{2})|([0-9a-fA-F]{2}[-]){5}([0-9a-fA-F]{2}))'
        + type_: 'super'|'config'|'user'|'normal'
        + key_replace: dict 替换最后一次命令返回内容的值 默认：{'\r\n':'', ' ': ''}
        + key_replace_type: 'cli'|'last_read'|'cli_last_read'，仅在key_replace 有值时生效，默认last_read
            + 'cli': 仅替换发出去的命令
            + 'last_read': 仅替换最后读取到的内容
            + 'cli_last_read': 既要替换cli 也要替换最后读取到的内容          
                
    - 返回（return）
        
    Exception|str or list ，根据正则表达式的个数返回值
    
    - 实例

```python
   my_device.re_match('ifconfig ath0', r'HWaddr(.*)inet6')
           
   ```
- kill_process(self, name: str)

使用kill杀死对应进程

    - 参数解析
        + name: 进程相关名称
    - 返回（return）
        
    None
    
    - 实例

```python
   my_device.kill_process('DeviceManager')
           
   ```

- reboot(self)

重启设备

    - 参数解析
    - 返回（return）
        
    None
    
    - 实例

```python
   my_device.reboot()
           
   ```
- close(self)

关闭连接

    - 参数解析
    - 返回（return）
        
    None
    
    - 实例

```python
   my_device.close()
           
   ```