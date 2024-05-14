from tkinter import *
import pickle
import vnakit
import numpy as np
import hidden as hid
import utils as ut
import pandas as pd
import math
from pathlib import Path

def insert_blank_line(root, row, num_columns):
    blank_line = Label(root, text="")
    blank_line.grid(row=row, column=0, columnspan=num_columns)

def init(start, stop, NOP, RBW, power):
    # VNA kit port mapping, defining the Transceiver ports (1,2,...,6)
    # to the VNA ports ('Tx1',Rx1A',...,'Rx2B')
    ports = {'Tx1': 6, 'Rx1A': 5, 'Rx1B': 4, 'Tx2': 3, 'Rx2A': 2, 'Rx2B': 1}

    # intializes the board object
    vnakit.Init()

    # VNA Kit settings
    """
            Attributes of settings:
            freqRange: of type FrequencyRange.
            rbw_khz: RBW (in KHz); use GetRbwLimits() for permitted values
            outputPower_dbm: Output power (in dbm); use GetPowerLimits() for permitted values
            txtr: Transmitter port -- integer from 1 to 6
            mode: One of VNAKIT_MODE_ONE_PORT ; VNAKIT_MODE_TWO_PORTS
    """


    settings = vnakit.RecordingSettings(
        vnakit.FrequencyRange(100, 1000, 11),     # @Florian: Gibt Fehlermeldung --> must be real number not str
        10,      # RBW (in KHz)
        -10,   # output power (dbM)
        ports['Tx1'],   # transmitter port
        vnakit.VNAKIT_MODE_TWO_PORTS
    )
    vnakit.ApplySettings(settings)

    """# Get variable from stored file with module pickle
    with open('../Pickle/settings.pkl', 'rb') as file:  # Daten laden
        settings = pickle.load(file)
        """


    # actual frequency vector used by the board
    freq_vec = np.array(vnakit.GetFreqVector_MHz())
    """
    # Get variable from stored file with module pickle
    with open('../Pickle/freq_vec.pkl', 'rb') as file:  # Daten laden
        freq_vec = pickle.load(file)
    """

    print('The board is initialized with settings:\n')

    # gets a formatted string of the board's settings. See vnakit_ex/utils.py
    settings_str = ut.getSettingsStr(settings)
    print(settings_str)

    return settings, freq_vec, ports

def get_input_settings(start, stop, NOP, RBW, power):
    settings = []
    settings.append(start.get().strip())
    settings.append(stop.get().strip())
    settings.append(NOP.get().strip())
    settings.append(RBW.get().strip())
    settings.append(power.get().strip())

    return settings[0], settings[1], settings[2], settings[3], settings[4]   # @Florian: Besser lösen

def plot(freq_vec, S_param_meas, S_param, settings):
    settings_str = ut.getSettingsStr(settings)
    hid.plotCompareDb(freq_vec, [S_param_meas, S_param],
                  ['Uncorrected', '12-term Corrected'], settings_str)


def calibration_12_term(s_param_meas, freq_vec, cal_files):
    # filenames of the open, short, load standards
    sol_stds = ['stds/open.S1P', 'stds/short.S1P', 'stds/load.S1P']

    # puts the reflection coefficents of the SOL standards in single array.
    # Also interpolates in frequency. See vnakit_ex/utils.py
    Gamma_listed = ut.loadGammaListed(sol_stds, freq_vec * 1e6)

    # loads S-parameter data of the thru standard, interpolates frequency
    Thru_listed = hid.readSnP('stds/thru.S2P', freq_desired=freq_vec * 1e6)

    # constructs the 12-term model from the standards data and the data measured
    # from the prompt
    print('Constructing 12-Term Error Model...')
    #####
    with open('../Pickle/gamma_meas_p1.pkl', 'rb') as file:  # Daten laden
        gamma_meas_p1 = pickle.load(file)
    with open('../Pickle/gamma_meas_p2.pkl', 'rb') as file:  # Daten laden
        gamma_meas_p2 = pickle.load(file)
    with open('../Pickle/thru_meas.pkl', 'rb') as file:  # Daten laden
        thru_meas = pickle.load(file)
    #####
    (fwd_terms, rev_terms) = hid.get12TermModel(Gamma_listed, gamma_meas_p1,
                                            Gamma_listed, gamma_meas_p2, Thru_listed, thru_meas)
    # calibration is now complete (by having obtained the error terms)

    # applying error correction with the error terms
    print('Applying 12-Term Model Correction...')
    return hid.correct12Term(s_param_meas, fwd_terms, rev_terms)


def single_measurement(vnakit, settings, tx, ports, freq_vec):
    print('Recording...', end='')
    rec_tx1 = hid.measure1Port(vnakit, settings, tx)
    print('Done.\n')

    # converting a/b waves to S-parameters
    rec_tx2 = rec_tx1
    s_param_kompl = hid.ab2S(rec_tx1, rec_tx2, ports)

    # converting complex S-parameters to magnitude and angle (dB and phase)
    s_param_dB = sKompl_2_sLog(s_param_kompl, freq_vec)

    return s_param_dB[len(rec_tx1),1,1]


