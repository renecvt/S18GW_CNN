# coding=utf-8
import csv
import os
from os.path import abspath, dirname

import numpy
import pylab
from numpy import genfromtxt
from pycbc.filter import highpass, resample_to_delta_t, sigma
from pycbc.types import TimeSeries
from pycbc.waveform import get_td_waveform

import GW_Data
import Tools
from Tools.masses_generator import masses_generator
from Tools.Tools import (cut_zero_values, get_bigger_value, move_ts_axis,
                         resize_ts)

DIRNAME = dirname(dirname(abspath(__file__)))
DEFAULT_APPROXIMANT = 'SEOBNRv3_opt'
MASSES = masses_generator()
TSEGMENT = 1.4
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
    # directory = create_folder('Files', 'convolution.csv')
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

            from pycbc.filter import highpass_fir, lowpass_fir

            pylab.subplot(3, 1, 1)
            pylab.plot(t.sample_times, t)

            t = highpass_fir(t, 40, 40)
            pylab.subplot(3, 1, 2)
            pylab.plot(t.sample_times, t)

            t = lowpass_fir(t, 40, 40)
            pylab.subplot(3, 1, 3)
            pylab.plot(t.sample_times, t)

            pylab.show()

            h1 = h1_strain + t
            l1 = l1_strain + t

            for i, ifo in enumerate([h1, l1]):
                strain = h1_strain if i == 0 else l1_strain
                # ifo_whiten = ifo.whiten(1, 1, remove_corrupted=False)
                p = 1 if i == 0 else 2
                # label = 'H1' if i == 0 else 'L1'

                pylab.subplot(5, 2, p)
                pylab.plot(strain.sample_times, strain)
                pylab.gca().axes.get_xaxis().set_visible(False)
                pylab.gca().axes.get_yaxis().set_visible(False)
                # pylab.ylabel('Signal %s' % label)
                # pylab.xlabel('Time (s)')

                p += 2
                pylab.subplot(5, 2, p)
                pylab.plot(t.sample_times, t)
                pylab.gca().axes.get_xaxis().set_visible(False)
                pylab.gca().axes.get_yaxis().set_visible(False)

                p += 2
                pylab.subplot(5, 2, p)
                pylab.plot(ifo.sample_times, ifo)
                pylab.gca().axes.get_xaxis().set_visible(False)
                pylab.gca().axes.get_yaxis().set_visible(False)

                times, f, qplane = ifo.qtransform(.001, logfsteps=100,
                                                  qrange=(8, 8),
                                                  frange=(20, 512))

                p += 2
                pylab.subplot(5, 2, p)
                pylab.pcolormesh(times, f, qplane**0.5, vmin=1, vmax=6)
                pylab.yscale('log')
                pylab.gca().axes.get_xaxis().set_visible(False)
                pylab.gca().axes.get_yaxis().set_visible(False)
                # pylab.xlabel('Time (s)')
                # pylab.ylabel('Frequency (Hz)')

            pylab.show()

            # h1_f = " ".join(str(hs) for hs in h1)
            # l1_f = " ".join(str(ls) for ls in l1)

            # file.write("%r\n" % h1_f)
            # file.write("%r\n" % l1_f)

    # file.close()


# template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
noise_template_generator()


# Enventanado
# Diferentes distancias
# Congreso Nacional de Físcia
# Imágenes 16 x 32
# Conjunto de datos de entrenamiento, conjunto de validación
