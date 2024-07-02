import math
from pathlib import Path
from tkinter import *
import numpy as np
import pandas as pd
import hidden as hid
import utils as ut
import skrf as rf
import matplotlib.pyplot as plt

def plot_meas(s_param_roh, s_param_8_term, s_param_12_term, settings, freq_vec_Hz):

    setting_str =   'Freq. Range: '+str(settings.freqRange.freqStartMHz)+' - '+ \
                                    str(settings.freqRange.freqStopMHz)+' [MHz]     ' + \
                    'Num. Points: '+str(settings.freqRange.numFreqPoints)+' [pts]       ' + \
                    'Output Power: '+str(settings.outputPower_dbm)+' [dBm]       ' + \
                    'Res. Bandwidth: '+str(settings.rbw_khz)+' [kHz]'

    fig, axes = plt.subplots(1, 3)
    DUT_roh = rf.Network(s=s_param_roh, f=freq_vec_Hz / 1e6, z0=50, f_unit='MHz')
    DUT_roh.plot_s_db(ax=axes[0])
    axes[0].set_title('Unkallibrierte S-Parameter-Messung')

    DUT_8_term = rf.Network(s=s_param_8_term, f=freq_vec_Hz / 1e6, z0=50, f_unit='MHz')
    DUT_8_term.plot_s_db(ax=axes[1])
    axes[1].set_title('S-Parameter nach 8-term-Correction')

    DUT_12_term = rf.Network(s=s_param_12_term, f=freq_vec_Hz / 1e6, z0=50, f_unit='MHz')
    DUT_12_term.plot_s_db(ax=axes[2])
    axes[2].set_title('S-Parameter nach 12-term-Correction')

    plt.suptitle(setting_str)
    plt.show()

def get_choosen_single_port(portauswahl):

    choosen_port = portauswahl.get(portauswahl.curselection())
    return choosen_port

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
        1,  # transmitter port
        vnakit.VNAKIT_MODE_TWO_PORTS
    )

    return settings

def get_ideal_s_params(freq_vec):

    # @ Florian: Ideale S-Parameter Dateien müssen noch mit dem richtigen Inhalt befüllt werden
    open_s_param_A = hid.readSnP("cal_files_VNA/open.S1P", freq_vec)
    short_s_param_A = hid.readSnP("cal_files_VNA/short.S1P", freq_vec)
    load_s_param_A = hid.readSnP("cal_files_VNA/load.S1P", freq_vec)
    open_s_param_B = hid.readSnP("cal_files_VNA/open.S1P", freq_vec)
    short_s_param_B = hid.readSnP("cal_files_VNA/short.S1P", freq_vec)
    load_s_param_B = hid.readSnP("cal_files_VNA/load.S1P", freq_vec)
    thru_s_param = hid.readSnP("cal_files_VNA/thru.S2P", freq_vec)

    return open_s_param_A, open_s_param_B, load_s_param_A, load_s_param_B, short_s_param_A, short_s_param_B, thru_s_param


def calibration_8_term(s_param_meas, freq_vec_Hz, cal_files):
    # filenames of the open, short, load standards
    sol_stds = ['stds_Measure/open.S1P', 'stds_Measure/short.S1P', 'stds_Measure/load.S1P']

    # puts the reflection coefficents of the SOL standards in single array.
    # Also interpolates in frequency. See vnakit_ex/utils.py
    gamma_listed = ut.loadGammaListed(sol_stds, freq_vec_Hz)

    # loads S-parameter data of the thru standard, interpolates frequency
    thru_listed = hid.readSnP('stds_Measure/thru.S2P', freq_desired=freq_vec_Hz)

    # Gm1: [num_pts,3] port 1 measured reflection coefficients in order OSL
    gamma_meas_p1 = np.array(cal_files[0:3]).T
    gamma_meas_p2 = np.array(cal_files[3:6]).T
    Thru_meas = np.array(cal_files[6])

    (A,B,q) = hid.get8TermModel(gamma_listed, gamma_meas_p1,
                                               gamma_listed, gamma_meas_p2, thru_listed, Thru_meas)
    # calibration is now complete (by having obtained the error terms)

    # applying error correction with the error terms
    print('Applying 8-Term Model Correction...')
    return hid.correct8Term(s_param_meas, A,B,q)


