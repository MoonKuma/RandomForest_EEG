#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : models_to_test.py
# @Author  : MoonKuma
# @Date    : 2019/2/23
# @Desc   : Test different hypothesis



from eeg_random_forest.learning_machines import *
import pandas as pd
import time

def test_regression_model(full_data, sample_dict, save_path, test_times = 10):
    model_dict = get_regression_model()
    result_dict_total = test_model_sample(full_data, sample_dict, model_dict, test_times = test_times, test_size=0.1)
    save_test_result(result_dict_total, save_path)

def test_classification_model(full_data, sample_dict, save_path, test_times = 10):
    model_dict = get_classification_model()
    result_dict_total = test_model_sample(full_data, sample_dict, model_dict, test_times=test_times, test_size=0.1)
    save_test_result(result_dict_total, save_path)

def test_model_sample(full_data, sample_dict, model_dict, test_times = 10, test_size=0.1):
    result_dict_total = dict()
    for key in sample_dict.keys():
        msg = 'Start testing:' + key
        print(msg)
        x_columns = sample_dict[key]['x_columns']
        y_column = sample_dict[key]['y_column']
        # clear na
        data_copy = full_data.copy(deep=True)
        data_copy_slice = pd.DataFrame(data_copy, columns=x_columns + y_column)
        data_copy_slice_dropped = data_copy_slice.dropna(axis=0)
        result_dict = dict()
        for test_time in range(0, test_times):
            sample = select_columns(df=data_copy_slice_dropped, x_columns=x_columns, y_column=y_column, test_size=test_size)
            for model_key in model_dict.keys():
                st, s = train_test(sample=sample, model_dict=model_dict,model_key=model_key)
                if model_key not in result_dict.keys():
                    result_dict[model_key] = dict()
                result_dict[model_key]['st'] =  result_dict[model_key].setdefault('st', 0) + st
                result_dict[model_key]['s'] = result_dict[model_key].setdefault('s', 0) + s
        for model_key in model_dict.keys():
            result_dict[model_key]['st'] = result_dict[model_key].setdefault('st', 0)/test_times
            result_dict[model_key]['s'] = result_dict[model_key].setdefault('s', 0) /test_times
        result_dict_total[key] = result_dict
    return result_dict_total

# save result
def save_test_result(result_dict, save_path):
    save_file_name = save_path + 'result_save' +  str(int(time.time())%10000)+ '.txt'
    with open(save_file_name, 'w') as file_save:
        for key in result_dict.keys():
            for model_name in result_dict[key].keys():
                str2wri = key + ',' + model_name + ',' + str(result_dict[key][model_name]['st']) + ',' + str(result_dict[key][model_name]['s']) + '\n'
                file_save.write(str2wri)


