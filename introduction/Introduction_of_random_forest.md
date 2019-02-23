# Introduction of random forest model

### Abstract

​	Random forest is a supervised machine learning techniques based on the combination of **ensemble** ("average" the result of multiple models for overall better performance) and **decision tree** ( predict certain target value based on splitting its features at different stage in a tree-like shape ). Random forest is used both in **classification** (when target values comes from discrete set like soft-max), and in **regression** ( for continuous target value like linear regression). The following introduction illustrate the basic principle, implementation and important hyper-parameters, pros and cons of random forest model. And then compare it with other machine learning model under same and different task condition.

- 总结来说，RandomForest是一种非线性的监督学习模型。
- 对比线性模型（ANOVA，线性回归）：
  - 其决策树的特性允许对**非线性**规律的学习
- 对比其他非线性模型（SVM）
  - 首先可以解决分类问题（因变量是分类变量），也可解决**回归问题**（因变量是连续变量）；
  - 其次，可以在做出预测的同时，提供关于自变量的各个**特性在预测中的重要性的评估**，以此具有一定的实际意义； 
  - 最后，随机森林的设计（多个随机的模型），避免了异常值/异常特征对于模型的影响，也使模型**免于过度拟合带来的准确率下降的问题**，最终使得训练过程相对**简单**并不要求高的模型理解或者预加工。
- 其问题包括：
  - 对于**非结构化数据学习能力差**（无法完成面孔识别，手写数字识别等问题）

### Principle

1. Decision Tree  - Tree



   ![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\cart_tree_titanic_survivors.png)

   - Using a tree like model to makes  decisions and predict their possible consequences. 
   - Traditional decision tree learn the importance(structure) and the cutting point. 
   - Note that the tree is actually reversed with root and nodes (different features of X) in the top, and leaves (predictions as compared to Y) in the bottom
   - Although it seems that decision tree is informative for understanding, the rules shown by a tree with high accuracy is **usually not "reasonable"**, for  a total different tree structure can easily reach similar good performance. 

2. Bagging (ensemble) - Forest

   - While one decision suffers from high variance for being too sensitive to noise in training, training more models at the same time with different subsets of training set won't. (outliers will be avoided by most other models)
   - After computing those trees, use the "average" vote of prediction    

3. Random features

   - Based on the bagging strategy, random forest select random subset of features in building each tree.
   - The basic idea is that is a small set of features and simpler model can do as better, there is no need to make it complicated (this also suppress the variance). 

### Hyperparameters

```python
# API : https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html#sklearn.ensemble.RandomForestClassifier

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=’warn’, criterion=’gini’, max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=’auto’, max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=None, random_state=None, verbose=0, warm_start=False, class_weight=None)
```

1. Important parameters

   - n_estimators : number of trees, increasing this will significantly increase the computational cost, more time
   - max_depth: depth of the tree, how complicated the highest tree should be

2. Scanning the parameters

   Related scripts : test_random_forest/ClassifierComparison.py

   ![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\scanning_hyperparameters.png)

   - Thanks to the bagging and random techniques, the model won't suffer from overfitting.
   - Which means that one can basically build a forest as complicated as he wants
   - We will run this scanning techniques to provide the evidence of a reasonable model has been picked in real case

### Pros and cons

- Pros:

  - Do not suffer from overfitting (low variance) as shown above, hence less dependent on the experience of developer
  - Suitable for both classification and regression problems. (Not ok with SVM)
  - Offers a weight table (feature importance)
- Cons:
  - Performance poor on non-structure data

### Comparison with other models on same task

![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\model_compare.jpg)

- See how Random Forest make more not that decisive classification compared to decision tree and hence saved if from overfitting (in example 3) without sacrifice very much bias ( example 1)
- Also both of them are not as good at non-linear classification as those kernel method like SVM   



