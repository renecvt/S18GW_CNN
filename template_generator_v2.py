import os
import numpy
from Tools.Tools import getBiggerValue, cutZeroValues
import csv
import Tools
from pycbc.waveform import get_td_waveform
import Tools.Plot as plt 
from Tools.masses_generator import masses_generator
from os.path import dirname, abspath
import pylab
DIRNAME = dirname(dirname(abspath(__file__)))
DEFAULT_APPROXIMANT = 'SEOBNRv3_opt'
MASSES = masses_generator()
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
    #csv_directory = create_folder('Files', 'dataset_one_second.csv')
    #counter = 1
    #csv_file = open(csv_directory, 'w')
    #csv_writer = csv.DictWriter(csv_file, fieldnames = field_names)
    for mass in masses:
        
        plus_polarization, _ = get_td_waveform(approximant = approximant, mass1 = mass[0], mass2 = mass[1], delta_t = 1.0 / 4096, f_lower = 20)
        pylab.plot(plus_polarization)
        pylab.show()
        duration = plus_polarization.duration
        plus_polarization = cutZeroValues(list(plus_polarization))
        pylab.plot(plus_polarization)
        pylab.show()
        
        #plus_polarization = " ".join(str(pl) for pl in plus_polarization)
        #print('Writing line number %s' % counter)
        #file.write("%r\n" % plus_polarization)
        #counter += 1
        #csv_writer.writerow(info)
        #data.append(info)
    #file.close()
    #csv_file.close()

template_generator(approximant = DEFAULT_APPROXIMANT, masses = [(10,10)])