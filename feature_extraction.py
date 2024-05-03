import pandas as pd
from scipy.signal import find_peaks

def feature_extraction(segments):
    features = pd.DataFrame()

    systolic = []
    diastolic = []
    sys_peak_time = []
    dias_peak_time = []
    time_interval = []
    pulse_interval = []
    aug_index = []

    firstmax2= []
    secondmax2=[]
    thirdmax2=[]
    firstmin2=[]

    for seg in segments:
        feature_peaks, _ = find_peaks(seg)
        # Sys Amp
        systolic.append(seg[feature_peaks[0]])
        # Pulse Interval
        pulse_interval.append(len(seg))
        # Diastolic Amp
        if len(feature_peaks) > 1:
            diastolic.append(seg[feature_peaks[1]])
            # Diastolic Peak Time
            dias_peak_time.append(feature_peaks[1])
            # Delta Time
            time_interval.append(feature_peaks[1] - feature_peaks[0])
            # Augmentation Index (Diastolic:Systolic)
            aug_index.append(seg[feature_peaks[1]] / seg[feature_peaks[0]])
        else:
            diastolic.append(None)
            time_interval.append(None)
            aug_index.append(None)
            dias_peak_time.append(None)

        # Systolic Peak Time
        sys_peak_time.append(feature_peaks[0])

        # New feature extraction: Second derivative analysis
        second_deriv = np.diff(seg)
        peaks2, _ = find_peaks(second_deriv)

        if len(peaks2) >= 3:
            firstmax2.append(second_deriv[peaks2[0]])
            secondmax2.append(second_deriv[peaks2[1]])
            thirdmax2.append(second_deriv[peaks2[2]])
        elif len(peaks2) == 2:
            firstmax2.append(second_deriv[peaks2[0]])
            secondmax2.append(second_deriv[peaks2[1]])
            thirdmax2.append(None)
        elif len(peaks2) == 1:
            firstmax2.append(second_deriv[peaks2[0]])
            secondmax2.append(None)
            thirdmax2.append(None)
        else:
            firstmax2.append(None)
            secondmax2.append(None)
            thirdmax2.append(None)

        if len(peaks2) >= 1:
            firstmin2.append(second_deriv[peaks2[0]])
        else:
            firstmin2.append(None)

    # Store all features into the DataFrame
    features['Systolic Amp'] = systolic
    features['Diastolic Amp'] = diastolic
    features['Sys Peak Time'] = sys_peak_time
    features['Delta Time'] = time_interval
    features['Augmentation Index'] = aug_index
    features['Pulse Interval'] = pulse_interval

    # Features from second derivative analysis
    features['First Max of Second Deriv'] = firstmax2
    features['Second Max of Second Deriv'] = secondmax2
    features['Third Max of Second Deriv'] = thirdmax2
    features['First Min of Second Deriv'] = firstmin2

    return features