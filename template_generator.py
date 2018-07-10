import csv
import os
from os.path import abspath, dirname

import pylab
from pycbc.filter import highpass, resample_to_delta_t
from pycbc.types import TimeSeries
from pycbc.waveform import get_td_waveform

import GW_Data
import numpy
import Tools
from numpy import genfromtxt
from Tools.masses_generator import masses_generator
from Tools.Tools import (cut_zero_values, get_bigger_value, move_ts_axis,
                         resize_ts)

DIRNAME = dirname(dirname(abspath(__file__)))
DEFAULT_APPROXIMANT = 'SEOBNRv3_opt'
MASSES = masses_generator()
TSEGMENT = 1
DELTA_T = 1.0 / 4096
F_LOWER = 20
LOWEST_TIME_CROP = .200
NORMAL_TIME_CROP = .400
HIGHEST_TIME_CROP = .600
data = []


def create_folder(folder_name, file_name):
    working_dir = os.getcwd()
    complete_directory = '{}/{}/{}'.format(working_dir, folder_name, file_name)
    folder_container = '{}/{}'.format(working_dir, folder_name)
    if not os.path.exists(complete_directory):
        if os.path.exists(folder_container):
            new_file = open(complete_directory, 'w+')
            new_file.close()
        else:
            os.makedirs(folder_container)
            new_file = open(complete_directory, 'w+')
            new_file.close()
    else:
        open(complete_directory, 'w').close()
    return complete_directory


def template_generator(approximant, masses):
    counter = 1
    directory = create_folder('Files', 'dataset.csv')
    file = open(directory, 'at')
    for mass in masses:
        plus_polarization, _ = get_td_waveform(
            approximant=approximant, mass1=mass[0], mass2=mass[1], delta_t=DELTA_T, f_lower=F_LOWER)
        cut_plus_polarization = cut_zero_values(ts=plus_polarization)
        resized_plus_polarization = resize_ts(
            ts=cut_plus_polarization, time=TSEGMENT)
        lowest_moved_axis_plus_polarization = move_ts_axis(
            ts=resized_plus_polarization, time_crop=LOWEST_TIME_CROP, duration=TSEGMENT)
        normal_moved_axis_plus_polarization = move_ts_axis(
            ts=resized_plus_polarization, time_crop=NORMAL_TIME_CROP, duration=TSEGMENT)
        highest_moved_axis_plus_polarization = move_ts_axis(
            ts=resized_plus_polarization, time_crop=HIGHEST_TIME_CROP, duration=TSEGMENT)
        resized_plus_polarization = " ".join(
            str(pl) for pl in resized_plus_polarization)
        lowest_moved_axis_plus_polarization = " ".join(
            str(pl) for pl in lowest_moved_axis_plus_polarization)
        normal_moved_axis_plus_polarization = " ".join(
            str(pl) for pl in normal_moved_axis_plus_polarization)
        highest_moved_axis_plus_polarization = " ".join(
            str(pl) for pl in highest_moved_axis_plus_polarization)
        file.write("%r\n" % resized_plus_polarization)
        file.write("%r\n" % lowest_moved_axis_plus_polarization)
        file.write("%r\n" % normal_moved_axis_plus_polarization)
        file.write("%r\n" % highest_moved_axis_plus_polarization)
        counter += 1
    file.close()



def noise_template_generator():
    h1_arr, l1_arr = GW_Data.read_files()
    directory = create_folder('Files', 'convolution.csv')
    # file = open(directory, 'at')
    templates = genfromtxt('%s/S18GW_CNN/Files/dataset.csv' %
                           DIRNAME, delimiter=' ')

    for i in range(len(h1_arr)):
        h1_strain = h1_arr[i]
        l1_strain = l1_arr[i]
        for template in templates:

            t = list(template)
            t = TimeSeries(t, DELTA_T, epoch=l1_strain._epoch)
            t = t/10

            h1 = h1_strain + t
            l1 = l1_strain + t


            pylab.subplot(4, 1, 1)
            pylab.plot(h1.sample_times, h1)
            pylab.ylabel('Signal H1')
            pylab.xlabel('Time (s)')

            h1 = numpy.nan_to_num(list(h1))
            l1 = numpy.nan_to_num(list(l1))

            h1 = TimeSeries(h1, DELTA_T, epoch=h1_strain._epoch)
            l1 = TimeSeries(l1, DELTA_T, epoch=l1_strain._epoch)

            pylab.subplot(4, 1, 2)
            pylab.plot(h1.sample_times, h1)
            pylab.ylabel('Signal H1')
            pylab.xlabel('Time (s)')

            h1 = h1.whiten(1,1, remove_corrupted=False)

            pylab.subplot(4, 1, 3)
            pylab.plot(h1.sample_times, h1)
            pylab.ylabel('Signal H1')
            pylab.xlabel('Time (s)')

            t, f, p = h1.qtransform(.001, logfsteps=100,
                                                  qrange=(8, 8),
                                                  frange=(20, 512))

            peak = abs(h1).numpy().argmax()
            time = h1.sample_times[peak]
            print time

            pylab.subplot(4, 1, 4)
            pylab.pcolormesh(t, f, p**0.5, vmin=1, vmax=6)
            pylab.yscale('log')
            pylab.xlabel('H1 Time (s)')
            pylab.ylabel('Frequency (Hz)')
            pylab.show()

            # l1 = l1.whiten(1,1, remove_corrupted=False)

            # pylab.subplot(2, 1, 1)
            # pylab.plot(l1.sample_times, l1)
            # pylab.ylabel('Signal L1')
            # pylab.xlabel('Time (s)')



            # t, f, p = l1.qtransform(.001, logfsteps=100,
            #                                       qrange=(8, 8),
            #                                       frange=(20, 512))


            # pylab.subplot(2, 1, 2)
            # pylab.pcolormesh(t, f, p**0.5, vmin=1, vmax=6)
            # pylab.yscale('log')
            # pylab.xlabel('L1 Time (s)')
            # pylab.ylabel('Frequency (Hz)')
            # pylab.show()


            # h1_f = " ".join(str(hs) for hs in h1)
            # l1_f = " ".join(str(ls) for ls in l1)

            # file.write("%r\n" % h1_f)
            # file.write("%r\n" % l1_f)

            # pylab.subplot(2, 1, 1)
            # pylab.plot(h1.sample_times, h1)
            # pylab.ylabel('Signal H1')
            # pylab.xlabel('Time (s)')

            # pylab.subplot(2, 1, 2)
            # pylab.plot(l1.sample_times, l1)
            # pylab.ylabel('Signal L1')
            # pylab.xlabel('Time (s)')

            # pylab.show()

            # pylab.close()
    # file.close()


# template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
noise_template_generator()
