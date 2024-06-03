"""
Mini-Circuits Vayyar UVNA-63 demo script "Uncalibrated Measurement.py"
Description: Takes an uncalibrated two port measurement
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import skrf as rf

from utils import getSettingsStr
from hidden import ab2S, measure2Port, userMsg

import vnakit
from Funktionen.sKompl_2_sLog import sKompl_2_sLog
from Funktionen.save_measurements import save_measurements
import pickle

output_folder = 'output'
print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
print(  '----------------- Uncalibrated Measurement -----------------\n')

# VNA kit port mapping, defining the Transceiver ports (1,2,...,6)
# to the VNA ports ('Tx1',Rx1A',...,'Rx2B')
ports = {'Tx1':6,'Rx1A':5,'Rx1B':4,'Tx2':3,'Rx2A':2,'Rx2B':1}

# intializes the board object
# vnakit.Init()

# VNA Kit settings
'''
settings = vnakit.RecordingSettings(
    vnakit.FrequencyRange(100, 6000, 1001), # fmin,fmax,num_points
    10, # RBW (in KHz)
    -20, # output power (dbM)
    ports['Tx1'], # transmitter port
    vnakit.VNAKIT_MODE_TWO_PORTS
)
'''
with open('Pickle/settings.pkl', 'rb') as file:     # Daten laden
    settings = pickle.load(file)

# vnakit.ApplySettings(settings)

# actual frequency vector used by the board
# freq_vec = np.array(vnakit.GetFreqVector_MHz())

with open('Pickle/freq_vec.pkl', 'rb') as file:     # Daten laden
    freq_vec_Hz = pickle.load(file)

print('The board is initialized with settings:\n')

# gets a formatted string of the board's settings. See vnakit_ex/utils.py
settings_str = getSettingsStr(settings)
print(settings_str)

# raw measurement of the DUT
print('Recording...',end='')
#(rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)

with open('Pickle/rec_tx1.pkl', 'rb') as file:     # Daten laden
    rec_tx1 = pickle.load(file)
with open('Pickle/rec_tx2.pkl', 'rb') as file:     # Daten laden
    rec_tx2 = pickle.load(file)

# converting a/b waves to S-parameters
s_param_kompl = ab2S(rec_tx1, rec_tx2, ports)
s_param_dB = sKompl_2_sLog(s_param_kompl, freq_vec_Hz)

save_measurements(settings, s_param_dB, 'Ausgaben', "DUT_meas")

# a plot comparing the raw uncorrected measurement
# to the corrected S-paramter measurement in Log-Magnitude
fig, axes = plt.subplots(2,1)
DUT = rf.Network(s=s_param_kompl, f=freq_vec_Hz, z0=50, f_unit='MHz')
DUT.plot_s_db(ax=axes[0])
DUT.plot_s_deg_unwrap(ax=axes[1])
axes[0].set_title('Uncalibrated S-Parameter Measurement')
plt.show()


