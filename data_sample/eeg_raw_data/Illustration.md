# Illustration of data

File structure

- sub* (* stand for the number of subject id)
  - gng*.cnt : EEG recording on a standard go/no-go test
    - event_type: 
      - 99 - no go events
      - 91 - go events
      - 1 - action
  - tb1/2.cnt : EEG recording on a two-back test with fear-triggering / neutral pictures 
    - event_type:
      - 11 - fear events (subjects are shown pictures which intended to trigger fearful feeling)
      - 19 - emotional neutral events

EEG equipments

- Neuroscan device with 64 channels (hence raw data are saved as *.cnt) eeg recording device
- EOG (catching eye movement through VEGO/HEOG channels) is applied, no other bioelectrical measurement involved

