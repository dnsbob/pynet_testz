''' watchdata.py 

read and write timestamped data to file in python pickle format
intended for monitoring
'''

import pickle
import sys
import time
import tempfile
import os

class WatchData(object):
    ''' data structures:
        var_list [var1, var2, ...]
        times [time1, time2, ...]
        data (list of lists)
            [ [var1 data at time1, data at time2, ...],
              [var2 data at time1, data at time2, ...],
            ...]
        saved in file (appended) as:
        var_list
        diff
        timestamp, var1 data, var2 data, ...
        Note that first line is the initial values,
        not graphed or reported if using differences
    '''
    def debug(self,msg):
        if self.debugflag:
            print("Debug: " + msg)

    def __init__(self, filename, var_list=None, initial='', diff='no', debugflag=False):
        ''' if file has not been initialized, then var_list is required
            initial is an optional list of initial (previous) values,
            prefixed with its timestamp (timestamp can be empty):
            [ timestamp, var1 initial value, var2 initial value, ...]
            used if carrying over from another log file,
            so that each log file can be stand-alone.
            "diff" is one of:
                "no" use values directly
                "diff" use difference between current and previous value
                "change" highlight any change in value
            "diff" can be a single value or a list of values, one per var
                if any are not "no", 
                then either "initial" or the first reading
                will be used as the comparison, and not reported or graphed
            4 cases:
                1. No file, no var_list, error
                2. No file, var_list, create file
                3. file exists, no var list, read var_list from file
                4. file exists, var_list, var_list must match file
        '''
        self.debugflag=debugflag
        # default values if not in arguments
        data=[]
        # try to read any existing file
        fileexists=False
        try:
            f=open(filename,'rb')
            fileexists=True
        except IOError:
            self.debug( 'notice - file does not exist yet')
        
        if fileexists:
            self.debug( 'try to read file header')
            try:
                file_var_list=pickle.load(f)
                self.debug('file_var_list {}'.format(file_var_list))
                file_diff=pickle.load(f)
                self.debug('file_diff {}'.format(file_diff))
                file_initial=pickle.load(f)
                self.debug('file_initial {}'.format(file_initial))
            except EOFError:
                raise ValueError('error - file exists but no proper header')
            file_data=[]
            while True:
                try:
                    datarow=pickle.load(f)
                    file_data.append(datarow)
                    self.debug('read data row {}'.format(datarow))
                except EOFError:
                    break
            self.debug('total data from file {}'.format(file_data))

            if var_list:
                # case 4. file exists, var_list, var_list must match file
                if file_var_list != var_list:
                    raise ValueError('error - file exists, but variable list does not match')
            else:
                # case 3. file exists, no var list, use var_list from file
                if file_initial:
                    print 'warning - file exists, initial list ignored'
                var_list=file_var_list
                diff=file_diff
                initial=file_initial
            # in either case, data comes from file
            data=file_data
            # file has been read, now switch to write append
            self.debug('close file and reopen for append')
            f.close()
            try:
                f=open(filename,'ab')
            except IOError:
                raise IOError('error - file is not writable')
        else: # file does not exist
            if not var_list:
                # case 1. No file, no var_list, error
                raise ValueError('error - file not found and no variable list given')
            else:
                # case 2. No file, var_list, create file
                self.debug('create new file')
                f=open(filename,'wb')
                pickle.dump(var_list,f)
                pickle.dump(diff,f)
                pickle.dump(initial,f)
                f.flush()
        # set object variables last
        self.filename=filename
        self.var_list= var_list
        self.initial=initial
        self.diff=diff
        self.data=data
        self.f=f

    def __del__(self):
        try:
            self.f.close()
        except:
            # ok if it was never created
            pass

    def add(self, datarow, timestamp=None):
        if not timestamp:
            timestamp=time.strftime('%Y/%m/%d %H:%M:%S')
        datarow.insert(0,timestamp)
        pickle.dump(datarow,self.f)
        self.f.flush()
        self.data.append(datarow)
        self.debug('added row {}'.format(datarow))

    def get_vars(self):
        return self.var_list
    def get_diff(self):
        return self.diff
    def get_initial(self):
        return self.initial
    def get_data(self):
        return self.data


def test():
    ''' test of WatchData '''
    # create random filename
    # by creating and deleting a tempfile
    f1=tempfile.NamedTemporaryFile(suffix='pk1',delete=False)
    filename1=f1.name
    f1.close()
    os.remove(filename1)
    # now use the filename for a new file
    varlist=['name','age']
    mywatch=WatchData(filename1,varlist,debugflag=True)
    print("vars {}".format(mywatch.get_vars()))
    print("diff default {}".format(mywatch.get_diff()))
    print("initial default {}".format(mywatch.get_initial()))
    print("data should be empty: {}".format(mywatch.get_data()))
    mywatch.add(['fred',24])
    print("data with one row {}".format(mywatch.get_data()))
    mywatch.add(['sam',16])
    print("data with two rows {}".format(mywatch.get_data()))

    # now close, move to new name
    print('close and reopen with new name')
    mywatch.f.close()
    filename2=filename1 + "x"
    os.rename(filename1, filename2)

    # open existing file
    mywatch2=WatchData(filename2,debugflag=True)
    print("vars {}".format(mywatch2.get_vars()))
    print("diff default {}".format(mywatch2.get_diff()))
    print("initial default {}".format(mywatch2.get_initial()))
    print("data should have two rows {}".format(mywatch2.get_data()))
    mywatch2.add(['jo',3])
    print("data with three rows {}".format(mywatch2.get_data()))

    # delete temp file
    os.remove(filename2)

if __name__ == '__main__':
    test()
