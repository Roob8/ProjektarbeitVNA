"""
Mini-Circuits Vayyar UVNA-63 demo script "Uncalibrated Measurement.py"
Description: Takes an uncalibrated two port measurement
"""
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import skrf as rf

import_from_src = True
if import_from_src:
    # To develop using the source code, import from: "utils.py" and "hidden.py"
    from utils import getSettingsStr
    from hidden import ab2S, measure2Port, userMsg
else:
    # To develop using the built-in library, import from the "vnakit_ex" module instead
    from vnakit_ex import getSettingsStr
    from vnakit_ex.hidden import ab2S, measure2Port, userMsg


import vnakit

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
    vnakit.FrequencyRange(2400, 2600, 1001), # fmin,fmax,num_points
    10, # RBW (in KHz)
    -10, # output power (dbM)
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

S_param = ab2S(rec_tx1,rec_tx2,ports)
print(test)
