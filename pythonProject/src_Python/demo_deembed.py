"""
Mini-Circuits Vayyar UVNA-63 demo script "demo_deembed.py"
Description: Takes a two port measurement applying adapter deembedding
"""
import numpy as np

import_from_src = True
if import_from_src:
    # To develop using the source code, import from: "utils.py" and "hidden.py" instead
    from utils import getSettingsStr, loadGammaListed
    from hidden import readSnP, prompt2PortSOLT, get12TermModel, deEmbed, \
                                measure2Port, ab2S, correct12Term, plotCompareDb, \
                                userMsg
else:                          
    # To develop using the built-in library, import from the "vnakit_ex" module
    from vnakit_ex import getSettingsStr, loadGammaListed
    from vnakit_ex.hidden import readSnP, prompt2PortSOLT, get12TermModel, deEmbed, \
                                measure2Port, ab2S, correct12Term, plotCompareDb, \
                                userMsg

import vnakit

def main():
    print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
    print(  '---------------------- De-Embedding ------------------------\n')
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
    Thru_listed = readSnP('stds/thru.S2P',freq_desired=freq_vec*1e6)
    (Gamma_meas1,Gamma_meas2,Thru_meas) = \
        prompt2PortSOLT(vnakit,settings,ports,isolation=False)
    print('Constructing 12-Term Error Model..')
    (fwd_terms,rev_terms) = get12TermModel(Gamma_listed,Gamma_meas1,
        Gamma_listed,Gamma_meas2,Thru_listed,Thru_meas)
    # calibration is now complete (by having obtained the error terms)
    # now measure the adapter(s) to be de-embedded
    S_adapter=[[],[]]
    N=1
    while(1):
        if N==1 or (N==2 and type(S_adapter[0])==np.ndarray):
            x=userMsg('>> Measure Port-'+str(N)+' adapter? (y/n):')
        else:
            x = 'Y'
            userMsg('>> Measure Port-2 adapter')
        if x.upper() in ['Y']:
            print('Recording...',end='')
            (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
            print('Done.\n')
            S_adapter_meas = ab2S(rec_tx1,rec_tx2,ports)
            S_adapter[N-1] = correct12Term(S_adapter_meas,fwd_terms,rev_terms)
            N=N+1
        elif x.upper() in ['N']:
            S_adapter[N-1] = []
            N=N+1
        else:
            print('Invalid option. Respond y or n')
            continue
        if N>2:
            break
        # we have measured the adapter to be removed from the measurement
        # now enter a loop that takes a measurement and plots the results
    while(1):
        userMsg('>> Measure DUT:')
        print('Recording...',end='')
        (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
        print('Done.\n')
        S_adapter_dut_meas = ab2S(rec_tx1,rec_tx2,ports)
        print('Applying 12-Term Model Correction...')
        S_adapter_dut = correct12Term(S_adapter_dut_meas,fwd_terms,rev_terms)
        print('De-embedding adapters...')
        S_dut = deEmbed(S_adapter_dut,S_adapter[0],S_adapter[1])
        print('Plotting...')
        plotCompareDb(freq_vec,[S_adapter_dut_meas,S_adapter_dut,S_dut],
            ['Uncorrected adapter-DUT device','Corrected adapter-DUT device','Corrected DUT'])

if __name__ == '__main__':
    main()
