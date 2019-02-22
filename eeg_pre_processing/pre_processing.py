#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : eeg_pre_processing.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : Check out mne API at : http://martinos.org/mne/index.html
# @Desc : This is specially used for this experiment

import numpy as np
import time
from eeg_pre_processing.methods import *
import traceback

def pre_processing(data_path, result_path_erp, result_path_eeg, patten, sample_rate, event_id, test_num = 1, target_file = None):
    # parameters
    # data_path = 'data_sample/eeg_raw_data/subject_data/EEG_Original'
    # result_path_erp = 'data_sample/formal_dataset/sub_evoked_data/'
    # result_path_eeg = 'data_sample/formal_dataset/sub_power_data/'
    # patten = 'tb'
    # sample_rate = 250
    # event_id = {"fear": 11, "neutral": 19}
    # erp
    filter_erp = (1., 40.)
    time_window_erp = (-0.5, 1.0)
    baseline_erp = (None, 0)
    # eeg
    filter_eeg = (1., None)
    time_window_eeg = (-1, 1.0)
    baseline_eeg = (None, None)
    freqs = np.array([2.5, 5.0, 10.0, 17., 35.]) # as Delta (~3 Hz), Theta(3.5~7.5 Hz), Alpha(7.5~13 Hz), Beta(14~ Hz)
    n_cycles = freqs / 2.
    # reject
    reject = 10.0

    # start computing
    file_dict = get_file_dict(data_path=data_path, patten=patten)
    # subjects failed ICA/Morlet
    ICA_failed = dict()
    Morlet_failed = dict()
    # iterate
    sub_ids = list(file_dict.keys())
    if 0 < test_num < len(sub_ids):
        sub_ids = sub_ids[0: test_num]
    if target_file is not None:
        sub_ids = [target_file]
    ts_total = time.time()
    for sub_id in sub_ids:
        ts = time.time()
        msg = '====start computing : ' + sub_id
        print(msg)
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
        ica = None
        try:
            ica = perform_ICA(raw_copy_erp)
        except:
            msg = '===ICA failed for subjects:' + sub_id
            print(msg)
            ICA_failed[sub_id] = traceback.format_exc()
        # Epoch
        erp_evoked_list, erp_epochs = epoch_raw(raw_copy=raw_copy_erp, time_window=time_window_erp, event_id=event_id,
                                                baseline=baseline_erp, reject=reject)
        # Save evoked data
        file_name = result_path_erp + sub_id + '-ave.fif'
        mne.write_evokeds(file_name, erp_evoked_list)
        # Drop raw_copy to save memory
        del raw_copy_erp
        msg = '====finish computing erp : ' + sub_id
        print(msg)


        # using raw data to compute eeg data
        raw.filter(filter_eeg[0], filter_eeg[1], fir_design='firwin')
        # ICA (using the already trained model)
        if ica is not None:
            ica.apply(raw)
        # Epoch
        eeg_evoked_list, eeg_epochs = epoch_raw(raw_copy=raw, time_window=time_window_eeg, event_id=event_id,
                                                baseline=baseline_eeg, reject=reject)
        # power
        try:
            powers = morlet_epochs(epochs=eeg_epochs, event_id=event_id, freqs=freqs, n_cycles=n_cycles)
            # save power
            file_name = result_path_eeg + sub_id + '-tfr.h5'
            mne.time_frequency.write_tfrs(file_name, powers, overwrite=True)

            msg = '====finish computing eeg : ' + sub_id + ' at time cost: ' + str(time.time() - ts)
            print(msg)
        except:
            msg = '===Morlet failed for subjects:' + sub_id
            print(msg)
            Morlet_failed[sub_id] = traceback.format_exc()
    msg = 'Finish computing all data from : ' + str(len(sub_ids)) + ' subjects at time cost: ' + str(time.time() - ts_total)
    print(msg)

    return [ICA_failed, Morlet_failed]