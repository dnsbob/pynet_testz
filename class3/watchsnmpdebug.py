''' watchsnmp.py

set snmp device(s) to monitor
set snmp oid list to monitor
get snmp info from devices using oid list
save snmp data
read saved snmp data
diff from prev smp data
graph snmp data
send alert email
'''

from snmp_helper import snmp_get_oid_v3,snmp_extract
from watchdata import WatchData
import time

ip='184.105.247.70'
port=161
devicename='pynet-rtr1'
device=(ip,port)
a_user='pysnmp'
auth_key='galileo1'
encrypt_key='galileo1'
snmp_user=(a_user, auth_key, encrypt_key)
filename='snmpdata.dat'
polltime=300
endtime=3600
debugflag=True

oidlist=[
('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5'),
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5'),
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5'),
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')
]

''' data structures:
    oid_nums [oid1, oid2, ...]
    oid_names [oid1name, oid2name, ...]
    oid_sets [ [oid1name, oid1], [oid2name, oid2], ...]
    Uses the "WatchData" class
    polltime (single value in seconds)
    device IP list
    Note that first reading is the initial values,
    not graphed or reported if using differences
'''
def debug(msg):
    if debugflag:
        print("Debug: " + msg)

watchobj=WatchData(filename,oidlist,debugflag=debugflag)

# polling loop
timer=0
while timer <= endtime:
    # gather data
    valuelist=[]
    for (oidname,oid) in oidlist:
        snmp_data=snmp_get_oid_v3(device,snmp_user, oid)
        data=snmp_extract(snmp_data)
        debug( "valuelist before:")
        debug( valuelist)
        debug( oidname + "  " + oid + "  " + data)
        valuelist.append(data)
    watchobj.add(valuelist)
    time.sleep(polltime)
