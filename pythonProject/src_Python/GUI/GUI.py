from cosmetic_defs import *

from tkinter import filedialog
from Functions import *
import pandas as pd

########################################################################################################################
global choosen_port  # Globale Variable ob single oder dual port
global which_single_port  # Globale Variable für den gewählten Port (A oder B)

global open_s_param_A
global short_s_param_A
global load_s_param_A
global open_s_param_B
global short_s_param_B
global load_s_param_B
global thru_s_param


########################################################################################################################

def get_ideal_s_params():
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    open_s_param_A = "ideale open s params"
    short_s_param_A = "ideale short s params"
    load_s_param_A = "ideale load s params"
    open_s_param_B = "ideale open s params"
    short_s_param_B = "ideale short s params"
    load_s_param_B = "ideale load s params"
    thru_s_param = "ideale thru s params"


def cal_buttom_clicked(port_variable, portlist):
    global choosen_port
    global which_single_port
    portlist_index = portlist.curselection()
    which_single_port = portlist.get(portlist_index)
    choosen_port = port_variable.get()  # 1 = Single, 2 = Dual

    own_meas.grid(row=7, column=0, sticky=center)
    s_meas.grid(row=7, column=2, sticky=center)
    ideal_meas.grid(row=7, column=4, sticky=center)

    checkbox_plot_cal.grid(row=9, column=columns - 1, sticky=right)


def own_meas_clicked():
    path_open_output.config(state="normal")
    path_open_output.delete("1.0", "end")
    path_open_output.config(state="disabled")

    path_short_output.config(state="normal")
    path_short_output.delete("1.0", "end")
    path_short_output.config(state="disabled")

    path_load_output.config(state="normal")
    path_load_output.delete("1.0", "end")
    path_load_output.config(state="disabled")

    path_open_A_output.config(state="normal")
    path_open_A_output.delete("1.0", "end")
    path_open_A_output.config(state="disabled")

    path_open_B_output.config(state="normal")
    path_open_B_output.delete("1.0", "end")
    path_open_B_output.config(state="disabled")

    path_short_A_output.config(state="normal")
    path_short_A_output.delete("1.0", "end")
    path_short_A_output.config(state="disabled")

    path_short_B_output.config(state="normal")
    path_short_B_output.delete("1.0", "end")
    path_short_B_output.config(state="disabled")

    path_load_A_output.config(state="normal")
    path_load_A_output.delete("1.0", "end")
    path_load_A_output.config(state="disabled")

    path_load_B_output.config(state="normal")
    path_load_B_output.delete("1.0", "end")
    path_load_B_output.config(state="disabled")

    path_thru_output.config(state="normal")
    path_thru_output.delete("1.0", "end")
    path_thru_output.config(state="disabled")

    if choosen_port == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_own.grid(row=8, column=1, columnspan=columns, sticky=left)
    if choosen_port == 2:
        single_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        dual_port_frame_own.grid(row=8, column=1, columnspan=columns, sticky=left)


def s_param_clicked():
    if choosen_port == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_own.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_s.grid(row=8, column=1, columnspan=columns, sticky=left)
    if choosen_port == 2:
        dual_port_frame_own.grid_remove()
        single_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid(row=8, column=0, columnspan=columns, sticky=left)


