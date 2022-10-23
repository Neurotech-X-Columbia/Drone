from brainflow.board_shim import BoardShim, BrainFlowInputParams
from time import sleep, ctime
from threading import Thread, Event

import os
import numpy as np
import pandas as pd
# import tkinter as tk

# To be used for data collection from Cyton/Daisy (16 channels 125 Hz)


class Timer(Thread):
    """Timing thread to be run parallel to main thread.
            event (threading.Event): contains flag value to indicate to main thread when to clear buffer
            interval (float): time between buffer clears in seconds
            self.complete (bool): set to True when finished collecting trial data"""
    def __init__(self, event, interval):
        super().__init__()
        self.flush = event
        self.complete = False
        self.interval = interval

    def run(self):
        """Overrides run() from threading.Thread to indicate when the buffer should be flushed. Stops after the end of
           the ongoing interval when self.complete is set to True"""
        # wait appropriate time interval to fill buffer, then cause main thread to store data from buffer
        while not self.complete:
            while not self.flush.wait(self.interval):  # every interval:
                self.flush.set()  # sets flush to True

    def end(self):
        self.complete = True


# Trial and Session Parameters
samples = 8000  # number of samples to capture in one trial (3750 = 30 seconds)
total_trials = 5  # number of complete trials (sets of data) generated for this session
buffer_size = 1001  # 1000 = 8 seconds stored in the buffer at once (buffer is actually one less than this value)
break_time = 30  # time between trials in seconds
srate = 125  # 125 for Cyton/Daisy; 250 for Cyton only
channels = 16

# Meta Information
subj = "MC"
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

    flush = Event()
    # interval is a little under time to fill buffer to capture all samples
    timer = Timer(flush, .9*float(buffer_size/srate))

    print(f"Starting trial {trial_count}...\nRecording {samples} samples ({round(samples/srate, 2)} seconds) with a " +
          f"buffer size of {buffer_size} samples.")

    timer.start() # from timer thread, telling to start
    total = 0  # total samples recorded

    # flags are ways for threads to communicate. Assigns to events
    # flush is the flag that tells main thread to wait


    while total < samples:
        timer.flush.wait()  # wait until flush flag set to True
        timer.flush.clear()  # reset flush flag to False
        buf_count = board.get_board_data_count()
        board_data = board.get_board_data()
        # print(f"{buf_count} samples in buffer |", end="")

        if total + buf_count <= samples:
            try:  # to account for new sample being added between getting board data count and getting board data
                raw_data[:, total:total+buf_count] = board_data[data_rows[0]: data_rows[-1]+1]
                total += buf_count
            except ValueError:
                raw_data[:, total:total+buf_count+1] = board_data[data_rows[0]: data_rows[-1]+1]
                total += buf_count + 1
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
