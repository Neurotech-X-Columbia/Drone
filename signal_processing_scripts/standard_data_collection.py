# To be used for data collection from Cyton/Daisy (16 channels 250 Hz)
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from MNE_Tests.DataClasses import Container
from MNE_Tests.VisualClasses import Plotter
from time import sleep
from threading import Thread, Event

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


samples = 3750  # number of samples to capture in the entire session (3750 = 30 seconds)
srate = 125  # 125 for Cyton/Daisy; 250 for Cyton only
buffer_size = 1001  # 1000 = 8 seconds stored in the buffer at once (buffer is actually one less than this value)
channels = 16

subj = "MC"
date = "9-13"
filename = f"Recorded\\{int(samples/srate)}sec_{subj}_{date}.csv"
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

params = BrainFlowInputParams()
params.serial_port = "COM3"  # check device manager on Windows
board_id = 2  # 0 for cyton, #2 for Cyton/Daisy, there is also an option for synthetic data
board = BoardShim(board_id, params)
board.disable_board_logger()
data_rows = board.get_eeg_channels(board_id)

raw_data = np.empty((channels, samples), dtype=np.float64)  # container for session data

flush = Event()
timer = Timer(flush, float(buffer_size/srate))  # interval defined as time it should take to fill the buffer
board.prepare_session()
while not board.is_prepared():
    sleep(.5)
board.start_stream(buffer_size)
sleep(2)  # wait for stream to stabilize

print(f"Starting session...\nRecording {samples} samples ({round(samples/srate, 2)} seconds) with a buffer size of " +
      f"{buffer_size} samples.")

timer.start()
total = 0  # total samples recorded
while total < samples:
    timer.flush.wait()  # wait until flush flag set to True
    timer.flush.clear()  # reset flush flag to False
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

pd.DataFrame(raw_data).to_csv(filename)

root = tk.Tk()
con = Container(srate, len(chan_names), raw_data, chan_names)
app = Plotter(con, channel_names=chan_names, datalimit=len(raw_data[0, :])-1, master=root)
app.mainloop()