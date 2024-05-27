import pickle
import GUI.vnakit as vnakit
import numpy as np

with open("C:\\Users\\RoobFlorian\Documents\\Studium\\Master\\2. Semester\Projekt_Sommersemester\\ProjektarbeitVNA\\pythonProject\\src_Python\Pickle\\frequenz_vek.pkl", 'rb') as file:  # Daten laden
    freq_vec1 = pickle.load(file)

freq_vec2 = np.linspace(100, 6000, 1001)


print("test")