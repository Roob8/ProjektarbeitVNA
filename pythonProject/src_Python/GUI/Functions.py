import math
from pathlib import Path
from tkinter import *
import numpy as np
import pandas as pd
import hidden as hid
import utils as ut
import pickle

def insert_blank_line(root, row, num_columns):
    blank_line = Label(root, text="")
    blank_line.grid(row=row, column=0, columnspan=num_columns)

def get_frequency_vector(start, stop, NOP):

    start_int = start.get().strip()
    stop_int = stop.get().strip()
    NOP_int = NOP.get().strip()

    freq_vec_Hz = np.linspace(int(start_int), int(stop_int), int(NOP_int))
    return freq_vec_Hz*1e6

def get_settings(start, stop, NOP, RBW, power, vnakit):

    start_int = int(start.get().strip())
    end_int = int(stop.get().strip())
    NOP_int = int(NOP.get().strip())
    RBW_int = int(RBW.get().strip())
    power_int = int(power.get().strip())

    settings = vnakit.RecordingSettings(
        vnakit.FrequencyRange(start_int, end_int, NOP_int),  # fmin,fmax,num_points
        RBW_int,  # RBW (in KHz)
        power_int,  # output power (dbM)
        ports['Tx1'],  # transmitter port ## Felix ist das unwichtig? weil eh überschrieben wird?
        vnakit.VNAKIT_MODE_TWO_PORTS
    )

    return settings

def get_ideal_s_params(freq_vec):

    # @ Florian: Ideale S-Parameter Dateien müssen noch mit dem richtigen Inhalt befüllt werden
    open_s_param_A = hid.readSnP("stds/open.S1P", freq_vec)
    short_s_param_A = hid.readSnP("stds/short.S1P", freq_vec)
    load_s_param_A = hid.readSnP("stds/load.S1P", freq_vec)
    open_s_param_B = hid.readSnP("stds/open.S1P", freq_vec)
    short_s_param_B = hid.readSnP("stds/short.S1P", freq_vec)
    load_s_param_B = hid.readSnP("stds/load.S1P", freq_vec)
    thru_s_param = hid.readSnP("stds/thru.S2P", freq_vec)

    return open_s_param_A, open_s_param_B, load_s_param_A, load_s_param_B, short_s_param_A, short_s_param_B, thru_s_param
def calibration_12_term(s_param_meas, freq_vec, cal_files, settings):
    '''
    cal files :     [0] open_s_param_A
                    [1] short_s_param_A
                    [2] load_s_param_A
                    [3] open_s_param_B
                    [4] short_s_param_B
                    [5] load_s_param_B
                    [6] thru_s_param
    '''

    # filenames of the open, short, load standards
    sol_stds = ['stds/open.S1P', 'stds/short.S1P', 'stds/load.S1P']

    # puts the reflection coefficents of the SOL standards in single array.
    # Also interpolates in frequency. See vnakit_ex/utils.py
    gamma_listed = ut.loadGammaListed(sol_stds, freq_vec)

    # loads S-parameter data of the thru standard, interpolates frequency
    thru_listed = hid.readSnP('stds/thru.S2P',freq_vec)

    N = settings.freqRange.numFreqPoints
    gamma_meas_p1 = np.zeros((N, 3), dtype=np.complex)
    gamma_meas_p2 = np.zeros((N, 3), dtype=np.complex)

    gamma_meas_p1[:,0] = cal_files[0]
    gamma_meas_p1[:,1] = cal_files[1]
    gamma_meas_p1[:,2] = cal_files[2]

    gamma_meas_p2[:,0] = cal_files[3]
    gamma_meas_p2[:,1] = cal_files[4]
    gamma_meas_p2[:,2] = cal_files[5]

    thru_s_param = cal_files[6]

    (fwd_terms, rev_terms) = hid.get12TermModel(gamma_listed, gamma_meas_p1,
                                                gamma_listed, gamma_meas_p2, thru_listed, thru_s_param)
    # calibration is now complete (by having obtained the error terms)

    # applying error correction with the error terms
    print('Applying 12-Term Model Correction...')
    return hid.correct12Term(s_param_meas, fwd_terms, rev_terms)


