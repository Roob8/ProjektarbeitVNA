"""
hidden.py
hidden-source helper functions for UVNA-63
"""
from __future__ import print_function
import sys
# from Funktionen.store_refl_coef import store_refl_coef

#try if not aready imported
if 'matplotlib' not in sys.modules:
    import matplotlib
    matplotlib.use('TkAgg')
else:
    #import for spyder users
    import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import solve, det, inv
import scipy as sp
import skrf as rf
#from vnakit_ex import beep

if sys.platform == 'win32':
    from winsound import Beep
    def beep():
        """Produce a short notification beep"""
        Beep(1000,120)
else:
    def beep():
        # do nothing
        return None

def userMsg(msg):
    """ Prints a message to the console and waits for user input.
        program continues on hitting Enter. Progam exits on 'q' input """
    x = input(msg)
    if x.lower() in ['quit','q']:
        sys.exit()
    else:
        return x

def readSnP(path,freq_desired=None,kind='dB'):
    """
    Reads a touchstone file, returning a frequency vector and S-parameter matrix.
    If freq_desired is provided, S-parameter data is interpolated and then returned.
    Units of freq_desired must be in Hz. Python uses the scikit-rf module
    for the reading in raw touchstone data.
    input:
        path: [string] path/to/filename of touchstone file (*.sNp)
        freq_desired (optional): [num_pts] frequency vector (in Hz)
            for interpolation
        kind (optional): (str) Specifies the kind of interpolation
            ('MA', 'DB', or 'RI') Function interpolated to frequency desired
            using linear interpolation on the magnitude and phase ('MP'),
            magnitude in dB and phase ('DB'), or real and imaginary parts
            ('RI'). Default is 'DB'
    output:
        S: [num_pts,1] or [num_pts,n,n] S-Parameter matrix
        f: (optional) [num_pts] frequency vector (in Hz) of file.
            Only returned if no freq_desired is given.
    """
    if type(path) == str:
        ntwk = rf.Network(path)
    elif type(path) == rf.network.Network:
        ntwk = path
    if freq_desired is None:
        return (ntwk.s,ntwk.f)
    else:
        freq_actual = ntwk.f
        m = ntwk.s.shape[1]
        n = ntwk.s.shape[2]
        if kind.upper() == 'RI':
            if (m,n) == (1,1):
                interp = sp.interpolate.interp1d(freq_actual,ntwk.s[:,0,0])
                return interp(freq_desired)
            else:
                S = np.zeros((len(freq_desired),m,n),dtype=np.complex)
                for i in range(m):
                    for j in range(n):
                        interp = sp.interpolate.interp1d(freq_actual,ntwk.s[:,i,j])
                        S[:,i,j] = interp(freq_desired)
                return S
        elif kind.upper() == 'DB':
            interp_dB = sp.interpolate.interp1d(freq_actual,ntwk.s_db,axis=0)
            interp_angle = sp.interpolate.interp1d(freq_actual,ntwk.s_deg_unwrap,axis=0)
            dBs = interp_dB(freq_desired)
            angles = np.pi*interp_angle(freq_desired)/180
            mags = 10**(dBs/20)
            S = mags*np.exp(1j*angles)
            return np.squeeze(S)
        elif kind.upper() == 'MA':
            interp_mag = sp.interpolate.interp1d(freq_actual,ntwk.s_mag,axis=0)
            interp_angle = sp.interpolate.interp1d(freq_actual,ntwk.s_deg_unwrap,axis=0)
            mags = interp_mag(freq_desired)
            angles = np.pi*interp_angle(freq_desired)/180
            S = mags*np.exp(1j*angles)
            return np.squeeze(S)
        else:
            print("Invalid option for kind. Please choose 'MA', 'DB', or 'RI'")

def writeSnP(freq_vec, S_data, path, freq_unit='Hz'):
    """
    writes S-parameter matrix to touchstone (*.SnP) file
    input:
        freq_vec: [num_pts] frequency vector of measurements
        S_data: [num_pts,2,2] S-parameter matrix to save
        path: [string] path/to/filename
        freq_unit: [string] units of the frequency vector (default: Hz)
    """
    import skrf as rf
    filename = path[path.rfind('/')+1:]
    if path.rfind('/'):
        dir = path[:path.rfind('/')]
    else:
        dir = None
    rf.network.Network(frequency=rf.Frequency.from_f(freq_vec,unit=freq_unit), \
        s=S_data,z0=50).write_touchstone(filename=filename,dir=dir)
