import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
from vnakit_ex import getSettingsStr
from vnakit_ex.hidden import *
import vnakit

num_points = 1001
start_freq = 2500
end_freq = 3500

freq_array = np.arange(start_freq, end_freq, ((end_freq - start_freq)/(num_points-1))).tolist()
freq_array.append(end_freq)

print(freq_array)

S3P = readSnP(r'C:\Users\RoobFlorian\Downloads\ZHDC-16-63-S+_S3P\ZHDC-16-63-S+_AP160930_110216_UNIT-2.s3p', freq_desired=freq_array, kind='dB')

print(S3P)