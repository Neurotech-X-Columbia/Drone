# To be used for data collection from Cyton/Daisy (16 channels 250 Hz)

from brainflow.board_shim import BoardShim, BrainFlowInputParams
from threading import Thread, Event

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from time import sleep

samples = 5000  # number of samples to capture in the entire session
srate = 250
buffer_size = 1000
channels = 16

subj = "MC"
date = "9-13"
filename = f"Recorded\\{int(samples/srate)}sec_{subj}_{date}.csv"

params = BrainFlowInputParams()
params.serial_port = 'COM3'  # or COM5 or COM4
board_id = 2  # 0 for cyton, #2 for cyton daisy, there is also an option for synthetic data
board = BoardShim(board_id, params)
data_rows = board.get_eeg_channels(board_id)

raw_data = np.empty((channels, samples), dtype=np.float64)  # container for session data


class Timer(Thread):  # sets flush to True every x seconds until raw_data is full
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


flush = Event()
timer = Timer(flush, float(2*buffer_size/srate))
board.prepare_session()
board.start_stream(buffer_size)
sleep(2)
timer.start()

total = 0  # total samples recorded
while total < samples:
    timer.flush.wait()  # wait until flush flag set to True
    timer.flush.clear()  # reset flush flag to False again
    buf_count = board.get_board_data_count()
    print(f"{board.get_board_data_count()} samples in buffer |", end="")
    if total + buf_count <= samples:
        raw_data[:, total:total+buf_count] = board.get_board_data()[data_rows[0]: data_rows[-1]+1]
        total += buf_count
    else:
        space = samples - total
        raw_data[:, total:samples] = board.get_board_data()[data_rows[0]: data_rows[-1]+1, :space]
        total += space

    print(f" {total} total samples recorded.")

timer.end()
board.stop_stream()
board.release_session()

fig, axs = plt.subplots(16)
print("raw_data shape is " + str(raw_data.shape))
for i, data_row in enumerate(raw_data):
    axs[i].plot(data_row)
plt.show()

pd.DataFrame(raw_data).to_csv(filename)