def S2T(S):
    """
    input:
        S: [num_pts,2,2] S-parameter matrix
    output:
        T: [num_pts,2,2] T-parameter matrix
    """
    return np.array([[-det(S)/S[:,1,0], S[:,0,0]/S[:,1,0]],
                     [-S[:,1,1]/S[:,1,0] , np.ones(S.shape[0])/S[:,1,0]]]).swapaxes(0,1).T

def T2S(T):
    """
    input:
        T: [num_pts,2,2] T-parameter matrix
    output:
        S: [num_pts,2,2] S-parameter matrix
    """
    return np.array([[T[:,0,1]/T[:,1,1]           , det(T)/T[:,1,1]],
                     [np.ones(T.shape[0])/T[:,1,1], -T[:,1,0]/T[:,1,1]]]).swapaxes(0,1).T

def measure1Port(vnakit,settings,tx):
    """
    makes a,b wave measurement at specified port
    input:
        vnakit: object (the board),
        settings: vnakit settings object,
        tx: port number of transmitter (ex. ports['Tx1'])
    output:
        rec: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
            recording dictionary with ports[tx] as transmitter
    """
    settings.txtr = tx
    vnakit.ApplySettings(settings)
    vnakit.Record()
    return vnakit.GetRecordingResult()

def ab2G(rec,ports):
    """
    ab2G   Returns reflection coefficient G (gamma) from a and b waves
        G = ab2G(rec,ports)
        Inputs:
            rec: dict{int:[num_pts]}
                reciever recording returned by measure1Port()
            ports: map that associates a port number with each VNA Tx/Rx
                possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
                possible values: [1, 2, 3, 4, 5, 6]
        Outputs:
            G = [num_pts] reflection coefficient (gamma) of the transmitting port
    """
    tx=0
    for k,v in rec.items():
        if v[0]==0:
            tx=k
    if tx is ports['Tx1']:
        return np.array(rec[ports['Rx1B']])/np.array(rec[ports['Rx1A']])
    if tx is ports['Tx2']:
        return np.array(rec[ports['Rx2B']])/np.array(rec[ports['Rx2A']])

def measure2Port(vnakit,settings,ports):
    """
    makes 2 port measurement
    input:
        vnakit: object (the board),
        settings: vnakit settings object,
        ports: mapping dictionary,
            possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
            possible values: [1, 2, 3, 4, 5, 6]
        tx: port number of transmitter (ie. ports['Tx1'])
    output:
        rec_tx1: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
            recording dictionary with tx1 as transmitter
        rec_tx2: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
            recording dictionary with tx2 as transmitter
    """
    settings.txtr = ports['Tx1']
    vnakit.ApplySettings(settings)
    vnakit.Record()
    rec_tx1 = vnakit.GetRecordingResult()
    settings.txtr = ports['Tx2']
    vnakit.ApplySettings(settings)
    vnakit.Record()
    rec_tx2 = vnakit.GetRecordingResult()
    return (rec_tx1,rec_tx2)

def ab2S_SwitchCorrect(rec_tx1,rec_tx2,ports):
    """
    Converts ab wave measurements from measure2Port() to S parameters with
    switch correction
    input:
        rec_tx1,rec_tx2: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
            recording dictionaries returned by measure2Port() with 'Tx1'
            and 'Tx2' transmitting
        ports: mapping dictionary,
            possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
            possible values: [1, 2, 3, 4, 5, 6]
    output:
        S: [num_pts,2,2] stack of S parameter matricies in frequency
    """
    p = ports
    # unpacking recordings into separate variables
    [a1, b1, a2, b2]  = (np.array(rec_tx1[p[i]]) for i in ['Rx1A','Rx1B','Rx2A','Rx2B'])
    [a1p,b1p,a2p,b2p] = (np.array(rec_tx2[p[i]]) for i in ['Rx1A','Rx1B','Rx2A','Rx2B'])
    g1 = a1p/b1p
    g2 = a2/b2
    d  = 1-(b2/a1)*(b1p/a2p)*g1*g2
    S11 = ((b1/a1)   - (b1p/a2p)*(b2/a1)*g2)/d
    S12 = ((b1p/a2p) - (b1/a1)*(b1p/a2p)*g1)/d
    S21 = ((b2/a1)   - (b2p/a2p)*(b2/a1)*g2)/d
    S22 = ((b2p/a2p) - (b2/a1)*(b1p/a2p)*g1)/d
    return np.array([[S11,S12],[S21,S22]]).swapaxes(0,1).T

