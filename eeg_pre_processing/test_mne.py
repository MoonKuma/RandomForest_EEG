#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_mne.py
# @Author: MoonKuma
# @Date  : 2019/2/13
# @Desc  : test those funcs in mne
# See official API documents here: http://martinos.org/mne/stable/index.html

import mne
from mne.preprocessing import ICA
from mne.preprocessing import create_eog_epochs, create_ecg_epochs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize



raw_file1 = 'data_sample/eeg_raw_data/example/sub2/tb1.cnt'
raw_file2 = 'data_sample/eeg_raw_data/example/sub2/tb2.cnt'

# I/O - read Neuroscan raw data (.cnt)
raw1 = mne.io.read_raw_cnt(input_fname=raw_file1, montage=None, preload=True, data_format='int32', eog='header')
raw2 = mne.io.read_raw_cnt(input_fname=raw_file2, montage=None, preload=True, data_format='int32', eog='header')
raw_data_list = [raw1, raw2]

# concatenate raw data
raw = mne.concatenate_raws(raw_data_list, preload=None, events_list=None, verbose=None)

# down-sampling to 100Hz
raw.resample(100, npad="auto")

# band filters (1Hz - 40Hz, band filter)
'''
Here, if you try to carry out a filter with frequency larger than the Nyquist boundary, the method will return a ValueError
ValueError: lowpass frequency 50.0 must be less than Nyquist (50.0)
See detail of Nyquist rate : https://en.wikipedia.org/wiki/Nyquist_rate
The basic idea is that to capture a 50Hz signal, at least 100 Hz sampling rate is required.
'''
raw.filter(1, 40., fir_design='firwin')

# using ICA to remove those component considered as triggered by the eog (eye movement and so on)
'''
Human intervened ICA processing is usually more powerful, yet time consuming hence we just adjust the automatic steps. XD
At least filtering(1 Hz above)/blaming bad channels should be carried out before ICA 
'''
picks_eeg = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')
ica = ICA(n_components=25, random_state=1)  # using default method 'fastica'
reject = dict(eeg=50.)
ica.fit(raw, picks=picks_eeg, reject=reject)
# # class ica offers many way of plotting
# ica.plot_components()
# ica.plot_properties(raw, picks=0)
eog_average = create_eog_epochs(raw, reject=reject, picks=picks_eeg).average()
eog_epochs = create_eog_epochs(raw, reject=reject)  # get single EOG trials
eog_inds, scores = ica.find_bads_eog(eog_epochs)  # find via correlation
ica.exclude.extend(eog_inds)
ica.plot_scores(scores, exclude=eog_inds)  # look at r scores of components
ica.plot_sources(eog_average, exclude=eog_inds)  # look at source time course
ica.plot_properties(eog_epochs, picks=eog_inds, psd_args={'fmax': 35.},
                    image_args={'sigma': 1.})  # the component we detected through ICA
raw_copy = raw.copy()
ica.apply(raw_copy)


# epoch data (and reject bad epochs)
reject = dict(eeg=10.)
events = mne.find_events(raw_copy, stim_channel='STI 014')
event_id = {"fear": 11, "neutral": 19}
color = {11: 'green', 19: 'red'}  # this for plotting events
mne.viz.plot_events(events, raw_copy.info['sfreq'], raw_copy.first_samp, color=color,
                    event_id=event_id)
tmin = -1  # -1000ms before
tmax = 1  # 1000ms after
baseline = (None, 0)  # means from the first instant to t = 0
# if trying to plot, montage should be corrected before
montage = mne.channels.read_montage('standard_1020')
picks_eeg = mne.pick_types(raw_copy.info, meg=False, eeg=True, eog=False, stim=False, exclude=['VEOG','HEOG', 'CP1', 'FC4'])
# CP1/FC4 is bad here for unknown reason, yet we won't be able to do this exculsion when computing large amount of data
epochs = mne.Epochs(raw_copy, events, event_id, tmin, tmax, proj=True, picks=picks_eeg, baseline=baseline,
                    reject=reject, reject_by_annotation=True)
