from MNE_Tests.DataClasses import Stream, Container
from MNE_Tests.VisualClasses import Plotter
import tkinter as tk

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

with Stream(srate=sample_freq, ch_names=chan_names, port='COM4') as stream:
    stream.start_stream()
    data = stream.collect(duration=10, fname="10secondtest.txt")

root = tk.Tk()
con = Container(sample_freq, len(chan_names), data, chan_names)
app = Plotter(con, channel_names=chan_names, datalimit=len(data[0, :])-1, master=root)
app.mainloop()
