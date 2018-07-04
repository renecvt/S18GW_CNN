from os.path import abspath, dirname

import numpy as np
import pylab as plt
from numpy import genfromtxt

from masses_generator import masses_generator

DIRNAME = dirname(dirname(abspath(__file__)))
DATA = genfromtxt('%s/Files/info.csv' % DIRNAME, delimiter=',')

M1 = DATA[:, 0]
M2 = DATA[:, 1]
MTOTAL = DATA[:, 2]
DURATION = DATA[:, 3]
DURATION1 = DATA[:, 4]
DURATION2 = DATA[:, 5]


def masses():
    plt.scatter(M1, M2)
    plt.title('Masses')
    plt.xlabel('M1')
    plt.ylabel('M2')
    plt.savefig('%s/Saved_files/saved_plots/masses.png' % DIRNAME)
    plt.show()


def duration():
    plt.scatter(MTOTAL, DURATION)
    plt.xlabel('M-Total')
    plt.ylabel('Duration')
    plt.savefig('%s/Saved_files/saved_plots/duration.png' % DIRNAME)
    plt.show()


def duration1():
    plt.scatter(MTOTAL, DURATION1)
    plt.xlabel('M-Total')
    plt.ylabel('Duration 1')
    plt.savefig('%s/Saved_files/saved_plots/duration1.png' % DIRNAME)
    plt.show()


def duration2():
    plt.scatter(MTOTAL, DURATION2)
    plt.xlabel('M-Total')
    plt.ylabel('Duration 2')
    plt.savefig('%s/Saved_files/saved_plots/duration2.png' % DIRNAME)
    plt.show()

# masses()
# duration()
# duration1()
# duration2()
