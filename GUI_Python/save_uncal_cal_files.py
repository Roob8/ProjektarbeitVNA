import Functions as fkt
import vnakit
import hidden as hid
import numpy as np

output_datei = r"C:\Users\RoobFlorian\Documents\Studium\Master\2. Semester\Projekt_Sommersemester\Messergebnisse\cal_files_VNA\thru.s2p"

ports = {'Tx1':6,'Rx1A':5,'Rx1B':4,'Tx2':3,'Rx2A':2,'Rx2B':1}
# intializes the board object
vnakit.Init()
# VNA Kit settings
settings = vnakit.RecordingSettings(
    vnakit.FrequencyRange(100, 6000, 5901), # fmin,fmax,num_points
    10, # RBW (in KHz)
    -10, # output power (dbM)
    ports['Tx1'], # transmitter port
    vnakit.VNAKIT_MODE_TWO_PORTS
)
vnakit.ApplySettings(settings)

sparams = fkt.single_measurement(vnakit, settings, "Tx1", ports)


#sparams = fkt.thru_measurement(vnakit, settings, ports)

freq_vec_MHz = np.array(vnakit.GetFreqVector_MHz())

hid.writeSnP(freq_vec_MHz, sparams, output_datei, freq_unit='MHz')