#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : data_concat.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : merge eeg/erp and behavior data

import mne
import numpy as np
import pandas as pd
import os

# read behavior data
file_path = 'data_sample/eeg_raw_data/subject_data/Behavior_Original/behavior_orig.txt'
txt_data = pd.read_table(file_path)



# read evoked data
file_path = 'data_sample/formal_dataset/sub_evoked_data/sub2-ave.fif'
evokes = mne.read_evokeds(file_path)
index = evokes[0].ch_names
evoke = evokes[0]
evoke.apply_baseline(baseline=(None, 0))
get_peak1 = evoke.get_peak(ch_type = 'eeg', tmin=0.05, tmax=0.15)
peak_time1 = get_peak1[1]
evt_copy = evoke.copy()
slice_1 = evt_copy.crop(tmin=peak_time1-0.01, tmax=peak_time1+0.01)




# read tfr data
file_path = 'data_sample/formal_dataset/sub_power_data/sub2-tfr.h5'
trfs = mne.time_frequency.read_tfrs(file_path)