def calibration_12_term(s_param_meas, freq_vec_Hz, cal_files):
    # filenames of the open, short, load standards
    sol_stds = ['stds_Measure/open.S1P', 'stds_Measure/short.S1P', 'stds_Measure/load.S1P']



    # puts the reflection coefficents of the SOL standards in single array.
    # Also interpolates in frequency. See vnakit_ex/utils.py
    gamma_listed = ut.loadGammaListed(sol_stds, freq_vec_Hz)

    # loads S-parameter data of the thru standard, interpolates frequency
    thru_listed = hid.readSnP('stds_Measure/thru.S2P', freq_desired=freq_vec_Hz)

    gamma_meas_p1 = np.array(cal_files[0:3]).T
    gamma_meas_p2 = np.array(cal_files[3:6]).T
    thru_meas = np.array(cal_files[6])

    (fwd_terms, rev_terms) = hid.get12TermModel(gamma_listed, gamma_meas_p1,
                                                gamma_listed, gamma_meas_p2, thru_listed, thru_meas)
    # calibration is now complete (by having obtained the error terms)

    # applying error correction with the error terms
    print('Applying 12-Term Model Correction...')
    return hid.correct12Term(s_param_meas, fwd_terms, rev_terms)


def single_measurement(vnakit, settings, tx, ports):

    rec_tx1 = hid.measure1Port(vnakit, settings, ports[tx])

    if tx == 'Tx1':
        s_params = np.array(rec_tx1[ports['Rx1B']])/np.array(rec_tx1[ports['Rx1A']])
    elif tx == 'Tx2':
        s_params = np.array(rec_tx1[ports['Rx2B']]) / np.array(rec_tx1[ports['Rx2A']])

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

def run_measurement(settings, single_dual, tx, cal_files, ports, freq_vec_Hz, vnakit):

    if single_dual == 1:  # single port measurement
        # measure S-parameters
        s_param_roh = single_measurement(vnakit, settings, tx, ports)

        # applying error correction with the error terms
        s_param_12_term = calibration_12_term(s_param_roh, freq_vec_Hz, cal_files)
        s_param_8_term = calibration_8_term(s_param_roh, freq_vec_Hz, cal_files)

    elif single_dual == 2:  # dual port measurement
        # measure S-parameters
        s_param_roh = dual_measurement(vnakit, settings, ports)

        # applying error correction with the error terms
        s_param_12_term = calibration_12_term(s_param_roh, freq_vec_Hz, cal_files)
        s_param_8_term = calibration_8_term(s_param_roh, freq_vec_Hz, cal_files)


    else:
        print("Wrong measurement parameter")

    plot_meas(s_param_roh, s_param_8_term, s_param_12_term, settings, freq_vec_Hz)

    return s_param_roh, s_param_8_term, s_param_12_term