def ideal_clicked():
    dual_port_frame_own.grid_remove()
    single_port_frame_own.grid_remove()
    dual_port_frame_s.grid_remove()
    single_port_frame_s.grid_remove()

    path_open_output.config(state="normal")
    path_open_output.delete("1.0", "end")
    path_open_output.config(state="disabled")

    path_short_output.config(state="normal")
    path_short_output.delete("1.0", "end")
    path_short_output.config(state="disabled")

    path_load_output.config(state="normal")
    path_load_output.delete("1.0", "end")
    path_load_output.config(state="disabled")

    path_open_A_output.config(state="normal")
    path_open_A_output.delete("1.0", "end")
    path_open_A_output.config(state="disabled")

    path_open_B_output.config(state="normal")
    path_open_B_output.delete("1.0", "end")
    path_open_B_output.config(state="disabled")

    path_short_A_output.config(state="normal")
    path_short_A_output.delete("1.0", "end")
    path_short_A_output.config(state="disabled")

    path_short_B_output.config(state="normal")
    path_short_B_output.delete("1.0", "end")
    path_short_B_output.config(state="disabled")

    path_load_A_output.config(state="normal")
    path_load_A_output.delete("1.0", "end")
    path_load_A_output.config(state="disabled")

    path_load_B_output.config(state="normal")
    path_load_B_output.delete("1.0", "end")
    path_load_B_output.config(state="disabled")

    path_thru_output.config(state="normal")
    path_thru_output.delete("1.0", "end")
    path_thru_output.config(state="disabled")

    get_ideal_s_params()


def run_button_clicked():
    global S_params

    output_folder_button.grid(row=12, column=1, sticky=center)
    output_folder_output.grid(row=12, column=2, sticky=center)
    scrollbar_output_folder.grid(row=13, column=2, sticky=center)
    name_text.grid(row=14, column=1, sticky=center)
    name_input.grid(row=14, column=2, sticky=left)
    save_button.grid(row=12, column=4, sticky=center)

    cal_files = [open_s_param_A, short_s_param_A, load_s_param_A, open_s_param_B, short_s_param_B, load_s_param_B,
                 thru_s_param]

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    choosen_port = "Tx1"
    which_single_port = "Tx1"
    S_params = run_measurement(input_settings, choosen_port, which_single_port, cal_files, cal_plot_check.get())


def output_folder_button_clicked():
    global folder_path

    folder_path = filedialog.askdirectory()
    output_folder_output.config(state="normal")
    output_folder_output.delete("1.0", "end")
    output_folder_output.insert("1.0", folder_path)
    output_folder_output.config(state="disabled")


def save_button_clicked():
    global folder_path
    # global S_params

    # Dateipfad zur S-Parameter-Datei
    load    = r"C:\Users\leix\Desktop\HTW Dresden\SS24\Projektarbeit Vector-Network-Analyzer\Github_Roob\ProjektarbeitVNA\pythonProject\src_Python\stds\load.s1p"
    open    = r"C:\Users\leix\Desktop\HTW Dresden\SS24\Projektarbeit Vector-Network-Analyzer\Github_Roob\ProjektarbeitVNA\pythonProject\src_Python\stds\open.s1p"
    short   = r"C:\Users\leix\Desktop\HTW Dresden\SS24\Projektarbeit Vector-Network-Analyzer\Github_Roob\ProjektarbeitVNA\pythonProject\src_Python\stds\short.s1p"
    # thru    = r"C:\Users\leix\Desktop\HTW Dresden\SS24\Projektarbeit Vector-Network-Analyzer\Github_Roob\ProjektarbeitVNA\pythonProject\src_Python\stds\thru.s1p"

    # Einlesen der S-Parameter-Datei
    df_load = pd.read_csv(load, skiprows=5, delimiter="\t", header=None,
                     names=['Frequency', 'S11_real', 'S11_imaginary', 'S21_real', 'S21_imaginary', 'S12_real',
                            'S12_imaginary', 'S22_real', 'S22_imaginary'])

    df_open = pd.read_csv(open, skiprows=5, delimiter="\t", header=None,
                          names=['Frequency', 'S11_real', 'S11_imaginary', 'S21_real', 'S21_imaginary', 'S12_real',
                                 'S12_imaginary', 'S22_real', 'S22_imaginary'])

    df_short = pd.read_csv(short, skiprows=5, delimiter="\t", header=None,
                          names=['Frequency', 'S11_real', 'S11_imaginary', 'S21_real', 'S21_imaginary', 'S12_real',
                                 'S12_imaginary', 'S22_real', 'S22_imaginary'])
    '''
    df_thru = pd.read_csv(thru, skiprows=5, delimiter="\t", header=None,
                          names=['Frequency', 'S11_real', 'S11_imaginary', 'S21_real', 'S21_imaginary', 'S12_real',
                                 'S12_imaginary', 'S22_real', 'S22_imaginary'])
    '''
    # in demo_full_2_port.py wird settings_str = getSettingsStr(settings) verwendet
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    S_params = [df_load, df_open, df_short]
    save_measurements(input_settings, S_params, folder_path, name_input.get())


