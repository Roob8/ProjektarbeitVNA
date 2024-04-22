"""
utils.py
Helper Functons to accompany the Vayyar VNAKit API
"""
import sys
import numpy as np

def portMap():
    """returns port mapping dictionary for the standard
    two port configuration of the UVNA-63+"""
    return {'Tx1':6,'Rx1A':5,'Rx1B':4,'Tx2':3,'Rx2A':2,'Rx2B':1}

def getSettingsStr(setting):
    """
    returns a nicely formated string of the board's settings
    input:
        setting: board.RecordingSettings() object
    output: [string]
    """
    return 'Freq. Range    : '+str(setting.freqRange.freqStartMHz)+' - '+ \
                              str(setting.freqRange.freqStopMHz)+' [MHz]\n' + \
           'Num. Points    : '+str(setting.freqRange.numFreqPoints)+' [pts]\n' + \
           'Output Power   : '+str(setting.outputPower_dbm)+' [dBm]\n' + \
           'Res. Bandwidth : '+str(setting.rbw_khz)+' [kHz]\n'

def loadGammaListed(sol_stds,freq_desired):
    """
    loads standards from SnP files for data-based calibration.
    inputs:
        sol_stds: list of filenames of the standards
        freq_desired: frequency vector for interpolation of data (must be in Hz)
    output:
        gamma_listed: [num_pts,3] complex reflection coefficients of OSL in
                    order specified by sol_stds
    """
    from vnakit_ex.hidden import readSnP

    gamma_listed = np.zeros((len(freq_desired),3),dtype=np.complex)
    for i in range(3):
        gamma_listed[:,i] = readSnP(sol_stds[i],freq_desired=freq_desired)
    return gamma_listed
