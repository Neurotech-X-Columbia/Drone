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

# Change to custom processing functions that take in only data as paremeters


def detect_blinks(data):  # DOES NOT WORK
    ch_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
                'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']
    mne_form = Container(125, 16, data, ch_names, lpass=7)
    locations = mne_form.detect_eog_events(["One, Two"])

    if locations.any():
        return 'a'


def procedure_one(data):
    if np.mean(data) <= 50:
        return 'a'
    else:
        return 'b'


def procedure_two(data):
    if np.median(data) <= 50:
        return 'a'
    else:
        return 'b'


def procedure_three(data):
    if np.median(data) > 50:
        return 'a'
    else:
        return 'b'


if __name__ == '__main__':
    buffer_size = 1001
    chunk_size = 500
    srate = 125
    serial_port = 'COM3'
    board_id = 2

    states = ['a', 'b']
    default = 'a'
    funcs = detect_blinks  # Tuple of processing functions to apply to every chunk. Should accept data and return state

    pro = Processor(states, default, funcs)
    process_loop(pro, *(buffer_size, chunk_size, srate, serial_port, board_id))