def get_path_open():
    global open_s_param_A
    global open_s_param_B

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)

    path_open = filedialog.askopenfilename()
    path_open_output.config(state="normal")
    path_open_output.delete("1.0", "end")
    path_open_output.insert("1.0", path_open)
    path_open_output.config(state="disabled")

    if which_single_port == "A":
        open_s_param_A = load_sparam(input_settings, path_open)
    elif which_single_port == "B":
        open_s_param_B = load_sparam(input_settings, path_open)


def get_path_short():
    global short_s_param_A
    global short_s_param_B

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)

    path_short = filedialog.askopenfilename()
    path_short_output.config(state="normal")
    path_short_output.delete("1.0", "end")
    path_short_output.insert("1.0", path_short)
    path_short_output.config(state="disabled")

    if which_single_port == "A":
        short_s_param_A = load_sparam(input_settings, path_short)
    elif which_single_port == "B":
        short_s_param_B = load_sparam(input_settings, path_short)


def get_path_load():
    global load_s_param_A
    global load_s_param_B

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)

    path_load = filedialog.askopenfilename()
    path_load_output.config(state="normal")
    path_load_output.delete("1.0", "end")
    path_load_output.insert("1.0", path_load)
    path_load_output.config(state="disabled")

    if which_single_port == "A":
        load_s_param_A = load_sparam(input_settings, path_load)
    elif which_single_port == "B":
        load_s_param_B = load_sparam(input_settings, path_load)


def get_path_open_A():
    global open_s_param_A
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_open_A = filedialog.askopenfilename()
    path_open_A_output.config(state="normal")
    path_open_A_output.delete("1.0", "end")
    path_open_A_output.insert("1.0", path_open_A)
    path_open_A_output.config(state="disabled")
    open_s_param_A = load_sparam(input_settings, path_open_A)


def get_path_short_A():
    global short_s_param_A
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_short_A = filedialog.askopenfilename()
    path_short_A_output.config(state="normal")
    path_short_A_output.delete("1.0", "end")
    path_short_A_output.insert("1.0", path_short_A)
    path_short_A_output.config(state="disabled")
    short_s_param_A = load_sparam(input_settings, path_short_A)


def get_path_load_A():
    global load_s_param_A
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_load_A = filedialog.askopenfilename()
    path_load_A_output.config(state="normal")
    path_load_A_output.delete("1.0", "end")
    path_load_A_output.insert("1.0", path_load_A)
    path_load_A_output.config(state="disabled")
    load_s_param_A = load_sparam(input_settings, path_load_A)


def get_path_open_B():
    global open_s_param_B
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_open_B = filedialog.askopenfilename()
    path_open_B_output.config(state="normal")
    path_open_B_output.delete("1.0", "end")
    path_open_B_output.insert("1.0", path_open_B)
    path_open_B_output.config(state="disabled")
    open_s_param_B = load_sparam(input_settings, path_open_B)


def get_path_short_B():
    global short_s_param_B
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_short_B = filedialog.askopenfilename()
    path_short_B_output.config(state="normal")
    path_short_B_output.delete("1.0", "end")
    path_short_B_output.insert("1.0", path_short_B)
    path_short_B_output.config(state="disabled")
    short_s_param_B = load_sparam(input_settings, path_short_B)


