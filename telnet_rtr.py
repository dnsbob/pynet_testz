
''' telnet_rtr.py '''

import telnetlib
import time

ip_addr='184.105.247.70'
TELNET_PORT=23
TELNET_TIMEOUT=6
username='pyclass'
password='88newclass'

cmd='show ip int brief'

conn=telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)

out=conn.read_until("sername:", TELNET_TIMEOUT)
conn.write(username + '\n')
out=conn.read_until("ssword:", TELNET_TIMEOUT)
conn.write(password + '\n')
out=conn.read_until("#", TELNET_TIMEOUT)
conn.write(cmd + '\n')
out=conn.read_until("#", TELNET_TIMEOUT)
print out
conn.close
