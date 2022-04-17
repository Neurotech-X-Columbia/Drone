import numpy as np
from os import path
import tkinter as tk
import scipy.io

from DataClasses import Container
from VisualClasses import Plotter

inp = int(input("Blink dataset (0) or movement dataset (1): "))
root = tk.Tk()

if not inp:
    pathway = "Src\\EEG-EyeBlinks\\EEG-IO\\S06_data.csv"
    cwd = path.dirname(path.abspath(__file__))
    filepath = path.join(cwd, pathway)

    data = np.genfromtxt(filepath, delimiter=';', skip_header=True, usecols=(1, 2)).transpose()
    sample_freq = 250
    chan_names = ['FP1', 'FP2']

    con = Container(sample_freq, 2, data, chan_names)
    app = Plotter(con, channel_names=chan_names, datalimit=len(data[0, :])-1, master=root)
    app.mainloop()

else:
    pathway = "Src\\Subject1_1D.mat"
    cwd = path.dirname(path.abspath(__file__))
    filepath = path.join(cwd, pathway)
    mat = scipy.io.loadmat(filepath)
    baseline = mat['right']  # 64300 total samples (~128 seconds)

    chan_names = ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2',
                  'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ', 'CZ', 'PZ']
    sample_freq = 500

    con = Container(sample_freq, len(chan_names), baseline, chan_names)
    app = Plotter(con, channel_names=chan_names, datalimit=len(baseline[0, :]), master=root)
    app.mainloop()
