#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : RandomForestClassifier.py
# @Author: MoonKuma
# @Date  : 2019/2/11
# @Desc  : An example with RF classifier ( for classifying data with ordered label) applying to the iris dataset
# refer : https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html


from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time

file_train = 'test_project_basic/iris_training.csv'
data_train = np.loadtxt(file_train, dtype=float, delimiter=',', skiprows=1)
x_train,y_train = np.split(data_train, (4,), axis=1)
y_train = y_train.astype('int')

file_test = 'test_project_basic/iris_test.csv'
data_test = np.loadtxt(file_train, dtype=float, delimiter=',', skiprows=1)
x_test,y_test = np.split(data_test, (4,), axis=1)
y_test = y_test.astype('int')

def test_model(max_depth=5, n_estimators=10, max_features=1):
    clf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)
    start = time.time()
    clf.fit(x_train,y_train)
    time_cost = time.time() - start
    score = clf.score(x_test,y_test)
    return [time_cost, score]


test_model()
# Out[4]: [0.11699986457824707, 0.9833333333333333]

# try different hyper-parameters
for max_depth in range(2,11):
    for n_estimators in range(10,100,10):
        for max_features in range(1,5):
            time_cost, score = test_model(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)







