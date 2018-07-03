# coding=utf-8
import pycbc
import os
import pycbc.frame
import numpy as np
from pycbc.frame import losc, read_frame
from os import listdir

def read_files():
    mypath = '%s/no_inj_data_gwf/' % os.getcwd()
    H_files = [f for f in listdir(mypath) if f.startswith('H')]
    L_files = [f for f in listdir(mypath) if f.startswith('L')]

    H_files_time = [f[15:-10] for f in listdir(mypath) if f.startswith('H')]
    L_files_time = [f[15:-10] for f in listdir(mypath) if f.startswith('L')]

    common_list = list(set(H_files_time).intersection(L_files_time))

    H_files = [f for f in H_files if f[15:-10] in common_list]
    L_files = [f for f in L_files if f[15:-10] in common_list]

    files = H_files + L_files

    h1_ts = []
    l1_ts = []

    for f in files:
        print 'Reading %s' % f
        location = mypath + f
        ## Default channel: H1:LOSC-STRAIN / L1:LOSC-STRAIN
        channel = '%s1:LOSC-STRAIN' % f[0]
        ts = read_frame(location, channel)
        if f[0] == 'H':
            h1_ts.append(ts)
        else:
            l1_ts.append(ts)

    return h1_ts, l1_ts


# h1, l1 = read_files()
