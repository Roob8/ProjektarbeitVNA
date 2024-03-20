"""
Mini-Circuits Vayyar UVNA-63 demo script "demo_response_cal.py"
Description: Takes a two port measurement applying a response calibration
"""
import numpy as np
from vnakit_ex import getSettingsStr
from vnakit_ex.hidden import prompt1PortMeasure,prompt2PortMeasure, \
                            getIdealSparams, get2PortResponseModel,userMsg,\
                            ab2S_SwitchCorrect,correctResponse,plotCompareDb,\
                            measure2Port
import vnakit

def main():
    print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
    print(  '------------------ Response Calibration --------------------\n')
    print(  '--------- Press Enter to continue. Type q to exit. ---------\n')
    # VNA kit port mapping
    ports = {'Tx1':6,'Rx1A':5,'Rx1B':4,'Tx2':3,'Rx2A':2,'Rx2B':1}
    # intializes the board object
    vnakit.Init()
    # VNA Kit settings
    settings = vnakit.RecordingSettings(
        vnakit.FrequencyRange(100, 6000, 236), # fmin,fmax,num_points
        1, # RBW (in KHz)
        -10, # output power (dbM)
        ports['Tx1'], # transmitter port
        vnakit.VNAKIT_MODE_TWO_PORTS
    )
    vnakit.ApplySettings(settings)
    # actual frequency vector used by the board
    freq_vec = np.array(vnakit.GetFreqVector_MHz())
    print('The board is initialized with settings:\n')
    settings_str = getSettingsStr(settings)
    print(settings_str)
    print('2-Port Response Calibration:')
    Gm1 = prompt1PortMeasure(vnakit,settings,ports,ports['Tx1'],name='Open')
    Gm2 = prompt1PortMeasure(vnakit,settings,ports,ports['Tx2'],name='Open')
    Tm  = prompt2PortMeasure(vnakit,settings,ports,name='Thru')
    print('Constructing Frequency Response Error Model...')
    (G_ideal,T_ideal) = getIdealSparams(len(freq_vec))
    G_open = G_ideal[:,0]
    H = get2PortResponseModel(G_open,Gm1,G_open,Gm2,T_ideal,Tm)
    # calibration is now complete (by having obtained the error terms)
    # now enter a loop that takes a measurement and plots the results
    while(1):
        userMsg('>> Measure DUT:')
        print('Recording...',end='')
        (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
        print('Done.')
        S_param_meas = ab2S_SwitchCorrect(rec_tx1,rec_tx2,ports)
        print('Applying Response Correction...')
        S_param = correctResponse(S_param_meas,H)
        print('Plotting...')
        plotCompareDb(freq_vec,[S_param_meas,S_param],
            ['Uncorrected','Frequency Response Correction'], settings_str)

if __name__ == '__main__':
    main()
