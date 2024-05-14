def sKompl_2_sLog(s_param_kompl, frequency):
    import numpy as np
    import math

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


