#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: MoonKuma
# @Date  : 2019/2/18
# @Desc  : control panel

import collections
from eeg_pre_processing.pre_processing import pre_processing


def subjects_pre_processing():
    """
    Pre-processing module
    Caution this is the control panel, where parameters are written INSIDE the funcs and there won't be any return
    """
    data_path = 'data_sample/eeg_raw_data/subject_data/EEG_Original'
    result_path_erp = 'data_sample/formal_dataset/sub_evoked_data/'
    result_path_eeg = 'data_sample/formal_dataset/sub_power_data/'
    patten = 'tb'
    sample_rate = 250
    # event
    event_id = collections.OrderedDict()
    event_id['fear'] = 11
    event_id['neutral'] = 19
    # event_id = {"fear": 11, "neutral": 19}
    test_num = 0
    ICA_failed, Morlet_failed = pre_processing(data_path=data_path, result_path_erp=result_path_erp, result_path_eeg=result_path_eeg,
                   patten=patten, sample_rate=sample_rate, event_id=event_id, test_num=test_num)

    if len(ICA_failed.keys()) > 0:
        print('ICA failed list: ',ICA_failed.keys())

    if len(Morlet_failed.keys()) > 0:
        print('Morlet failed list: ',Morlet_failed.keys())


# subjects_pre_processing()