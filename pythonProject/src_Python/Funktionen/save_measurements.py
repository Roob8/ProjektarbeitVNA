def save_measurements(settings, s, folder_path, file_name):
    import pandas as pd
    from pathlib import Path
    import datetime as dt
    import os
    import pickle

    """
    Die SOLT-Kalibriermessung wird durch das Verwenden von gespeicherten Kalibrierdaten ersetzt.
    input:
        settings: L
        s_param: S-parameter from measurement. Dictionary, with a list of complex phasors for each port (1-6) in order OSLT
        folder_path: String with absolute path of folder
    output:
    """

    setup = []
    freq_vec = []

    # actual frequency vector used by the board
    # freq_vec = np.array(vnakit.GetFreqVector_MHz())
    with open('Pickle/freq_vec.pkl', 'rb') as file:  # Daten laden
        freq_vec = pickle.load(file)

    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    for x in range(len(freq_vec)-5):
        setup.append("")

    data1 = pd.DataFrame(data={"Setup": setup, "Frequenz": freq_vec,
                              "S11 Betrag": s[0], "S11 Phase": s[1]})

    # "Ausgaben" Ordner erzeugen'
    subfolder_path = Path(folder_path)

    # check if folder exist
    if not subfolder_path.is_dir():
        subfolder_path.mkdir()

    ''' check if filename exist
    current_date_and_time = dt.datetime.now()
    filename = folder_path + "/" + file_name + ".xlsx"

    no = 1
    while(os.subfolder_path.isfile(filename)):
        filename = filename + str(no)
        no += 1
        if no >= 10:
            print("Measurement could not be stored!")
            break
    '''
    file_name = folder_path + "/" +file_name + ".xlsx"
    with pd.ExcelWriter(file_name) as writer:
        data1.to_excel(writer, sheet_name='Calibrated measurement')
        # data2.to_excel(writer, sheet_name='UncCalibrated measurement')

    # data.to_excel(filename + ".xlsx")
    print("Measurement store to Excel done!")