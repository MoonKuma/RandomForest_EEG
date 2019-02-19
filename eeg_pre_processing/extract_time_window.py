#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : extract_time_window.py
# @Author: MoonKuma
# @Date  : 2019/2/19
# @Desc  : extrat time window from computed erp/eeg data

import os


erp_data_file = 'data_sample/formal_dataset/sub_evoked_data'
eeg_data_file = 'data_sample/formal_dataset/sub_power_data'

sub_list = list()
file_list = os.listdir(erp_data_file) # assuming no erp data is missing
for file_name in file_list:
    if file_name.startswith('sub'):
        sub_id = file_name.split('-')[0] # all erp/eeg file name should be like 'subx-ave/trf.fif'
        sub_list.append(sub_id)
print('Subjects num: ', len(sub_list))