def ab2S(rec_tx1,rec_tx2,ports):
    """
    Converts ab wave measurements from measure2Port() to S parameters.
    input:
        rec_tx1,rec_tx2: {1:[num_pts] , 2:[num_pts], ..., 6:[num_pts]}
            recording dictionaries returned by measure2Port()
    output:
        S: [num_pts,2,2] stack of S parameter matricies in frequency
    """
    p = ports
    S11 = np.array(rec_tx1[p['Rx1B']])/np.array(rec_tx1[p['Rx1A']])
    S21 = np.array(rec_tx1[p['Rx2B']])/np.array(rec_tx1[p['Rx1A']])
    S12 = np.array(rec_tx2[p['Rx1B']])/np.array(rec_tx2[p['Rx2A']])
    S22 = np.array(rec_tx2[p['Rx2B']])/np.array(rec_tx2[p['Rx2A']])
    return np.array([[S11,S12],[S21,S22]]).swapaxes(0,1).T

def getIdealSparams(num_pts):
    """
    Returns S-Parameters of the 'Ideal' Open Short Load and Thru Components
    input:
        num_pts: (int) number of points in the frequency vector
    outputs:
        G_ideal: [num_pts, 3] matrix of 'canonical' Open,Short,Load reflection
            coefficients (1,-1,0)
        T_ideal: [numpts, 2, 2] stack of S matricies of an ideal thru
            ie. S = [0 1
                     1 0]
    """
    N = num_pts
    G_open = np.ones(N)
    G_short = -1*np.ones(N)
    G_load = np.zeros(N)
    G_ideal = np.zeros((N,3),dtype=np.complex)
    G_ideal[:,0] = G_open
    G_ideal[:,1] = G_short
    G_ideal[:,2] = G_load
    T_ideal = np.array([[np.zeros(N),np.ones(N)],[np.ones(N),np.zeros(N)]]).swapaxes(0,1).T
    return (G_ideal,T_ideal)

def get1PortResponseModel(G,Gm):
    """
    returns a model for the reflection channel: Gm = H(w)G
    input:
        G: [num_pts] actual, listed, or ideal reflection coefficient
        Gm: [num_pts] measured reflection coefficient
    output:
        H: [num_pts] reflection channel
    """
    return Gm/G

def get2PortResponseModel(G1,G1m,G2,G2m,T,Tm):
    """
    returns a model for a 2x2 Frequency Response model (channel):
    Sijm = Hij(w)Sij
    input:
        G1,G2: [num_pts] actual, listed, or ideal reflection coefficient
            at port 1 and port 2
        Gm1,Gm2: [num_pts] measured reflection coefficient at port 1 and port 2
        T,Tm: [num_pts,2,2] actual, listed, or ideal thru measurement (T)
            and measured thru (Tm)
    output:
        H: [num_pts,2,2] 2x2 Frequency Response model (channel)
    """
    H = np.zeros((T.shape),dtype=np.complex)
    H[:,0,0] = get1PortResponseModel(G1,G1m)
    H[:,1,1] = get1PortResponseModel(G2,G2m)
    H[:,0,1] = Tm[:,0,1]/T[:,0,1]
    H[:,1,0] = Tm[:,1,0]/T[:,1,0]
    return H

def correctResponse(Sm,H):
    """
    Computes DUT S-parameters by inverting the channel modeled by H
    input:
        Sm: [num_pts,2,2] measured S-parameters
        H: [num_pts,2,2] Frequency Response channel model
    output:
        S: [num_pts,2,2] DUT S-parameters
    """
    return Sm/H

