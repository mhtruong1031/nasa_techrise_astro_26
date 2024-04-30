import numpy as np
import pandas as pd

from scipy.signal import butter,filtfilt
import matplotlib.pyplot as plt

# Filter requirements.
T = 10.0         # Sample Period
fs = 30.0       # sample rate, Hz
cutoff = .5      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
nyq = 0.5 * fs  # Nyquist Frequency
order = 5       # sin wave can be approx represented as quadratic
n = int(T * fs) # total number of samples

df = pd.read_csv('resources/sample_data.csv')
data = df['y']


def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

x = df['x']
y = butter_lowpass_filter(data, cutoff, fs, order)

plt.scatter(x, data, s=3)
plt.plot(x, y, c='r')
plt.title("Low Pass Filtering Algorithm")
plt.ylabel("Height")
plt.show()