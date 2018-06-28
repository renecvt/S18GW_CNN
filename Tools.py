import numpy as np

class SegmentList():
    def __init__(self, filename, numcolumns=3):

        if type(filename) is str:
            try:
                if numcolumns == 4:
                    _, start, stop, _ = np.loadtxt(filename, dtype='int',unpack=True)
                elif numcolumns == 2:
                    start, stop = np.loadtxt(filename, dtype='int',unpack=True)
                elif numcolumns == 3:
                    start, stop, _ = np.loadtxt(filename, dtype='int',unpack=True)
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