def get_path_load_B():
    global load_s_param_B
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_load_B = filedialog.askopenfilename()
    path_load_B_output.config(state="normal")
    path_load_B_output.delete("1.0", "end")
    path_load_B_output.insert("1.0", path_load_B)
    path_load_B_output.config(state="disabled")
    load_s_param_B = load_sparam(input_settings, path_load_B)


def get_path_thru():
    global thru_s_param
    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)
    path_thru = filedialog.askopenfilename()
    path_thru_output.config(state="normal")
    path_thru_output.delete("1.0", "end")
    path_thru_output.insert("1.0", path_thru)
    path_thru_output.config(state="disabled")
    thru_s_param = load_sparam(input_settings, path_thru)


def one_port_cal(port, DUT):
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)

    s_params = single_measurement(input_settings, port)

    if port == "A":
        if DUT == "Open":
            print("Open A")
            open_s_param_A = s_params
        if DUT == "Short":
            print("Short A")
            short_s_param_A = s_params
        if DUT == "Load":
            print("Load A")
            load_s_param_A = s_params
    if port == "B":
        # Messung starten
        if DUT == "Open":
            print("Open B")
            open_s_param_B = s_params
        if DUT == "Short":
            print("Short B")
            short_s_param_B = s_params
        if DUT == "Load":
            print("Load B")
            load_s_param_B = s_params
    if DUT == "Thru":
        thru_s_param = s_params


def two_port_cal(port, DUT):
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    input_settings = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input)

    if port == "AB":
        thru_s_param = dual_measurement(input_settings)
    if port == "A":
        if DUT == "Open":
            open_s_param_A = single_measurement(input_settings, "A")
        if DUT == "Short":
            short_s_param_A = single_measurement(input_settings, "A")
        if DUT == "Load":
            load_s_param_A = single_measurement(input_settings, "A")
    if port == "B":
        if DUT == "Open":
            open_s_param_B = single_measurement(input_settings, "B")
        if DUT == "Short":
            short_s_param_B = single_measurement(input_settings, "B")
        if DUT == "Load":
            load_s_param_B = single_measurement(input_settings, "B")


columns = 5

root = Tk()

get_ideal_s_params()

choosen_port_internal = IntVar(value=2)  # Dual ist ausgewählt
channel_cal_method = IntVar(value=3)  # Ideale Kalibration ist ausgewählt

root.title("Network Analyzer GUI")
x_size = 1000
y_size = root.winfo_screenheight()
root.geometry("%dx%d" % (x_size, y_size))

# define variable width for all columns
for i in range(columns):
    root.columnconfigure(i, weight=1)

headline = Label(root, text="Grafische Umgebung für die Verwendung des Network Analyzers", font=header_bold_underline)
headline.grid(row=0, column=0, columnspan=columns, sticky=center)

insert_blank_line(root, 1, columns)

start_freq_text = Label(root, text="Startfrequenz in MHz", font=text_normal)
start_freq_text.grid(row=2, column=0, sticky=center)

start_freq_input = Entry(root, font=text_normal, bd=bw)
start_freq_input.grid(row=2, column=1, sticky=center)

end_freq_text = Label(root, text="Endfrequenz in MHz", font=text_normal)
end_freq_text.grid(row=2, column=3, sticky=center)

end_freq_input = Entry(root, font=text_normal, bd=bw)
end_freq_input.grid(row=2, column=4, sticky=center)

power_text = Label(root, text="Eingangsleistung in dBm", font=text_normal)
power_text.grid(row=3, column=0, sticky=center)

power_input = Entry(root, font=text_normal, bd=bw)
power_input.insert(0, "-10")
power_input.grid(row=3, column=1, sticky=center)

nop_text = Label(root, text="Anzahl der Messpunkte", font=text_normal)
nop_text.grid(row=3, column=3, sticky=center)

nop_input = Entry(root, font=text_normal, bd=bw)
nop_input.grid(row=3, column=4, sticky=center)

