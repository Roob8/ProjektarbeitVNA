import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import skrf as rf
from vnakit_ex import getSettingsStr
from vnakit_ex.hidden import *
import vnakit

f_start = 2000
f_stop = 2600
num_p = 601

RBW = 1
power = -10
output_port = 'Tx1'


ports = {'Tx1': 6, 'Rx1A': 5, 'Rx1B': 4, 'Tx2': 3, 'Rx2A': 2, 'Rx2B': 1}

portNumber = ports[output_port]

vnakit.Init()

settings = vnakit.RecordingSettings(vnakit.FrequencyRange(f_start, f_stop, num_p), RBW, power, portNumber, vnakit.VNAKIT_MODE_TWO_PORTS)

vnakit.ApplySettings(settings)

settings_str = getSettingsStr(settings)
print(settings_str)

(rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)

print(rec_tx1)
print(rec_tx2)