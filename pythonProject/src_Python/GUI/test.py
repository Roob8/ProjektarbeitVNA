import tkinter as tk

def get_selected_radio_button(radio_button1, radio_button2):
    selected_value = tk.IntVar()

    def on_button_click():
        print(selected_value.get())  # Hier können Sie den ausgewählten Wert verwenden oder zurückgeben

    radio_button1.config(variable=selected_value, value=1, command=on_button_click)
    radio_button2.config(variable=selected_value, value=2, command=on_button_click)

    radio_button1.pack()
    radio_button2.pack()

    root.mainloop()

# Initialisierung der Tk-Instanz außerhalb der Funktion
root = tk.Tk()

# Beispielaufruf
radio1 = tk.Radiobutton(root, text="Option 1")
radio2 = tk.Radiobutton(root, text="Option 2")
get_selected_radio_button(radio1, radio2)
