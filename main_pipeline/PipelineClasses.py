from brainflow.board_shim import BoardShim, BrainFlowInputParams
from time import sleep


class Headset:
    def __init__(self, buffer_size, chunk_size, srate, serial_port, board_id=2):
        self.serial_port = serial_port
        self.bid = board_id
        self.buf_size = buffer_size + 1
        self.chk_size = chunk_size
        self.srate = srate

        self.is_active = False
        self.drows = None
        self.board = None

        if self.chk_size > self.buf_size:
            raise BufferSizeException("Headset buffer size must be larger than chunksize.")

    def initialize(self):
        params = BrainFlowInputParams()
        params.serial_port = self.serial_port
        self.board = BoardShim(self.bid, params)
        self.board.disable_board_logger()
        self.drows = self.board.get_eeg_channels(self.bid)

    def start_stream(self):
        if not self.is_active:
            print("Cannot start stream before initializing headset.")
            return

        self.board.prepare_session()
        while not self.board.is_prepared():
            sleep(.5)
        self.board.start_stream(self.buf_size)
        sleep(2)  # wait for stream to stabilize
        self.is_active = True

    def end_stream(self):
        self.board.stop_stream()
        self.board.release_session()
        self.is_active = False

    def collect(self):
        return self.board.get_board_data(self.chk_size)[self.drows[0]: self.drows[-1]+1]


class Processor:
    def __init__(self, states, default_state, *proc_funcs):
        self.states = states
        self.current = default_state
        self.proc_funcs = proc_funcs
        self.state_dict = {}

    def process_chunk(self, data):
        for state in self.states:
            self.state_dict[state] = 0

        for func in self.proc_funcs[0]:
            self.state_dict[func(data)] += 1

        self.update_state()

    def update_state(self):
        state_counts = list(zip(self.states, [self.state_dict[st] for st in self.states]))
        state_counts.sort(key=lambda x: x[1])

        self.current = state_counts[-1][0]

    def get_state(self):
        return self.current


class BufferSizeException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message