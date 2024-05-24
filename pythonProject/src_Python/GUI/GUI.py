from cosmetic_defs import *
from tkinter import filedialog
from Functions import *
import vnakit

########################################################################################################################
#global choosen_port  # Globale Variable ob single oder dual port
#global which_single_port  # Globale Variable für den gewählten Port (A oder B)

global open_s_param_A
global short_s_param_A
global load_s_param_A
global open_s_param_B
global short_s_param_B
global load_s_param_B
global thru_s_param
global choosen_port

########################################################################################################################



def cal_buttom_clicked(port_variable, portlist):
    global choosen_port
    global which_single_port
    global cal_s_param

    own_meas.grid(row=7, column=0, sticky=center)
    s_meas.grid(row=7, column=2, sticky=center)
    ideal_meas.grid(row=7, column=4, sticky=center)
    checkbox_plot_cal.grid(row=9, column=columns - 1, sticky=right)

    portlist_index = portlist.curselection()
    which_single_port = portlist.get(portlist_index)    # Port A = 'A', Port B = 'B'
    choosen_port = port_variable.get()                  # 1 = Single, 2 = Dual


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

    if choosen_port_internal.get() == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_own.grid(row=8, column=1, columnspan=columns, sticky=left)
    if choosen_port_internal.get() == 2:
        single_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        dual_port_frame_own.grid(row=8, column=1, columnspan=columns, sticky=left)


def s_param_clicked():

    if choosen_port_internal.get() == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_own.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_s.grid(row=8, column=1, columnspan=columns, sticky=left)
    if choosen_port_internal.get() == 2:
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

    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param



    # @ Florian: Ideale S-Parameter Dateien müssen noch mit dem richtigen Inhalt befüllt werden
    open_s_param_A = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Open.s1p", freq_vec)
    short_s_param_A = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Short.s1p", freq_vec)
    load_s_param_A = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Load.s1p", freq_vec)
    open_s_param_B = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Open.s1p", freq_vec)
    short_s_param_B = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Short.s1p", freq_vec)
    load_s_param_B = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Load.s1p", freq_vec)
    thru_s_param = hid.readSnP("pythonProject/src_Python/GUI/stds/Ideal_Thru.s2p", freq_vec)


def run_button_clicked():
    global S_param_kompl
    global S_param_cor
    global S_param_dB
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    output_folder_button.grid(row=12, column=1, sticky=center)
    output_folder_output.grid(row=12, column=2, sticky=center)
    scrollbar_output_folder.grid(row=13, column=2, sticky=center)
    name_text.grid(row=14, column=1, sticky=center)
    name_input.grid(row=14, column=2, sticky=left)
    save_button.grid(row=12, column=4, sticky=center)

    start, stop, NOP, RBW, power = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input,
                                                      power_input)
    settings, freq_vec = init(start, stop, NOP, RBW, power, ports['Tx1'], "VNAKIT_MODE_ONE_PORT")

    cal_files = [open_s_param_A, short_s_param_A, load_s_param_A, open_s_param_B, short_s_param_B, load_s_param_B,
                 thru_s_param]

    calibration_selected = 1  # @Florian: Woran erkennt man, dass Kalibration ausgewählt ist?
    # channel_cal_method kann erkennen welche Kallibrationsmethode ausgewählt ist --> Nur checken wenn channel_cal_method == (1 oder 2) --> denn dann entweder eigene messung oder s params ausgewählt+
    # channel_cal_method muss dann aber eine globale Variable sein
    if calibration_selected == 1:
        status_cal = check_calibration(start, stop, NOP, RBW, power, cal_files)  # check if all calibration files exist
        if status_cal == 1:     # status_cal == 1 --> missing calibration file
            print("Messung nicht gestartet\n")
            return

    if which_single_port == "A":
        tx = "Tx1"
    elif which_single_port == "B":
        tx = "Tx2"

    S_param_kompl, S_param_cor, S_param_dB = run_measurement(settings, choosen_port_internal, tx, cal_files, ports,
                                                             freq_vec)


def output_folder_button_clicked():
    global folder_path

    folder_path = filedialog.askdirectory()
    output_folder_output.config(state="normal")
    output_folder_output.delete("1.0", "end")
    output_folder_output.insert("1.0", folder_path)
    output_folder_output.config(state="disabled")


