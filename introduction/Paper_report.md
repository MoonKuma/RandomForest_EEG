# Paper report: Persistent metabolic youth in the aging female brain

### Abstract

- Data : PET brain imaging data from 205 subjects
- Method : 
  - Random Forest Model
- Main result
  - Find a way in measuring brain aging 
  - Female has younger metabolic brain age
- To summarize :
  -  这篇文章的工作是，找了200个人的PET数据，训练了一个random forest模型，用PET数据实现了对被试生理年龄的准确率约为90%的预测，然后认为这PET数据就是脑老化的一种表征，再对相同生理年龄不同性别的被试套用上面的模型，发现女性的预测值明显小于男性。以此得出了女性的脑老化比男性慢的结论。

### Data Structure

- Input (X)
  - normalize brain metabolism data (4 parameters) from 79 brain region (316 features)
- Target (Y) : actual chronological age

### Method

- Main

  - Compute random forest on those 316 features from 165 subjects to predict their chronological age

    - The following scripts come from the original scripts

      ```R
      # The following trains the bias corrected random forest regression (rfbc) function
      rfbc = function(trainingdata,actualtrain,ntree1=10000,importance1=TRUE,spar1=1){
        
        rfbctrained = randomForest(trainingdata,
                                   actualtrain,
                                   ntree=ntree1,
                                   importance=importance1)
      
        # Now need to compute bias with cubic spline
        biasfix = smooth.spline(actualtrain~rfbctrained$predicted, spar=spar1)
        return(list("RFR" = rfbctrained, "BF" = biasfix))
      }
      ```

    - 10000 trees, split by 1

  - Ten-fold cross validation to measure the performance

- Supplementary

  - test the  across time stability through compare the brain age results from 19 of 165 subjects who took the experiment 2 times in 1-2 years 

### Result

- On model training

  - Overall high prediction accuracy

    ![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\paper_result1.png)

  - 59 of 316 features are important (as rule of thumbs) for predicting(Yet there is no cutting points)

    ![](D:\Data\PythonProjects\RandomForest_EEG\reference\img\paper_result2.png)

- On using model in testing gender difference

  - mean metabolic brain age (minus actual age) was on average 3.8 y less for females
    compared with males (n = 108 females and 76 males, 95% CI
    1.0–6.6 y, P < 0.010 t test, Cohen’s d > 0.40)
