import mne
import numpy as np

"""
EEG-IO:Voluntary single eye-blinks (external stimulation was provided) and EEG was recorded for frontal electrodes 
(Fp1, Fp2) for 20 subjects using OpenBCI Device and BIOPAC Cap100C. One session was conducted including around 25 blinks 
per subject. Manual annotation was done using video feed.
"""

path = "EEG-EyeBlinks/EEG-IO/S02_data.csv"
data = np.genfromtxt(path, delimiter=';', skip_header=True, usecols=(1, 2)).transpose()
sample_freq = 250
chan_names = ['FP1', 'FP2']
info = mne.create_info(chan_names, sample_freq, 'eeg')

raw = mne.io.RawArray(data, info)

raw.plot(block=True, scalings=80)  # Plotted Range = 0 +/- scale V
raw.filter(l_freq=10, h_freq=50)

raw.plot(block=True, scalings=80)

# Find EOG events
eog_events = mne.preprocessing.find_eog_events(raw, ch_name=['FP1', 'FP2'], event_id=0, thresh=10)
# Plot with markers at EOG events
raw.plot(block=True, events=eog_events, event_color='darkblue', scalings=50, n_channels=2)
