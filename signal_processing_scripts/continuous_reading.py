from MNE_Tests.DataClasses import Stream, Container
from MNE_Tests.VisualClasses import Plotter
import tkinter as tk

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

stream = Stream(srate=sample_freq, ch_names=chan_names, port='COM4')
stream.start_stream()

data = stream.collect(time=10)

stream.stop_stream()
stream.close_port()

root = tk.Tk()
con = Container(sample_freq, 2, data, chan_names)
app = Plotter(con, channel_names=chan_names, datalimit=len(data[0, :])-1, master=root)
app.mainloop()
