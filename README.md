# RandomForest_EEG
#### Abstract

​	An introduction of random forest model as well as its application demo on one EEG study.

#### File Structure

- introduction

  - Introduction_of_random_forest

    An introduction file on random forest model including its **pros**, **cons**, important **hyper-parameters** and its map search result, **suitable situations** as well as **comparison** with other related non-linear simple models.

  - Paper_report

    A brief **report on paper** named *Persistent metabolic youth in the aging female brain* by Goyal ., et al from 2019 (*PNAS*) 

  - **Experiment_report**

    An introduction on the **experiment design, data structure and results report** on the performance of random forest model in real eeg and behavior data, as well as the performance of some other models

- data_sample

  - test_data

    Iris data for testing the  behavior of random forest model in different hyper-parameters sets. 

  - eeg_raw_data

    **EEG raw data (.cnt) from one of the subjects** to realize and test the eeg/erp data pre-processing with python package, as well as its description

  - formal_dataset

    **All pre-processed data**, including their eeg data (power of different frequency), erp data(amplitude in certain time window), and behavior data (gender, age, anxiety trait and so on)  from 60 subjects, as well as its description. (This part will be kept private for certification reason until authorized)

- test_random_forest

  - python scripts on testing random forest model and compare it with other models

- eeg_pre-processing

  - python scripts on **eeg/erp preprocessing**

- eeg_random_forest

  - python scripts on applying **random forest model** in those pre-processed data with different hyper-parameters

- eeg_neural_network

  - python scripts on using **neural network model** in analyzing and predicting  pre-processed data 

- utils

  - some other tool methods been used

- reference

  - img

    images used in .md files

  - papers

    related papers

#### Environment

- Python 3.6 (Anaconda)
  - numpy, sklearn, plt and other related packages
- mne
  - mne is used for eeg/erp pre-processing, this package is not necessary in case when raw data pre processing is not needed
- Tensor1.6
  - for building neural network models