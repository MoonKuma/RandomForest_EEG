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
     - all 64 channels
   - Time window[*Auto-detected in real time]
     - First Peak [50ms ~ 150ms] and its amplitudes
     - Second Peak [200ms ~ 500ms] and its amplitudes

3. EEG (morlet) data

   - Event type, Channel Position, Time window[*same as above]

   - Frequency of interest

     ```python
     # computed as
     freqs = [2.5, 5.0, 10.0, 17, 35] # as Delta (~3 Hz), Theta(3.5~7.5 Hz), Alpha(7.5~13 Hz), Beta(14~ Hz) 
     ```


### EEG analyze pipeline

```python
import mne
# the erp and eeg data preprocessing is run within python, package mne
```

1. Pre-processing

   - import raw data and concatenate (*.cnt -> mne.raw)
   - down sampling to 250 Hz 

2. ERP data

   - band filter 1~40 Hz
   - ICA removing eye movement
   - epoch, -0,5s~1s, baseline correction[,0], reject bad epochs(>10.0)
   - average across events type  and get amplitude

3. EEG data

   - high-pass filter 1Hz~
   - ICA removing eye movement
   - epoch, -1s~1s, baseline correction[total], reject bad epochs(>10.0)
   -  Morlet and get power


