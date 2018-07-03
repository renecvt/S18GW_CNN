import os
import numpy
import csv
import Tools
from pycbc.waveform import get_td_waveform
from masses_generator import masses_generator

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
    counter = 1
    directory = create_folder('txts', 'dataset.txt')
    csv_directory = create_folder('csvs', 'info.csv')
    file = open(directory, 'at')
    csv_file = open(csv_directory, 'w')
    field_names = ['mass_one', 'mass_two', 'total_mass', 'duration', 'duration_one', 'duration_two']
    csv_writer = csv.DictWriter(csv_file, fieldnames = field_names)
    for mass in masses:
        info = {}
        plus_polarization, _ = get_td_waveform(approximant = approximant, mass1 = mass[0], mass2 = mass[1], delta_t = 1.0 / 4096, f_lower = 20)
        plus_polarization.resize(4096)
        duration = plus_polarization.duration
        total_mass = mass[0] + mass[1]
        index = Tools.getBiggerValue(list(plus_polarization))
        first_part = plus_polarization[:index]
        second_part = plus_polarization[index:]
        plus_polarization = " ".join(str(pl) for pl in plus_polarization)
        print('Writing line number %s' % counter)
        file.write("%r\n" % plus_polarization)
        counter += 1
        info['duration'] = duration
        info['total_mass'] = total_mass
        info['mass_one'] = mass[0]
        info['mass_two'] = mass[1]
        info['duration_one'] = first_part.duration
        info['duration_two'] = second_part.duration
        csv_writer.writerow(info)
        data.append(info)
    file.close()
    csv_file.close()


template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)