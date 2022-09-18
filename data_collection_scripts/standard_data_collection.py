# To be used for data collection from Cyton/Daisy (16 channels 125 Hz)
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from signal_processing_scripts.MNE_Tests.DataClasses import Container
from signal_processing_scripts.MNE_Tests.VisualClasses import Plotter
from time import sleep, ctime
from threading import Thread, Event

import os
import numpy as np
import pandas as pd
import tkinter as tk


class Timer(Thread):  # sets flush to True every {interval} seconds until raw_data is full
    def __init__(self, event, interval):
        super().__init__()
        self.flush = event
        self.complete = False
        self.interval = interval

    def run(self):
        # wait appropriate time interval to fill buffer, then cause main thread to store data from buffer
        while not self.complete:
            while not self.flush.wait(self.interval):  # every interval:
                self.flush.set()  # sets flush to True

    def end(self):
        self.complete = True


# Session and trial parameters
samples = 8000  # number of samples to capture in one trial (3750 = 30 seconds)
total_trials = 1  # number of complete trials (sets of data) generated for this session
buffer_size = 1001  # 1000 = 8 seconds stored in the buffer at once (buffer is actually one less than this value)
break_time = 15  # time between trials
srate = 125  # 125 for Cyton/Daisy; 250 for Cyton only
channels = 16

# 8000 total 5 buffer_size 1001 break_time 30 srate 125
# ((8000/125)*5 + 30*4)*6/60 = 44 minutes per subject
# ~5.3 minutes of data per frequency per subject

subj = "test"
stim_freq = "BottomRight"  # Hz
date = "9-18"
notes = "EC 1013 9/18/22 natural light and some fluorescent"  # miscellaneous info about collection conditions

os.makedirs(f"Recorded\\{subj}\\{stim_freq}", exist_ok=True)
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

with open(f"{os.getcwd()}\\Recorded\\{subj}\\info.txt", 'w') as info:
    info.write(f"Session: {total_trials} trials of {round(samples/srate, 2)} seconds each." +
               f"\nStimulation frequency: {stim_freq}" +
               f"\nSubject: {subj}" +
               f"\nTime between trials: {break_time} seconds." +
               f"\nBuffer Size: {buffer_size}\n"
               f"\nNotes: {notes}")

params = BrainFlowInputParams()
params.serial_port = "COM3"  # check device manager on Windows
board_id = 2  # 0 for cyton, #2 for Cyton/Daisy, there is also an option for synthetic data
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

    flush = Event()
    timer = Timer(flush, .9*float(buffer_size/srate))  # interval defined as time it should take to fill the buffer

    print(f"Starting trial {trial_count}...\nRecording {samples} samples ({round(samples/srate, 2)} seconds) with a " +
          f"buffer size of {buffer_size} samples.")

    timer.start()
    total = 0  # total samples recorded
    while total < samples:
        timer.flush.wait()  # wait until flush flag set to True
        timer.flush.clear()  # reset flush flag to False
        buf_count = board.get_board_data_count()
        board_data = board.get_board_data()
        # print(f"{buf_count} samples in buffer |", end="")

        if total + buf_count <= samples:
            raw_data[:, total:total+buf_count] = board_data[data_rows[0]: data_rows[-1]+1]
            total += buf_count
        else:
            space = samples - total
            raw_data[:, total:samples] = board_data[data_rows[0]: data_rows[-1] + 1, :space]
            total += space

        # print(f" {total} total samples recorded.")

    timer.end()
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
# root = tk.Tk()
# con = Container(srate, len(chan_names), raw_data, chan_names)
# app = Plotter(con, channel_names=chan_names, datalimit=len(raw_data[0, :])-1, master=root)
# app.mainloop()