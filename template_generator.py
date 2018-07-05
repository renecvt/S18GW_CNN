import csv
import os
from os.path import abspath, dirname

import numpy
import pylab
from pycbc.waveform import get_td_waveform

import Tools

from Tools.masses_generator import masses_generator
from Tools.Tools import get_bigger_value, cut_zero_values, resize_ts, move_ts_axis

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
        plus_polarization, _ = get_td_waveform(approximant = approximant, mass1 = mass[0], mass2 = mass[1], delta_t = DELTA_T, f_lower = F_LOWER)
        cut_plus_polarization = cut_zero_values(ts = plus_polarization)
        resized_plus_polarization = resize_ts(ts = cut_plus_polarization, time = TSEGMENT)
        lowest_moved_axis_plus_polarization = move_ts_axis(ts = resized_plus_polarization, time_crop = LOWEST_TIME_CROP, duration = TSEGMENT)
        normal_moved_axis_plus_polarization = move_ts_axis(ts = resized_plus_polarization, time_crop = NORMAL_TIME_CROP, duration = TSEGMENT)
        highest_moved_axis_plus_polarization = move_ts_axis(ts = resized_plus_polarization, time_crop = HIGHEST_TIME_CROP, duration = TSEGMENT)
        file.write("%r\n" % list(resized_plus_polarization))
        file.write("%r\n" % list(lowest_moved_axis_plus_polarization))
        file.write("%r\n" % list(normal_moved_axis_plus_polarization))
        file.write("%r\n" % list(highest_moved_axis_plus_polarization))
        counter += 1    
    file.close()


template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
