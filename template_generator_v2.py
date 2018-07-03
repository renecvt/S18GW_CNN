import os
import numpy
import Tools
from pycbc.waveform import get_td_waveform
from masses_generator import masses_generator

DEFAULT_APPROXIMANT = 'SEOBNRv3_opt'
MASSES = masses_generator()
data = []

def template_generator(approximant, masses):
    counter = 1
    file_path = '%s/txts/dataset.txt' % os.getcwd()
    file = open(file_path, 'at')
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


    file.close()


template_generator(approximant = DEFAULT_APPROXIMANT, masses = MASSES)