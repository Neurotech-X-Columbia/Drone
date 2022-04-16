from MNE_Tests.DataClasses import Stream

sample_freq = 250
chan_names = ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2',
              'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ', 'CZ', 'PZ']

stream = Stream(srate=sample_freq, ch_names=chan_names, port='COM4')
stream.start_stream()

while True:
    try:
        print(stream.get_sample())
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close_port()
        break
