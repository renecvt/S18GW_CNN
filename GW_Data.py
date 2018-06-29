# coding=utf-8
import pycbc
import os
import pycbc.frame
from pycbc.frame import losc, read_frame
from os import listdir

def read_files(files, path=""):
    h1_ts = []
    l1_ts = []

    for f in files:
        print 'Reading %s' % f
        location = path + f
        ## Default channel: H1:LOSC-STRAIN / L1:LOSC-STRAIN
        channel = '%s1:LOSC-STRAIN' % f[0]
        ts = read_frame(location, channel)
        if f[0] == 'H':
            h1_ts.append(ts)
        else:
            l1_ts.append(ts)

    return h1_ts, l1_ts


###### Examples #####
# Path for multiple files in a folder
# mypath = '%s/no_inj_data/' % os.getcwd()
# files = [f for f in listdir(mypath) if f.endswith(".gwf")]

# h1, l1 = read_files(files, mypath)

# 1 file in current folder
# _, l1 = read_files(['L-L1_LOSC_4_V1-1126068224-4096.gwf'])

# Multiple files in current folder
#files = [f for f in listdir('./') if f.endswith(".gwf")]
# h1, l1 = read_files(files)

