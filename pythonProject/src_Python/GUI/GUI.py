from utils import getSettingsStr
from cosmetic_defs import *
from tkinter import filedialog
from Functions import *
import vnakit

########################################################################################################################
global choosen_single_port_global

global open_s_param_A
global short_s_param_A
global load_s_param_A
global open_s_param_B
global short_s_param_B
global load_s_param_B
global thru_s_param

global s_param_roh
global s_param_12_term
global s_param_8_term

########################################################################################################################

def init_buttom_clicked():
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param


    own_meas.grid(row=8, column=0, sticky=center)
    s_meas.grid(row=8, column=2, sticky=center)
    ideal_meas.grid(row=8, column=4, sticky=center)
    run_buttom.grid(row=10, column=1, columnspan=3, sticky=center)

    try:
        vnakit.Init()

        freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
        open_s_param_A, open_s_param_B, load_s_param_A, load_s_param_B, short_s_param_A, short_s_param_B, thru_s_param = get_ideal_s_params(
            freq_vec_Hz)

        # eventuell schon beim initialisieren, die eingegebenen Werte aif Plausibilität überprüfen

        ''' Muss am Ende hier rein --> nur zum Ausprobieren steht es weiter oben
        own_meas.grid(row=8, column=0, sticky=center)
        s_meas.grid(row=8, column=2, sticky=center)
        ideal_meas.grid(row=8, column=4, sticky=center)
        run_buttom.grid(row=10, column=1, columnspan=3, sticky=center)
        '''

        init_button.config(bg=green)
        print("Initialisierung abgeschlossen!")

    except:
        print("VNA-INIT fehlgeschlagen! Bitte überprüfen ob das Gerät angeschlossen ist")
        init_button.config(bg=red)

def own_meas_clicked():
    global choosen_single_port_global

    choosen_single_port = get_choosen_single_port(portlist)
    choosen_single_port_global = choosen_single_port

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

    if dual_or_single_port.get() == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_own.grid(row=9, column=1, columnspan=columns, sticky=left)
        if choosen_single_port == "A":
            port_B_anzeige.grid_remove()
            port_A_anzeige.grid(row=9, column=0, sticky=center)
        elif choosen_single_port == "B":
            port_A_anzeige.grid_remove()
            port_B_anzeige.grid(row=9, column=0, sticky=center)

    if dual_or_single_port.get() == 2:
        single_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        dual_port_frame_s.grid_remove()
        port_A_anzeige.grid_remove()
        port_B_anzeige.grid_remove()
        dual_port_frame_own.grid(row=9, column=1, columnspan=columns, sticky=left)


def s_param_clicked():
    choosen_single_port = get_choosen_single_port(portlist)

    if dual_or_single_port.get() == 1:
        dual_port_frame_own.grid_remove()
        single_port_frame_own.grid_remove()
        dual_port_frame_s.grid_remove()
        single_port_frame_s.grid(row=9, column=1, columnspan=columns, sticky=left)
        if choosen_single_port == "A":
            port_B_anzeige.grid_remove()
            port_A_anzeige.grid(row=9, column=0, sticky=center)
        elif choosen_single_port == "B":
            port_A_anzeige.grid_remove()
            port_B_anzeige.grid(row=9, column=0, sticky=center)
    if dual_or_single_port.get() == 2:
        dual_port_frame_own.grid_remove()
        single_port_frame_own.grid_remove()
        single_port_frame_s.grid_remove()
        port_A_anzeige.grid_remove()
        port_B_anzeige.grid_remove()
        dual_port_frame_s.grid(row=9, column=0, columnspan=columns, sticky=left)


def ideal_clicked():
    dual_port_frame_own.grid_remove()
    single_port_frame_own.grid_remove()
    dual_port_frame_s.grid_remove()
    single_port_frame_s.grid_remove()
    port_A_anzeige.grid_remove()
    port_B_anzeige.grid_remove()

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

    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)

    open_s_param_A, open_s_param_B, load_s_param_A, load_s_param_B, short_s_param_A, short_s_param_B, thru_s_param = get_ideal_s_params(freq_vec_Hz)


def run_button_clicked():
    global s_param_roh
    global s_param_8_term
    global s_param_12_term
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

    settings = get_settings(start_freq_input,end_freq_input,nop_input,rbw_input,power_input,vnakit)
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    choosen_single_port = get_choosen_single_port(portlist)
    dual_or_single = dual_or_single_port.get()

    cal_files = [open_s_param_A, short_s_param_A, load_s_param_A, open_s_param_B, short_s_param_B, load_s_param_B,
                 thru_s_param]

    if choosen_single_port == "A":
        tx = "Tx1"
    elif choosen_single_port == "B":
        tx = "Tx2"

    s_param_roh, s_param_8_term, s_param_12_term = run_measurement(settings, dual_or_single, tx, cal_files, ports, freq_vec_Hz, vnakit)

def output_folder_button_clicked():
    global folder_path

    folder_path = filedialog.askdirectory()
    output_folder_output.config(state="normal")
    output_folder_output.delete("1.0", "end")
    output_folder_output.insert("1.0", folder_path)
    output_folder_output.config(state="disabled")


