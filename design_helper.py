#this is a file to test what we design filter
import pickle 
from scipy.fft import fft, fftfreq, fftshift
import numpy as np
import matplotlib.pyplot as plt

def load_data(path):
    f = open(path, 'rb')
    d = pickle.load(f)
    f.close()
    return d

def mag2db(mag):
    return 20*np.log(mag)

d_noise = np.array(load_data("./data/data_clip_noise.dat"))
d_true = np.array(load_data("./data/data_clip_true.dat"))

N_noise = len(d_noise)
N_true =  len(d_true)
Fs = 30.0

xf_noise = fftshift(fftfreq(N_noise, 1/Fs))
yf_noise=fftshift(fft(d_noise))
xf_true = fftshift(fftfreq(N_true, 1/Fs))
yf_true = fftshift(fft(d_true))


plt.plot(xf_noise, mag2db(abs(yf_noise)), label="noise")
plt.plot(xf_true, mag2db(abs(yf_true)), label="detected data")
plt.legend()


plt.show()