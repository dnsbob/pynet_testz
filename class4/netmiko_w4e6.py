#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
password='88newclass'
pynet1={'device_type': 'cisco_ios',
        'ip':'184.105.247.70',
        'username':'pyclass',
        'password':password
}
pynet2={'device_type': 'cisco_ios',
        'ip':'184.105.247.71',
        'username':'pyclass',
        'password':password
}
juniper_srx={'device_type': 'juniper',
        'ip':'184.105.247.76',
        'username':'pyclass',
        'password':password
}
for svr in [ pynet1, pynet2, juniper_srx]:
    conn=ConnectHandler(**svr)
    #conn.config_mode()
    outp=conn.send_command("show arp")
    print svr.get("ip")
    print outp
