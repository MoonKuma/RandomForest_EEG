#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : eeg_pre_processing.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : Check out mne API at : http://martinos.org/mne/index.html

import numpy as np
import mne

# test reading
data_example = 'data_sample/eeg_raw_data/example/sub2/tb1.cnt'
raw = mne.io.read_raw_cnt(input_fname=data_example, montage=None, preload=True, data_format='int32', eog='header')
# read events
events = mne.event.find_events(raw=raw)
