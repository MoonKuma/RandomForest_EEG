#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : eeg_pre_processing.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : Check out mne API at : http://martinos.org/mne/index.html
# @Desc : This is specially used for this experiment

import numpy as np
import mne
import os
from eeg_pre_processing.methods import *

# parameters
data_path = 'data_sample/eeg_raw_data/ERP_Original'
patten = 'tb'
sample_rate = 250
filter_erp = (1., 40.)
filter_eeg = (1., None)
event_id = {"fear": 11, "neutral": 19}
time_window_erp = (-0.5, 1.0)
time_window_eeg = (-1, 1.0)
baseline_erp = (None, 0)
result_path = 'data_sample/formal_data/'
# start computing
file_dict = get_file_dict(data_path=data_path, patten=patten)
# iterate
for sub_id in file_dict.keys():
    if len(file_dict[sub_id])<1:
        print('[Warning]',sub_id, 'is missing!')
        continue
    # concat
    raw = concat_raw_cnt(file_dict[sub_id])
    # down sample
    raw.resample(sample_rate, npad="auto")

    # copy raw data here for erp compute
    raw_copy_erp = raw.copy()
    # filter
    raw_copy_erp.filter(filter_erp[0], filter_erp[1], fir_design='firwin')
    # ICA
    perform_ICA(raw_copy_erp)
    # Epoch
    erp_evoked_list, erp_epochs = epoch_raw(raw_copy=raw_copy_erp, time_window=time_window_erp, event_id=event_id, baseline=baseline_erp)
    # Save evoked data
    file_name = result_path + 'erp_data/' +  sub_id + '-ave.fif'
    mne.write_evokeds(file_name, erp_evoked_list)
    # Drop raw_copy
    del raw_copy_erp

    # using raw data to compute eeg data
