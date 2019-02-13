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
tmin = -0.2  # 200ms before
tmax = 0.5  # 500ms after
baseline = (None, 0)  # means from the first instant to t = 0
# if trying to plot, montage should be corrected before
montage = mne.channels.read_montage('standard_1020')
picks_eeg = mne.pick_types(raw_copy.info, meg=False, eeg=True, eog=False, stim=False, exclude=['VEOG','HEOG', 'CP1', 'FC4']) # CP1/FC4 is bad here
epochs = mne.Epochs(raw_copy, events, event_id, tmin, tmax, proj=True, picks=picks_eeg, baseline=baseline,
                    reject=reject, reject_by_annotation=True)
# del raw_copy  # here we can release raw data for saving memory
epochs.set_montage(montage=montage)
epoch_avg = epochs.average()
title = 'EEG Average reference'
epoch_avg.plot(titles=dict(eeg=title), time_unit='s')
epoch_avg.plot_topomap(times=[0.13], size=3., title=title, time_unit='s')  # set show_names=True for checking channels
all_evokeds = dict((cond, epochs[cond].average()) for cond in event_id)
joint_kwargs = dict(ts_args=dict(time_unit='s'),
                    topomap_args=dict(time_unit='s'))
for cond in all_evokeds:
    all_evokeds[cond].plot_joint(title=cond, **joint_kwargs)












