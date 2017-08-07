''' watchconfig.py

Watch router for config changes
and send email alert
'''

from snmp_helper import snmp_get_oid_v3,snmp_extract
import time

def debug(self,msg):
    if self.debugflag:
        print("Debug: " + msg)

ip='184.105.247.71'
port=161
devicename='pynet-rtr2'
device=(ip,port)
a_user='pysnmp'
auth_key='galileo1'
encrypt_key='galileo1'
snmp_user=(a_user, auth_key, encrypt_key)

oidlist=[
('ccmHistoryRunningLastChanged','1.3.6.1.4.1.9.9.43.1.1.1.0'),
('ccmHistoryRunningLastSaved','1.3.6.1.4.1.9.9.43.1.1.2.0' ),
('ccmHistoryStartupLastChanged','1.3.6.1.4.1.9.9.43.1.1.3.0')
]
polltime=100 # seconds (typ 300 = 5 min)
count=len(oidlist)
currentvalue=[]
previousvalue=[]
found=False

while True:
    print('time {}'.format(time.strftime('%Y/%m/%d %H:%M:%S')))
    for i in range(count):
        oid=oidlist[i][1]
        snmp_data=snmp_get_oid_v3(device,snmp_user, oid)
        data=snmp_extract(snmp_data)
        ##print oidlist[i][0] + " " + data
        if len(currentvalue) <= i:
            ##print('len(currentvalue) {}'.format(len(currentvalue)))
            currentvalue.append(data)
        else:
            ##print('len(currentvalue) {}'.format(len(currentvalue)))
            currentvalue[i]=data
        # check for change
        ##print('len(previousvalue) {}'.format(len(previousvalue)))
        ##print('i {}'.format(i))
        ##if len(previousvalue) > i:
            ##print('data {} prev {}'.format(data,previousvalue[i]))
            ##if data !=previousvalue[i]:
                ##print "CHANGED"
        if not ( len(previousvalue) <= i or data == previousvalue[i] ):
            print('{} value of {} changed from {} to {}'.format(
            time.strftime('%Y/%m/%d %H:%M:%S'),
            oidlist[i][0],
            previousvalue[i],data))
            found=True
            break   # from 'for', but really want to exit 'while'
    if found:
        break   # break out another layer to exit
    previousvalue=currentvalue[:]   # make copy of list
    # (without [:] it would beanother pointer to same list)
    print previousvalue
    time.sleep(polltime)
