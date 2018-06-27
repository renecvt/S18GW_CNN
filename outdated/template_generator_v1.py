from pycbc.filter import matched_filter, sigma, resample_to_delta_t, highpass
from pycbc.waveform import get_td_waveform, td_approximants
from pycbc.catalog import Merger, Catalog
from pycbc.psd import interpolate, inverse_spectrum_truncation
import pylab
import numpy
import pycbc.frame

masses = [5, 10, 30, 100]
files = ["PyCBC_T2_0.gwf"]

def generate_and_save_signals(files, masses):
    counter = 0
    for file in files:
        ts = pycbc.frame.read_frame(file, 'H1:TEST-STRAIN', 0, 128)
        psd = ts.psd(4)
        psd = interpolate(psd, ts.delta_f)
        psd = inverse_spectrum_truncation(psd, 4 * ts.sample_rate, low_frequency_cutoff = 15)
        for mass in masses:
            counter += 1
            try:
                plus_polarization, cross_polarization = get_td_waveform(approximant = 'SEOBNRv4_opt', mass1 = mass, mass2 = mass, delta_t = ts.delta_t, f_lower = 20)
            except:
                print('error')
                continue
            cross_polarization.resize(len(ts))
            template = cross_polarization.cyclic_time_shift(plus_polarization.start_time)
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
            white_data = white_data.highpass_fir(30., 512).lowpass_fir(300, 512)
            white_template = white_template.highpass_fir(30, 512).lowpass_fir(300, 512)
            white_data = white_data.time_slice(white_data.start_time, white_data.end_time)
            white_template = white_template.time_slice(white_template.start_time, white_template.end_time)
            pylab.figure(figsize = [15, 3])
            pylab.plot(white_data.sample_times, white_data, label = "Data")
            pylab.plot(white_template.sample_times, white_template, label = "Template")
            pylab.legend()
            # pylab.savefig('{}_{}_{}.png'.format('SEOBNRv4_opt', counter, mass), dpi = 'figure')
            pylab.show()
            # subtracted = ts - aligned
            # for data, title in [(ts, 'Original H1 Data'), (subtracted, 'Signal Subtracted from H1 Data')]:
            #     t, f, p = data.whiten(4, 4).qtransform(.001, logfsteps=100, qrange=(8, 8), frange=(20, 512))
            #     pylab.figure(figsize=[15, 3])
            #     pylab.title(title)
            #     pylab.pcolormesh(t, f, p ** 0.5, vmin = 1, vmax = 6)
            #     pylab.yscale('log')
            #     pylab.xlabel('Time (s)')
            #     pylab.ylabel('Frequency (Hz)')
            #     pylab.xlim((ts.start_time + 1) - 2, (ts.end_time - 1) + 1)
            #     pylab.savefig('{}_{}_{}_SUBSTRACTED.png'.format('SEOBNRv4_opt', counter, mass), dpi='figure')
            #     pylab.close()