import mne
import numpy as np
# import random

from time import ctime
from PipelineClasses import Headset, Processor
from ProcessingFunctions import detect_blinks


def process_loop(proc, *hs_params):
    headset = Headset(*hs_params)
    headset.initialize()
    headset.start_stream()

    chunk_num = 0
    while headset.is_active:
        try:
            if (chunk := headset.collect()).any():
                proc.process_chunk(chunk)
                chunk_num += 1

            new = proc.get_state()
            print(f"State: {new}")

        except KeyboardInterrupt:
            headset.end_stream()
            print("Session end.")


if __name__ == '__main__':
    # For both live and simulated
    window_size = 250

    # For live data collection
    srate = 125
    serial_port = 'COM3'
    board_id = 2

    states = ['blink', 'no blink']
    default = 'no blink'

    # Tuple of processing functions to apply to every chunk. Should accept data and return state
    funcs = (detect_blinks)

    pro = Processor(states, default, funcs, logfile=None)

    hs_params = (window_size, srate, serial_port, board_id)
    process_loop(pro, *hs_params)
