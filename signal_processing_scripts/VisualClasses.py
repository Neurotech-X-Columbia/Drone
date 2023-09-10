"""GUI for visualizing raw data and data after basic processing (one channel at a time)"""
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk


class Plotter(ttk.Frame):
    """Displays plots and controls for visualizer"""
    def __init__(self, simulator, datalimit, channel_names, master=None):
        super().__init__(master)
        self.main_frame = tk.Frame(self.master, background="white")
        self.main_frame.grid()
        self.configure_gui()

        self.menu = ParamMenu(self.main_frame, channel_names, int(datalimit/simulator.srate))
        self.menu.grid(column=1, rowspan=2, sticky='nsew')

        self.run_button = tk.Button(self.menu, text="RUN", width=10,
                                    font=tk.font.Font(size=15, family="Calibri"),
                                    command=self.update_and_run)
        self.run_button.grid(column=1, row=7, pady=10)

        self.ch_names = channel_names
        self.sim = simulator
        self.datalim = datalimit

        self.raw = self.draw_raw(simulator, chan=channel_names[0], end=datalimit)
        self.proc = self.draw_proc(simulator, chan=channel_names[0], end=datalimit)

    def configure_gui(self):
        self.master.title("Processing Plotter")
        self.master.maxsize(1375, 510)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

    def draw_raw(self, simulator, end, chan, start=0.0):
        raw = EmbeddedPlot(self.main_frame, simulator.plot_raw(start, end, channel=chan))
        raw.grid(column=0, row=0)
        raw.plot()

        return raw

    def draw_proc(self, simulator, end, chan, start=0.0, lpass=15, hpass=30, eog=False):
        proc_fig = simulator.plot_processed(start, end, channel=chan, lpass=lpass, hpass=hpass, eog=eog)
        proc = EmbeddedPlot(self.main_frame, proc_fig)
        proc.grid(column=0, row=1)
        proc.plot()

        return proc

    def update_and_run(self):
        self.raw.clear()
        self.proc.clear()

        low = int(self.menu.lpass.get())
        high = int(self.menu.hpass.get())
        start = float(self.menu.st_ent.get())
        end = float(self.menu.end_ent.get())
        channel = self.menu.menuvar.get()
        eog = self.menu.check_var.get()

        if not low:
            low = None
        if not high:
            high = None

        self.raw = self.draw_raw(self.sim, start=start, end=end, chan=channel)
        self.proc = self.draw_proc(self.sim, start=start, end=end, lpass=low, hpass=high, chan=channel, eog=eog)


class EmbeddedPlot(tk.Frame):
    def __init__(self, main_frame, figure):
        super().__init__(main_frame, background="white", borderwidth=2.5, relief='solid')
        self.figure = figure
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def plot(self):
        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(column=0, row=0)

    def clear(self):
        self.figure.clf()
        self.destroy()


class ParamMenu(tk.Frame):
    def __init__(self, main_frame, c_names, maxi):
        super().__init__(main_frame, background="white", borderwidth=2.5, relief='solid')

        self.title_font = tk.font.Font(size=25, weight="bold", family="Calibri")
        self.menu_font = tk.font.Font(size=15, family="Calibri")

        self.lpass = ttk.Entry(self, font=self.menu_font, width=5, textvariable=tk.StringVar())
        self.lpass.insert(0, "15")

        self.hpass = ttk.Entry(self, font=self.menu_font, width=5, textvariable=tk.StringVar())
        self.hpass.insert(0, "30")

        self.st_ent = ttk.Entry(self, font=self.menu_font, width=5, textvariable=tk.StringVar())
        self.st_ent.insert(0, "0")

        self.end_ent = ttk.Entry(self, font=self.menu_font, width=5, textvariable=tk.StringVar())
        self.end_ent.insert(0, str(maxi))

        self.check_var = tk.IntVar()
        self.blink_check = tk.Checkbutton(self, font=self.menu_font, variable=self.check_var, text="Detect EOG events",
                                          background="white")

        self.menuvar = tk.StringVar()
        self.ch_select = ttk.OptionMenu(self, self.menuvar, c_names[0], *c_names)

        self.create_menu()

    def create_menu(self):
        yspace = 5

        title = ttk.Label(self, text="Processing Parameters", font=self.title_font,
                          background="white")
        title.grid(column=0, columnspan=3, padx=25, pady=yspace)

        self.ch_select.grid(column=1, row=1, sticky='e')
        ch_label = ttk.Label(self, font=self.menu_font, text="Channel: ", background="white")
        ch_label.grid(column=1, row=1, sticky='w', pady=yspace)

        self.lpass.grid(column=1, row=2, sticky='e')
        lplabel = ttk.Label(self, font=self.menu_font, text="Frequency Min: ", background="white")
        lplabel.grid(column=1, row=2, sticky='w', pady=yspace)

        self.hpass.grid(column=1, row=3, sticky='e')
        hplabel = ttk.Label(self, font=self.menu_font, text="Frequency Max: ", background="white")
        hplabel.grid(column=1, row=3, sticky='w', pady=yspace)

        self.st_ent.grid(column=1, row=4, sticky='e')
        stlabel = ttk.Label(self, font=self.menu_font, text="Start Time: ", background="white")
        stlabel.grid(column=1, row=4, sticky='w', pady=yspace)

        self.end_ent.grid(column=1, row=5, sticky='e')
        stlabel = ttk.Label(self, font=self.menu_font, text="End Time: ", background="white")
        stlabel.grid(column=1, row=5, sticky='w', pady=yspace)

        self.blink_check.grid(column=1, row=6)

        col_num = 3
        row_num = 6
        for x in range(col_num):
            self.columnconfigure(x, weight=1)
        for x in range(row_num):
            self.rowconfigure(x, weight=1)
