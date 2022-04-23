from MNE_Tests.DataClasses import Stream, Container
from MNE_Tests.VisualClasses import Plotter
import numpy as np
import tkinter as tk
import time
import brainflow

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']


def brainflow_collect(samples):
    params = brainflow.BrainFlowInputParams()
    params.serial_port = "COM4"
    board_id = 2
    board = brainflow.board_shim.BoardShim(board_id, params)

    board.prepare_session()
    board.start_stream()
    time.sleep(int(samples/sample_freq))
    data = board.get_board_data(samples)
    board.stop_stream()
    board.release_session()
    data_rows = board.get_eeg_channels(2)

    return data[1:17, :]


# with Stream(srate=sample_freq, nchans=16, ch_names=chan_names, port='COM4') as stream:
#     stream.start_stream()
#     data = stream.collect(duration=10, fname="10secondtest", write=False)
#
#     root = tk.Tk()
#     con = Container(sample_freq, len(chan_names), data, chan_names)
#     app = Plotter(con, channel_names=chan_names, datalimit=len(data[0, :]) - 1, master=root)
#     app.mainloop()


# data = np.genfromtxt("Recorded\\10secondtest.txt")


data = brainflow_collect(2500)

root = tk.Tk()
con = Container(sample_freq, len(chan_names), data, chan_names)
app = Plotter(con, channel_names=chan_names, datalimit=len(data[0, :])-1, master=root)
app.mainloop()