def prompt1PortMeasure(vnakit,settings,ports,tx,name=''):
    """
    Prompts the user to measure reflection coefficient at chosen port (tx)
    input:
        vnakit: (the board) object,
        settings: vnakit settings object,
        ports: mapping dictionary,
            possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
            possible values: [1, 2, 3, 4, 5, 6]
        tx: port number of transmitter
        name: (optional) name of component is printed in the prompt
    output:
        Gm: [num_pts] measured reflection coefficient
    """
    tx_nums = {ports['Tx1']:1, ports['Tx2']:2}
    port_num = tx_nums[tx]
    userMsg('>> Measure '+name+' @ Port-'+str(port_num)+': ')
    print('Recording...',end='')
    rec = measure1Port(vnakit,settings,tx)
    beep()
    print('Done.\n')
    return ab2G(rec,ports)

def prompt2PortMeasure(vnakit,settings,ports,name='DUT',sw_corr=True):
    """
    Prompts the user to measure 2-port S-parameters
    input:
        vnakit: (the board) object
        settings: vnakit settings object
        ports: mapping dictionary
            possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
            possible values: [1, 2, 3, 4, 5, 6]
        name: string (optional) name of component is printed in the prompt
        sw_corr: bool (optional) apply switch correction. Default True
    output:
        Sm: [num_pts,2,2] measured S-parameters
    """
    userMsg('>> Measure '+name+': ')
    print('Recording...',end='')
    (rec_tx1,rec_tx2) = measure2Port(vnakit,settings,ports)
    beep()
    print('Done.\n')
    if sw_corr:
        return ab2S_SwitchCorrect(rec_tx1,rec_tx2,ports)
    else:
        return ab2S(rec_tx1,rec_tx2,ports)
def get1PortModel(G,Gm):
    """
    returns 3 error terms from 1 port calibration
    parameters are ideal and measured reflection coefficients for 3 components
    G and Gm must have standards listed in the same order
    inputs:
        G: [num_pts,3] actual component reflection coefficients
        Gm: [num_pts,3] measured component reflection coeffcients
    outputs:
    x: [num_pts,3] solution to the matrix equation Ax=b,
        where A and b are defined by the system of equations for the 1 port model,
        resulting in x containing [e_00, e_11, delta_e] (in that order)
    """
    A = np.array([[np.ones(G.shape[0]),G[:,0]*Gm[:,0],-G[:,0]],
                  [np.ones(G.shape[0]),G[:,1]*Gm[:,1],-G[:,1]],
                  [np.ones(G.shape[0]),G[:,2]*Gm[:,2],-G[:,2]]]).swapaxes(0,1).T
    b = np.array([[Gm[:,0]],[Gm[:,1]],[Gm[:,2]]]).T.swapaxes(1,2)
    return np.squeeze(solve(A,b),axis=2)

def correct1Port(Gm,err_terms):
    """
    corrects a reflection coefficient measurement using the one-port VEC terms
    returned from get1PortModel()
    input:
        Gm: [num_pts] measured reflection coefficient
        err_terms: [num_pts,3] matrix of 1-port error terms obtained from
            get1PortModel()
    output:
        G: corrected reflection coefficient
    """
    [e00, e11, delta_e] = (err_terms[:,i] for i in range(3))
    return (Gm-e00)/(Gm*e11-delta_e)

def prompt1PortSOL(vnakit,settings,ports,tx):
    """
    Prompts the user to measure SOL parameters at chosen port (tx)
    input:
        vnakit: (the board) object,
        settings: vnakit settings object,
        ports: mapping dictionary,
            possible keys: ['Tx1','Tx2','Rx1A','Rx1B','Rx2A','Rx2B']
            possible values: [1, 2, 3, 4, 5, 6]
        tx: port number of transmitter
    output:
        Gm: measured reflection coefficients array [num_pts, 3] in order of OSL
    """
    tx_nums = {ports['Tx1']:1, ports['Tx2']:2}
    port_num = tx_nums[tx]
    N = settings.freqRange.numFreqPoints
    Gm = np.zeros((N,3),dtype=np.complex)
    Gm[:,0] = prompt1PortMeasure(vnakit,settings,ports,tx,'OPEN')
    Gm[:,1] = prompt1PortMeasure(vnakit,settings,ports,tx,'SHORT')
    Gm[:,2] = prompt1PortMeasure(vnakit,settings,ports,tx,'LOAD')
    return Gm

