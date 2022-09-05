from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
import pandas as pd
from brainflow.data_filter import DataFilter
#from MNE_Tests.DataClasses import Container
#from MNE_Tests.VisualClasses import Plotter
import tkinter as tk
#import mne
import numpy as np
import time
import matplotlib.pyplot as plt


chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
chunksize = 300
buffer_size = 450000
lpass = 5
hpass = 35

params = BrainFlowInputParams()
params.serial_port = '/dev/cu.usbserial-DM03H2PV' #or COM5 or COM4
board_id = 2 #0 for cyton, #2 for cyton daisy, there is also an option for synthetic data
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream(buffer_size)
data_rows = board.get_eeg_channels(board_id)

#mne_info = mne.create_info(chan_names, sample_freq, 'eeg')
full_data = []
#Collect data for 10 seconds
t_end = time.time() + 10
chunk_count = 0
while (time.time() < t_end):
    try:
        print("blink")
        time.sleep(2)
        data = board.get_board_data()[data_rows[0]: data_rows[-1] + 1]
        print("length of data is " + str(data.shape))
        chunk_count+=1
        #CREATE A MATRIX OF CUMULATIVE SIGNAL
        if len(full_data):
            print("appending")
            full_data = np.append(full_data, data, axis = 1)
        else:
            if chunk_count > 1:
                full_data = data

        #EYE BLINK DETECTION
        #raw_mne = mne.io.RawArray(data, info=mne_info)
        #raw_mne.filter(l_freq=lpass, h_freq=hpass)
       # eog_events = mne.preprocessing.find_eog_events(raw_mne, ch_name=["One", "Two"])
        #locations = eog_events[:, 0]
    except KeyboardInterrupt:
        break
board.stop_stream()
board.release_session()

#PLOT CUMULATIVE SIGNAL
fig, axs = plt.subplots(16)
print("full_data shape is " + str(full_data.shape))
for i, data_row in enumerate(full_data):
   axs[i].plot(data_row)
plt.show()

#WRITE TO FILE
#DataFilter.write_file(full_data, "cumulative_signal_blinks.csv", 'w') 

# EYE BLINKING STUFF I THINK
# root = tk.Tk()
# con = Container(sample_freq, len(chan_names), full_data, chan_names)
# app = Plotter(con, channel_names=chan_names, datalimit=len(full_data[0, :])-1, master=root)
# app.mainloop()
