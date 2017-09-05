#!/usr/bin/env python

from netmiko import ConnectHandler
from getpass import getpass
password='88newclass'
pynet2={'device_type': 'cisco_ios',
	'ip':'184.105.247.71',
	'username':'pyclass',
	'password':password
}
pynet_rtr2=ConnectHandler(**pynet2)
pynet_rtr2.config_mode()
state=pynet_rtr2.check_config_mode()
print state