def save_button_clicked():
    global freq_vec
    global S_param_kompl
    global S_param_cor
    global folder_path
    global settings

    file_name = name_input.get()
    save_measurements(settings, freq_vec, S_param_kompl, S_param_cor, folder_path, file_name)

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

    start, stop, NOP, RBW, power = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input,
                                                      power_input)
    if port == "A":
        settings, freq_vec = init(start, stop, NOP, RBW, power, ports['Tx1'], "VNAKIT_MODE_ONE_PORT")
        if DUT == "Open":
            print('Measure Open Port A')
            open_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
        if DUT == "Short":
            print('Measure Short Port A')
            short_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
        if DUT == "Load":
            print('Measure Load Port A')
            load_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
    if port == "B":
        settings, freq_vec = init(start, stop, NOP, RBW, power, ports['Tx2'], "VNAKIT_MODE_ONE_PORT")
        if DUT == "Open":
            print('Measure Open Port B')
            open_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])
        if DUT == "Short":
            print('Measure Short Port B')
            short_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])
        if DUT == "Load":
            print('Measure Load Port B')
            load_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])
    if DUT == "Thru":
        settings, freq_vec = init(start, stop, NOP, RBW, power, ports['Tx2'], "VNAKIT_MODE_TWO_PORT")
        print('Measure Thru')
        thru_s_param = cal_measure_t(vnakit, settings, ports, sw_corr=True)  # @Florian: Auswahl von switch correction?
        # ich würde immer mit switch correction Kallibrieren kann aber auch eine Box setzen

def two_port_cal(port, DUT):
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    start, stop, NOP, RBW, power = get_input_settings(start_freq_input, end_freq_input, nop_input, rbw_input,
                                                      power_input)
    settings, freq_vec = init(start, stop, NOP, RBW, power, ports['Tx1'], "VNAKIT_MODE_TWO_PORT")

    if port == "AB":
        print('Measure Thru')
        thru_s_param = cal_measure_t(vnakit, settings, ports, sw_corr=True)         # @Florian: Auswahl von switch correction? # genau so wie oben
    if port == "A":
        if DUT == "Open":
            print('Measure Open Port A')
            open_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
        if DUT == "Short":
            print('Measure Short Port A')
            short_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
        if DUT == "Load":
            print('Measure Load Port A')
            load_s_param_A = cal_measure_sol(vnakit, settings, ports, ports['Tx1'])
    if port == "B":
        if DUT == "Open":
            print('Measure Open Port B')
            open_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])
        if DUT == "Short":
            print('Measure Short Port B')
            short_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])
        if DUT == "Load":
            print('Measure Load Port B')
            load_s_param_B = cal_measure_sol(vnakit, settings, ports, ports['Tx2'])


columns = 5
root = Tk()
ports = {'Tx1': 6, 'Rx1A': 5, 'Rx1B': 4, 'Tx2': 3, 'Rx2A': 2, 'Rx2B': 1}

choosen_port_internal = IntVar(value=2)     # Dual ist ausgewählt
channel_cal_method = IntVar(value=3)        # Ideale Kalibration ist ausgewählt

# Initialisieren von globalen Variablen
open_s_param_A = 0
short_s_param_A = 0
load_s_param_A = 0
open_s_param_B = 0
short_s_param_B = 0
load_s_param_B = 0
thru_s_param = 0
choosen_port = 0

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
start_freq_input.insert(0,"100")
start_freq_input.grid(row=2, column=1, sticky=center)

end_freq_text = Label(root, text="Endfrequenz in MHz", font=text_normal)
end_freq_text.grid(row=2, column=3, sticky=center)

end_freq_input = Entry(root, font=text_normal, bd=bw)
end_freq_input.insert(0,"6000")
end_freq_input.grid(row=2, column=4, sticky=center)

power_text = Label(root, text="Eingangsleistung in dBm", font=text_normal)
power_text.grid(row=3, column=0, sticky=center)

power_input = Entry(root, font=text_normal, bd=bw)
power_input.insert(0, "-10")
power_input.grid(row=3, column=1, sticky=center)

nop_text = Label(root, text="Anzahl der Messpunkte", font=text_normal)
nop_text.grid(row=3, column=3, sticky=center)

nop_input = Entry(root, font=text_normal, bd=bw)
nop_input.insert(0,"1001")
nop_input.grid(row=3, column=4, sticky=center)

rbw_text = Label(root, text="RBW in kHz", font=text_normal)
rbw_text.grid(row=4, column=0, sticky=center)

rbw_input = Entry(root, font=text_normal, bd=bw)
rbw_input.insert(0,"10")
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
