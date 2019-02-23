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
import time
from sklearn import preprocessing



def data_merge(behavior_file_path, brain_file_path, save_file):
    # parameters
    # save_file = 'data_sample/formal_data/merged_data/'
    # behavior_file_path = 'data_sample/formal_data/behavior_data/Behavior_raw.txt'
    # brain_file_path = 'data_sample/formal_data/time_window_data/time_window_data_5062.txt'

    # read behavior data
    behavior_data = pd.read_table(behavior_file_path, sep='\t', header=0, index_col=0)

    # read time window data
    brain_data = pd.read_table(brain_file_path, sep=',', header=0, index_col=0)

    # merge by index
    full_data = pd.merge(behavior_data, brain_data, left_index=True, right_index=True)

    # fix gender
    full_data['Gender'] = full_data['Gender'].map(lambda x: x-1)
    # normalize behavior
    columns = full_data.columns.values
    peak_col = list()
    for i in range(0, columns.shape[0]):
        name = columns[i]
        if name.startswith('erp_peak'):
            peak_col.append(str(name))
    column_to_norm = ['Age', 'AVGcor', 'AVGrt', 'Atsum'] + peak_col
    index = full_data.index.values
    column_stay = list()
    for key in list(columns):
        if key not in column_to_norm:
            column_stay.append(key)
    norm_ndarray = preprocessing.normalize(pd.DataFrame(full_data, columns=column_to_norm),axis=0)
    norm_df = pd.DataFrame(norm_ndarray, columns=column_to_norm, index=index)
    merge_df = pd.merge(norm_df, pd.DataFrame(full_data, columns=column_stay), left_index=True, right_index=True)
    # save the merged file
    save_file = save_file + 'saving_' + str(int(time.time())%10000) + '.txt'
    merge_df.to_csv(save_file)

# try read csv
# save_file_data = 'data_sample/formal_data/merged_data/saving_5715.txt'
# data = pd.read_table(save_file_data, sep=',', header=0, index_col=0)