from pycbc.filter import resample_to_delta_t, highpass, sigma, matched_filter
from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.waveform import get_td_waveform
from GW_Data import read_files
from os import listdir
import os
import pylab
import numpy

# Reading the data corresponding to both L1 (Livingston) and H1 (Hanford) interferometers
mypath = '%s/no_inj_data/' % os.getcwd()
files = [f for f in listdir(mypath) if f.endswith(".gwf")]

h1, _ = read_files(files, mypath)

# Array defining random masses
masses = [20]

# Getting the fd approximants
# approximants = get_approximants('fd', 3)
approximant = 'SEOBNRv4_opt'

def template_generator(ts_list, approximant, masses, save):
    for ts in ts_list:
       ts = resample_to_delta_t(highpass(ts, 15.0), 1.0/2048)
       conditioned = ts.crop(2, 2) 
       psd = conditioned.psd(4)
       psd = interpolate(psd, conditioned.delta_f)
       psd = inverse_spectrum_truncation(psd, 4 * conditioned.sample_rate, low_frequency_cutoff=15)
       for mass in masses:
           plus_polarization, cross_polarization = get_td_waveform(approximant="SEOBNRv4_opt", mass1=mass, mass2=mass, delta_t=conditioned.delta_t, f_lower=20)
           plus_polarization.resize(len(conditioned))
           template = plus_polarization.cyclic_time_shift(plus_polarization.start_time)
           snr = matched_filter(template, conditioned, psd=psd, low_frequency_cutoff=20)
           snr = snr.crop(4 + 4, 4)
           peak = abs(snr).numpy().argmax()
           snrp = snr[peak]
           if numpy.isnan(snrp) == False:
               time = snr.sample_times[peak]
               print("We found a signal at {}s with SNR {}".format(time, abs(snrp)))
               dt = time - conditioned.start_time
               aligned = template.cyclic_time_shift(dt)
               aligned /= sigma(aligned, psd=psd, low_frequency_cutoff=20.0)
               aligned = (aligned.to_frequencyseries() * snrp).to_timeseries()
               aligned.start_time = conditioned.start_time
               white_data = (conditioned.to_frequencyseries() / psd**0.5).to_timeseries()
               tapered = aligned.highpass_fir(30, 512, remove_corrupted=False)
               white_template = (tapered.to_frequencyseries() / psd**0.5).to_timeseries()
               white_data = white_data.highpass_fir(30., 512).lowpass_fir(300, 512)
               white_template = white_template.highpass_fir(30, 512).lowpass_fir(300, 512)
               white_data = white_data.time_slice(time-.2, time+.1)
               white_template = white_template.time_slice(time-.2, time+.1)
               pylab.figure(figsize=[15, 3])
               pylab.plot(white_data.sample_times, white_data, label="Data")
               pylab.plot(white_template.sample_times, white_template, label="Template")
               pylab.legend()
               if save == True:
                   save_path = '%s/saved_templates/' % os.getcwd()
                   file_name = '{}_{}_{}_{}.png'.format(approximant, mass, snrp, ts.start_time)
                   pylab.savefig('{}{}'.format(save_path, file_name))
               else:
                   pylab.show()
               pylab.close()

template_generator(ts_list = h1, approximant = approximant, masses = masses, save = True)
