import os
import numpy
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
        os.makedirs(folder_container)
        new_file = open(complete_directory, 'w+')
        new_file.close()
    return complete_directory

def template_generator(approximant, masses):
    counter = 1
    directory = create_folder('txts', 'dataset.txt')
    file = open(directory, 'at')
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
        info['duration1'] = first_part.duration
        info['duration2'] = second_part.duration
        data.append(info)
        plus_polarization = numpy.asarray(plus_polarization)
        plus_polarization = list(plus_polarization)
        plus_polarization = " ".join(str(pl) for pl in plus_polarization)
        print('Writing line number %s' % counter)
        file.write("%r\n" % plus_polarization)
        counter += 1
    file.close()


template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)