# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : pypi_common
@Time    : 2023/7/7 11:30
@Auth    : wangjw
@Email   : wangjiaw@inhand.com.cn
@File    : er_default_config.py
@IDE     : PyCharm
------------------------------------
"""
"""
er805的默认配置, 根据页面的配置项进行配置, 未标注必填的配置为页面点击添加或编辑时已自动填入的配置(可进行选择性更改), 
8标注必填的配置为添加或编辑时必须手动填写的配置
"""
er_default_config = {
    "system": {
        "hostname": "ER805",
        "timezone": "UTC-8",
        "language": "English",
        "web_timeout": 360,
        "cloud_enabled": True,
        "mqtt_keepalive": 60,
        "log_server": {
            "enabled": False,
            "server": [
                {
                    "address": "",
                    "port": 514
                },
                {
                    "address": "",
                    "port": 514
                }
            ]
        }
    },
    "admin": {
        "adm_user": "adm",
        "adm_password": "$1$hGPgEjA6$J1izSbET/clVTEPx/aUtg."
    },
    "uplink": {
        "mode": "failover",
        "down_delay": 0,
        "link_detect": {
            "target": ""
        },
        "interface": {
            "0000f0804da7846f": {
                "name": "wan1",
                "priority": 1
            },
            "0000fbd1d5a379a8": {
                "name": "cellular1",
                "priority": 2
            },
            "000164a77843ddd8": {
                "name": "wlan-sta",
                "priority": 3
            },
            "000164a7784ce64a": {
                "name": "wan2",
                "priority": 4
            }
        }
    },
    "email": {
        "receiver": [],
        "sender": {
            "enable": False,
            "server": "inhand.mail.com.cn",
            "port": 25,
            "username": "",
            "password": "",
            "tls": False
        }
    },
    "record": {
        "cpu_used": 70,
        "mem_used": 70
    },
    "data_usage": {
        "sim1": {
            "monthly_data_plan": {
                "enabled": False,
                "threshold": 1,
                "threshold_unit": "GB",
                "start_date": 1,
                "over_threshold_oper": "switch-sim"
            }
        },
        "sim2": {
            "monthly_data_plan": {
                "enabled": False,
                "threshold": 1,
                "threshold_unit": "GB",
                "start_date": 1,
                "over_threshold_oper": "switch-sim"
            }
        }
    },
    "ntp": {
        "enabled": True,
        "server": [
            {
                "address": "pool.ntp.org",
                "port": 123
            }
        ]
    },
    "alerts": {
        "email_out": []
    },
    "link_quality": {
        "enabled": True,
        "delay": {
            "enable": False,
            "sustain": 5,
            "threshold": 200
        },
        "jitter": {
            "enable": False,
            "sustain": 5,
            "threshold": 200
        },
        "loss": {
            "enable": False,
            "sustain": 5,
            "threshold": 5
        },
        "signal": {
            "enable": False,
            "sustain": 5,
            "threshold": 1
        }
    },
    "l2tp": {
        "server": {
            "enabled": True,
            "interface": "any",
            "ip": "1.1.1.1",  # 必填
            "start_ip": "1.1.1.1",  # 必填
            "end_ip": "1.1.1.254",  # 必填
            "username": "adm",  # 必填
            "password": "123456",  # 必填
            "ppp_auth": "auto",
            "tunnel_auth": {
                "enabled": False,
                "server": "",
                "password": ""
            }
        },
        "clients": {
            "alias": "test",
            "enabled": True,
            "nat": True,
            "interface": "any",
            "server_ip": "1.1.1.1",
            "username": "adm",
            "password": "123456",
            "ppp_auth": "auto",
            "tunnel_auth": {
                "enabled": False
            },
            "name": "l2tp1"
        }
    },
    "ipsec": {  # 去除uuid
        "name": "test",  # 必填
        "ike_version": "ikev1",
        "key": "123456789",  # 必填
        "remote_key": "",
        "interface": "wan1",
        "peeraddr": "0.0.0.0",  # 必填
        "mode": "tunnel",
        "local_subnet": [],
        "remote_subnet": [],
        "ike_policy": {
            "encrypt": "aes128",
            "auth": "sha1",
            "dh": 2,
            "lifetime": 86400
        },
        "ipsec_policy": {
            "sec_protocol": "esp",
            "encrypt": "aes128",
            "auth": "sha1",
            "pfs": "2",
            "lifetime": 86400
        }
    },
    "ippt": {
        "enabled": False,
        "bind_mac": ""
    },
    "dhcp": {
        "server": {  # 去除uuid
            "enabled": True,
            "interface": "vlan2",
            "alias": "test",  # 必填
            "lease": 1440,
            "ip_pool": {
                "start_ip": "192.168.3.1",  # 必填
                "end_ip": "192.168.3.254"  # 必填
            },
            "option": {
                "domain_name": "",
                "dns_type": "auto",
                "dns1": "",
                "dns2": ""
            }
        },
        "manual_bind": {}
    },
    "wlan_ap": {
        "2.4G": {
            "name": "wlan1",
            "band": "2.4G",
            "mode": "ap",
            "enabled": True,
            "ssid": "ER805-1826BC",  # 必填
            "auth": "WPA2-PSK",
            "encrypt": "CCMP",
            "key": "21000058",  # 必填
            "vlan": 1,
            "channel": "Auto",
            "ap_isolate": False
        },
        "5G": {
            "name": "wlan2",
            "band": "5G",
            "mode": "ap",
            "enabled": True,
            "ssid": "ER805-5G-1826BD",  # 必填
            "auth": "WPA2-PSK",
            "encrypt": "CCMP",
            "key": "21000058",  # 必填
            "vlan": 1,
            "channel": "36",
            "ap_isolate": False
        }
    },
    "wlan_sta": {
        "name": "wlan-sta",
        "band": "2.4G",
        "mode": "sta",
        "enabled": True,
        "ssid": "test",  # 必填
        "mtu": 1500,
        "nat": True,
        "auth": "WPA2-PSK",
        "encrypt": "CCMP",
        "key": "12345678",  # 必填
        "ipv4": {
            "dhcpc": True,
            "ip": "",
            "prefix_len": 0,
            "gateway": "",
            "dns1": "",
            "dns2": ""
        }
    },
    "admin_access": {
        "http": {
            "enabled": False,
            "port": 80
        },
        "https": {
            "enabled": False,
            "port": 443
        },
        "ssh": {
            "enabled": False,
            "port": 22
        },
        "ping": {
            "enabled": False
        }
    },
    "firewall": {
        "inbound_rules": [
            {
                "uuid": "000064a778d1012c",
                "sequence": 2000,
                "name": "test",  # 必填
                "enabled": True,
                "interface": "any",
                "protocol": "any",
                "action": "permit",
                "source": "any",
                "destination": "any",
                "sport": "",
                "dport": ""
            }
        ],
        "outbound_rules": [
            {
                "uuid": "000064a778d730ce",
                "sequence": 2000,
                "name": "test2",  # 必填
                "enabled": True,
                "interface": "any",
                "protocol": "any",
                "action": "permit",
                "source": "any",
                "destination": "any",
                "sport": "",
                "dport": ""
            }
        ],
        "inbound_default": {
            "action": "deny"
        },
        "outbound_default": {
            "action": "permit"
        }
    },
    "policy_route": {
        "ip_rules": [
            {
                "uuid": "000064a779ada8a6",
                "sequence": 2000,
                "name": "test4",  # 必填
                "enabled": True,
                "preferred_outif": "wan1",
                "protocol": "any",
                "source": "any",
                "destination": "1.1.1.1/32",  # 必填
                "sport": "",
                "dport": ""
            }
        ]
    },
    "qos": {
        "uplink_rules": {
            "0000f0804da7846f": {
                "interface": "wan1",
                "egress_rate": "0Mbps",
                "ingress_rate": "0Mbps"
            },
            "0000fbd1d5a37908": {
                "interface": "cellular1",
                "egress_rate": "0Mbps",
                "ingress_rate": "0Mbps"
            },
            "000164a7784352d6": {
                "interface": "wlan-sta",
                "egress_rate": "0Mbps",
                "ingress_rate": "0Mbps"
            },
            "000264a7784c33db": {
                "interface": "wan2",
                "egress_rate": "0Mbps",
                "ingress_rate": "0Mbps"
            }
        },
        "user_rules": [
            {
                "uuid": "000064a779b68c04",
                "sequence": 2000,
                "name": "test",  # 必填
                "enabled": True,  # 必填
                "protocol": "any",
                "source": "any",
                "destination": "any",
                "sport": "",
                "dport": "",
                "priority": "highest",
                "dscp": "",
                "egress_rate": "0Mbps",
                "egress_ceil": "0Mbps",
                "ingress_rate": "0Mbps",
                "ingress_ceil": "0Mbps"
            }
        ]
    },
    "cellular": {
        "modem": {
            "enabled": True,
            "nat": True,
            "sim1": {
                "profile": "0",
                "network_type": "auto",
                "nr5g_mode": "sa-nsa",
                "pin_code": ""
            },
            "sim2": {
                "profile": "1",
                "network_type": "auto",
                "nr5g_mode": "sa-nsa",
                "pin_code": ""
            },
            "conn_mode": "always-online",
            "dual_sim": {
                "enabled": True,
                "main_sim": "sim1"
            },
            "mtu": 1500,
            "ipv4": {
                "prefix_len": 0
            }
        },
        "profile": {
            "0": {
                "type": "ipv4",
                "apn": "",
                "access_num": "*99***1#",
                "auth": "auto",
                "username": "",
                "password": ""
            },
            "1": {
                "type": "ipv4",
                "apn": "",
                "access_num": "*99***1#",
                "auth": "auto",
                "username": "",
                "password": ""
            }
        }
    },
    "port_mapping": {  # 去除uuid
        "name": "test3",  # 必填
        "interface": "any",
        "enabled": True,  # 必填
        "protocol": "tcp-udp",
        "external_port": "12",  # 必填
        "ip": "192.168.2.100",  # 必填
        "internal_port": "12"  # 必填
    },
    "lan": {  # 去除uuid
        "name": "vlan2",
        "alias": "test",  # 必填
        "vlan": 2,  # 必填
        "enabled": True,
        "mtu": 1500,
        "l3_vlan": True,
        "ipv4": {
            "dhcpc": False,
            "ip": "192.168.3.1",  # 必填
            "prefix_len": 24  # 必填
        }
    },
    "wan": {
        "wan1": {
            "name": "wan1",
            "alias": "WAN1",
            "vlan": 4010,
            "enabled": True,
            "mtu": 1500,
            "nat": True,
            "ipv4": {
                "dhcpc": True,
                "ip": "",
                "prefix_len": 0,
                "gateway": "",
                "dns1": "",
                "dns2": ""
            },
            "pppoe": {
                "enabled": False,
                "username": "",
                "password": "",
                "local_ip": "",
                "remote_ip": ""
            }
        },
        "wan2": {
            "name": "wan2",
            "alias": "WAN2",
            "vlan": 4011,
            "enabled": True,
            "mtu": 1500,
            "nat": True,
            "ipv4": {
                "dhcpc": True,
                "ip": "",
                "prefix_len": 0,
                "gateway": "",
                "dns1": "",
                "dns2": ""
            },
            "pppoe": {
                "enabled": False,
                "username": "",
                "password": "",
                "local_ip": "",
                "remote_ip": ""
            }
        }
    },
    "switch_port": {
        "lan0": {
            "name": "lan0",
            "enabled": True,
            "link_rate": "auto",
            "mode": "access",
            "pvid": 4010,
            "vid": [
                4010
            ]
        },
        "lan1": {
            "name": "lan1",
            "enabled": True,
            "link_rate": "auto",
            "mode": "access",
            "pvid": 4011,
            "vid": [
                4011
            ]
        },
        "lan2": {
            "name": "lan2",
            "enabled": True,
            "link_rate": "auto",
            "mode": "trunk",
            "pvid": 1,
            "vid": [
                "all"
            ]
        },
        "lan3": {
            "name": "lan3",
            "enabled": True,
            "link_rate": "auto",
            "mode": "trunk",
            "pvid": 1,
            "vid": [
                "all"
            ]
        },
        "lan4": {
            "name": "lan4",
            "enabled": True,
            "link_rate": "auto",
            "mode": "trunk",
            "pvid": 1,
            "vid": [
                "all"
            ]
        }
    },
    "static_route4": {
        "destination": "0.0.0.0/0",
        "desc": "default1",
        "next_hop": {
            "type": "interface",
            "interface": "wan1",
            "distance": 60
        }
    }
}
