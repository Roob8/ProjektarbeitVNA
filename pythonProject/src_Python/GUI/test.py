import numpy as np
from hidden import readSnP
import skrf as rf
import matplotlib.pyplot as plt

path = "C:\\Users\\RoobFlorian\\Documents\\Studium\\Master\\2. Semester\\Projekt_Sommersemester\\ProjektarbeitVNA\\pythonProject\\src_Python\\stds\\thru.S2P"

freq_vec_Hz = np.linspace(100000000, 6000000000, 1001)

s_param_roh = readSnP(path, freq_vec_Hz)
s_param_8_term = s_param_roh
s_param_12_term = s_param_8_term

fig, axes = plt.subplots(1,3)
DUT_roh = rf.Network(s=s_param_roh, f=freq_vec_Hz/1e6, z0=50, f_unit='MHz')
DUT_roh.plot_s_db(ax=axes[0])
axes[0].set_title('Unkallibrierte S-Parameter')

DUT_8_term = rf.Network(s=s_param_8_term, f=freq_vec_Hz/1e6, z0=50, f_unit='MHz')
DUT_8_term.plot_s_db(ax=axes[1])
axes[1].set_title('S-Parameter nach 8-term-Correction')

DUT_12_term = rf.Network(s=s_param_12_term, f=freq_vec_Hz/1e6, z0=50, f_unit='MHz')
DUT_12_term.plot_s_db(ax=axes[2])
axes[2].set_title('S-Parameter nach 12-term-Correction')


plt.show()