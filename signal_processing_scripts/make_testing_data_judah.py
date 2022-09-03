from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
import pandas as pd
import tkinter as tk
import numpy as np
import time
import matplotlib.pyplot as plt

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
chunksize = 300
buffer_size = 450000
params = BrainFlowInputParams()
params.serial_port = '/dev/cu.usbserial-DM03H2PV' #or COM5 or COM4
board_id = 2 #0 for cyton, #2 for cyton daisy 
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream(buffer_size)
data_rows = board.get_eeg_channels(board_id)

full_data = []
t_end = time.time() + 300
start_chunk = 0
file_num = 1
while (time.time() < t_end):
    try:
        print("blink " + str(start_chunk))
        time.sleep(2)
        data = board.get_board_data()[data_rows[0]: data_rows[-1] + 1]
        print("length of data is before trimming " + str(data.shape))
        if start_chunk<1:
            start_chunk+=1
            continue
#TRIMMING DATA SO ALL IS 250 DATA POINTS IN LENGTH (OMIT EXTRA AT TAIL)
        if (len(data[0])>=250):
            if (len(data[0])>250):
                data = np.delete(data, np.s_[-(len(data[0]) - 250):], axis=1)
#WRITE DATA TO FILE IN FOLDER data/blinks
            print("length of data is after trimming " + str(data.shape))
            file_name = '/Users/judahdengel/Documents/neurotechxcolumbia_drone/data/no_blinks/' + 'blink_' + str(file_num) + '.csv'
            file_num+=1
            DataFilter.write_file(data, file_name, 'w')    

        start_chunk+=1
    except KeyboardInterrupt:
        break
board.stop_stream()
board.release_session()
