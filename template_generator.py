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
    DIRNAME = dirname(dirname(abspath(__file__)))
    h1, l1 = GW_Data.read_files()
    directory = create_folder('Files', 'convolution.csv')
    file = open(directory, 'at')
    for i in range(len(h1)):
        h1_strain = h1[i]
        l1_strain = l1[i]
        templates = genfromtxt('%s/S18GW_CNN/Files/dataset.csv' % DIRNAME, delimiter=' ')
        for template in templates:

            h1_strain = h1_strain.time_slice(h1_strain.start_time, h1_strain.start_time + 1)
            l1_strain = l1_strain.time_slice(l1_strain.start_time, l1_strain.start_time + 1)
            
            t = list(template)
            t = TimeSeries(t, DELTA_T, epoch=h1_strain._epoch)
            t = t/10

            h1 = h1_strain + t
            l1 = l1_strain + t

            h1 = " ".join(str(hs) for hs in h1)
            l1 = " ".join(str(ls) for ls in l1)
            
            file.write("%r\n" % h1)
            file.write("%r\n" % l1)
        file.close()



# template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
noise_template_generator()
