import numpy as np
import matplotlib.pyplot as plt
import h5py
import readligo as rl

filename = 'L-L1_LOSC_4_V1-1126068224-4096.hdf5'

strain, time, dq, dq_dict, inj_dict = rl.loaddata(filename)
dt = time[1] - time[0]
fs = 1.0 / dt


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

plt.plot(burst3 + 14, label='Burst cat 3')
plt.plot(burst2 + 12, label='Burst cat 2')
plt.plot(burst1 + 10, label='Burst cat 1')
plt.plot(cat3 + 8, label='CBC Cat 3')
plt.plot(cat2 + 6, label='CBC Cat 2')
plt.plot(cat1 + 4, label='CBC Cat 1')
plt.plot(goodData_1hz + 2, label='Good_Data')
plt.plot(sci, label='DATA')
plt.axis([0, 4096, -1, 16])
plt.legend(loc=2)
plt.xlabel('Time (s)')
plt.show()

no_cbc_inj = inj_dict['NO_CBC_HW_INJ']
no_burst_inj = inj_dict['NO_BURST_HW_INJ']
no_detchar_inj = inj_dict['NO_DETCHAR_HW_INJ']
no_cw_inj = inj_dict['NO_CW_HW_INJ']
no_stoch_inj = inj_dict['NO_STOCH_HW_INJ']

goodData_2 = no_cbc_inj & no_burst_inj & no_detchar_inj & no_cw_inj & no_stoch_inj

plt.plot(no_stoch_inj + 12, label='no_stoch_inj')
plt.plot(no_cw_inj + 10, label='no_cw_inj')
plt.plot(no_detchar_inj + 8, label='no_detchar_inj')
plt.plot(no_burst_inj + 6, label='no_burst_inj')
plt.plot(no_cbc_inj + 4, label='no_cbc_inj')
plt.plot(goodData_2 + 2, label='Good_Data')
plt.plot(sci, label='DATA')
plt.axis([0, 4096, -1, 14])
plt.legend(loc=2)
plt.xlabel('Time (s)')
plt.show()

goodData = goodData_1hz & goodData_2

plt.plot(goodData_1hz + 6, label='DQ Data')
plt.plot(goodData_2 + 4, label='No INJ Data')
plt.plot(goodData + 2, label='Good_Data')
plt.plot(sci, label='DATA')
plt.axis([0, 4096, -1, 14])
plt.legend(loc=2)
plt.xlabel('Time (s)')
plt.show()

## ------- ##
# dataFile = h5py.File(filename, 'r')
# gpsStart = dataFile['meta']['GPSstart'].value

# print dataFile['quality']
# dqInfo = dataFile['quality']['simple']
# bitnameList = dqInfo['DQShortnames'].value
# nbits = len(bitnameList)

# for bit in range(nbits):
#     print bit, bitnameList[bit]

# qmask = dqInfo['DQmask'].value
# sci = (qmask >> 0) & 1
# cat1 = (qmask >> 1) & 1
# cat2 = (qmask >> 2) & 1
# cat3 = (qmask >> 3) & 1
# burst1 = (qmask >> 4) & 1
# burst2 = (qmask >> 5) & 1
# burst3 = (qmask >> 6) & 1

# goodData_1hz = sci & burst1 & burst2 & burst3 & cat1 & cat2 & cat3

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

# dummy = np.zeros(goodData_1hz.shape)
# masked_dummy = np.ma.masked_array(dummy, np.logical_not(goodData_1hz) )
# segments = np.ma.flatnotmasked_contiguous(masked_dummy)
# segList = [(int(seg.start+gpsStart), int(seg.stop+gpsStart)) for seg in segments]
# print segList
