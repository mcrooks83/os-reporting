import numpy as np
import pandas as pd
import math
import time
from scipy.signal import medfilt, butter, filtfilt, lfilter, find_peaks, find_peaks_cwt,resample, detrend
from scipy import integrate
import statistics


# pass in 3 sensors
def vector_magnitude(vectors):
    n = len(vectors[0])
    assert all(len(v) == n for v in vectors), "Vectors have different lengths"
    vm = np.sqrt(sum(v ** 2 for v in vectors))
    return vm

def build_filter(frequency, sample_rate, filter_type, filter_order):
    nyq = 0.5 * sample_rate

    if filter_type == "bandpass":
        nyq_cutoff = (frequency[0] / nyq, frequency[1] / nyq)
        b, a = butter(filter_order, (frequency[0], frequency[1]), btype=filter_type, analog=False, output='ba', fs=sample_rate)
    elif filter_type == "low":
        nyq_cutoff = frequency[1] / nyq
        b, a = butter(filter_order, frequency[1], btype=filter_type, analog=False, output='ba', fs=sample_rate)
    else:
        nyq_cutoff = frequency / nyq

    return b, a
                 
def filter_signal(b, a, signal, filter):
    if(filter=="lfilter"):
        return lfilter(b, a, signal)
    elif(filter=="filtfilt"):
        return filtfilt(b, a, signal)
    elif(filter=="sos"):
        return sosfiltfilt(sos, signal)
    

def compute_fft_mag(data):
    fftpoints = int(math.pow(2, math.ceil(math.log2(len(data)))))
    #print(fftpoints)
    fft = np.fft.fft(data, n=fftpoints)
    mag = np.abs(fft) / (fftpoints/2)
    return mag.tolist()


def compute_loading_intensity(fft_magnitudes, sampling_frequency, high_cut_off):
    fftpoints = int(math.pow(2, math.ceil(math.log2(len(fft_magnitudes)))))
    LI = 0
    fs = sampling_frequency
    fc = high_cut_off
    kc = int((fftpoints/fs)* fc) + 1

    magnitudes = fft_magnitudes

    f = []
    for i in range(0, int(fftpoints/2)+1):
        f.append((fs*i)/fftpoints)

    for k in range(0, kc):
        LI = LI + (magnitudes[k] * f[k])

    return LI


# main weight bearing function

def compute_weight_bearing(accel_x, accel_y, accel_z, sampling_rate, window, lc_off, hc_off, filter_order, filter_type):
    # build the filter
    b,a = build_filter((lc_off, hc_off), sampling_rate, filter_type, filter_order)
    
    accel_x = accel_x.to_numpy()  / 9.80665
    accel_y = accel_x.to_numpy()  / 9.80665
    accel_z = accel_x.to_numpy()  / 9.80665
    
    # chunk the data
    a_x = [accel_x[i:i + window] for i in range(0, len(accel_x), window)]
    a_y = [accel_y[i:i + window] for i in range(0, len(accel_y), window)]
    a_z = [accel_z[i:i + window] for i in range(0, len(accel_z), window)]
    
    # for each chunk
    li = []
    for idx, chunk in enumerate(a_x):
        a_mag = vector_magnitude([chunk, a_y[idx], a_z[idx]])
        filtered_mag = filter_signal(b,a, a_mag, "filtfilt")
        fft_mag = compute_fft_mag(filtered_mag)
        li_result = compute_loading_intensity(fft_mag, sampling_rate, hc_off)
        li.append(li_result)
        
    return li

# weight bearing per axis

# frequency response of an axis

