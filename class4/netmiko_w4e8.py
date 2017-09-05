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
for svr in [ pynet1, pynet2 ]:
    conn=ConnectHandler(**svr)
    print svr.get("ip")
    #outp=conn.config_mode()
    #print outp
    outp=conn.find_prompt()
    print outp
    outp=conn.send_command("show run | inc logging")
    print outp
    outp =conn.send_config_from_file(config_file='config_file.txt')
    print outp
    outp=conn.send_command("wr")
    print outp
    outp=conn.send_command("show run | inc logging")
    print outp

