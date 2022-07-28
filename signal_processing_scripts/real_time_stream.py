from brainflow.board_shim import BoardShim, BrainFlowInputParams

from MNE_Tests.DataClasses import Container
from MNE_Tests.VisualClasses import Plotter
import tkinter as tk
import mne
import numpy as np
import time
import matplotlib.pyplot as plt

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
chunksize = 250
buffer_size = 450000
lpass = 5
hpass = 35

params = BrainFlowInputParams()
params.serial_port = "COM5" #COM5 or COM4
board_id = 2 #0 for cyton, #2 for cyton daisy 
board = BoardShim(board_id, params)

board.prepare_session()

board.start_stream(buffer_size)

data_rows = board.get_eeg_channels(board_id)

mne_info = mne.create_info(chan_names, sample_freq, 'eeg')
full_data = []


t_end = time.time() + 5

while (time.time() < t_end):
    try:
        time.sleep(2)
        data = board.get_board_data()[data_rows[0]: data_rows[-1] + 1, 10:]
        full_data.append(data)

        raw_mne = mne.io.RawArray(data, info=mne_info)
        raw_mne.filter(l_freq=lpass, h_freq=hpass)

        eog_events = mne.preprocessing.find_eog_events(raw_mne, ch_name=["One", "Two"])
        locations = eog_events[:, 0]

        if locations.any():
            print("Blink!")

    except KeyboardInterrupt:
        break

board.stop_stream()
board.release_session()

for data in full_data:
    print(data.shape)

# root = tk.Tk()
# con = Container(sample_freq, len(chan_names), full_data, chan_names)
# app = Plotter(con, channel_names=chan_names, datalimit=len(full_data[0, :])-1, master=root)
# app.mainloop()
