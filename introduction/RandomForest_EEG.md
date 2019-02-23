## Using Random Forest Model on EEG /ERP Data

### Data Structure

- Behavior : Priming Type, Gender, Age, Anxiety Score, Reaction Time, Accuracy ()
- Peak : ERP peak data on events *time window ()
- ERP data : Average ERP amplitude data on events * time window * channels ()
- EEG data : EEG power data on events * time window * channels * frequency ()

![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\data_structure.png)

### Hypothesis

- Fake hypothesis
  - Brain electronical activity in response to stimuli can predict their anxiety level
  - Women performance less neural anxiety compared to man 

| No   | Input Features (X)                     | Target (Y) | Question Type [*] |
| ---- | -------------------------------------- | ---------- | ----------------- |
| 1    | Behavior[-Anxiety]                     | Anxiety    | Regression        |
| 2    | Peak                                   | Anxiety    | Regression        |
| 3    | Behavior[-Anxiety-Gender] + Peak       | Anxiety    | Regression        |
| 4    | Behavior[-Anxiety-Gender] + Peak + ERP | Anxiety    | Regression        |
| 5    | Behavior[-Anxiety-Gender] + EEG        | Anxiety    | Regression        |
| 6    | Behavior[-Gender]                      | Gender     | Classification    |
| 7    | Peak                                   | Gender     | Classification    |
| 8    | Behavior[-Anxiety-Gender] + Peak       | Gender     | Classification    |
| 9    | Behavior[-Anxiety-Gender] + Peak + ERP | Gender     | Classification    |
| 10   | Behavior[-Anxiety-Gender] + EEG        | Gender     | Classification    |

### Model

- Question Type decide which algorism : 
  - For regression task,  linear regression / decision tree / random forest mode will be used
  - For classification task, linear regression(logistic) / decision tree / random forest / SVM will be used 
- Cross-validation : 
  - For the reason of lacking enough cases (60 in total),  6-Fold is used in cross validation

### Result

