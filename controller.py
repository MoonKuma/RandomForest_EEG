#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: MoonKuma
# @Date  : 2019/2/18
# @Desc  : control panel

import collections
from eeg_pre_processing.pre_processing import pre_processing
from eeg_pre_processing.extract_time_window import get_time_window_data

# file location
raw_data_path = 'data_sample/eeg_raw_data/subject_data/EEG_Original'
result_path_erp = 'data_sample/formal_dataset/sub_evoked_data/'
result_path_eeg = 'data_sample/formal_dataset/sub_power_data/'
time_window_result = 'data_sample/formal_dataset/time_window_data/'

def subjects_pre_processing():
    """
    Pre-processing module
    Caution this is the control panel, where parameters are written INSIDE the funcs and there won't be any return
    """
    # data_path = 'data_sample/eeg_raw_data/subject_data/EEG_Original'
    # result_path_erp = 'data_sample/formal_dataset/sub_evoked_data/'
    # result_path_eeg = 'data_sample/formal_dataset/sub_power_data/'
    patten = 'tb'
    sample_rate = 250
    # event
    event_id = collections.OrderedDict()
    event_id['fear'] = 11
    event_id['neutral'] = 19
    # event_id = {"fear": 11, "neutral": 19}
    test_num = 0
    ICA_failed, Morlet_failed = pre_processing(data_path=raw_data_path, result_path_erp=result_path_erp,
                                               result_path_eeg=result_path_eeg, patten=patten, sample_rate=sample_rate,
                                               event_id=event_id, test_num=test_num, target_file='sub56')

    if len(ICA_failed.keys()) > 0:
        print('ICA failed list: ',ICA_failed.keys())

    if len(Morlet_failed.keys()) > 0:
        print('Morlet failed list: ',Morlet_failed.keys())


def time_window_selection():
    """
    First detect the peak in certain time window
    Then compute the average amplitude/power data around that peak
    This will generate several data files in (.txt) form with time stamp for identification, yet have no return values
    """
    time_window = {'early': (0.05, 0.15), 'late': (0.2, 0.4)}  # pick time windows (/s)
    time_span = 0.01 # +-10ms pick time span around peak
    # is_norm  = True # once normalized the data will only reflect the relative difference across channels
    # baseline = (None, 0) #
    # test_s = True
    # test_times = 2
    get_time_window_data(erp_data_file=result_path_erp, eeg_data_file=result_path_eeg, save_file=time_window_result,
                         time_window=time_window, time_span=time_span, test_s=False, test_times=2)
    # subject 56 seems to have some problems?


time_window_selection()

# subjects_pre_processing()