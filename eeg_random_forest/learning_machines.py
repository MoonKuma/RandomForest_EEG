#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @File    : learning_machines.py
# @Author  : MoonKuma
# @Date    : 2019/2/23
# @Desc   : including several learning models used in this example


from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split

import pandas as pd
import time


def select_columns(df, x_columns, y_column,test_size=0.1):
    X_train, X_test, y_train, y_test = train_test_split(pd.DataFrame(df, columns=x_columns), pd.DataFrame(df, columns=y_column), test_size=test_size)
    return [X_train.values, X_test.values, y_train.values, y_test.values]

# SvmClassifier
def SVM_clf():
    model = SVC()
    return model
# LogisticClassifier
def Logistic_clf():
    model = LogisticRegression()
    return model
# RandomForestClassifier
def RandomForest_clf(max_depth=100, n_estimators=1000, max_features=1):
    model = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)
    return model
# DecisionTreeClassifier
def DecisionTree_clf(max_depth=100):
    model = DecisionTreeClassifier(max_depth=max_depth)
    return model

# LinearRegression
def Linear_reg():
    model = LinearRegression()
    return model
# DecisionTreeRegressor
def DecisionTree_reg(max_depth=100):
    model = DecisionTreeRegressor(max_depth=max_depth)
    return model
# RandomForestRegressor
def RandomForest_reg(max_depth=100, n_estimators=1000, max_features=1):
    model = RandomForestRegressor(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features)
    return model
# Model dict
def get_regression_model():
    model_dict = dict()
    model_dict['RandomForestRegressor'] = RandomForest_reg()
    model_dict['LinearRegressor'] = Linear_reg()
    model_dict['DecisionTreeRegressor'] = DecisionTree_reg()
    return model_dict

def get_classification_model():
    model_dict = dict()
    model_dict['SvmClassifier'] = SVM_clf()
    model_dict['LogisticClassifier'] = Logistic_clf()
    model_dict['RandomForestClassifier'] = RandomForest_clf()
    model_dict['DecisionTreeClassifier'] = DecisionTree_clf()
    return model_dict


# train and test
def train_test(sample, model_dict, model_key):
    model = model_dict[model_key]
    start = time.time()
    [X_train, X_test, y_train, y_test] = sample
    model.fit(X_train, y_train.ravel())
    time_cost = time.time() - start
    score_train = model.score(X_train, y_train.ravel())
    score = model.score(X_test, y_test.ravel())
    msg = 'Training on model ['+ str(model_key) + '], with time cost [' + str(time_cost) + '], train score [' + str(score_train) +'], test score[' + str(score) + ']'
    print(msg)
    return score_train, score

