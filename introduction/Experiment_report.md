# Experiment report

### Experiment design

1. Mix design, 3 * 2
2. Interdependent variables
   -  Priming type
     - Between subjects, 3 levels
     - Mortality priming, neutral priming, negative control priming
   - Events type
     - Fearful pictures
     - Neutral pictures
3. Dependent variables
   - EEG recording
   - Behavior data	

### Data structure 

1. Behavior

   - Anxiety Questionnaire
     - Trait anxiety , measured before experiment
     - State anxiety, measured two times between and after experiment
   - Anthropological
     - Gender
     - Age
   - Manipulation
     - Priming group
   - Task results
     - Task accuracy
     - Reaction time 

2. ERP data

   - Event type
     - Fear
     - Neutral
   - Channel Position
     - FCZ
     - CZ
     - PZ
     - OZ
   - Time window[*Auto-detected]
     - First Peak
     - Second Peak

3. EEG (morlet) data

   - Event type[*same as above]

   - Channel Position[*same as above]

   - Frequency of interest

     ```python
     # computed as
     freqs = np.logspace(*np.log10([1, 35]), num=6)
     ```

     - 1 Hz
     - 2.03 Hz
     - 4.14 Hz
     - 8.44 Hz
     - 17.18 Hz
     - 35 Hz

### EEG analyze pipeline

```python
import mne
# the erp and eeg data preprocessing is run within python, package mne
# see the acutal codes in 
# /eeg_pre_processing/eeg_pre_processing.py
# /eeg_pre_processing/erp_pre_processing.py
```

1. Pre-processing

   - import raw data and concatenate (*.cnt -> mne.raw)
   - down sampling to 250 Hz 

2. ERP data

   - band filter 1~40 Hz
   - ICA removing eye movement
   - epoch, -0,5s~1s, baseline correction[,0], reject bad epochs(>10.0)
   - average across events type  

3. EEG data

   - high-pass filter 1Hz~
   - ICA removing eye movement
   - epoch, -1s~1s, baseline correction[total], reject bad epochs(>10.0)
   -  