def prompt2PortSOLT(vnakit, settings, ports, isolation=False, sw_corr=True):
    """
    Uses prompt1PortSOL to get SOL measurements at each port, an additional
    thru measurement, and an optional isolation measurement
    input:
        vnakit: (the board) object,
        settings: vnakit settings object,
        ports: port mapping dictionary
        isolation: (bool) will the isolation measurement be taken
        sw_corr: (bool) will switch correction be applied
    output:
        Gm1: [num_pts,3] port 1 measured reflection coefficients in order OSL
        Gm2: [num_pts,3] port 2 measured reflection coefficients in order OSL
        Tm: [num_pts,2,2] measured thru S-parameters
        (optional) Im: [num_pts,2,2] measured isolation S-parameters
    """
    Gm1 = prompt1PortSOL(vnakit,settings,ports,ports['Tx1'])
    print('-- Switch to Port-2 --\n')
    Gm2 = prompt1PortSOL(vnakit,settings,ports,ports['Tx2'])
    Tm = prompt2PortMeasure(vnakit,settings,ports,'THRU',sw_corr)
    # store_refl_coef(settings, Gm1, Gm2, Tm)
    if isolation:
        Im = prompt2PortMeasure(vnakit,settings,ports,'ISOLATION',sw_corr)
        return (Gm1,Gm2,Tm,Im)
    return (Gm1,Gm2,Tm)

def get8TermModel(G1,Gm1,G2,Gm2,T,Tm):
    """
    Constructs 8-term model based on measured and actual SOLT S-parmeters.
    input:
        G1,G2: [num_pts,3] actual (G) and measured (Gm) reflection coefficients
            of standards used on port 1 and 2 respectively. Standards used in
            G,Gm must be in same order (ie. G = [O,S,L] Gm = [Om,Sm,Lm])
        T,Tm: [num_pts,2,2] actual (T) and measured (Tm) relfection coefficients
            of thru standard
    output:
        A,B: [num_pts,2,2] normalized error adapter [-delta_e e00
                                                        e11     1 ]
            at ports 1 and 2 respectively
        q: [num_pts,1] thru error term e10e32
    """
    # convert thru to T parameters
    Tt = S2T(T)
    Tmt = S2T(Tm)
    x = get1PortModel(G1,Gm1)
    y = get1PortModel(G2,Gm2)
    A = np.array([[-x[:,2], x[:,0]],
                  [-x[:,1], np.ones(x.shape[0])]]).swapaxes(0,1).T
    B = np.array([[-y[:,2], y[:,1]],
                  [-y[:,0], np.ones(y.shape[0])]]).swapaxes(0,1).T
    Q = np.matmul(A,np.matmul(Tt,np.matmul(B,inv(Tmt))))
    s = np.sign(np.real(Q[:,0,0]))
    q = s*np.sqrt(det(Q))
    return (A,B,q)

