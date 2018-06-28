import pycbc
import urllib
import os
from pycbc.frame import losc
import Tools

def get_file(url, fname):
    fullfilename = os.path.join('%s/no_inj_data/' % os.getcwd(), fname)
    if os.path.exists(fullfilename):
        print "%s exist" % fname
    else:
        print 'Saving to %s' % fullfilename
        urllib.urlretrieve(url, fullfilename)
        print('Getting : {}'.format(url))

def get_data(ifo):
    for s in ifo['strain']:
        if s['format'] == 'gwf':
            fileName = '%s-%s_LOSC_4_V1-%s-%s.gwf' % (
                s['detector'][0], s['detector'], s['GPSstart'], s['duration'])
            get_file(s['url'], fileName)

def read_segs(ifo, ifo_segs):
    for s in ifo_segs:
        start = s[0]
        end = s[1]
        frame = losc.losc_frame_json(ifo, start, end)
        get_data(frame)

read_segs('H1', Tools.SegmentList('SL/H1_NO_CBC_HW.txt'))
read_segs('L1', Tools.SegmentList('SL/L1_NO_CBC_HW.txt'))