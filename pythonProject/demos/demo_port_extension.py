"""
Mini-Circuits Vayyar UVNA-63 demo script "demo_port_extension.py"
Description: Applies 12-Term correction and port extensions
             to correct for fixturing
"""
import numpy as np
from vnakit_ex import getSettingsStr, loadGammaListed
from vnakit_ex.hidden import readSnP, prompt2PortSOLT, get12TermModel, \
                            measure2Port, ab2S, correctPortExt, userMsg,\
                            correct12Term, plotCompareDb, getPortExtModel,\
                            getIdealSparams
import vnakit

def main():
    print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
    print(  '---------------------- Port Extension ----------------------\n')
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
    # now measure the port extensions
    (G_ideal,T_ideal) = getIdealSparams(len(freq_vec))
    G_open = G_ideal[:,0]
    while(1):
        port_num = 0;
        while(port_num not in [1,2]):
            port_num = userMsg('>> Port Extend @:\n[1] Port-1\n[2] Port-2\n>> ');
            if port_num.isdigit():
                port_num=int(port_num)
        userMsg('>> Measure OPEN @ Port-'+str(port_num)+': ')
        print('Recording...',end='')
        (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
        print('Done.\n')
        S_ext_meas = ab2S(rec_tx1,rec_tx2,ports)
        S_ext = correct12Term(S_ext_meas,fwd_terms,rev_terms)
        G_ext = S_ext[:,port_num-1,port_num-1]
        print('Getting Port Extension Model...')
        e10e01 = getPortExtModel(G_ext, G_open)
        # we have measured the port extensions to be removed from the measurement
        # now enter a loop that takes a measurement and plots the results
        while(1):
            userMsg('>> Measure DUT:')
            print('Recording...',end='')
            (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
            print('Done.\n')
            S_ext_dut_meas = ab2S(rec_tx1,rec_tx2,ports)
            print('Applying 12-Term Model Correction...')
            S_ext_dut = correct12Term(S_ext_dut_meas,fwd_terms,rev_terms)
            print('Port Extending at Port-'+str(port_num)+'...')
            S_dut = correctPortExt(S_ext_dut,e10e01,port_num)
            print('Plotting...')
            plotCompareDb(freq_vec,[S_ext_dut_meas,G_ext,S_ext_dut,S_dut],
                ['Uncorrected S-Params','Extension Reflection Coefficient',
                'Corrected Extension-DUT device','Corrected DUT'])

if __name__ == '__main__':
    main()
