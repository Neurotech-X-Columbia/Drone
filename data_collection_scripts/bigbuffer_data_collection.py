from brainflow.board_shim import BoardShim, BrainFlowInputParams
from time import sleep, ctime
from threading import Thread, Event

import os
import numpy as np
import pandas as pd
# import tkinter as tk

# Testing non-threaded data collection that just stores all desired data in the buffer at once and then collects
# once at the end of the session

# Trial and Session Parameters
samples = 3500  # number of samples to capture in one trial (3750 = 30 seconds)
total_trials = 5  # number of complete trials (sets of data) generated for this session
buffer_size = int(1.25 * samples)  # buffer size 125% of trial size (max buffer size = 450000)
break_time = 30  # time between trials in seconds
srate = 125  # 125 for Cyton/Daisy; 250 for Cyton only
channels = 16

# Meta Information
subj = "bigbuffertest"
stim_freq = "TopLeft"
date = "9-23-22"
notes = f"\n{date}"  # miscellaneous info about collection conditions
storage_dir = f"{os.getcwd()}\\Recorded\\{subj}\\{stim_freq}"  # directory where trial files are stored
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

# BrainFlow Parameters
params = BrainFlowInputParams()
params.serial_port = "COM3"  # check device manager on Windows
board_id = 2  # 0 for cyton, #2 for Cyton/Daisy, there is also an option for synthetic data

os.makedirs(storage_dir, exist_ok=True)
with open(f"{storage_dir}\\info.txt", 'w') as info:
    info.write(f"Session: {total_trials} trials of {round(samples/srate, 2)} seconds each." +
               f"\nStimulation frequency: {stim_freq}" +
               f"\nSubject: {subj}" +
               f"\nTime between trials: {break_time} seconds." +
               f"\nBuffer Size: {buffer_size}\n"
               f"\nNotes: {notes}")

board = BoardShim(board_id, params)
board.disable_board_logger()
data_rows = board.get_eeg_channels(board_id)

board.prepare_session()
while not board.is_prepared():
    sleep(.5)
board.start_stream(buffer_size)
sleep(2)  # wait for stream to stabilize

raw_data = np.empty((channels, samples), dtype=np.float64)  # container for session data
trial_count = 1

print(f"Session: {total_trials} trials of {round(samples/srate, 2)} seconds each." +
      f"\nStimulation frequency: {stim_freq}" +
      f"\nSubject: {subj}" +
      f"\nTime between trials: {break_time} seconds.\n")

for x in range(total_trials):
    timestamp = "_" + ctime()[-13:-5].replace(":", "-")
    filename = f"Recorded\\{subj}\\{stim_freq}\\{int(samples/srate)}sec_{trial_count}{timestamp}.csv"

    print(f"Starting trial {trial_count}...\nRecording {samples} samples ({round(samples/srate, 2)} seconds) with a " +
          f"buffer size of {buffer_size} samples.")

    while board.get_board_data_count() < samples:
        sleep(1)

    board_data = board.get_board_data()
    buf_count = len(board_data[0, :])
    # print(f"{buf_count} samples in buffer |", end="")

    raw_data = board_data[data_rows[0]: data_rows[-1]+1, :samples]

    # print(f" {total} total samples recorded.")

    pd.DataFrame(raw_data).to_csv(filename)

    if trial_count < total_trials:
        print(f"Trial {trial_count} complete. Starting next trial in {break_time} seconds.\n")
        sleep(break_time-10)
        print("10 seconds until next trial.\n")
        sleep(10)

    trial_count += 1

board.stop_stream()
board.release_session()

print("\nData collection complete.")
