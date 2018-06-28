import pycbc
import os
import pycbc.frame
from pycbc.frame import losc
from os import listdir

def read_files():
    h1_ts = []
    l1_ts = []

    mypath = '%s/data_24hrs/' % os.getcwd()
    files = listdir(mypath)

    for f in files:
        location = mypath + f
        channel = '%s1:LOSC-STRAIN' % f[0]
        ts = pycbc.frame.read_frame(location, channel)
        if f[0] == 'H':
            h1_ts.append(ts)
        else:
            l1_ts.append(ts)

    return h1_ts, l1_ts

