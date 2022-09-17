import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq

data = pd.read_csv(r"C:\Users\mathe\PycharmProjects\Drone\signal_processing_scripts\Recorded\GG\6Hz\64sec_1.csv").to_numpy()
print(data.shape)
N = len(data[14,:])
fs = 125
Y = fft(data[14, :])
xf = fftfreq(N, 1/fs)[:N//2]
# freq = np.fft.fftfreq(len(data[0,:]), 1/fs)
plt.plot(xf[1:], 2.0/N*np.abs(Y[1:N//2]))
# plt.psd(data[14, :], Fs=125, NFFT=512)
plt.yscale('log')
plt.show()


