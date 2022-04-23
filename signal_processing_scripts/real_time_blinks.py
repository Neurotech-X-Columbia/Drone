from MNE_Tests.DataClasses import Stream, Container

sample_freq = 250
chan_names = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve',
              'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen']

with Stream(srate=sample_freq, nchans=16, ch_names=chan_names, port='COM4') as stream:
    stream.start_stream()
    blink_count = 0
    while True:
        try:
            data = stream.collect(samples=750, fname="10secondtest", write=True)

            blink = False
            if blink:
                blink_count += 1
                print("BLINK " + str(blink_count))

        except KeyboardInterrupt:
            break
