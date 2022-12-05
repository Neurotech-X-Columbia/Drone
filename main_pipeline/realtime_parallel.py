import mne
import numpy as np

from time import ctime
from PipelineClasses import Headset, SimulatedHeadset, Processor

# import random


def process_loop(proc, *hs_params):
    # headset = Headset(*hs_params)
    # headset.initialize()
    # headset.start_stream()

    headset = SimulatedHeadset(*hs_params)

    chunk_num = 0
    while headset.is_active:
        try:
            start = int(chunk_num * ((1-overlap)*window_size))
            end = start + window_size

            if (chunk := headset.collect()).any():
                proc.process_chunk(chunk)
                chunk_num += 1

            new = proc.get_state()
            proc.log_change(start, end, new_state=new)

            print(f"State: {new}")

        except KeyboardInterrupt:
            headset.end_stream()
            print("Session end.")

    proc.close_log()

# Change to custom processing functions that take in only data as parameters and return a state as output


def detect_blinks(data):  # Accepts data and returns the number of blinks detected in it
    chan_names = ['FP1', 'FP2']
    sample_freq = 250
    lpass = 1
    hpass = 10
    mne_info = mne.create_info(chan_names, sample_freq, 'eeg')

    raw_mne = mne.io.RawArray(data, info=mne_info)
    raw_mne.filter(l_freq=lpass, h_freq=hpass)
    threshold = (np.max(raw_mne[0][0]) - np.min(raw_mne[0][0])) / 4
    eog_events = mne.preprocessing.find_eog_events(raw_mne, ch_name=["FP1", "FP2"], thresh=threshold)
    locations = eog_events[:, 0] / sample_freq

    if len(locations):
        state = 'blink'
    else:
        state = 'no blink'

    return state


if __name__ == '__main__':
    # For both live and simulated
    window_size = 250

    # For live data collection
    srate = 125
    serial_port = 'COM3'
    board_id = 2

    # For simulated data collection
    overlap = 0
    datapath = "signal_processing_scripts\\Src\\EEG-EyeBlinks\\EEG-IO\\S06_data.csv"
    logfilename = "log.txt"

    states = ['blink', 'no blink']
    default = 'no blink'

    # Tuple of processing functions to apply to every chunk. Should accept data and return state
    funcs = (detect_blinks)

    pro = Processor(states, default, funcs, logfile=logfilename)

    hs_params = (window_size, srate, serial_port, board_id)
    shs_params = (window_size, overlap, datapath)
    process_loop(pro, *shs_params)
