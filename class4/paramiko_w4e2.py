#!/usr/bin/env python
''' paramiko_w4e2.py '''

import paramiko
from getpass import getpass
import time

ip_addr = '184.105.247.71'
username='pyclass'
password=getpass()
port=22

remote_conn_pre = paramiko.SSHClient() # create object
remote_conn_pre.load_system_host_keys() # reads .ssh/known_hosts
remote_conn_pre.connect(ip_addr, username=username, password=password, look_for_keys=False,allow_agent=False, port=port) # make outer ssh connection
remote_conn = remote_conn_pre.invoke_shell() # ssh session inside the connection
remote_conn.send("terminal length 0\n")
time.sleep(1)
remote_conn.send("show run | inc logging\n")
time.sleep(1)
outp=remote_conn.recv(500)
print outp

remote_conn.send("config term\n")
time.sleep(1)
remote_conn.send("logging buffered 10101\n")
time.sleep(1)
remote_conn.send("end\n")
time.sleep(1)
remote_conn.send("wr\n")
time.sleep(10)

remote_conn.send("show run | inc logging\n")
time.sleep(1)
outp=remote_conn.recv(500)
print outp
remote_conn.close()
remote_conn_pre.close()
