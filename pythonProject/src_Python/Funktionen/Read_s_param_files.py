def Read_s_param_files(path, settings, isolation=False):
    import numpy as np
    from pathlib import Path
    import pandas as pd
    """
    Die SOLT-Kalibriermessung wird durch das Verwenden von gespeicherten Kalibrierdaten ersetzt.
    input:
        path: List with Strings of input files in order: Port1 OSL, Port2 OSL and Tm (and optional Im)
        settings: vnakit settings object
    output:
        Gm1: [num_pts,3] port 1 measured reflection coefficients in order OSL
        Gm2: [num_pts,3] port 2 measured reflection coefficients in order OSL
        Tm: [num_pts,2,2] measured thru S-parameters (with switch correction and without switch correction)
        (optional) Im: [num_pts,2,2] measured isolation S-parameters
    """

    N = settings.freqRange.numFreqPoints
    Gm1 = np.zeros((N, 3), dtype=np.complex)
    Gm2 = np.zeros((N, 3), dtype=np.complex)
    # Tm = np.zeros() ?

    # Port 1
    Gm1[:, 0] = pd.read_excel(path[0], index_col=0, dtype={'MHz': float, 'S': float})  # OPEN
    Gm1[:, 1] = pd.read_excel(path[1], index_col=0, dtype={'MHz': float, 'S': float})# SHORT
    Gm1[:, 2] = pd.read_excel(path[2], index_col=0, dtype={'MHz': float, 'S': float})# LOAD

    # Port 2
    Gm2[:, 0] = pd.read_excel(path[3], index_col=0, dtype={'MHz': float, 'S': float})  # OPEN
    Gm2[:, 1] = pd.read_excel(path[4], index_col=0, dtype={'MHz': float, 'S': float})# SHORT
    Gm2[:, 2] = pd.read_excel(path[5], index_col=0, dtype={'MHz': float, 'S': float})# LOAD

    Tm = pd.read_excel(path[6], index_col=0, dtype={'MHz': float, 'S': float})

    # Interpolation
    startFreq = settings.freqRange.freqStartMHz
    stopFreq = settings.freqRange.freqStopMHz


    if isolation:
        Im = pd.read_excel(path[7], index_col=0, dtype={'MHz': float, 'S': float})
        return Gm1, Gm2, Tm, Im
    else:
        return Gm1, Gm2, Tm
