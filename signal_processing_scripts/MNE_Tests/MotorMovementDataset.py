import matplotlib as plt
import mne
import numpy as np
import scipy.io

"""
This subject is a 21 year old, right handed male with no known medical conditions. The EEG consists of actual random 
movements of left and right hand recorded with eyes closed. Each row represents one electrode.

The order of the electrodes is FP1 FP2 F3 F4 C3 C4 P3 P4 O1 O2 F7 F8 T3 T4 T5 T6 FZ CZ PZ. The recording was done at 
500Hz using Neurofax EEG System which uses a daisy chain montage. The data was exported with a common reference using 
Eemagine EEG. AC Lines in this country work at 50 Hz.
"""

# Convert .mat to ndarray to Raw MNE object
path = "Src\\Subject1_1D.mat"
mat = scipy.io.loadmat(path)
baseline = mat['baseline'][:, :1000]  # 64300 total samples (~128 seconds)

ch_names = ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2',
            'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ', 'CZ', 'PZ']
sample_freq = 500
info = mne.create_info(ch_names, sample_freq, 'eeg')

# Plot raw data
raw = mne.io.RawArray(baseline, info)
raw.plot(block=True, scalings=95, n_channels=5)  # Plotted Range = 0 +/- scale V

raw.filter(l_freq=8, h_freq=100)  # Bandpass between 8 Hz and 50 Hz
raw.plot(block=True, scalings=50, n_channels=5)

raw.plot_psd(fmax=250)  # See AC artifacts at 50Hz and harmonics

eog_events = mne.preprocessing.find_eog_events(raw, ch_name=['FP1', 'FP2'])  # Find EOG events from electrodes near eyes
raw.plot(block=True, events=eog_events, scalings=50, n_channels=2)  # Plot with markers at EOG events
print("Debug")

'''
# Dataset 2
path = "Src\\right_thumb_eeg.txt"
full_thumb = np.loadtxt(path, dtype=float).transpose()

ch_names = [str(num+1) for num in range(13)]
info = mne.create_info(ch_names, 500, 'eeg')

raw = mne.io.RawArray(full_thumb, info)
raw.plot(block=True, scalings=2)
'''