def get8TermModelUThru(G1,Gm1,G2,Gm2,Tm,freq_vec,phys_length=.05):
    """
    Constructs 8-term model based on measured SOLT and actual SOL S-parmeters.
    Uses the Unknown Thru Method.
    input:
        G1,G2: [num_pts,3] actual (G) and measured (Gm) reflection coefficients
            of standards used on port 1 and 2 respectively. Standards used in
            G,Gm must be in same order (ie. G = [O,S,L] Gm = [Om,Sm,Lm])
        Tm: [num_pts,2,2] measured S-parameters of the unknown-thru
        freq_vec: [num_pts] frequency vector (in [Hz]!) of the measurements
        phys_length: (optional) approximate length of the
            unknown thru component in meters for velocity factor of 0.695
            Default is 5cm.
    output:
        A,B: [num_pts,2,2] normalized error adapter [-delta_e e00
                                                        e11     1 ]
            at ports 1 and 2 respectively
        q: [num_pts,1] thru error term e10e32
    """
    Tmt = S2T(Tm)
    x = get1PortModel(G1,Gm1)
    y = get1PortModel(G2,Gm2)
    A = np.array([[-x[:,2], x[:,0]],
                  [-x[:,1], np.ones(x.shape[0])]]).swapaxes(0,1).T
    B = np.array([[-y[:,2], y[:,1]],
                  [-y[:,0], np.ones(y.shape[0])]]).swapaxes(0,1).T
    # Unknown-Thru
    q = np.sqrt(det(A)*det(B)/det(Tmt))
    U = np.matmul(inv(A),np.matmul(Tmt,inv(B)))
    phi = np.angle(U[:,1,1])
    vf = .695 # velocity factor in PTFE coaxial cable
    gd = phys_length/(sp.constants.speed_of_light*vf)
    s = np.sign(np.cos(phi+gd*2*np.pi*freq_vec))
    q = s*q
    return (A,B,q)

def correct8Term(Sm,A,B,q):
    """
    returns DUT S parameters from 8-term error model
    input:
        Sm: [num_pts,2,2] raw measured DUT S-parmeters
        A,B,q: 8-term mdoel error terms from get8TermModel()
    output:
        S: [num_pts,2,2] corrected DUT S-params
    """
    Tm = S2T(Sm) # measured T parameters
    # Q = qI , I stack of 2x2 identity matricies
    Q = np.array([[q,np.zeros(q.shape)],[np.zeros(q.shape),q]]).swapaxes(0,1).T
    T  = np.matmul(Q,np.matmul(inv(A),np.matmul(Tm,inv(B))))
    S = T2S(T)
    return S

def get12TermModel(G1,Gm1,G2,Gm2,T,Tm,isolation=None):
    """
    Constructs the 12-Term error model (with optional isolation measurement),
    using measured SOLT data and listed SOLT data.
    input:
        G1,G2: [num_pts,3] listed (G) and measured (Gm) reflection coefficients
            of standards used on port 1 and 2 respectively. Standards used in
            G,Gm must be in same order (ie. G = [O,S,L] Gm = [Om,Sm,Lm])
        T,Tm: [num_pts,2,2] listed (T) and measured (Tm) relfection coefficients
            of thru standard
        isolation (optional): [num_pts,2,2] measured S-parameters of an isolation measurement.
            ie. matched loads on each port
    output:
        fwd_terms: [num_pts,6] [e00 ,e11 ,e10e01  ,e10e32  ,e22 ,e30]
        rev_terms: [num_pts,6] [ep33,ep22,ep23ep32,ep23ep01,ep11,ep03]
    """
    x = get1PortModel(G1,Gm1)
    y = get1PortModel(G2,Gm2)
    # one port terms
    [e00 ,e11 ,delta_e ] = (x[:,i] for i in [0,1,2])
    [ep33,ep22,delta_ep] = (y[:,i] for i in [0,1,2])
    e10e01   = e00*e11   - delta_e
    ep23ep32 = ep33*ep22 - delta_ep
    # isolation (optional)
    if isolation is not None:
        e30  = isolation[:,1,0]
        ep03 = isolation[:,0,1]
    else:
        e30  = np.zeros(e00.shape)
        ep03 = np.zeros(e00.shape)
    # port-match and tracking terms (of opposite port)
    e22  = (e10e01*T[:,0,0]   - (Tm[:,0,0]-e00 )*(1-e11*T[:,0,0])) /  ((e11*det(T) -T[:,1,1])*(Tm[:,0,0]-e00)  + e10e01*det(T))
    ep11 = (ep23ep32*T[:,1,1] - (Tm[:,1,1]-ep33)*(1-ep22*T[:,1,1])) / ((ep22*det(T)-T[:,0,0])*(Tm[:,1,1]-ep33) + ep23ep32*det(T))
    e10e32   = ((Tm[:,1,0]-e30)/T[:,1,0])*(1-e11*T[:,0,0] -e22*T[:,1,1] -e11*e22*det(T))
    ep23ep01 = ((Tm[:,0,1]-ep03)/T[:,0,1])*(1-ep22*T[:,1,1]-ep11*T[:,0,0]-ep11*ep22*det(T))
    # wrapping up error terms
    fwd_terms = np.array([e00 ,e11 ,e10e01  ,e10e32  ,e22 ,e30 ]).T
    rev_terms = np.array([ep33,ep22,ep23ep32,ep23ep01,ep11,ep03]).T
    return (fwd_terms,rev_terms)

