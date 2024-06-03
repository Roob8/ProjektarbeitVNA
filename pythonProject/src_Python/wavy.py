# wavy.py
# Introduction to the Vayyar Board.
# Connect a thru line between two ports on the board and see the transmitted wave!
# Set the transmit port and receive port on lines 20 and 21.

import_from_src = True
if import_from_src:
    # To develop using the source code, import from: "utils.py" and "hidden.py" instead
    from utils import getSettingsStr
else:
    # To develop using the built-in library, import from the "vnakit_ex" module
    from vnakit_ex import getSettingsStr

import sys
#try if not aready imported
if 'matplotlib' not in sys.modules:
    import matplotlib
    matplotlib.use('TkAgg')
else:
    #import for spyder users
    import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import vnakit

print('\n------------ DEMO: wavy.py ------------\n')

# Intialize the Vayyar board
vnakit.Init()

# Define Settings for the Board
rx_num = 3 #Reciever Port to be read from
tx_num = 6 #Transmitter Port {VNAKit.RecordingSettings.txTr}
LF = 100 #Start Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStartMHz}
UF = 6000 #Stop Freq. (MHz) {VNAKit.RecordingSettings.freqRange.freqStopMHz}
PTS = 236 #Num Freq. Pts (MHz) {VNAKit.RecordingSettings.freqRange.numFreqPoints}
RBW = 1 #Resolution BW (KHz) {VNAKit.RecordingSettings.rbw_khz}
PWR = -10 #Tx Power setting (dBm) {VNAKit.RecordingSettings.outputPower_dbm)
#VNA Kit Mode {VNAKit.RecordingSettings.mode}
MODE = vnakit.VNAKIT_MODE_TWO_PORTS

# Create RecordingSettings Object and apply settings to the board
settings = vnakit.RecordingSettings(vnakit.FrequencyRange(LF,UF,PTS),RBW,PWR,tx_num,MODE)
vnakit.ApplySettings(settings)

print('The board is initialized with settings:\n')
print(getSettingsStr(settings))

# Record a single frequency sweep
print('Recording...',end='')
vnakit.Record()
print('Done.\n')
rec = vnakit.GetRecordingResult()

# Returns the frequency vector rounded
# to the nearest allowable frequency point
freq_vec_Hz = vnakit.GetFreqVector_MHz()

# Plot magnitude of Rx output
print('Plotting...')
plt.figure()
plt.plot(freq_vec_Hz, np.abs(rec[rx_num]))
plt.title('wavy.py')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Magnitude')
plt.xlim([500,6000])
#plt.ylim([0,1.5])
plt.legend(['Transceiver #'+str(rx_num)], loc='upper right')
plt.show()
