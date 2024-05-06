def SParam_to_ecxel(settings,frequency,s_params):
    import pandas as pd
    import numpy as np
    import math
    from pathlib import Path

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

    freq = np.array(vnakit.GetFreqVector_MHz())
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

    data = pd.DataFrame(data={"Setup": setup, "Frequenz": freq,
                              "S11 Betrag": S11_Betrag, "S11 Phase": S11_Phase,
                              "S21 Betrag": S21_Betrag, "S21 Phase": S21_Phase,
                              "S12 Betrag": S21_Betrag, "S12 Phase": S21_Phase,
                              "S22 Betrag": S22_Betrag, "S22 Phase": S22_Phase})

    # "Ausgaben" Ordner erzeugen
    subfolder_name = 'Ausgaben'
    subfolder_path = Path(subfolder_name)

    # checken ob der Ordner existiert
    if not subfolder_path.is_dir():
        subfolder_path.mkdir()

    data.to_excel("Ausgaben/Output.xlsx")
    print("Export to Excel done!")