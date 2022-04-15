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

stream = Stream(srate=sample_freq, ch_names=chan_names, port='COM3')
stream.initialize_cyton()
stream.start_stream()

while True:
    print(stream.get_sample())
