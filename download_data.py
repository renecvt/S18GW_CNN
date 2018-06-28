import pycbc
import urllib
import os
from pycbc.frame import losc
import Tools

segs = Tools.SegmentList('H1_NO_CW_HW_INJ.txt')
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
