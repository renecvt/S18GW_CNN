
import pycbc
from pycbc.waveform import get_td_waveform
import numpy as np



plus_polarization, _ = get_td_waveform(approximant="SEOBNRv4_opt", mass1=36, mass2=29, delta_t=1/4096, f_lower=20)
template = plus_polarization
np.savetxt('template.txt', template)



