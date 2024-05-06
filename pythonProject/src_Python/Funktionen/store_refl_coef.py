def store_refl_coef(settings, Gm1, Gm2, Tm):
    import pandas as pd
    import vnakit
    import numpy as np

    # N = settings.freqRange.numFreqPoints
    setup = []
    setup.append('Startfrequenz: ' + str(settings.freqRange.freqStartMHz) + " MHz")
    setup.append('Endfrequenz: ' + str(settings.freqRange.freqStopMHz) + " MHz")
    setup.append("Eingangsleistung: " + str(settings.outputPower_dbm) + " dBm")
    setup.append("Anzahl der Messpunkte: " + str(settings.freqRange.numFreqPoints))
    setup.append("RBW: " + str(settings.rbw_khz) + " kHz")

    freq = np.array(vnakit.GetFreqVector_MHz())
    for x in range(len(freq)-5):
        setup.append("")

    data1 = pd.DataFrame(data={"Settings:": setup,
                               "Tx1: O": Gm1[:,0], "Tx1: S": Gm1[:,1], "Tx1: L": Gm1[:,2],
                               "Tx2: O": Gm2[:,0], "Tx2: S": Gm2[:,1], "Tx2: L": Gm2[:,2]})

    filename = "Refelction_Coefficient.xlsx"
    data1.to_excel(filename)
    print("Measurment store to Excel done!")