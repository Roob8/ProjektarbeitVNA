"""
Mini-Circuits Vayyar UVNA-63 demo script "demo_unknown_thru.py"
Description: Takes an two port measurement applying the unknown thru technique
"""
import numpy as np
from vnakit_ex import getSettingsStr, loadGammaListed
from vnakit_ex.hidden import prompt2PortSOLT, userMsg,ab2S_SwitchCorrect,\
                            measure2Port, get8TermModelUThru, \
                            correct8Term, plotCompareDb
import vnakit

def main():
    print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
    print(  '----------------------- Unknown Thru -----------------------\n')
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
    print('2-Port Calibration:')
    sol_stds = ['stds/open.S1P','stds/short.S1P','stds/load.S1P']
    Gamma_listed = loadGammaListed(sol_stds,freq_vec*1e6)
    (Gamma_meas_p1,Gamma_meas_p2,Thru_meas) = \
        prompt2PortSOLT(vnakit,settings,ports,isolation=False)
    print('Constructing 8-Term Error Model..')
    (A,B,q) = get8TermModelUThru(Gamma_listed,Gamma_meas_p1,
        Gamma_listed,Gamma_meas_p2,Thru_meas,freq_vec*1e6)
    # calibration is now complete (by having obtained the error terms)
    # now enter a loop that takes a measurement and plots the results
    while(1):
        userMsg('>> Measure DUT:')
        print('Recording...',end='')
        (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
        print('Done.\n')
        S_param_meas = ab2S_SwitchCorrect(rec_tx1,rec_tx2,ports)
        print('Applying 8-Term Model Correction...')
        S_param = correct8Term(S_param_meas,A,B,q)
        print('Plotting...')
        plotCompareDb(freq_vec,[S_param_meas,S_param],
            ['Uncorrected','8-Term Model (w/ unknown-thru) Correction'])

if __name__ == '__main__':
    main()
