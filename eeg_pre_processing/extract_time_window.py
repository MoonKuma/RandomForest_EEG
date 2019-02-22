#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extract_time_window.py
# @Author: MoonKuma
# @Date  : 2019/2/19
# @Desc  : extract time window from computed erp/eeg data

import os
import numpy as np
import collections
import mne
from sklearn.preprocessing import normalize
import time


def get_time_window_data(erp_data_file, eeg_data_file, save_file, time_window, time_span, is_norm=True, baseline=(None, 0), test_s=True, test_times=5, target_subject=None):
    # parameter requirement
    # erp_data_file = 'data_sample/formal_dataset/sub_evoked_data/' # where raw evoked data is stored
    # eeg_data_file = 'data_sample/formal_dataset/sub_power_data/'
    # save_file = 'data_sample/formal_dataset/time_window_data/' # save the time window files
    # time_window = {'early': (0.05, 0.15), 'late': (0.2, 0.4)}  # pick time windows (/s)
    # time_span = 0.01 # +-10ms pick time span around peak
    # is_norm  = True # once normalized the data will only reflect the relative difference across channels
    # baseline = (None, 0) #
    # test_s = True
    # test_times = 2
    # target_subject  = None
    # start here
    test = 1
    time_stamp = int(time.time())%10000
    is_test_file = ''
    if test_s:
        is_test_file = '_test_'
    file_name_data = 'time_window_data_' + str(time_stamp) + is_test_file + '.txt'
    file_name_info = 'time_window_info_' + str(time_stamp) + is_test_file + '.txt'
    # get subject list
    sub_dict = collections.OrderedDict()
    file_list = os.listdir(erp_data_file)  # assuming no erp data is missing
    for file_name in file_list:
        if file_name.startswith('sub'):
            sub_id = file_name.split('-')[0]  # all erp/eeg file name should be like 'subx-ave/trf.fif'
            sub_dict[sub_id] = dict()
            erp_file = erp_data_file + sub_id + '-ave.fif'
            if os.path.exists(erp_file):
                sub_dict[sub_id]['erp'] = erp_file
            eeg_file = eeg_data_file + sub_id + '-tfr.h5'
            if os.path.exists(eeg_file):
                sub_dict[sub_id]['eeg'] = eeg_file
    print('Subjects num from len(sub_dict.keys()): ', len(sub_dict.keys()))

    if target_subject is not None:
        tmp = sub_dict[target_subject]
        sub_dict = dict()
        sub_dict[target_subject] = tmp
    # walking through each subjects
    data_dict = dict()
    # {sub1:{col_name1:data1}}
    # col name of peak: 'peak' + event + time window
    # col name of erp: 'erp' + event + time window + channel name
    # col name of eeg: 'eeg' + event + time window + freq_type + channel name
    info_dict = dict()
    info_dict['time_window'] = time_window
    info_dict['time_span'] = time_span
    info_dict['is_norm'] = is_norm
    if is_norm:
        info_dict['normal_failed'] = set()
    # time window list
    # freq list
    col_list = list()
    row_list = list()

    for sub_id in sub_dict.keys():
        row_list.append(sub_id)
        data_dict[sub_id] = dict()
        # compute erp files
        erp_file = sub_dict[sub_id]['erp']
        evokes = mne.read_evokeds(erp_file)
        # across events
        for event in evokes:
            channels = event.ch_names
            comment = event.comment
            event.apply_baseline(baseline=baseline)
            # across time window
            for tw_name in time_window.keys():
                peak_channel, peak = event.get_peak(ch_type = 'eeg', tmin=time_window[tw_name][0], tmax=time_window[tw_name][1])
                # save peak
                key_name = 'erp_peak_' + comment + '_' + tw_name
                data_dict[sub_id][key_name] = peak
                if key_name not in col_list:
                    col_list.append(key_name)
                event_copy = event.copy()
                slice_evt = event_copy.crop(tmin=peak - time_span, tmax=peak + time_span)
                mean = np.mean(slice_evt.data, axis=1).reshape(slice_evt.data.shape[0], 1)
                norm_mean = mean.T
                if is_norm:
                    try:
                        norm_mean = normalize(mean, axis=0).T  # normalize (1,61)
                    except:
                        info_dict['normal_failed'].add(sub_id)

                norm_list = norm_mean[0,:].tolist()
                if len(norm_list) == len(channels):
                    for index in range(0, len(channels)):
                        key_name = 'erp_' + comment + '_' + tw_name + '_' + channels[index]
                        data_dict[sub_id][key_name] = norm_list[index]
                        if key_name not in col_list:
                            col_list.append(key_name)
        msg = '===finish computing erp from sub' + sub_id
        print(msg)
        # compute eeg files
        eeg_file = sub_dict[sub_id]['eeg']
        tfrs = mne.time_frequency.read_tfrs(eeg_file)
        for tfr in tfrs:
            channels = tfr.ch_names
            comment = tfr.comment
            freqs = tfr.freqs.tolist()
            tfr.apply_baseline(baseline=baseline)
            for tw_name in time_window.keys():
                # get peak
                key_name = 'erp_peak_' + comment + '_' + tw_name
                peak = data_dict[sub_id][key_name]
                tfr_copy = tfr.copy()
                slice_evt = tfr_copy.crop(tmin=peak - time_span, tmax=peak + time_span) # (61,5,n_times)
                mean = np.mean(slice_evt.data, axis=2)
                norm_mean = mean.T
                if is_norm:
                    try:
                        norm_mean = normalize(mean, axis=0).T  # normalize (1,61)
                    except:
                        info_dict['normal_failed'].add(sub_id)
                if norm_mean.shape[0] == len(freqs):
                    for freq_index in range(0, len(freqs)):
                        name_freq = str(freqs[freq_index])
                        norm_list = norm_mean[freq_index, :].tolist()
                        if len(norm_list) == len(channels):
                            for ch_index in range(0, len(channels)):
                                key_name = 'eeg_' + comment + '_' + tw_name + '_' + name_freq + '_' + channels[ch_index]
                                data_dict[sub_id][key_name] = norm_list[ch_index]
                                if key_name not in col_list:
                                    col_list.append(key_name)
        msg = '===finish computing eeg from sub' + sub_id
        print(msg)
        test += 1
        if test_s and test > test_times:
            msg = 'Break for testing, test time = ' + str(test-1)
            print(msg)
            break

    # write into files
    data_file = save_file + file_name_data
    with open(data_file, 'w') as file_w:
        # header
        header = ['sub_id'] + col_list
        str2wri = ','.join(header) + '\n'
        file_w.write(str2wri)
        # content
        for sub in row_list:
            sub_id = sub.replace('sub', '')
            data_list = [sub_id]
            for col in col_list:
                data_list.append(str(data_dict[sub].setdefault(col, '')))
            str2wri = ','.join(data_list) + '\n'
            file_w.write(str2wri)

    # write info files
    info_files = save_file + file_name_info
    with open(info_files, 'w') as file_w:
        for key in info_dict.keys():
            str2wri = key + ':' + str(info_dict[key]) + '\n'
            file_w.write(str2wri)












