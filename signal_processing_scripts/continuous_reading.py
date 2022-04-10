import numpy as np
from os import path
import tkinter as tk
import scipy.io

from simulate import Stream
from visualize import Plotter

root = tk.Tk()
sample_freq = 250
chan_names = ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2',
              'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ', 'CZ', 'PZ']

stream = Stream(sample_freq, len(chan_names), chan_names)

while True:
    data = stream.get_chunk(1000)

    sim = Simulator(sample_freq, 2, data, chan_names)
    app = Plotter(sim, channel_names=chan_names, datalimit=len(data[0, :])-1, master=root)
    app.mainloop()
