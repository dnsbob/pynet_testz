''' watchconfigsave.py

Watch router for config changes
and send email alert
save data in file, can be called from cron
'''

from snmp_helper import snmp_get_oid_v3,snmp_extract
import time
import pickle
import yaml
import json
from email_helper import send_mail

def debug(self,msg):
    if self.debugflag:
        print("Debug: " + msg)

ip='184.105.247.71'
port=161
devicename='pynet-rtr2'
a_user='pysnmp'
auth_key='galileo1'
encrypt_key='galileo1'
statefileprefix='watchconfigstate'
to='rharolde@umich.edu'
fromwho='bharold@pylab12b.twb-tech.com'
#filetype='pickle'
#filetype='yaml'
filetype='json'
device=(ip,port)
snmp_user=(a_user, auth_key, encrypt_key)

oidlist=[
('ccmHistoryRunningLastChanged','1.3.6.1.4.1.9.9.43.1.1.1.0'),
('ccmHistoryRunningLastSaved','1.3.6.1.4.1.9.9.43.1.1.2.0' ),
('ccmHistoryStartupLastChanged','1.3.6.1.4.1.9.9.43.1.1.3.0')
]
##polltime=100 # seconds (typ 300 = 5 min)
count=len(oidlist)
currentvalue=[]
previousvalue=[]

def readfile(statefileprefix):
    try:
        if filetype == 'pickle':
            f=open(statefileprefix + ".pk1","rb")
            previousvalue=pickle.load(f)
        elif filetype == 'yaml':
            f=open(statefileprefix + ".yaml","r")
            previousvalue=yaml.load(f)
        else:
            f=open(statefileprefix + ".json","r")
            previousvalue=json.load(f)
    except IOError:
        previousvalue=[]
    return previousvalue

def writefile(statefileprefix,previousvalue):
    if filetype == 'pickle':
        f=open(statefileprefix + ".pk1","wb")
        pickle.dump(previousvalue,f)
    elif filetype == 'yaml':
        f=open(statefileprefix + ".yaml","w")
        f.write(yaml.dump(previousvalue, default_flow_style=False))
    else:
        f=open(statefileprefix + ".json","w")
        json.dump(previousvalue,f)
    return

previousvalue=readfile(statefileprefix)
print('time {}'.format(time.strftime('%Y/%m/%d %H:%M:%S')))
print('readfile')
print previousvalue
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
        subject="router config changed"
        text='{} value of {} changed from {} to {}'.format(
        time.strftime('%Y/%m/%d %H:%M:%S'),
        oidlist[i][0],
        previousvalue[i],data)
        print(text)
        if send_mail(to,subject,text,fromwho):
            print 'email sent ok'
        break # only send email on first value that changed
previousvalue=currentvalue[:]   # make copy of list
# (without [:] it would beanother pointer to same list)
print "writefile"
print previousvalue
writefile(statefileprefix,previousvalue)
# no sleep, writing file instead
#time.sleep(polltime)
