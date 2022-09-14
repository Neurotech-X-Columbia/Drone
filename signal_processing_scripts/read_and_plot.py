from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
from MNE_Tests.DataClasses import Container
from MNE_Tests.VisualClasses import Plotter
import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_blinks(data, eog_events):
    locations = eog_events[:, 0]
    print("locations")
    print(locations)
    fig, axs = plt.subplots(2)
    for i, data_row in enumerate(data[0:2]):
        axs[i].plot(data_row)
    for blink in locations:
        axs[i].plot(blink, data_row[blink],  '.', 'r')
    plt.show()

lpass = 5
hpass = 35
sample_freq = 125
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
mne_info = mne.create_info(chan_names, sample_freq, 'eeg')

recorded_data = DataFilter.read_file('../data/double_blinks/blink_2.csv')
raw_mne = mne.io.RawArray(recorded_data, info=mne_info)
raw_mne.filter(l_freq=lpass, h_freq=hpass)
threshold =np.max(raw_mne[0][0]) - np.min(raw_mne[0][0]) / 4
print(threshold)
eog_events = mne.preprocessing.find_eog_events(raw_mne, ch_name=["One", "Two"], thresh = threshold)
plot_blinks(recorded_data, eog_events)