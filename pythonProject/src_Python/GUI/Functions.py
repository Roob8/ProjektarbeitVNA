from tkinter import *


def insert_blank_line(root, row, num_columns):
    blank_line = Label(root, text="")
    blank_line.grid(row=row, column=0, columnspan=num_columns)


def get_input_settings(start, stop, NOP, RBW, power):
    settings = []
    settings.append(start.get().strip())
    settings.append(stop.get().strip())
    settings.append(NOP.get().strip())
    settings.append(RBW.get().strip())
    settings.append(power.get().strip())
    return settings


def single_measurement(input_settings, port):
    S_params = "Platzhalter"
    return S_params


def dual_measurement(input_settings):
    S_Params = "Platzhalter"
    return S_Params


def load_sparam(input_setings, path):
    S_param = "Platzhalter"
    return S_param


def run_measurement(input_settings, single_dual, which_single_port, calibration_files, plot_cal):
    print(input_settings)
    print(single_dual)
    print(which_single_port)
    print(calibration_files)
    print(plot_cal)


    S_params = "Platzhalter"
    return S_params


def save_measurements(input_setting, S_Params, folder_path, file_name):

    # Speichern der Daten in eine S-Parameter-Datei
    S_Params[0].to_csv(folder_path+file_name+"open.s1p", sep="\t", index=False, header=False)
    S_Params[1].to_csv(folder_path+file_name+"short.s1p", sep="\t", index=False, header=False)
    S_Params[2].to_csv(folder_path+file_name+"load.s1p", sep="\t", index=False, header=False)
    #S_Params[3].to_csv(path_thru+file_name, sep="\t", index=False, header=False)

    print("Save measurements done!")