def dual_measurement(vnakit, settings, ports):
    print('Recording...', end='')
    (rec_tx1, rec_tx2) = hid.measure2Port(vnakit, settings, ports)
    """#####
    with open('../Pickle/rec_tx1.pkl', 'rb') as file:  # Daten laden
        rec_tx1 = pickle.load(file)
    with open('../Pickle/rec_tx2.pkl', 'rb') as file:  # Daten laden
        rec_tx2 = pickle.load(file)
    #####"""
    print('Done.\n')

    return hid.ab2S(rec_tx1, rec_tx2, ports) # converting a/b waves to S-parameter

def sKompl_2_sLog(s_param_kompl, frequency):
    setup = []
    S11_Betrag = []
    S11_Phase = []
    S21_Betrag =[]
    S21_Phase = []
    S12_Betrag = []
    S12_Phase = []
    S22_Betrag = []
    S22_Phase = []

    for x in range(len(frequency)):
        S11_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][0][0])))
        S11_Phase.append(np.angle(s_param_kompl[x][0][0], deg=True))

        S21_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][1][0])))
        S21_Phase.append(np.angle(s_param_kompl[x][1][0], deg=True))

        S12_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][0][1])))
        S12_Phase.append(np.angle(s_param_kompl[x][0][1], deg=True))

        S22_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][1][1])))
        S22_Phase.append(np.angle(s_param_kompl[x][1][1], deg=True))

    return S11_Betrag, S11_Phase, S21_Betrag, S21_Phase, S12_Betrag, S12_Phase, S22_Betrag, S22_Phase

def load_sparam(input_setings, path):
    S_param = "Platzhalter"
    return S_param

def calibration(choosen_port, which_single_port, vnakit, settings, ports):

    if choosen_port == 1:   # single-port measure
        rec = hid.measure1Port(vnakit, settings, which_single_port)
    elif choosen_port == 2:
        (rec_tx1, rec_tx2) = hid.measure2Port(vnakit, settings, ports)
    else:
        print("Wrong measurement parameter!")

def run_measurement(settings, single_dual, tx, cal_files, ports, freq_vec):
    """
        makes port measurement
        input:
            settings: vnakit settings object
            single_dual: 1 for one port measure, 2 for two port measure
            tx: port number of transmitter. 'Tx1' or Tx2'
            calibration_files: calibration files (measured, from stored file or ideal)
            ports: mapping dictionary,
                possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
                possible values: [1, 2, 3, 4, 5, 6]
        output:
            rec_tx1: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
                recording dictionary with tx1 as transmitter
            rec_tx2: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
                recording dictionary with tx2 as transmitter
        """

    if single_dual == 1:
        rec = single_measurement(vnakit, settings, tx, ports, freq_vec)

    elif single_dual == 2:
        # measure S-parameters
        s_param_kompl = dual_measurement(vnakit, settings, ports)

        # applying error correction with the error terms
        # s_param_cor = calibration_12_term(s_param_kompl, freq_vec, cal_files)

        # converting complex S-parameters to magnitude and angle (dB and phase)
        s_param_dB = sKompl_2_sLog(s_param_kompl, freq_vec) # s_param_kompl eigentlich s_param_cor

        #plot(freq_vec, s_param_kompl, s_param_cor, settings)

    else:
        print("Wrong measurement parameter")

    s_param_cor = s_param_kompl     # Weil calibration_12_term noch nicht implementiert
    return s_param_kompl, s_param_cor, s_param_dB


def save_measurements(settings, freq_vec, s_param_kompl, S_param_cor, folder_path, file_name):
    file_path = folder_path + "/" + file_name
    
    # store measurement in touchstone files
    hid.writeSnP(freq_vec, s_param_kompl, file_path + "_uncorrected.S2P", freq_unit='MHz')
    hid.writeSnP(freq_vec, S_param_cor, file_path + ".S2P", freq_unit='MHz')

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

    freq = list(freq_vec)

    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    freq = np.array(vnakit.GetFreqVector_MHz())
    for x in range(len(freq) - 5):
        setup.append("")

    for x in range(len(freq)):
        S11_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][0][0])))
        S11_Phase.append(np.angle(s_param_kompl[x][0][0], deg=True))

        S21_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][1][0])))
        S21_Phase.append(np.angle(s_param_kompl[x][1][0], deg=True))

        S12_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][0][1])))
        S12_Phase.append(np.angle(s_param_kompl[x][0][1], deg=True))

        S22_Betrag.append(20 * math.log10(np.abs(s_param_kompl[x][1][1])))
        S22_Phase.append(np.angle(s_param_kompl[x][1][1], deg=True))

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