rbw_text = Label(root, text="RBW in kHz", font=text_normal)
rbw_text.grid(row=4, column=0, sticky=center)

rbw_input = Entry(root, font=text_normal, bd=bw)
rbw_input.grid(row=4, column=1, sticky=center)

portlist = Listbox(selectmode='single', height=2)
portlist.insert("end", "A")
portlist.insert("end", "B")
portlist.select_set(0)
portlist.grid(row=4, column=3, sticky=center)

single_port_check = Radiobutton(root, text="Single Port", font=text_normal, variable=choosen_port_internal, value=1)
single_port_check.grid(row=4, column=2, sticky=center)

dual_port_check = Radiobutton(root, text="Dual Port", font=text_normal, variable=choosen_port_internal, value=2)
dual_port_check.grid(row=4, column=4, sticky=center)

insert_blank_line(root, 6, columns)

open_cal_button = Button(root, text="Kalibrationsauswahl öffnen/aktualisieren", font=text_normal)
open_cal_button.config(command=lambda: cal_buttom_clicked(choosen_port_internal, portlist))
open_cal_button.grid(row=5, column=0, columnspan=2, sticky=left)

own_meas = Radiobutton(root, text="Eigene Messung Starten", font=text_normal, variable=channel_cal_method, value=1)
own_meas.config(command=lambda: own_meas_clicked())

s_meas = Radiobutton(root, text="S-Parameter wählen", font=text_normal, variable=channel_cal_method, value=2)
s_meas.config(command=lambda: s_param_clicked())

ideal_meas = Radiobutton(root, text="Ideale Kalibrierung nutzen", font=text_normal, variable=channel_cal_method,
                         value=3)
ideal_meas.config(command=lambda: ideal_clicked())

########################################################################################################################

single_port_frame_own = Frame(root)
for i in range(columns):
    single_port_frame_own.columnconfigure(i, weight=1)

open_meas = Button(single_port_frame_own, text="Open messen", font=text_normal)
open_meas.config(command=lambda: one_port_cal(which_single_port, "Open"))
open_meas.grid(row=0, column=0, sticky=center)

short_meas = Button(single_port_frame_own, text="Short messen", font=text_normal)
short_meas.config(command=lambda: one_port_cal(which_single_port, "Short"))
short_meas.grid(row=1, column=0, sticky=center)

load_meas = Button(single_port_frame_own, text="Load messen", font=text_normal)
load_meas.config(command=lambda: one_port_cal(which_single_port, "Load"))
load_meas.grid(row=2, column=0, sticky=center)

########################################################################################################################
dual_port_frame_own = Frame(root)
for i in range(columns):
    dual_port_frame_own.columnconfigure(i, weight=1)

open_meas_A = Button(dual_port_frame_own, text="Open an Port A messen", font=text_normal)
open_meas_A.config(command=lambda: two_port_cal("A", "Open"))
open_meas_A.grid(row=0, column=0, sticky=center)

short_meas_A = Button(dual_port_frame_own, text="Short an Port A messen", font=text_normal)
short_meas_A.config(command=lambda: two_port_cal("A", "Short"))
short_meas_A.grid(row=1, column=0, sticky=center)

load_meas_A = Button(dual_port_frame_own, text="Load an Port A messen", font=text_normal)
load_meas_A.config(command=lambda: two_port_cal("A", "Load"))
load_meas_A.grid(row=2, column=0, sticky=center)

open_meas_B = Button(dual_port_frame_own, text="Open an Port B messen", font=text_normal)
open_meas_B.config(command=lambda: two_port_cal("B", "Open"))
open_meas_B.grid(row=0, column=1, sticky=center)

short_meas_B = Button(dual_port_frame_own, text="Short an Port B messen", font=text_normal)
short_meas_B.config(command=lambda: two_port_cal("B", "Short"))
short_meas_B.grid(row=1, column=1, sticky=center)

