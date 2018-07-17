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
                         resize_ts, windowing)

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
        window= windowing(cut_plus_polarization)
        tem_plus_wind= cut_plus_polarization * window
        resized_plus_polarization = resize_ts(
            ts=tem_plus_wind, time=TSEGMENT)
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
    pylab.close()
def noise_template_generator():
    h1_arr, l1_arr = GW_Data.read_files()
    templates = genfromtxt('%s/S18GW_CNN/Files/dataset.csv' %
                           DIRNAME, delimiter=' ')
    flag = 0
    for i in range(len(h1_arr)):
        h1_strain = h1_arr[i]
        l1_strain = l1_arr[i]
        if flag == 179:
            break
        for n, template in enumerate(templates):
            t = list(template)
            t[0] = 0
            t[len(t) - 1] = 0
            t = TimeSeries(t, DELTA_T, epoch=l1_strain._epoch)
            t = t/10

            h1 = h1_strain + t
            l1 = l1_strain + t

            for i, ifo in enumerate([h1, l1]):
                strain = 'H1' if i == 0 else 'L1'
                times, f, qplane = ifo.qtransform(.001, logfsteps=100,
                                                  qrange=(8, 8),
                                                  frange=(20, 512),
                                                  mismatch=0.4)

                pylab.figure(figsize=(33, 17), frameon=False)
                ax = pylab.figure().add_axes([0, 0, 1, 1])
                ax.axis('off')
                pylab.pcolormesh(times, f, qplane**0.5, vmin=1, vmax=6)
                pylab.yscale('log')
                xlim = pylab.xlim()
                pylab.xlim(xmin=xlim[0]+0.07, xmax=xlim[1]-0.07)
                pylab.gca().axes.get_xaxis().set_visible(False)
                pylab.gca().axes.get_yaxis().set_visible(False)
                directory = '{}/S18GW_CNN/Files/qtransform/{}'.format(DIRNAME, n)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                pylab.savefig('{}/S18GW_CNN/Files/qtransform/{}/Strain_{}_Template_{}.png'.format(DIRNAME, n, strain, n), transparent=True)
                pylab.close()
                flag = n

    # file.close()

def noise_generator():
    h1_arr, l1_arr = GW_Data.read_files()
    flag = 0
    for index in range(len(h1_arr)):
        h1_noise = h1_arr[index]
        l1_noise = l1_arr[index]
        if flag == 179:
            break
        for i, ifo in enumerate([h1_noise, l1_noise]):
            strain = 'H1_noise' if i == 0 else 'L1_noise'
            times, f, qplane = ifo.qtransform(.001, logfsteps=100,qrange=(8, 8),frange=(20, 512),mismatch=0.4)
            pylab.figure(figsize=(33, 17), frameon=False)
            ax = pylab.figure().add_axes([0, 0, 1, 1])
            ax.axis('off')
            pylab.pcolormesh(times, f, qplane**0.5, vmin=1, vmax=6)
            pylab.yscale('log')
            xlim = pylab.xlim()
            pylab.xlim(xmin=xlim[0]+0.07, xmax=xlim[1]-0.07)
            pylab.gca().axes.get_xaxis().set_visible(False)
            pylab.gca().axes.get_yaxis().set_visible(False)
            directory = '{}/S18GW_CNN/Files/noise/{}'.format(DIRNAME, index)
            if not os.path.exists(directory):
                os.makedirs(directory)
            pylab.savefig('{}/S18GW_CNN/Files/noise/{}/Strain_{}_{}.png'.format(DIRNAME, index, strain, index), transparent=True)
            pylab.close()




#noise_generator()
# template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)
noise_template_generator()


# Enventanado
# Diferentes distancias
# Congreso Nacional de Físcia
# Imágenes 16 x 32
# Conjunto de datos de entrenamiento, conjunto de validación
