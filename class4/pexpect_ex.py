#!/usr/bin/env python

import pexpect
from getpass import getpass
import re
import time
import sys

def main():
	username='pyclass'
	ip_addr=raw_input("enter ip: ")
	port = 22
	password = getpass()

        ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(username, ip_addr, port))
        ssh_conn.logfile = sys.stdout  # for debugging
        ssh_conn.timeout=3
        ssh_conn.expect('ssword:')
        ssh_conn.sendline(password)   # automatically adds newline
        ssh_conn.expect('#')

        ssh_conn.sendline('terminal length 0')
        ssh_conn.expect('#')

        ssh_conn.sendline('show version')
        # the "re.MULTILINE" tells it to match any line in the string
        # otherwise ^ would be start of string instead of line
        pattern = re.compile(r'^Lic.*DI:.*$', re.MULTILINE)
        ssh_conn.expect(pattern)
        #print "before " + ssh_conn.before  # what it saw before the last expect
        #print "after " + ssh_conn.after   # what matched the last expect
        time.sleep(10)

if __name__ == "__main__":
	main()

