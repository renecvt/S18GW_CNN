import pycbc
import urllib
import os
import Tools
import numpy as np
import matplotlib.pyplot as plt
import h5py
import readligo as rl

from pycbc.frame import losc
from os import listdir

def get_file(url, fname):
    fullfilename = os.path.join('%s/no_inj_data_gwf/' % os.getcwd(), fname)
    if os.path.exists(fullfilename):
        print "%s exist" % fname
    else:
        print 'Saving to %s' % fullfilename
        urllib.urlretrieve(url, fullfilename)
        print('Getting : {}'.format(url))

def get_data(ifo, hdf5=False):
    for s in ifo['strain']:
        if s['format'] == 'gwf' and hdf5 == False:
            fileName = '%s-%s_LOSC_4_V1-%s-%s.gwf' % (
                s['detector'][0], s['detector'], s['GPSstart'], s['duration'])
            get_file(s['url'], fileName)
        elif s['format'] == 'hdf5' and hdf5 == True:
            fileName = '%s-%s_LOSC_4_V1-%s-%s.hdf5' % (
                s['detector'][0], s['detector'], s['GPSstart'], s['duration'])
            get_file(s['url'], fileName)

def read_segs(ifo, ifo_segs):
    for s in ifo_segs:
        start = s[0]
        end = s[1]
        frame = losc.losc_frame_json(ifo, start, end)
        get_data(frame)


def read_quality_inj(files, directory, path=""):
    for f in files:
        print 'Reading %s' % f
        filename = path + f

        _, time, _, dq_dict, inj_dict = rl.loaddata(filename)
        dt = time[1] - time[0]
        _ = 1.0 / dt


        # Everything
        # c = 0
        # goodData_1hz = 0
        # for k in dq.keys():
        #     goodData_1hz = goodData_1hz & dq[k]
        #     plt.plot(dq[k] + c, label=k)
        #     c = c+2

        # plt.plot(goodData_1hz + c + 2, label= 'Good data')
        # plt.xlabel('Time since ' + str(time[0]) + ' (s)')
        # plt.axis([0, 4096, -1, c+4])
        # plt.legend(loc=2)
        # plt.show()

        sci = dq_dict['DATA']
        cat1 = dq_dict['CBC_CAT1']
        cat2 = dq_dict['CBC_CAT2']
        cat3 = dq_dict['CBC_CAT3']
        burst1 = dq_dict['BURST_CAT1']
        burst2 = dq_dict['BURST_CAT2']
        burst3 = dq_dict['BURST_CAT3']

        goodData_1hz = burst1 & burst2 & burst3 & cat1 & cat2 & cat3

        # plt.plot(burst3 + 14, label='Burst cat 3')
        # plt.plot(burst2 + 12, label='Burst cat 2')
        # plt.plot(burst1 + 10, label='Burst cat 1')
        # plt.plot(cat3 + 8, label='CBC Cat 3')
        # plt.plot(cat2 + 6, label='CBC Cat 2')
        # plt.plot(cat1 + 4, label='CBC Cat 1')
        # plt.plot(goodData_1hz + 2, label='Good_Data')
        # plt.plot(sci, label='DATA')
        # plt.axis([0, 4096, -1, 16])
        # plt.legend(loc=2)
        # plt.xlabel('Time (s)')
        # plt.show()

        no_cbc_inj = inj_dict['NO_CBC_HW_INJ']
        no_burst_inj = inj_dict['NO_BURST_HW_INJ']
        no_detchar_inj = inj_dict['NO_DETCHAR_HW_INJ']
        no_cw_inj = inj_dict['NO_CW_HW_INJ']
        no_stoch_inj = inj_dict['NO_STOCH_HW_INJ']

        goodData_2 = no_cbc_inj & no_burst_inj & no_detchar_inj & no_cw_inj & no_stoch_inj

        # plt.plot(no_stoch_inj + 12, label='no_stoch_inj')
        # plt.plot(no_cw_inj + 10, label='no_cw_inj')
        # plt.plot(no_detchar_inj + 8, label='no_detchar_inj')
        # plt.plot(no_burst_inj + 6, label='no_burst_inj')
        # plt.plot(no_cbc_inj + 4, label='no_cbc_inj')
        # plt.plot(goodData_2 + 2, label='Good_Data')
        # plt.plot(sci, label='DATA')
        # plt.axis([0, 4096, -1, 14])
        # plt.legend(loc=2)
        # plt.xlabel('Time (s)')
        # plt.show()

        goodData = goodData_1hz & goodData_2

        # plt.plot(goodData_1hz + 6, label='DQ Data')
        # plt.plot(goodData_2 + 4, label='No INJ Data')
        # plt.plot(goodData + 2, label='Good_Data')
        # plt.plot(sci, label='DATA')
        # plt.axis([0, 4096, -1, 14])
        # plt.legend(loc=2)
        # plt.xlabel('Time (s)')
        # plt.show()

        dummy = np.zeros(goodData.shape)
        masked_dummy = np.ma.masked_array(dummy, np.logical_not(goodData) )
        segments = np.ma.flatnotmasked_contiguous(masked_dummy)
        if segments is not None:
            segList = [(int(seg.start+time[0]), int(seg.stop+time[0])) for seg in segments]
            fR = open(directory, "a")
            np.savetxt(fR, segList, fmt='%i')
            fR.close()


# Get hdf5 files, time from run O1
L_frame = losc.losc_frame_json('L1', 1126051217, 1137254417)
H_frame = losc.losc_frame_json('H1', 1126051217, 1137254417)
get_data(L_frame, hdf5=True)
get_data(H_frame, hdf5=True)

# Read hdf5 files, dquality and no injections
mypath = '%s/no_inj_data/' % os.getcwd()
L_files = [f for f in listdir(mypath) if f.endswith(".hdf5") and f.startswith('L')]
H_files = [f for f in listdir(mypath) if f.endswith(".hdf5") and f.startswith('H')]

# Save segment list
read_quality_inj(H_files, 'SL/H1_NO_INJ_DQ.txt', mypath)
read_quality_inj(L_files, 'SL/L1_NO_INJ_DQ.txt', mypath)

# Read segment list to download gwf
read_segs('H1', Tools.SegmentList('SL/H1_NO_INJ_DQ.txt', numcolumns=2))
read_segs('L1', Tools.SegmentList('SL/L1_NO_INJ_DQ.txt', numcolumns=2))