# del raw_copy  # here we can release raw data for saving memory
epochs.set_montage(montage=montage)
epoch_avg = epochs.average()
title = 'EEG Average reference'
epoch_avg.plot(titles=dict(eeg=title), time_unit='s')
epoch_avg.plot_topomap(times=[0.13], size=3., title=title, time_unit='s')  # set show_names=True for checking channels
# carry out average for different epochs and plot them
all_evokeds = dict((cond, epochs[cond].average()) for cond in event_id)
joint_kwargs = dict(ts_args=dict(time_unit='s'),
                    topomap_args=dict(time_unit='s'))
for cond in all_evokeds:
    all_evokeds[cond].plot_joint(title=cond, **joint_kwargs)
# save epoch and epoch_avg()
epochs.save('data_sample/eeg_raw_data/example/test-epo.fif')  # epoch data should be stored with -epo.fif
evoke_list = list()
for cond in all_evokeds:
    evoke_list.append(all_evokeds[cond])
mne.write_evokeds('data_sample/eeg_raw_data/example/test-ave.fif', evoke_list) # evoked data stored with -ave.fif
# clean ram here
# read in data
epochs = mne.read_epochs('data_sample/eeg_raw_data/example/test-epo.fif')
evoked_data = mne.read_evokeds('data_sample/eeg_raw_data/example/test-ave.fif')
# using epoch data to continue time-frequency analyze
epochs.plot_psd(fmin=2., fmax=40.) # avg frequency and power
epochs.plot_psd_topomap(normalize=True) # standard delta - gamma frequency-power topo-graph
# Morlet (Not knowing whats going on, anyway...)
freqs = np.logspace(*np.log10([1, 35]), num=8)
n_cycles = freqs / 2.  # different number of cycle per frequency
power = mne.time_frequency.tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=True, return_itc=False, decim=3, n_jobs=1)
'''
ValueError: At least one of the wavelets is longer than the signal. Use a longer signal or shorter wavelets.
Here to ensure the morlet work, we need each epoch data be long enough (70 points in the first time no longer suit)
Lets try the original sampling rate (250Hz) and cut out a window of two seconds
'''
power.plot_topo(baseline=(-1, 0), mode='logratio', title='Average power')
power.plot([17], baseline=(-1, 0), mode='logratio', title=power.ch_names[17]) # channel 17 is fcz
power.plot_joint(baseline=(-1, 0), mode='mean', tmin=-.5, tmax=2,
                 timefreqs=[(0, 10), (0.7, 8)])
#power works as a 3-D nparray data
# mne.time_frequency.read_tfrs(fname, condition=None)
# mne.time_frequency.write_tfrs(fname, tfr, overwrite=False)

# read behavior data
file_path = 'data_sample/eeg_raw_data/subject_data/Behavior_Original/behavior_orig.txt'
txt_data = pd.read_table(file_path)

# read evoked data
file_path = 'data_sample/formal_dataset/sub_evoked_data/sub56-ave.fif'
evokes = mne.read_evokeds(file_path)  # caution this data is not baseline corrected
index = evokes[0].ch_names
evoke = evokes[0]
comments = evoke.comment
evoke.apply_baseline(baseline=(None, 0))
get_peak1 = evoke.get_peak(ch_type = 'eeg', tmin=0.05, tmax=0.15)
peak_time1 = get_peak1[1]
evt_copy = evoke.copy()
slice_1 = evt_copy.crop(tmin=peak_time1-0.01, tmax=peak_time1+0.01) # average across 5 plots (0.020s * 250 /s)
d_tmp = slice_1.data # this return a np.ndarray
mean = np.mean(d_tmp, axis=1).reshape(d_tmp.shape[0], 1)
norm_mean = normalize(mean,axis=0).T  # normalize and transform
# save this into a data_frame
index_list = list()
for channel in index:
    col = comments + '_peak1_erp'
    index_list.append(col)


# read tfr data
file_path = 'data_sample/formal_dataset/sub_power_data/sub56-tfr.h5'
trfs222 = mne.time_frequency.read_tfrs(file_path)


