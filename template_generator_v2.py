import os
import numpy
from pycbc.waveform import get_td_waveform

default_approximant = 'SEOBNRv3_opt'
masses = [36]

def template_generator(approximant, masses):
    for mass in masses:
        plus_polarization, _ = get_td_waveform(approximant=approximant, mass1=mass, mass2=mass - 5, delta_t=1.0 / 4096, f_lower=20)
        save_path = '%s/txts/' % os.getcwd()
        file_name = '{}_{}.txt'.format(approximant, mass)
        numpy.savetxt('{}{}'.format(save_path, file_name), plus_polarization, newline=" ")


template_generator(approximant = default_approximant, masses = masses)
