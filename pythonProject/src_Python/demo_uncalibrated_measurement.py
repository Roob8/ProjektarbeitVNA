"""
Mini-Circuits Vayyar UVNA-63 demo script "Uncalibrated Measurement.py"
Description: Takes an uncalibrated two port measurement
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
import pickle

from utils import getSettingsStr
from hidden import ab2S, measure2Port, userMsg

import vnakit

from Funktionen.S_to_excel import SParam_to_ecxel

output_folder = 'output'
print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
print(  '----------------- Uncalibrated Measurement -----------------\n')

# VNA kit port mapping, defining the Transceiver ports (1,2,...,6)
# to the VNA ports ('Tx1',Rx1A',...,'Rx2B')
ports = {'Tx1':6,'Rx1A':5,'Rx1B':4,'Tx2':3,'Rx2A':2,'Rx2B':1}

# intializes the board object
vnakit.Init()

# VNA Kit settings
settings = vnakit.RecordingSettings(
    vnakit.FrequencyRange(100, 6000, 1001), # fmin,fmax,num_points
    10, # RBW (in KHz)
    -20, # output power (dbM)
    ports['Tx1'], # transmitter port
    vnakit.VNAKIT_MODE_TWO_PORTS
)
vnakit.ApplySettings(settings)

# actual frequency vector used by the board
freq_vec = np.array(vnakit.GetFreqVector_MHz())
print('The board is initialized with settings:\n')

# gets a formatted string of the board's settings. See vnakit_ex/utils.py
settings_str = getSettingsStr(settings)
print(settings_str)

# raw measurement of the DUT
print('Recording...',end='')
(rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
print('Done.\n')

# converting a/b waves to S-parameters
S_param_meas = ab2S(rec_tx1, rec_tx2, ports)

SParam_to_ecxel(settings, freq_vec, S_param_meas)

# a plot comparing the raw uncorrected measurement
# to the corrected S-paramter measurement in Log-Magnitude
fig, axes = plt.subplots(2,1)
DUT = rf.Network(s=S_param_meas, f=freq_vec, z0=50, f_unit='MHz')
DUT.plot_s_db(ax=axes[0])
DUT.plot_s_deg_unwrap(ax=axes[1])
axes[0].set_title('Uncalibrated S-Parameter Measurement')
plt.show()


