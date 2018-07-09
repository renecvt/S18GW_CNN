# coding=utf-8
import os
from os import listdir

import numpy as np
import pycbc
import pycbc.frame
from pycbc.frame import losc, read_frame


def read_files():
    mypath = '%s/Data/no_inj_data_gwf/' % os.getcwd()
    H_files = [f for f in listdir(mypath) if f.startswith('H')]
    L_files = [f for f in listdir(mypath) if f.startswith('L')]

    H_files_time = [f.split('-')[2] for f in listdir(mypath) if f.startswith('H')]
    L_files_time = [f.split('-')[2] for f in listdir(mypath) if f.startswith('L')]

    common_list = list(set(H_files_time).intersection(L_files_time))
    H_files = [f for f in H_files if f.split('-')[2] in common_list]
    L_files = [f for f in L_files if f.split('-')[2] in common_list]

    files = H_files + L_files

    h1_ts = []
    l1_ts = []

    files = ['L-L1_LOSC_4_V1-1126109184-4096.gwf', 'H-H1_LOSC_4_V1-1126109184-4096.gwf']

    for f in files:

        print 'Reading %s' % f
        location = mypath + f

        # Default channel: H1:LOSC-STRAIN / L1:LOSC-STRAIN
        channel = '%s1:LOSC-STRAIN' % f[0]
        ts = read_frame(location, channel)

        for i in range(0, 4096):
            start_time = ts.start_time + i
            strain = ts.time_slice(start_time, start_time + 1)

            if f[0] == 'H':
                h1_ts.append(strain)
            else:
                l1_ts.append(strain)



    return h1_ts, l1_ts


