import mne
import numpy as np


def detect_blinks(data):  # Accepts data and returns if at least one blink detected
    chan_names = ['FP1', 'FP2']
    sample_freq = 250
    mne_info = mne.create_info(chan_names, sample_freq, 'eeg')

    length = 208
    lpass = 7
    ltrans = 4
    hpass = None
    htrans = None

    raw_mne = mne.io.RawArray(data, info=mne_info)
    raw_mne.filter(filter_length=length, l_freq=lpass, h_freq=hpass, l_trans_bandwidth=ltrans, h_trans_bandwidth=htrans)
    threshold = (np.max(raw_mne[0][0]) - np.min(raw_mne[0][0])) / 2
    eog_events = mne.preprocessing.find_eog_events(raw_mne, filter_length=length,
                                                   ch_name=["FP1", "FP2"], thresh=threshold)
    locations = eog_events[:, 0]

    if len(locations):
        state = 'blink'
    else:
        state = 'no blink'

    return state
