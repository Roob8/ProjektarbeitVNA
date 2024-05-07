def save_measurments(input_settings, S_params, folder_path, file_name ):
    import pandas as pd
    import numpy as np
    import math
    from pathlib import Path
    import datetime as dt
    import os
    """
    Die SOLT-Kalibriermessung wird durch das Verwenden von gespeicherten Kalibrierdaten ersetzt.
    input:
        input_settings: List with start, stop, NOP, RBW, power
        S_params: S-parameter from measurement. Dictionary, with a list of complex phasors for each port (1-6) in order OSLT
        
        folder_path: String with absolute path of filder
    output:

    """
    setup = []
    freq = []
    S11_Betrag = []
    S11_Phase = []
    S21_Betrag =[]
    S21_Phase = []
    S12_Betrag = []
    S12_Phase = []
    S22_Betrag = []
    S22_Phase = []

    freq = list(frequency)

    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    for x in range(len(freq)-5):
        setup.append("")

    for x in range(len(freq)):
        S11_Betrag.append(20*math.log10(np.abs(s_params[x][0][0])))
        S11_Phase.append(np.angle(s_params[x][0][0], deg=True))

        S21_Betrag.append(20*math.log10(np.abs(s_params[x][1][0])))
        S21_Phase.append(np.angle(s_params[x][1][0], deg=True))

        S12_Betrag.append(20 * math.log10(np.abs(s_params[x][0][1])))
        S12_Phase.append(np.angle(s_params[x][0][1], deg=True))

        S22_Betrag.append(20 * math.log10(np.abs(s_params[x][1][1])))
        S22_Phase.append(np.angle(s_params[x][1][1], deg=True))

    data1 = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                              "S11 Betrag": S11_Betrag, "S11 Phase": S11_Phase,
                              "S21 Betrag": S21_Betrag, "S21 Phase": S21_Phase,
                              "S12 Betrag": S21_Betrag, "S12 Phase": S21_Phase,
                              "S22 Betrag": S22_Betrag, "S22 Phase": S22_Phase})

    # "Ausgaben" Ordner erzeugen
    subfolder_name = 'Ausgaben'
    subfolder_path = Path(subfolder_name)

    # check if folder exist
    if not subfolder_path.is_dir():
        subfolder_path.mkdir()

    # check if filename exist
    current_date_and_time = dt.datetime.now()
    filename = "Ausgaben/" + current_date_and_time + ".xlsx"
    no = 1
    while(os.subfolder_path.isfile(filename)):
        filename = filename + str(no)
        no += 1
        if no = 10:
            print("Measurment could not be stored!")
            break


    with pd.ExcelWriter(filename) as writer:
        data1.to_excel(writer, sheet_name='Calibrated measurement')
        data2.to_excel(writer, sheet_name='UncCalibrated measurement')

    # data.to_excel(filename + ".xlsx")
    print("Measurment store to Excel done!")