from pathlib import Path
import datetime as dt
import os
import numpy as np
import sys
import pandas as pd

# "Ausgaben" Ordner erzeugen
subfolder_name = 'Ausgaben'
subfolder_path = Path(subfolder_name)

# check if folder exist
if not subfolder_path.is_dir():
    subfolder_path.mkdir()

# check if filename exist
date_time = dt.datetime.now()
date_time = date_time.strftime("%Y%m%d_%H_%M")
filename = "Ausgaben/" + str(date_time) + ".xlsx"
no = 1

while os.path.exists(filename):
    filename = filename[:-5] + '_' + str(no) + ".xlsx"
    no += 1
    if no >= 10:
        print("Measurement could not be stored!")
        sys.exit()

data1 = np.random.rand(100)
data2 = np.random.rand(100)
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)


excel_writer = pd.ExcelWriter(filename)    # Excel-Datei erstellen
df1.to_excel(excel_writer, sheet_name="Calibrated measurement")
df2.to_excel(excel_writer, sheet_name="UncCalibrated measurement")
excel_writer.save()  # Excel-Writer schließen, um die Datei zu speichern

print("Measurement store to Excel done!")