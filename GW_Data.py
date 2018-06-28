import pycbc
import os
import pycbc.frame
from pycbc.frame import losc
from os import listdir


def read_files(files, path=""):
    h1_ts = []
    l1_ts = []

    for f in files:
        print 'Reading %s' % f
        location = path + f
        channel = '%s1:LOSC-STRAIN' % f[0]
        ts = pycbc.frame.read_frame(location, channel)
        if f[0] == 'H':
            h1_ts.append(ts)
        else:
            l1_ts.append(ts)

    return h1_ts, l1_ts


###### Examples #####
# Multiple files
mypath = '%s/data_24hrs/' % os.getcwd()
files = listdir(mypath)
read_files(files, mypath)

# 1 file
_, l1_ts = read_files(['L-L1_LOSC_4_V1-1126068224-4096.gwf'])
print l1_ts
