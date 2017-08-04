''' watchsnmp.py

functions
set snmp device(s) to monitor
set snmp oid list to monitor
get snmp info from devices using oid list
save snmp data
read saved snmp data
diff from prev smp data
graph snmp data
send alert email
'''

''' thoughts
save initial value and diffs (needed to graph)
or raw data ?
or both ?

'''

from snmp_helper import snmp_get_oid_v3,snmp_extract

class WatchSnmp(object):
    ''' data structures:
        oid_nums [oid1, oid2, ...]
        oid_names [oid1name, oid2name, ...]
        oid_sets [ [oid1name, oid1], [oid2name, oid2], ...]
        Uses the "WatchData" class
        Note that first reading is the initial values,
        not graphed or reported if using differences
    '''
    def debug(self,msg):
        if self.debugflag:
            print("Debug: " + msg)

    def __init__(self, filename, var_list=None, polltime=None, initial='', diff='no', debugflag=False):
        ''' if file has not been initialized, then var_list is required
            initial is an optional list of initial (previous) values,
            prefixed with its timestamp (timestamp can be empty):
            [ timestamp, var1 initial value, var2 initial value, ...]
            "diff" is one of:
                "no" use values directly
                "diff" use difference between current and previous value
                "change" highlight any change in value
            "diff" can be a single value or a list of values, one per var
                if any are not "no", 
                then either "initial" or the first reading
                will be used as the comparison, and not reported or graphed
        '''

''' skip
class WatchSnmp(object):
    def __init__(self,device_ip_list,oid_list):
        self.device_ip_list=device_ip_list
        self.oid_list=oid_list
        
    def 
'''

def test():
    ''' test of WatchSnmp '''
    # create random filename
    # by creating and deleting a tempfile
    f1=tempfile.NamedTemporaryFile(delete=False)
    filename1=f1.name
    f1.close()
    os.remove(filename1)
    # now use the filename for a new file
    varlist=['name','age']

    # delete temp file
    os.remove(filename2)

if __name__ == '__main__':
    test()
