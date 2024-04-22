"""
Mini-Circuits Vayyar UVNA-63 demo script "demo_full_2_port.py"
Description: Takes a two port corrected measurement by applying an SOLT
calibration to a 12-term error model. Plots S-Parameters of uncalibrated and
calibrated measurements side by side and outputs SnP files: 'DUT.S2P' and
'DUT_uncorrected.S2P' for the corrected and uncorrected S-Parameters
respectively. This script is a good reference for new UVNA applications.
"""
import numpy as np

import_from_src = True
if import_from_src:
    # To develop using the source code, import from: "utils.py" and "hidden.py"
    from utils import getSettingsStr, loadGammaListed
    from hidden import userMsg,readSnP,prompt2PortSOLT,get12TermModel,\
                       measure2Port,ab2S,correct12Term,plotCompareDb,writeSnP
else:
    # To develop using the built-in library, import from the "vnakit_ex" module instead
    from vnakit_ex import getSettingsStr, loadGammaListed
    from vnakit_ex.hidden import userMsg,readSnP,prompt2PortSOLT,get12TermModel,\
                                measure2Port,ab2S,correct12Term,plotCompareDb,writeSnP

import vnakit

def main():
    print('\n------------ DEMO: Mini-Circuits Vayyar VNA kit ------------\n')
    print(  '------------ Data-Based 2-Port SOLT Calibration ------------\n')
    print(  '--------- Press Enter to continue. Type q to exit. ---------\n')
    # VNA kit port mapping, defining the Transceiver ports (1,2,...,6)
    # to the VNA ports ('Tx1',Rx1A',...,'Rx2B')
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
    # gets a formatted string of the board's settings. See vnakit_ex/utils.py
    settings_str = getSettingsStr(settings)
    print(settings_str)
    print('-- 2-Port Calibration --')
    # filenames of the open, short, load standards
    sol_stds = ['stds/open.S1P','stds/short.S1P','stds/load.S1P']
    # puts the reflection coefficents of the SOL standards in single array.
    # Also interpolates in frequency. See vnakit_ex/utils.py
    Gamma_listed = loadGammaListed(sol_stds,freq_vec*1e6)
    # loads S-parameter data of the thru standard, interpolates frequency
    Thru_listed = readSnP('stds/thru.S2P',freq_desired=freq_vec*1e6)
    # prompts user for SOLT measurements and returns raw measured
    # SOLT reflection coefficents and S-parameters
    (Gamma_meas_p1,Gamma_meas_p2,Thru_meas) = \
        prompt2PortSOLT(vnakit,settings,ports,isolation=False)
    # constructs the 12-term model from the standards data and the data measured
    # from the prompt.
    print('Constructing 12-Term Error Model...')
    (fwd_terms,rev_terms) = get12TermModel(Gamma_listed,Gamma_meas_p1,
        Gamma_listed,Gamma_meas_p2,Thru_listed,Thru_meas)
    # calibration is now complete (by having obtained the error terms)
    # now enter a loop that takes a measurement and plots the results
    while(1):
        # raw measurement of the DUT
        userMsg('>> Measure DUT:')
        print('Recording...',end='')
        (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
        print('Done.\n')
        # converting a/b waves to S-parameters
        S_param_meas = ab2S(rec_tx1,rec_tx2,ports)
        # applying error correction with the error terms previoulsy obtained
        print('Applying 12-Term Model Correction...')
        S_param = correct12Term(S_param_meas,fwd_terms,rev_terms)
        # touchstone files of the measurement are written to the current directory
        print('Writing files: DUT_uncorrected.S2P, DUT.S2P ...')
        writeSnP(freq_vec,S_param_meas,'C:/Temp/DUT_uncorrected.S2P',freq_unit='MHz')
        writeSnP(freq_vec,S_param,'C:/Temp/DUT.S2P',freq_unit='MHz')
        # a plot comparing the raw uncorrected measurement
        # to the corrected S-paramter measurement in Log-Magnitude
        print('Plotting...')
        plotCompareDb(freq_vec,[S_param_meas,S_param],
            ['Uncorrected','12-term Corrected'], settings_str)

if __name__ == '__main__':
    main()
