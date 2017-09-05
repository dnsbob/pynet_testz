#!/usr/bin/env python

import pexpect
from getpass import getpass
import re
import time
import sys

def main():
	username='pyclass'
	#ip_addr=raw_input("enter ip: ")
        ip_addr='184.105.247.71'
	port = 22
	password = getpass()

        ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))
        ssh_conn.timeout=3
        ssh_conn.expect('ssword:')
        ssh_conn.sendline(password)   # automatically adds newline
        ssh_conn.expect('#')

        ssh_conn.sendline('terminal length 0')
        ssh_conn.expect('#')
        #print ssh_conn.before
        #print "sending cmd...\n"

        ssh_conn.sendline('show run | inc logging')
        ssh_conn.expect('#')
        print ssh_conn.before

        ssh_conn.sendline('config term')
        ssh_conn.expect('#')

        ssh_conn.sendline('logging buffered 11223')
        ssh_conn.expect('#')

        ssh_conn.sendline('end')
        ssh_conn.expect('#')

        ssh_conn.sendline('wr')
        ssh_conn.expect('#')

        ssh_conn.sendline('show run | inc logging')
        ssh_conn.expect('#')
        print ssh_conn.before

if __name__ == "__main__":
	main()