def save_button_clicked():
    global s_param_roh
    global s_param_8_term
    global s_param_12_term
    global folder_path

    freq_vec = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    settings = get_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input, vnakit)
    dual_or_single = dual_or_single_port.get()

    file_name = name_input.get()
    save_measurements(settings, freq_vec, s_param_roh, s_param_8_term, folder_path, file_name, dual_or_single, vnakit)

def get_path_open():
    global open_s_param_A
    global open_s_param_B

    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    choosen_single_port = get_choosen_single_port(portlist)

    path_open = filedialog.askopenfilename()
    path_open_output.config(state="normal")
    path_open_output.delete("1.0", "end")
    path_open_output.insert("1.0", path_open)
    path_open_output.config(state="disabled")

    if choosen_single_port == "A":
        open_s_param_A = load_sparam(freq_vec_Hz, path_open)
        print("done")
    elif choosen_single_port == "B":
        open_s_param_B = load_sparam(freq_vec_Hz, path_open)
        print("done")

def get_path_short():
    global short_s_param_A
    global short_s_param_B

    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    choosen_single_port = get_choosen_single_port(portlist)

    path_short = filedialog.askopenfilename()
    path_short_output.config(state="normal")
    path_short_output.delete("1.0", "end")
    path_short_output.insert("1.0", path_short)
    path_short_output.config(state="disabled")

    if choosen_single_port == "A":
        short_s_param_A = load_sparam(freq_vec_Hz, path_short)
    elif choosen_single_port == "B":
        short_s_param_B = load_sparam(freq_vec_Hz, path_short)


def get_path_load():
    global load_s_param_A
    global load_s_param_B

    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    choosen_single_port = get_choosen_single_port(portlist)

    path_load = filedialog.askopenfilename()
    path_load_output.config(state="normal")
    path_load_output.delete("1.0", "end")
    path_load_output.insert("1.0", path_load)
    path_load_output.config(state="disabled")

    if choosen_single_port == "A":
        load_s_param_A = load_sparam(freq_vec_Hz, path_load)
    elif choosen_single_port == "B":
        load_s_param_B = load_sparam(freq_vec_Hz, path_load)


def get_path_open_A():
    global open_s_param_A
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_open_A = filedialog.askopenfilename()
    path_open_A_output.config(state="normal")
    path_open_A_output.delete("1.0", "end")
    path_open_A_output.insert("1.0", path_open_A)
    path_open_A_output.config(state="disabled")
    open_s_param_A = load_sparam(freq_vec_Hz, path_open_A)


def get_path_short_A():
    global short_s_param_A
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_short_A = filedialog.askopenfilename()
    path_short_A_output.config(state="normal")
    path_short_A_output.delete("1.0", "end")
    path_short_A_output.insert("1.0", path_short_A)
    path_short_A_output.config(state="disabled")
    short_s_param_A = load_sparam(freq_vec_Hz, path_short_A)


def get_path_load_A():
    global load_s_param_A
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_load_A = filedialog.askopenfilename()
    path_load_A_output.config(state="normal")
    path_load_A_output.delete("1.0", "end")
    path_load_A_output.insert("1.0", path_load_A)
    path_load_A_output.config(state="disabled")
    load_s_param_A = load_sparam(freq_vec_Hz, path_load_A)


def get_path_open_B():
    global open_s_param_B
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_open_B = filedialog.askopenfilename()
    path_open_B_output.config(state="normal")
    path_open_B_output.delete("1.0", "end")
    path_open_B_output.insert("1.0", path_open_B)
    path_open_B_output.config(state="disabled")
    open_s_param_B = load_sparam(freq_vec_Hz, path_open_B)


def get_path_short_B():
    global short_s_param_B
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_short_B = filedialog.askopenfilename()
    path_short_B_output.config(state="normal")
    path_short_B_output.delete("1.0", "end")
    path_short_B_output.insert("1.0", path_short_B)
    path_short_B_output.config(state="disabled")
    short_s_param_B = load_sparam(freq_vec_Hz, path_short_B)


def get_path_load_B():
    global load_s_param_B
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_load_B = filedialog.askopenfilename()
    path_load_B_output.config(state="normal")
    path_load_B_output.delete("1.0", "end")
    path_load_B_output.insert("1.0", path_load_B)
    path_load_B_output.config(state="disabled")
    load_s_param_B = load_sparam(freq_vec_Hz, path_load_B)


def get_path_thru():
    global thru_s_param
    freq_vec_Hz = get_frequency_vector(start_freq_input, end_freq_input, nop_input)
    path_thru = filedialog.askopenfilename()
    path_thru_output.config(state="normal")
    path_thru_output.delete("1.0", "end")
    path_thru_output.insert("1.0", path_thru)
    path_thru_output.config(state="disabled")
    thru_s_param = load_sparam(freq_vec_Hz, path_thru)


