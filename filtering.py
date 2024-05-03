# Importing packages and libraries 
import numpy as np 
import pandas as pd 
from scipy import signal 
from scipy.signal import find_peaks, filtfilt, butter


# making the high pass function 

def high_pass_fct(data):
    # making the filter 
    sos = signal.butter(2,2,'hp', fs=30, output= 'sos')
    # applying the filter to the data 
    filtered = signal.sosfilt(sos, data )
    # cutting off the first 50 data points 
    end= len(data)
    filtered_signal = filtered[50:end]
    return filtered_signal