def correct12Term(Sm,fwd_terms,rev_terms,**kwargs):
    """
    Applies 12-Term Model error correction with terms obtained from get12TermModel()
    input:
        Sm: [num_pts,2,2] raw S-parameter measurements
        fwd_terms: [num_pts,6] [e00 ,e11 ,e10e01  ,e10e32  ,e22 ,e30]
        rev_terms: [num_pts,6] [ep33,ep22,ep23ep32,ep23ep01,ep11,ep03]
    output:
        S: [num_pts,2,2] 12-term corrected S-parmeters
    """
    [e00 ,e11 ,e10e01  ,e10e32  ,e22 ,e30]  = (fwd_terms[:,i] for i in range(6))
    [ep33,ep22,ep23ep32,ep23ep01,ep11,ep03] = (rev_terms[:,i] for i in range(6))
    x   = (Sm[:,0,0]-e00)/e10e01
    y   = (Sm[:,0,1]-ep03)/ep23ep01
    z   = (Sm[:,1,0]-e30)/e10e32
    w   = (Sm[:,1,1]-ep33)/ep23ep32
    D   = (1+x*e11)*(1+w*ep22) - z*y*e22*ep11
    S11 = (x*(1+w*ep22) - e22*y*z)/D
    S21 = z*(1+w*(ep22-e22))/D
    S22 = (w*(1+x*e11) - ep11*y*z)/D
    S12 = y*(1+x*(e11-ep11))/D
    return np.array([[S11,S12],[S21,S22]]).swapaxes(0,1).T

def deEmbed(S_A_DUT_B,S_A=[],S_B=[]):
    """
    deEmbed    De-Embeds an adapter or multiple adapters from a 2-port
               measurement. All S-Parameter inputs must be aligned. Port 2 of
               one network feeds port 1 of the subsequent network (see diag).
               This fuction supports de-embedding of adapters on either side
               of the DUT. If only a single adapter is used, set unused
               adapter to [] or np.tile([[0,1],[1,0]],(num_pts,1,1))
                     _______________________________________
                    |    _______     _______     _______    |
         A_DUT_B  o-|---|P1   P2|---|P1   P2|---|P1   P2|---|-o  A_DUT_B
          Port1     |   |  S_A  |   | S_DUT |   |  S_B  |   |    Port2
                  o-|---|_______|---|_______|---|_______|---|-o
                    |_______________________________________|
        inputs:
            S_A_DUT_B: [num_pts,2,2] S-Parameter description of the combined
                       network Adapter A - DUT - Adapter B
            S_A      : [num_pts,2,2] S-Parameter description of adapter on
                       the left (Port 1) side of the DUT
            S_B      : [num_pts,2,2] S-Parameter description of adapter on
                       the right (Port 2) side of the DUT
        outputs:
            S_DUT: [num_pts,2,2] S-parameter description of the DUT
    """
    num_pts=np.shape(S_A_DUT_B)[0]
    ideal_thru=np.tile([[0,1],[1,0]],(num_pts,1,1))
    if not type(S_A)==np.ndarray:
        S_A=ideal_thru
    if not type(S_B)==np.ndarray:
        S_B=ideal_thru
    T_A_DUT_B = S2T(S_A_DUT_B)
    T_A = S2T(S_A)
    T_B = S2T(S_B)
    T_DUT = np.matmul(inv(T_A),np.matmul(T_A_DUT_B,inv(T_B)))
    return T2S(T_DUT)

def getPortExtModel(gamma, gamma_listed):
    """
    Returns error term for the port-extension model. Port-extension is
    measured with an open or short termination at the desired measurement plane.
    input:
        gamma,gamma_listed: [num_pts] measured and listed reflection
            coefficient at the extended port
    output:
        e10e01: [num_pts] Transmission tracking coefficients of the error model
    """
    return gamma/gamma_listed