def cal_port_measure(port, DUT):
    global open_s_param_A
    global short_s_param_A
    global load_s_param_A
    global open_s_param_B
    global short_s_param_B
    global load_s_param_B
    global thru_s_param

    settings = get_settings(start_freq_input, end_freq_input, nop_input, rbw_input, power_input, vnakit)

    if port == "AB":
        print('Measure Thru')
        thru_s_param = thru_measurement(vnakit, settings, ports)
    if port == "A":
        if DUT == "Open":
            print('Measure Open Port A')
            open_s_param_A = single_measurement(vnakit, settings, ports['Tx1'], ports)
        if DUT == "Short":
            print('Measure Short Port A')
            short_s_param_A = single_measurement(vnakit, settings, ports['Tx1'], ports)
        if DUT == "Load":
            print('Measure Load Port A')
            load_s_param_A = single_measurement(vnakit, settings, ports['Tx1'], ports)
    if port == "B":
        if DUT == "Open":
            print('Measure Open Port B')
            open_s_param_B = single_measurement(vnakit, settings, ports['Tx2'], ports)
        if DUT == "Short":
            print('Measure Short Port B')
            short_s_param_B = single_measurement(vnakit, settings, ports['Tx2'], ports)
        if DUT == "Load":
            print('Measure Load Port B')
            load_s_param_B = single_measurement(vnakit, settings, ports['Tx2'], ports)


# GUI start ------------------------------------------------------------------------------------------------------------
columns = 5
root = Tk()
ports = {'Tx1': 6, 'Rx1A': 5, 'Rx1B': 4, 'Tx2': 3, 'Rx2A': 2, 'Rx2B': 1}

dual_or_single_port = IntVar(value=2)     # Dual ist ausgewählt
channel_cal_method = IntVar(value=3)        # Ideale Kalibration ist ausgewählt

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

single_port_check = Radiobutton(root, text="Single Port", font=text_normal, variable=dual_or_single_port, value=1)
single_port_check.grid(row=4, column=2, sticky=center)

dual_port_check = Radiobutton(root, text="Dual Port", font=text_normal, variable=dual_or_single_port, value=2)
dual_port_check.grid(row=4, column=4, sticky=center)

insert_blank_line(root, 5, columns)

own_meas = Radiobutton(root, text="Eigene Messung Starten", font=text_normal, variable=channel_cal_method, value=1)
own_meas.config(command=lambda: own_meas_clicked())
port_A_anzeige = Label(root, text="Port A", font=text_normal)
port_B_anzeige = Label(root, text="Port B", font=text_normal)

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
open_meas.config(command=lambda: cal_port_measure(choosen_single_port_global, "Open"))
open_meas.grid(row=0, column=0, sticky=center)

short_meas = Button(single_port_frame_own, text="Short messen", font=text_normal)
short_meas.config(command=lambda: cal_port_measure(choosen_single_port_global, "Short"))
short_meas.grid(row=1, column=0, sticky=center)

load_meas = Button(single_port_frame_own, text="Load messen", font=text_normal)
load_meas.config(command=lambda: cal_port_measure(choosen_single_port_global, "Load"))
load_meas.grid(row=2, column=0, sticky=center)

########################################################################################################################
dual_port_frame_own = Frame(root)
for i in range(columns):
    dual_port_frame_own.columnconfigure(i, weight=1)

open_meas_A = Button(dual_port_frame_own, text="Open an Port A messen", font=text_normal)
open_meas_A.config(command=lambda: cal_port_measure("A", "Open"))
open_meas_A.grid(row=0, column=0, sticky=center)

short_meas_A = Button(dual_port_frame_own, text="Short an Port A messen", font=text_normal)
short_meas_A.config(command=lambda: cal_port_measure("A", "Short"))
short_meas_A.grid(row=1, column=0, sticky=center)

load_meas_A = Button(dual_port_frame_own, text="Load an Port A messen", font=text_normal)
load_meas_A.config(command=lambda: cal_port_measure("A", "Load"))
load_meas_A.grid(row=2, column=0, sticky=center)

open_meas_B = Button(dual_port_frame_own, text="Open an Port B messen", font=text_normal)
open_meas_B.config(command=lambda: cal_port_measure("B", "Open"))
open_meas_B.grid(row=0, column=1, sticky=center)

short_meas_B = Button(dual_port_frame_own, text="Short an Port B messen", font=text_normal)
short_meas_B.config(command=lambda: cal_port_measure("B", "Short"))
short_meas_B.grid(row=1, column=1, sticky=center)

load_meas_B = Button(dual_port_frame_own, text="Load an Port B messen", font=text_normal)
load_meas_B.config(command=lambda: cal_port_measure("B", "Load"))
load_meas_B.grid(row=2, column=1, sticky=center)

thru_meas = Button(dual_port_frame_own, text="Thru messen", font=text_normal)
thru_meas.config(command=lambda: cal_port_measure("AB", "Thru"))
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

insert_blank_line(root, 7, columns)

init_button = Button(root, text="INIT.", font=text_normal, bg=red)
init_button.config(command=lambda: init_buttom_clicked())
init_button.grid(row=6, column=1, columnspan=3, sticky=center)

run_buttom = Button(root, text="Messung starten", font=text_normal, bg=green)
run_buttom.config(command=lambda: run_button_clicked())

insert_blank_line(root, 9, columns)

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
