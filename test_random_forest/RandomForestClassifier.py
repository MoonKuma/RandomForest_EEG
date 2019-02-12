#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : RandomForestClassifier.py
# @Author: MoonKuma
# @Date  : 2019/2/11
# @Desc  : An example with RF classifier ( for classifying data with ordered label) applying to the iris dataset


from sklearn.ensemble import RandomForestClassifier
import numpy as np
import matplotlib.pyplot as plt
import time

file_train = 'data_sample/test_data/iris_training.csv'
data_train = np.loadtxt(file_train, dtype=float, delimiter=',', skiprows=1)
x_train,y_train = np.split(data_train, (4,), axis=1)
y_train = y_train.astype('int')
y_train = y_train.ravel()

file_test = 'data_sample/test_data/iris_test.csv'
data_test = np.loadtxt(file_train, dtype=float, delimiter=',', skiprows=1)
x_test,y_test = np.split(data_test, (4,), axis=1)
y_test = y_test.astype('int')
y_test = y_test.ravel()

def test_model(max_depth=5, n_estimators=10, max_features=1):
    clf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)
    start = time.time()
    clf.fit(x_train,y_train)
    time_cost = time.time() - start
    score = clf.score(x_test,y_test)
    return [time_cost, score]


# test_model()
# Out[4]: [0.11699986457824707, 0.9833333333333333]

# try different hyper-parameters
'''
# the number of features turns out doesn't make much difference here
for max_depth in range(2, 10):
    for n_estimators in (list(range(1,11)) + list(range(10,100,10))):
        for max_features in range(1, 4):
            time_cost, score = test_model(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)
            result_array = np.append(result_array, [[max_depth, n_estimators, max_features, time_cost, score]], axis=0)
'''
result_array = np.zeros((1, 4))
max_depth = list(range(2, 10))
n_estimators = (list(range(1,10)) + list(range(10,100,10)))
for depth in max_depth:
    for estimators in n_estimators:
        time_cost, score = test_model(max_depth=depth, n_estimators=estimators)
        result_array = np.append(result_array, [[depth, estimators, time_cost, score]], axis=0)
result_array = result_array[1:,:]
scores_time = result_array[:,2].reshape(len(max_depth), len(n_estimators))
scores_accuracy = result_array[:,3].reshape(len(max_depth), len(n_estimators))

# show the heat map on time and accuracy
plt.clf()
plt.figure(figsize=(8, 6))
plt.subplot(1, 2, 1)
plt.imshow(scores_time.T, interpolation='nearest', cmap=plt.cm.hot)
plt.xlabel('max_depth')
plt.ylabel('n_estimators')
plt.colorbar()
plt.xticks(np.arange(len(max_depth)), max_depth, rotation=45)
plt.yticks(np.arange(len(n_estimators)), n_estimators)
plt.title('Training time cost')
plt.subplot(1, 2, 2)
plt.imshow(scores_accuracy.T, interpolation='nearest', cmap=plt.cm.hot)
plt.xlabel('max_depth')
plt.ylabel('n_estimators')
plt.colorbar()
plt.xticks(np.arange(len(max_depth)), max_depth, rotation=45)
plt.yticks(np.arange(len(n_estimators)), n_estimators)
plt.title('Validation accuracy')

plt.show()