def save_measurements(settings, freq_vec_Hz, s_param_roh, s_param_8, s_param_12, folder_path, file_name, dual_single, vnakit):
    file_path = folder_path + "/" + file_name
    freq_vec_MHz = freq_vec_Hz/1000000
    # store measurement in touchstone files
    if dual_single == 1:  # single port measurement
        hid.writeSnP(freq_vec_MHz, s_param_roh, file_path + "_uncorrected.S1P", freq_unit='MHz')

    if dual_single == 2:  # dual port measurement
        hid.writeSnP(freq_vec_MHz, s_param_roh, file_path + "_uncorrected.S2P", freq_unit='MHz')
        hid.writeSnP(freq_vec_MHz, s_param_8, file_path + "_8Term.S2P", freq_unit='MHz')
        hid.writeSnP(freq_vec_MHz, s_param_12, file_path + "_12Term.S2P", freq_unit='MHz')

    # store measurement in Excel file_path
    setup = []
    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    S11_Betrag = []
    S11_Phase = []
    S21_Betrag = []
    S21_Phase = []
    S12_Betrag = []
    S12_Phase = []
    S22_Betrag = []
    S22_Phase = []
    # freq = []
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

    df1 = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                             "S11 Betrag": S11_Betrag, "S11 Phase": S11_Phase,
                             "S21 Betrag": S21_Betrag, "S21 Phase": S21_Phase,
                             "S12 Betrag": S21_Betrag, "S12 Phase": S21_Phase,
                             "S22 Betrag": S22_Betrag, "S22 Phase": S22_Phase})

    # Create DataFrames for s_param_8
    S11_Betrag_8 = []
    S11_Phase_8 = []
    S21_Betrag_8 = []
    S21_Phase_8 = []
    S12_Betrag_8 = []
    S12_Phase_8 = []
    S22_Betrag_8 = []
    S22_Phase_8 = []

    for x in range(len(freq)):
        S11_Betrag_8.append(20 * math.log10(np.abs(s_param_8[x][0][0])))
        S11_Phase_8.append(np.angle(s_param_8[x][0][0], deg=True))

        S21_Betrag_8.append(20 * math.log10(np.abs(s_param_8[x][1][0])))
        S21_Phase_8.append(np.angle(s_param_8[x][1][0], deg=True))

        S12_Betrag_8.append(20 * math.log10(np.abs(s_param_8[x][0][1])))
        S12_Phase_8.append(np.angle(s_param_8[x][0][1], deg=True))

        S22_Betrag_8.append(20 * math.log10(np.abs(s_param_8[x][1][1])))
        S22_Phase_8.append(np.angle(s_param_8[x][1][1], deg=True))

    df2 = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                             "S11 Betrag": S11_Betrag_8, "S11 Phase": S11_Phase_8,
                             "S21 Betrag": S21_Betrag_8, "S21 Phase": S21_Phase_8,
                             "S12 Betrag": S12_Betrag_8, "S12 Phase": S12_Phase_8,
                             "S22 Betrag": S22_Betrag_8, "S22 Phase": S22_Phase_8})

    # Create DataFrames for s_param_8
    S11_Betrag_12 = []
    S11_Phase_12 = []
    S21_Betrag_12 = []
    S21_Phase_12 = []
    S12_Betrag_12 = []
    S12_Phase_12 = []
    S22_Betrag_12 = []
    S22_Phase_12 = []

    for x in range(len(freq)):
        S11_Betrag_12.append(20 * math.log10(np.abs(s_param_12[x][0][0])))
        S11_Phase_12.append(np.angle(s_param_12[x][0][0], deg=True))

        S21_Betrag_12.append(20 * math.log10(np.abs(s_param_12[x][1][0])))
        S21_Phase_12.append(np.angle(s_param_12[x][1][0], deg=True))

        S12_Betrag_12.append(20 * math.log10(np.abs(s_param_12[x][0][1])))
        S12_Phase_12.append(np.angle(s_param_12[x][0][1], deg=True))

        S22_Betrag_12.append(20 * math.log10(np.abs(s_param_12[x][1][1])))
        S22_Phase_12.append(np.angle(s_param_12[x][1][1], deg=True))

    df3 = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                             "S11 Betrag": S11_Betrag_12, "S11 Phase": S11_Phase_12,
                             "S21 Betrag": S21_Betrag_12, "S21 Phase": S21_Phase_12,
                             "S12 Betrag": S12_Betrag_12, "S12 Phase": S12_Phase_12,
                             "S22 Betrag": S22_Betrag_12, "S22 Phase": S22_Phase_12})

    # "Ausgaben" Ordner erzeugen
    subfolder_path = Path(folder_path)

    # checken ob der Ordner existiert
    if not subfolder_path.is_dir():
        subfolder_path.mkdir()

    with pd.ExcelWriter(file_path + ".xlsx") as writer:
        df1.to_excel(writer, sheet_name='Uncorrect', index=False)
        df2.to_excel(writer, sheet_name='8-Term', index=False)
        df3.to_excel(writer, sheet_name='12-Term', index=False)

    print("Save measurements done!")


