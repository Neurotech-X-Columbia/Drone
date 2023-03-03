import mne
import numpy as np

from time import ctime
from PipelineClasses import SimulatedHeadset, Processor
from ProcessingFunctions import detect_blinks

# import random


def process_loop(proc, *hs_params):
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


if __name__ == '__main__':
    # For both live and simulated
    window_size = 1000

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
