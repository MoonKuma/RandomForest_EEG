#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : methods.py
# @Author: MoonKuma
# @Date  : 2019/2/16
# @Desc  : mutual methods

import os
import mne
from mne.preprocessing import ICA
from mne.preprocessing import create_eog_epochs, create_ecg_epochs

def get_file_dict(data_path, patten):
    # data file path like : data_sample/eeg_raw_data/ERP_Original/sub2/tb1.cnt
    # this method scan all data inside data_path(data_sample/eeg_raw_data/ERP_Original/) and start with patten('tb')
    # and return a dict like {sub2 : data_sample/eeg_raw_data/ERP_Original/sub2/tb1.cnt}
    raw_data_dict = dict()
    dir_list = os.listdir(data_path)
    for dir_name in dir_list:
        raw_data_dict[dir_name] = list()
        inner_file = os.path.join(data_path, dir_name)
        raw_names = os.listdir(inner_file)
        for raw_name in raw_names:
            if raw_name.startswith(patten):
                raw_data_dict[dir_name].append(os.path.abspath(os.path.join(inner_file, raw_name)))

def concat_raw_cnt(raw_file_list, preload=True, data_format='int32', eog='header'):
    # open and transfer a list of raw data file name into one raw data
    # has to be .cnt data
    # input : raw_file_list as the list of raw cnt file names
    # return : raw (mne.raw object as a concatenation)
    raw = mne.io.read_raw_cnt(raw_file_list[0], preload=preload, data_format=data_format, eog=eog)
    for i in range(1,len(raw_file_list)):
        raw_tmp = mne.io.read_raw_cnt(raw_file_list[i], preload=preload, data_format=data_format, eog=eog)
        mne.concatenate_raws([raw, raw_tmp])
    return raw

def perform_ICA(raw, eeg_reject=50.):
    picks_eeg = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False, exclude='bads')
    ica = ICA(n_components=25, random_state=1)  # using default method 'fastica'
    reject = dict(eeg=eeg_reject)
    ica.fit(raw, picks=picks_eeg, reject=reject)
    eog_average = create_eog_epochs(raw, reject=reject, picks=picks_eeg).average()
    eog_epochs = create_eog_epochs(raw, reject=reject)  # get single EOG trials
    eog_inds, scores = ica.find_bads_eog(eog_epochs)  # find via correlation
    ica.exclude.extend(eog_inds)
    ica.apply(raw)

def epoch_raw(raw_copy, time_window, event_id, baseline= (None, 0), reject = 10.0, stim_channel='STI 014'):
    reject = dict(eeg=reject)
    events = mne.find_events(raw_copy, stim_channel=stim_channel)
    tmin = time_window[0]  # before
    tmax = time_window[1]  # after
    baseline = baseline  # means from the first instant to t = 0
    picks_eeg = mne.pick_types(raw_copy.info, meg=False, eeg=True, eog=False, stim=False,
                               exclude=['VEOG', 'HEOG'])
    epochs = mne.Epochs(raw_copy, events, event_id, tmin, tmax, proj=True, picks=picks_eeg, baseline=baseline,
                        reject=reject, reject_by_annotation=True)
    epoch_avg = epochs.average()
    all_evokeds = dict((cond, epochs[cond].average()) for cond in event_id)
    evoked_list = list()
    for cond in all_evokeds:
        evoked_list.append(all_evokeds[cond])
    return [evoked_list, epochs]