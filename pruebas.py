from pycbc.waveform import get_td_waveform
import pylab
from GW_Data import read_files
from pycbc.filter import resample_to_delta_t, highpass
import os
from os import listdir
import numpy

def createTemplate(ifo):
    for strain in ifo:
        strain = resample_to_delta_t(highpass(strain, 15.0), 1.0/2048)
        conditioned = strain.crop(2, 2)

        from pycbc.psd import interpolate, inverse_spectrum_truncation

        # We use 4 second samles of our time series in Welch method.
        psd = conditioned.psd(4)

        # Now that we have the psd we need to interpolate it to match our data
        # and then limit the filter length of 1 / PSD. After this, we can
        # directly use this PSD to filter the data in a controlled manner

        psd = interpolate(psd, conditioned.delta_f)

        # 1/PSD will now act as a filter with an effective length of 4 seconds
        # Since the data has been highpassed above 15 Hz, and will have low values
        # below this we need to informat the function to not include frequencies
        # below this frequency.
        psd = inverse_spectrum_truncation(psd, 4 * conditioned.sample_rate,
                                        low_frequency_cutoff=15)

        m = 20 # Solar masses
        hp, _ = get_td_waveform(approximant="SEOBNRv4_opt",
                            mass1=m,
                            mass2=m,
                            delta_t=conditioned.delta_t,
                            f_lower=20)

        # We will resize the vector to match our data
        hp.resize(len(conditioned))

        template = hp.cyclic_time_shift(hp.start_time)


        from pycbc.filter import matched_filter

        snr = matched_filter(template, conditioned,
                            psd=psd, low_frequency_cutoff=20)

        # Remove time corrupted by the template filter and the psd filter
        # We remove 4 seonds at the beginning and end for the PSD filtering
        # And we remove 4 additional seconds at the beginning to account for
        # the template length (this is somewhat generous for
        # so short a template). A longer signal such as from a BNS, would
        # require much more padding at the beginning of the vector.
        snr = snr.crop(4 + 4, 4)

        peak = abs(snr).numpy().argmax()
        snrp = snr[peak]

        if numpy.isnan(snrp):
            continue

        time = snr.sample_times[peak]

        print("We found a signal at {}s with SNR {}".format(time,
                                                            abs(snrp)))

        from pycbc.filter import sigma

        # Shift the template to the peak time
        dt = time - conditioned.start_time
        aligned = template.cyclic_time_shift(dt)
        aligned /= sigma(aligned, psd=psd, low_frequency_cutoff=20.0)

        # Scale the template amplitude and phase to the peak value
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
        # pylab.savefig('{}_{}.png'.format('ej', '2'))
        pylab.show()
        pylab.close()



mypath = '%s/no_inj_data/' % os.getcwd()
files = [f for f in listdir(mypath) if f.endswith(".gwf")]

h1, l1 = read_files(files, mypath)

print 'Paso 1 -- Terminado '
numpy.save('h1', h1)
print 'Paso 2 -- Terminado '
numpy.save('l1', l1)
print 'Paso 3 -- Terminado '

# from pycbc.types import TimeSeries
# h1 = TimeSeries(numpy.load('h1.npy'))
# l1 = TimeSeries(numpy.load('l1.npy'))

# createTemplate(h1)
# createTemplate(l1)