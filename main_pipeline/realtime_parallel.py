import numpy as np
from PipelineClasses import Headset, Processor
from signal_processing_scripts.DataClasses import Container

# import random


def process_loop(proc, *hs_params):
    headset = Headset(*hs_params)
    headset.initialize()
    headset.start_stream()

    while headset.is_active:
        try:
            proc.process_chunk(headset.collect())
            print(f"State: {proc.get_state()}")
        except KeyboardInterrupt:
            headset.end_stream()
            print("Session end.")

    # active = True
    # while active:
    #     try:
    #         new_chunk = random.sample(range(0, 100), 50)
    #         proc.process_chunk(new_chunk)
    #         print(f"State: {proc.get_state()}")
    #     except KeyboardInterrupt:
    #         active = False
    #         print("Session end.")

# Change to custom processing functions that take in only data as parameters and return a state as output


def detect_blinks(data):
    if np.mean(data) <= 50:
        return 'blink'
    else:
        return 'no blink'


if __name__ == '__main__':
    window_size = 500
    srate = 125
    serial_port = 'COM3'
    board_id = 2

    states = ['blink', 'no blink']
    default = 'no blink'

    # Tuple of processing functions to apply to every chunk. Should accept data and return state
    funcs = (detect_blinks)

    pro = Processor(states, default, funcs)
    process_loop(pro, *(window_size, srate, serial_port, board_id))
