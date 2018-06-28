import pycbc
import urllib
import os
from pycbc.frame import losc
import numpy as np

class SegmentList():
    def __init__(self, filename, numcolumns=3):

        if type(filename) is str:
            try:
                if numcolumns == 4:
                    number, start, stop, duration = np.loadtxt(filename, dtype='int',unpack=True)
                elif numcolumns == 2:
                    start, stop = np.loadtxt(filename, dtype='int',unpack=True)
                elif numcolumns == 3:
                    start, stop, duration = np.loadtxt(filename, dtype='int',unpack=True)
                if isinstance(start, int):
                    self.seglist = [[start, stop]]
                else:
                    self.seglist = zip(start, stop)
            except:
                self.seglist = []
        elif type(filename) is list:
            self.seglist = filename
        else:
            raise TypeError("SegmentList() expects the name of a segmentlist file from the LOSC website Timeline")

    def __repr__(self):
        return 'SegmentList( {0} )'.format(self.seglist)
    def __iter__(self):
        return iter(self.seglist)
    def __getitem__(self, key):
        return self.seglist[key]


segs = SegmentList('H1_NO_CW_HW_INJ.txt')
start = segs[0][0]
end = segs[0][1]

h1 = losc.losc_frame_json('H1', start, end)
l1 = losc.losc_frame_json('L1', start, end)

def get_file(url, fname):
    if os.path.exists(fname):
        print "%s exist" % fname
    else:
        urllib.urlretrieve(url, fname)
        print('Getting : {}'.format(url))


def get_data(ifo):
    for s in ifo['strain']:
        if s['format'] == 'gwf':
            fileName = '%s-%s_LOSC_4_V1-%s-%s.gwf' % (
                s['detector'][0], s['detector'], s['GPSstart'], s['duration'])
            get_file(s['url'], fileName)


get_data(l1)
get_data(h1)


