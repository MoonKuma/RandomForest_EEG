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
  - Brain electronical activity in response to stimuli can predict their gender type

### Models

- On predicting anxiety (a regression task)

| No   | Input Features (X)                 | #Features | Target (Y) |
| ---- | ---------------------------------- | --------- | ---------- |
| 1    | Behavior[-Anxiety]                 | 4         | Anxiety    |
| 2    | Peak                               | 4         | Anxiety    |
| 3    | ERP                                | 244       | Anxiety    |
| 4    | EEG                                | 1220      | Anxiety    |
| 5    | Behavior[-Anxiety] + Peak          | 8         | Anxiety    |
| 6    | Behavior[-Anxiety] + Peak + ERP    | 252       | Anxiety    |
| 7    | Behavior[-Anxiety] + Peak +EEG     | 1228      | Anxiety    |
| 8    | Behavior[-Anxiety] + Peak +EEG+ERP | 1472      | Anxiety    |

- On prediction gender (a classification task)

| No   | Input Features (X)                | #Features | Target (Y) |
| ---- | --------------------------------- | --------- | ---------- |
| 1    | Behavior[-Gender]                 | 4         | Gender     |
| 2    | Peak                              | 4         | Gender     |
| 3    | ERP                               | 244       | Gender     |
| 4    | EEG                               | 1220      | Gender     |
| 5    | Behavior[-Gender] + Peak          | 8         | Gender     |
| 6    | Behavior[-Gender] + Peak + ERP    | 252       | Gender     |
| 7    | Behavior[-Gender] + Peak +EEG     | 1228      | Gender     |
| 8    | Behavior[-Gender] + Peak +EEG+ERP | 1472      | Gender     |

### Algorism

- Training and testing : 
  - For regression task,  **linear regression** / **decision tree** / **random forest** mode will be used
  - For classification task, **linear regression(logistic)** / **decision tree** / **random forest** / **SVM** will be used 
- Cross-validation : 
  - For the reason of lacking enough cases (60 in total),  **6-Fold(10%)** is used in cross validation for **10 times**

### Result

- Regression result: train score(testing score)

| Num  | Model                                | Linear      | DecisionTree | RandomForest |
| ---- | ------------------------------------ | ----------- | ------------ | ------------ |
| 1    | Behavior[-Anxiety]                   | 0.08(-0.42) | 1(-3.56)     | 1(-3.56)     |
| 2    | Peak                                 | 0.85(-4.49) | 0.85(-4.49)  | 0.85(-4.49)  |
| 3    | ERP                                  | 1(-1.67)    | 1(-1.67)     | 1(-1.67)     |
| 4    | EEG                                  | 1(-4.89)    | 1(-4.89)     | 1(-4.89)     |
| 5    | Behavior[-Anxiety]   + Peak          | 1(-12.56)   | 1(-12.56)    | 1(-12.56)    |
| 6    | Behavior[-Anxiety]   + Peak + ERP    | 1(-1.8)     | 1(-1.8)      | 1(-1.8)      |
| 7    | Behavior[-Anxiety]   + Peak +EEG     | 1(-3.49)    | 1(-3.49)     | 1(-3.49)     |
| 8    | Behavior[-Anxiety]   + Peak +EEG+ERP | 1(-2.45)    | 1(-2.45)     | 1(-2.45)     |

​	* Testing score can be negative for regression task, when the prediction is really worse

- Classification result

| Num  | Model                             | Logistic   | DecisionTree | RandomForestClassifier | Svm        |
| ---- | --------------------------------- | ---------- | ------------ | ---------------------- | ---------- |
| 1    | Behavior[-Gender]                 | 0.58(0.45) | 1(0.57)      | 1(0.58)                | 0.56(0.45) |
| 2    | Peak                              | 0.54(0.53) | 0.99(0.37)   | 0.99(0.53)             | 0.55(0.53) |
| 3    | ERP                               | 0.81(0.57) | 1(0.43)      | 1(0.62)                | 0.56(0.42) |
| 4    | EEG                               | 1(0.7)     | 1(0.47)      | 1(0.57)                | 0.53(0.42) |
| 5    | Behavior[-Gender] + Peak          | 0.57(0.47) | 1(0.55)      | 1(0.65)                | 0.56(0.45) |
| 6    | Behavior[-Gender] + Peak + ERP    | 0.84(0.52) | 1(0.5)       | 1(0.55)                | 0.58(0.43) |
| 7    | Behavior[-Gender] + Peak +EEG     | 1(0.58)    | 1(0.38)      | 1(0.6)                 | 0.53(0.37) |
| 8    | Behavior[-Gender] + Peak +EEG+ERP | 1(0.57)    | 1(0.48)      | 1(0.47)                | 0.52(0.48) |

### Conclusion 

- Regression model show serious over-fitting problems in all models,  lacking of enough data may be the main cost of such problem
- In classification task,  Tree models still suffers from this over-fitting problem, SVM behave bad in learning, while logistic model show best performance with limited features

 