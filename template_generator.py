import csv
import os
from os.path import abspath, dirname

import numpy
import pylab
from pycbc.filter import highpass, resample_to_delta_t
from pycbc.waveform import get_td_waveform

import GW_Data
import Tools
from Tools.masses_generator import masses_generator
from Tools.Tools import (cut_zero_values, get_bigger_value, move_ts_axis,
                         resize_ts)

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


from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.types import TimeSeries
from os.path import abspath, dirname
from numpy import genfromtxt
from pycbc.filter import matched_filter


def noise_template_generator(approximant, masses):
    DIRNAME = dirname(dirname(abspath(__file__)))
    h1, l1 = GW_Data.read_files()
    for i in range(len(h1)):
        h1_strain = h1[i]
        l1_strain = l1[i]
        h1_strain = resample_to_delta_t(highpass(h1_strain, 15.0), 1.0/4096)
        l1_strain = resample_to_delta_t(highpass(l1_strain, 15.0), 1.0/4096)
        templates = genfromtxt('%s/S18GW_CNN/Files/dataset.csv' % DIRNAME, delimiter=' ')
        for template in templates:
            t = list(template)
            t = TimeSeries(t, DELTA_T)
            print len(h1_strain)
            print len(t)
            t.resize(len(h1_strain))
            print len(t)

            h1_psd = h1_strain.psd(1)
            l1_psd = l1_strain.psd(1)
            h1_psd = interpolate(h1_psd, h1_strain.delta_f)
            l1_psd = interpolate(l1_psd, l1_strain.delta_f)
            h1_psd = inverse_spectrum_truncation(h1_psd, 1 * h1_strain.sample_rate,
                                                 low_frequency_cutoff=15)
            l1_psd = inverse_spectrum_truncation(l1_psd, 1 * l1_strain.sample_rate,
                                                 low_frequency_cutoff=15)
            h1_snr = matched_filter(t, h1_strain,
                                    psd=h1_psd, low_frequency_cutoff=20)
            l1_snr = matched_filter(t, l1_strain,
                                    psd=l1_psd, low_frequency_cutoff=20)
            pylab.figure(figsize=[10, 4])
            pylab.plot(h1_snr.sample_times, abs(h1_snr))
            pylab.ylabel('Signal-to-noise H1')
            pylab.xlabel('Time (s)')
            pylab.show()

            pylab.figure(figsize=[10, 4])
            pylab.plot(l1_snr.sample_times, abs(l1_snr))
            pylab.ylabel('Signal-to-noise L1')
            pylab.xlabel('Time (s)')
            pylab.show()

            pylab.close()



# template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
noise_template_generator(approximant=DEFAULT_APPROXIMANT, masses=MASSES)
