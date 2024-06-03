import numpy as np
from hidden import readSnP
path = "C:\\Users\\RoobFlorian\\Documents\\Studium\\Master\\2. Semester\\Projekt_Sommersemester\\ProjektarbeitVNA\\pythonProject\\src_Python\\stds\\short.S1P"

freq_vec_Hz = np.linspace(100000000, 6000000000, 1001)

s_param = readSnP(path, freq_vec_Hz)

print(s_param)