def correctPortExt(S_ext_dut, e10e01, port_num):
    """
    Performs correction of S-parameter data on one port based on the
    the port-extension model. Supports 2-Port networks only.
    input:
        S_ext_dut: [num_pts,2,2] uncorrected S-parameter data
        e10e01: [num_pts] Transmission tracking coefficients of the error model
        port_num: (1 or 2) port at which the adapter is connected
    output:
        S_dut: [num_pts] Corrected S-Parameters

                e10       __________
    Port    o---->----o--|          |--o
 (port_num)     e01      |   DUT    |
            o----<----o--|__________|--o
    """
    n,k = 0,0
    if port_num == 1:
        k = 1
    elif port_num == 2:
        n = 1
    else:
        print('Invalid Port Number. Options are 1 or 2')
    S_dut = sp.zeros([len(S_ext_dut),2,2],sp.complexfloating)
    S_dut[:,n,n] = S_ext_dut[:,n,n]/e10e01
    S_dut[:,n,k] = S_ext_dut[:,n,k]/np.sqrt(e10e01)
    S_dut[:,k,n] = S_ext_dut[:,k,n]/np.sqrt(e10e01)
    S_dut[:,k,k] = S_ext_dut[:,k,k]
    return S_dut

def plotCompareDb(freq_vec,S_array,title_array,settings_str=None):
    """
    Plots comparison of S-parameter objects given in the list S_array.
    Titles must be given for each plot in the list title_array uses scikit-rf
    plotting and matplotlib.
    input:
        freq_vec: [num_pts] frequency vector in MHz
        S_array: list of S-parameter 'stacks' size [num_pts,2,2] corrected S-parameters
        title_array: list of titles for the S-parameter plots
    """
    n = len(S_array)
    fig, axes = plt.subplots(1,n)
    for i in range(n):
        DUT = rf.Network(s=S_array[i],f=freq_vec,z0=50,f_unit='MHz')
        DUT.plot_s_db(ax=axes[i])
        axes[i].set_title(title_array[i])
    if settings_str is not None:
        plt.suptitle(settings_str)
    plt.show()

def plotCompareDeg(freq_vec,S_array,title_array,settings_str=None):
    """
    Plots comparison of S-parmeter objects given in the list S_array.
    Titles must be given for each plot in the list title_array uses scikit-rf
    plotting and matplotlib.
    input:
        freq_vec: [num_pts] frequency vector in MHz
        S_array: list of S-parameter 'stacks' size [num_pts,2,2] corrected S-parameters
        title_array: list of titles for the S-parameter plots
    """
    n = len(S_array)
    fig, axes = plt.subplots(1,n)
    for i in range(n):
        DUT = rf.Network(s=S_array[i],f=freq_vec,z0=50,f_unit='MHz')
        DUT.plot_s_deg_unwrap(ax=axes[i])
        axes[i].set_title(title_array[i])
    if settings_str is not None:
        plt.suptitle(settings_str)
    plt.show()

def plotCompareDbDeg(freq_vec,S_array,title_array,settings_str=None):
    """
    Plots comparison of S-parmeter objects given in the list S_array.
    Titles must be given for each plot in the list title_array uses scikit-rf
    plotting and matplotlib.
    input:
        freq_vec: [num_pts] frequency vector in MHz
        S_array: list of S-parameter 'stacks' size [num_pts,2,2] corrected S-parameters
        title_array: list of titles for the S-parameter plots
    """
    n = len(S_array)
    fig, axes = plt.subplots(2,n)
    for i in range(n):
        DUT = rf.Network(s=S_array[i],f=freq_vec,z0=50,f_unit='MHz')
        DUT.plot_s_db(ax=axes[0,i])
        DUT.plot_s_deg_unwrap(ax=axes[1,i])
        axes[0,i].set_title('Mag: '+title_array[i])
        axes[1,i].set_title('Phase: '+title_array[i])
    if settings_str is not None:
        plt.suptitle(settings_str)
    plt.show()