load_meas_B = Button(dual_port_frame_own, text="Load an Port B messen", font=text_normal)
load_meas_B.config(command=lambda: two_port_cal("B", "Load"))
load_meas_B.grid(row=2, column=1, sticky=center)

thru_meas = Button(dual_port_frame_own, text="Thru messen", font=text_normal)
thru_meas.config(command=lambda: two_port_cal("AB", "Thru"))
thru_meas.grid(row=3, column=0, columnspan=2, sticky=center)

########################################################################################################################
single_port_frame_s = Frame(root)

for i in range(columns):
    single_port_frame_s.columnconfigure(i, weight=1)

open_s = Button(single_port_frame_s, text="Open S-Parameter wählen", font=text_normal)
open_s.config(command=lambda: get_path_open())
open_s.grid(row=0, column=0, sticky=center)

path_open_output = Text(single_port_frame_s, wrap="none", height=1, width=50)
path_open_output.grid(row=0, column=1, sticky=center)
path_open_output.config(state="disabled")

scrollbar_open = Scrollbar(single_port_frame_s, orient=HORIZONTAL, command=path_open_output.xview)
scrollbar_open.grid(row=1, column=1, sticky=center)
path_open_output.config(xscrollcommand=scrollbar_open.set)

short_s = Button(single_port_frame_s, text="Short S-Parameter wählen", font=text_normal)
short_s.config(command=lambda: get_path_short())
short_s.grid(row=2, column=0, sticky=center)

path_short_output = Text(single_port_frame_s, wrap="none", height=1, width=50)
path_short_output.grid(row=2, column=1, sticky=center)
path_short_output.config(state="disabled")

scrollbar_short = Scrollbar(single_port_frame_s, orient=HORIZONTAL, command=path_short_output.xview)
scrollbar_short.grid(row=3, column=1, sticky=center)
path_short_output.config(xscrollcommand=scrollbar_short.set)

load_s = Button(single_port_frame_s, text="Load S-Parameter wählen", font=text_normal)
load_s.config(command=lambda: get_path_load())
load_s.grid(row=4, column=0, sticky=center)

path_load_output = Text(single_port_frame_s, wrap="none", height=1, width=50)
path_load_output.grid(row=4, column=1, sticky=center)
path_load_output.config(state="disabled")

scrollbar_load = Scrollbar(single_port_frame_s, orient=HORIZONTAL, command=path_load_output.xview)
scrollbar_load.grid(row=5, column=1, sticky=center)
path_load_output.config(xscrollcommand=scrollbar_load.set)
########################################################################################################################
dual_port_frame_s = Frame(root)
for i in range(columns):
    dual_port_frame_s.columnconfigure(i, weight=1)

open_s_A = Button(dual_port_frame_s, text="Open S-Parameter Port A", font=text_normal)
open_s_A.config(command=lambda: get_path_open_A())
open_s_A.grid(row=0, column=0, sticky=center)

path_open_A_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_open_A_output.grid(row=0, column=1, sticky=center)
path_open_A_output.config(state="disabled")

scrollbar_open_A = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_open_A_output.xview)
scrollbar_open_A.grid(row=1, column=1, sticky=center)
path_open_A_output.config(xscrollcommand=scrollbar_open_A.set)

short_s_A = Button(dual_port_frame_s, text="Short S-Parameter Port A", font=text_normal)
short_s_A.config(command=lambda: get_path_short_A())
short_s_A.grid(row=2, column=0, sticky=center)

path_short_A_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_short_A_output.grid(row=2, column=1, sticky=center)
path_short_A_output.config(state="disabled")

scrollbar_short_A = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_short_A_output.xview)
scrollbar_short_A.grid(row=3, column=1, sticky=center)
path_short_A_output.config(xscrollcommand=scrollbar_short_A.set)

load_s_A = Button(dual_port_frame_s, text="Load S-Parameter Port A", font=text_normal)
load_s_A.config(command=lambda: get_path_load_A())
load_s_A.grid(row=4, column=0, sticky=center)

