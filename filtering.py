# This script is for filtering the raw data and segmenting into individual waveforms 

# Importing packages and libraries 
import numpy as np 
import pandas as pd 
from scipy import signal 
from scipy.signal import find_peaks, filtfilt, butter
import statsmodels.stats.stattools


# making the high pass function (input:IR data, output:filtered signal)

def high_pass_fct(data):
    # making the filter 
    sos = signal.butter(2,2,'hp', fs=30, output= 'sos')
    # applying the filter to the data 
    filtered = signal.sosfilt(sos, data )
    # cutting off the first 50 data points 
    end= len(data)
    filtered_signal = filtered[50:end]
    return filtered_signal

# making the segmentation function (input: filtered signal, output:acceptable segments)

def segmentation_fct(filtered_signal):
    # finding the bottom peaks
    peaks,_ = find_peaks(-filtered_signal,height=70)
    # making an array of segments 
    all_segments= []
    segments= []
    skewness_values= []
    i = 0
    for i in range(len(peaks)-1):
        all_segments.append(filtered_signal[peaks[i]:peaks[i+1]])
    # calculating skewness values for segments and making a new segment array 
    for segment in all_segments:
        if statsmodels.stats.stattools.robust_skewness(segment,0)[1] > 0:
            segments.append(segment)  
            skewness_values.append(statsmodels.stats.stattools.robust_skewness(segment,0)[1] )    
    return(segments, skewness_values)
    
