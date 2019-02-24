#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : controller.py
# @Author: MoonKuma
# @Date  : 2019/2/18
# @Desc  : control panel

import collections
import pandas as pd
from eeg_pre_processing.pre_processing import pre_processing
from eeg_pre_processing.extract_time_window import get_time_window_data
from utils.data_merge import data_merge
from eeg_random_forest.models_to_test import test_regression_model,test_classification_model
# file location
raw_data_path = 'data_sample/eeg_raw_data/EEG_Original'
result_path_erp = 'data_sample/formal_data/sub_evoked_data/'
result_path_eeg = 'data_sample/formal_data/sub_power_data/'
time_window_result = 'data_sample/formal_data/time_window_data/'
behavior_file_path = 'data_sample/formal_data/behavior_data/Behavior_raw.txt'
brain_file_path = 'data_sample/formal_data/time_window_data/time_window_data_5062.txt'
merge_data_file = 'data_sample/formal_data/merged_data/'
merge_data_name = 'data_sample/formal_data/merged_data/saving_8307.txt'
model_result_path = 'data_sample/formal_data/model_result/'


# pre-processing eeg raw data
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
                                               event_id=event_id, test_num=test_num)

    if len(ICA_failed.keys()) > 0:
        print('ICA failed list: ',ICA_failed.keys())

    if len(Morlet_failed.keys()) > 0:
        print('Morlet failed list: ',Morlet_failed.keys())


# slicing time window
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


# merge this two
def merge_data():
    """
    This is to merge the behavior and brain data and do some simple
    processing like one-hot gender and normalize questionnaire data
    :return:  nothing will return, see the merged data in ${merge_data_file}
    """
    data_merge(brain_file_path=brain_file_path,behavior_file_path=behavior_file_path,save_file=merge_data_file)


# testing regression models
def test_regression_models():
    full_data = pd.read_csv(merge_data_name, delimiter=',', header=0, index_col=0)
    columns = full_data.columns.values
    behavior_col = ['Gender', 'Age', 'AVGcor', 'AVGrt']
    target_col = ['Atsum']
    eeg_col = list()
    erp_col = list()
    peak_col = list()
    for i in range(0, columns.shape[0]):
        name = columns[i]
        if name.startswith('erp_peak'):
            peak_col.append(name)
        elif name.startswith('erp'):
            erp_col.append(name)
        elif name.startswith('eeg'):
            eeg_col.append(name)

    sample_dict = dict()
    sample_dict['01'] = {'x_columns': behavior_col, 'y_column': target_col}
    sample_dict['02'] = {'x_columns': peak_col, 'y_column': target_col}
    sample_dict['03'] = {'x_columns': erp_col, 'y_column': target_col}
    sample_dict['04'] = {'x_columns': eeg_col, 'y_column': target_col}
    sample_dict['05'] = {'x_columns': behavior_col + peak_col, 'y_column': target_col}
    sample_dict['06'] = {'x_columns': behavior_col + peak_col + erp_col, 'y_column': target_col}
    sample_dict['07'] = {'x_columns': behavior_col + peak_col + eeg_col, 'y_column': target_col}
    sample_dict['08'] = {'x_columns': behavior_col + peak_col + eeg_col + erp_col, 'y_column': target_col}

    test_regression_model(full_data=full_data, sample_dict=sample_dict, save_path=model_result_path+'reg_',test_times=10)

# testing classification models
def test_classification_models():
    full_data = pd.read_csv(merge_data_name, delimiter=',', header=0, index_col=0)
    columns = full_data.columns.values
    behavior_col = ['Atsum', 'Age', 'AVGcor', 'AVGrt']
    target_col = ['Gender']
    eeg_col = list()
    erp_col = list()
    peak_col = list()
    for i in range(0, columns.shape[0]):
        name = columns[i]
        if name.startswith('erp_peak'):
            peak_col.append(name)
        elif name.startswith('erp'):
            erp_col.append(name)
        elif name.startswith('eeg'):
            eeg_col.append(name)

    sample_dict = dict()
    sample_dict['01'] = {'x_columns': behavior_col, 'y_column': target_col}
    sample_dict['02'] = {'x_columns': peak_col, 'y_column': target_col}
    sample_dict['03'] = {'x_columns': erp_col, 'y_column': target_col}
    sample_dict['04'] = {'x_columns': eeg_col, 'y_column': target_col}
    sample_dict['05'] = {'x_columns': behavior_col + peak_col, 'y_column': target_col}
    sample_dict['06'] = {'x_columns': behavior_col + peak_col + erp_col, 'y_column': target_col}
    sample_dict['07'] = {'x_columns': behavior_col + peak_col + eeg_col, 'y_column': target_col}
    sample_dict['08'] = {'x_columns': behavior_col + peak_col + eeg_col + erp_col, 'y_column': target_col}

    test_classification_model(full_data=full_data, sample_dict=sample_dict, save_path=model_result_path + 'clf_',
                          test_times=10)
    pass

# subjects_pre_processing()
# time_window_selection()
# merge_data()
# test_regression_models()
test_classification_models()