path_load_A_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_load_A_output.grid(row=4, column=1, sticky=center)
path_load_A_output.config(state="disabled")

scrollbar_load_A = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_load_A_output.xview)
scrollbar_load_A.grid(row=5, column=1, sticky=center)
path_load_A_output.config(xscrollcommand=scrollbar_load_A.set)

open_s_B = Button(dual_port_frame_s, text="Open S-Parameter Port B", font=text_normal)
open_s_B.config(command=lambda: get_path_open_B())
open_s_B.grid(row=0, column=2, sticky=center)

path_open_B_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_open_B_output.grid(row=0, column=3, sticky=center)
path_open_B_output.config(state="disabled")

scrollbar_open_B = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_open_B_output.xview)
scrollbar_open_B.grid(row=1, column=3, sticky=center)
path_open_B_output.config(xscrollcommand=scrollbar_open_B.set)

short_s_B = Button(dual_port_frame_s, text="Short S-Parameter Port B", font=text_normal)
short_s_B.config(command=lambda: get_path_short_B())
short_s_B.grid(row=2, column=2, sticky=center)

path_short_B_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_short_B_output.grid(row=2, column=3, sticky=center)
path_short_B_output.config(state="disabled")

scrollbar_short_B = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_short_B_output.xview)
scrollbar_short_B.grid(row=3, column=3, sticky=center)
path_short_B_output.config(xscrollcommand=scrollbar_short_B.set)

load_s_B = Button(dual_port_frame_s, text="Load S-Parameter Port B", font=text_normal)
load_s_B.config(command=lambda: get_path_load_B())
load_s_B.grid(row=4, column=2, sticky=center)

path_load_B_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_load_B_output.grid(row=4, column=3, sticky=center)
path_load_B_output.config(state="disabled")

scrollbar_load_B = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_load_B_output.xview)
scrollbar_load_B.grid(row=5, column=3, sticky=center)
path_load_B_output.config(xscrollcommand=scrollbar_load_B.set)

thru_s = Button(dual_port_frame_s, text="Thru S-Parameter", font=text_normal)
thru_s.config(command=lambda: get_path_thru())
thru_s.grid(row=6, column=0, sticky=center)

path_thru_output = Text(dual_port_frame_s, wrap="none", height=1, width=35)
path_thru_output.grid(row=6, column=1, sticky=center)
path_thru_output.config(state="disabled")

scrollbar_thru = Scrollbar(dual_port_frame_s, orient=HORIZONTAL, command=path_thru_output.xview)
scrollbar_thru.grid(row=7, column=1, sticky=center)
path_thru_output.config(xscrollcommand=scrollbar_thru.set)

########################################################################################################################

cal_plot_check = IntVar(value=0)
checkbox_plot_cal = Checkbutton(root, text="Kalibrationsergebnisse plotten?", variable=cal_plot_check, font=text_short)

insert_blank_line(root, 9, columns)

run_buttom = Button(root, text="Messung starten", font=text_normal, bg=green)
run_buttom.config(command=lambda: run_button_clicked())
run_buttom.grid(row=10, column=1, columnspan=3, sticky=center)

insert_blank_line(root, 11, columns)

output_folder_button = Button(root, text="Ausgabeordner wählen", font=text_normal)
output_folder_button.config(command=lambda: output_folder_button_clicked())

output_folder_output = Text(root, wrap="none", height=1, width=40)

output_folder_output.config(state="disabled")

scrollbar_output_folder = Scrollbar(root, orient=HORIZONTAL, command=output_folder_output.xview)
output_folder_output.config(xscrollcommand=scrollbar_output_folder.set)

name_text = Label(root, text="Namen wählen", font=text_normal)

name_input = Entry(root, font=text_normal, bd=bw)

save_button = Button(root, text="Save", font=text_normal, bg=grey)
save_button.config(command=lambda: save_button_clicked())

root.mainloop()
