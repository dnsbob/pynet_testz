#!/usr/bin/env python
# test_telnet.py

import telnetlib
import time
import socket
import sys

TELNET_PORT=23
TELNET_TIMEOUT=6

def telnet_connect(ip_addr, TELNET_PORT, TELNET_TIMEOUT):
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("Connection timed out")

def login(remote_conn, username, password):
    output=remote_conn.read_until("sername:", TELNET_TIMEOUT)
    remote_conn.write(username + '\n')
    output += remote_conn.read_until("ssword:", TELNET_TIMEOUT)
    remote_conn.write(password + '\n')
    return output

def send_command(remote_conn, cmd):
    cmd=cmd.rstrip()  # remove trailing linefeed if any
    remote_conn.write(cmd + '\n')
    time.sleep(1)
    return remote_conn.read_very_eager()

def main():
    ip_addr='184.105.247.70'
    username='pyclass'
    password='88newclass'

    remote_conn=telnet_connect(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    
    output=login(remote_conn, username, password)
    print output

    time.sleep(1)
    output=remote_conn.read_very_eager()
    print output

    output=send_command(remote_conn, 'terminal length 0')
    print output
    output=send_command(remote_conn, 'show version')
    print output

    

    remote_conn.close

if __name__ == '__main__':
    main()
