from pycbc.filter import matched_filter, sigma, resample_to_delta_t, highpass
from pycbc.waveform import get_td_waveform, td_approximants
from pycbc.catalog import Merger, Catalog
from pycbc.psd import interpolate, inverse_spectrum_truncation
import pycbc.frame
import pylab
import numpy
from GW_Data import read_files
from approximant import get_approximants

# Reading the data corresponding to both L1 (Livingston) and H1 (Hanford) interferometers
h1, l1 = read_files()

# Array defining random masses
masses = [5, 10, 30, 100]

# Getting the fd approximants
approximants = get_approximants('fd', 3)

def template_generator(ts_list, masses, approximants, save):
    for approximant in approximants:
        for ts in ts_list:
            if numpy.isnan(ts[0]) == False:
                psd = ts.psd(ts.duration)
                psd = interpolate(psd, ts.delta_f)
                psd = inverse_spectrum_truncation(psd, 4 * ts.sample_rate, low_frequency_cutoff = 15)
                for mass in masses:
                    try:
                        plus_polarization, cross_polarization = get_td_waveform(approximant = approximant, mass1 = mass, mass2 = mass, delta_t = ts.delta_t, f_lower = 150)
                    except:
                        continue
                    plus_polarization.resize(len(ts))
                    template = plus_polarization.cyclic_time_shift(plus_polarization.start_time)
                    snr = matched_filter(template, ts, psd = psd, low_frequency_cutoff = 20)
                    snr = snr.crop(8, 4)
                    peak = abs(snr).numpy().argmax()
                    snrp = snr[peak]
                    time = snr.sample_times[peak]
                    dt = time - (ts.start_time + 1)
                    aligned = template.cyclic_time_shift(dt)
                    aligned /= sigma(aligned, psd=psd, low_frequency_cutoff=20.0)
                    aligned = (aligned.to_frequencyseries() * snrp).to_timeseries()
                    aligned.start_time = (ts.start_time + 1)
                    white_data = (ts.to_frequencyseries() / psd ** 0.5).to_timeseries()
                    tapered = aligned.highpass_fir(30, 512, remove_corrupted = False)
                    white_template = (tapered.to_frequencyseries() / psd ** 0.5).to_timeseries()
                    white_data = white_data.highpass_fir(30, 512).lowpass_fir(300, 512)
                    white_template = white_template.highpass_fir(30, 512).lowpass_fir(300, 512)
                    white_data = white_data.time_slice(white_data.start_time, white_data.end_time)
                    white_template = white_template.time_slice(white_template.start_time, white_template.end_time)
                    pylab.figure(figsize = [15, 3])
                    pylab.plot(white_data.sample_times, white_data)
                    pylab.plot(white_template.sample_times, white_template)
                    if save == True:
                        pylab.savefig('{}_{}.png'.format(approximant, mass))
                    else:
                        pylab.show()
                    pylab.close()

template_generator(ts_list = h1, masses = masses, approximants = approximants, save = False)