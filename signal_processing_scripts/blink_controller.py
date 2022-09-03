from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter
from MNE_Tests.DataClasses import Container
from MNE_Tests.VisualClasses import Plotter
from read_and_plot import plot_blinks
import mne
import pandas as pd
import tkinter as tk
import numpy as np
import time
import matplotlib.pyplot as plt
from djitellopy import Tello
tello = Tello()
def takeoff_land():
    tello.connect()
    tello.takeoff()
    tello.land()

def take_off():
    tello.connect()
    tello.takeoff()

def land():
    tello.land()
    
sample_freq = 125
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
chunksize = 300
buffer_size = 450000
lpass = 5
hpass = 35
params = BrainFlowInputParams()
params.serial_port = '/dev/cu.usbserial-DM03H2PV' #or COM5 or COM4
board_id = 2 #0 for cyton, #2 for cyton daisy 
board = BoardShim(board_id, params)
board.prepare_session()
board.start_stream(buffer_size)
data_rows = board.get_eeg_channels(board_id)
mne_info = mne.create_info(chan_names, sample_freq, 'eeg')

full_data = []
t_end = time.time() + 5
start_chunk = 0
file_num = 1
taken_off = False
while (time.time() < t_end):
    try:
        print("blink " + str(start_chunk))
        time.sleep(2)
        data = board.get_board_data()[data_rows[0]: data_rows[-1] + 1]
        print("length of data is before trimming " + str(data.shape))
        if start_chunk<1:
            start_chunk+=1
            continue

        raw_mne = mne.io.RawArray(data, info=mne_info)
        raw_mne.filter(l_freq=lpass, h_freq=hpass)
        threshold =np.max(raw_mne[0][0]) - np.min(raw_mne[0][0]) / 4
        eog_events = mne.preprocessing.find_eog_events(raw_mne, ch_name=["One", "Two"], thresh = threshold)
        print("FINISHED MNE PROCESSING: DETECTING BLINKS. EOG EVENTS:")
        print(len(eog_events[:, 0]))
        if len(eog_events[:, 0]) == 0 or len(eog_events[:, 0]) == 1:
            print("Zero blinks detected")
        elif len(eog_events[:, 0]) == 2:
            print("Two blinks detected: Takeoff")
            if not taken_off:
                #takeoff_land()
                taken_off = True
        elif len(eog_events[:, 0]) == 3:
            print("Three blinks detected: Landing")
            
            #land()
        plot_blinks(data, eog_events)
        start_chunk+=1
    except KeyboardInterrupt:
        break
board.stop_stream()
board.release_session()
#land()