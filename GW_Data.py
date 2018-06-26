import pycbc, os
import pycbc.frame
from pycbc.frame import losc
from os import listdir
from pycbc.strain import StrainBuffer

mypath = '%s/data_24hrs/' % os.getcwd()
files = listdir(mypath)

for f in files:
    location = mypath + f
    channel =  '%s1:LOSC-STRAIN' % f[0]
    ts = pycbc.frame.read_frame(location, channel)
