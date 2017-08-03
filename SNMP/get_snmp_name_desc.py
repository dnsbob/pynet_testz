
''' get_snmp_name_desc.py '''

from snmp_helper import snmp_get_oid,snmp_extract

PORT=161
COMMUNITY='galileo'
rtrs={'pynet-rtr1':'184.105.247.70', 'pynet-rtr2':'184.105.247.71'}
oids={'sysName':'1.3.6.1.2.1.1.5.0', 'sysDescr':'1.3.6.1.2.1.1.1.0'}

for rtr in rtrs.keys():
    print rtr
    for oid in oids.keys():
        print "    " + oid + " = " + snmp_extract(snmp_get_oid((rtrs[rtr],COMMUNITY,PORT),oids[oid]))