def single_measurement(vnakit, settings, tx, ports):

    rec_tx1 = hid.measure1Port(vnakit, settings, tx)
    # converting a/b waves to S-parameters
    rec_tx2 = rec_tx1
    s_params = hid.ab2S(rec_tx1, rec_tx2, ports)

    return s_params

def thru_measurement(vnakit, settings, ports):
    (rec_tx1, rec_tx2) = hid.measure2Port(vnakit, settings, ports)

    return hid.ab2S_SwitchCorrect(rec_tx1, rec_tx2, ports)  # converting a/b waves to S-parameter

def dual_measurement(vnakit, settings, ports):
    (rec_tx1, rec_tx2) = hid.measure2Port(vnakit, settings, ports)

    return hid.ab2S(rec_tx1, rec_tx2, ports)  # converting a/b waves to S-parameter


def load_sparam(freq_vec, path):
    S_param = hid.readSnP(path, freq_vec)
    return S_param

def run_measurement(settings, single_dual, tx, cal_files, ports, freq_vec, vnakit):

    if single_dual == 1:
        s_param_roh = single_measurement(vnakit, settings, tx, ports, freq_vec)

    elif single_dual == 2:
        # measure S-parameters
        s_param_roh = dual_measurement(vnakit, settings, ports)

    else:
        print("Wrong measurement parameter")
        return

    # applying error correction with the error terms
    s_param_12_cor = calibration_12_term(s_param_roh, freq_vec, cal_files, settings)

    s_param_8_cor = s_param_12_cor  # Weil calibration_12_term noch nicht implementiert
    # plot(freq_vec, s_param_kompl, s_param_cor, settings)
    return s_param_roh, s_param_8_cor, s_param_12_cor


def save_measurements(settings, freq_vec, s_param_roh, s_param_8, folder_path, file_name, vnakit):
    file_path = folder_path + "/" + file_name

    # store measurement in touchstone files
    hid.writeSnP(freq_vec, s_param_roh, file_path + "_uncorrected.S2P")
    hid.writeSnP(freq_vec, s_param_8, file_path + ".S2P")

    # store measurement in excel file_path
    setup = []
    freq = []
    S11_Betrag = []
    S11_Phase = []
    S21_Betrag = []
    S21_Phase = []
    S12_Betrag = []
    S12_Phase = []
    S22_Betrag = []
    S22_Phase = []

    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    freq = np.array(vnakit.GetFreqVector_MHz())
    for x in range(len(freq) - 5):
        setup.append("")

    for x in range(len(freq)):
        S11_Betrag.append(20 * math.log10(np.abs(s_param_roh[x][0][0])))
        S11_Phase.append(np.angle(s_param_roh[x][0][0], deg=True))

        S21_Betrag.append(20 * math.log10(np.abs(s_param_roh[x][1][0])))
        S21_Phase.append(np.angle(s_param_roh[x][1][0], deg=True))

        S12_Betrag.append(20 * math.log10(np.abs(s_param_roh[x][0][1])))
        S12_Phase.append(np.angle(s_param_roh[x][0][1], deg=True))

        S22_Betrag.append(20 * math.log10(np.abs(s_param_roh[x][1][1])))
        S22_Phase.append(np.angle(s_param_roh[x][1][1], deg=True))

    data = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                              "S11 Betrag": S11_Betrag, "S11 Phase": S11_Phase,
                              "S21 Betrag": S21_Betrag, "S21 Phase": S21_Phase,
                              "S12 Betrag": S21_Betrag, "S12 Phase": S21_Phase,
                              "S22 Betrag": S22_Betrag, "S22 Phase": S22_Phase})

    # "Ausgaben" Ordner erzeugen
    subfolder_path = Path(folder_path)

    # checken ob der Ordner existiert
    if not subfolder_path.is_dir():
        subfolder_path.mkdir()

    data.to_excel(file_path + ".xlsx")

    print("Save measurements done!")


ports = {'Tx1': 6, 'Rx1A': 5, 'Rx1B': 4, 'Tx2': 3, 'Rx2A': 2, 'Rx2B': 1}
