# We import the GUI
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import ImageTk, Image

# We import the data manipulation library
import pandas as pd

# Import the signal-simulating library
import neurokit2 as nk  # Load the package

# Import the plotter
import matplotlib.pyplot as plt

# Import the random generating numbers
from random import *


# Function to remove the present widgets when changing profiles and not leaving behind previous charts
def reset_buttons():
    for widgets in root.winfo_children():
        widgets.destroy()
    add = ttk.Button(root, text='+', command=lambda: add_patient())
    add.place(x=640, y=130, width=50, height=30)
    remove = ttk.Button(root, text='-', command=lambda: remove_patient())
    remove.place(x=700, y=130, width=50, height=30)

    button_list()


# Generation and print of the profile's data
def show_data(selector):
    if selector:
        # Table
        table(selector)
        ecg(selector)
        eeg(selector)
        rsp(selector)
    # In case the profile is empty
    else:
        reset_buttons()


# Function create a new profile
def add_patient():
    answer = simpledialog.askstring('Input', 'Full name:',
                                    parent=root)
    if isinstance(answer, str):
        file_new = messagebox.askyesno(message='Do yo want to create a new data file?', title='New File')
        if file_new:
            patient_data = pd.DataFrame([[randint(45, 120), randint(100, 180), randint(100, 180), randint(45, 120)],
                                         [randint(20, 70), randint(20, 70), randint(20, 70), randint(20, 70)],
                                         [randint(35, 40), randint(36, 41), randint(37, 42), randint(37, 42)]],
                                        index=['BPM', 'Respiratory rate', 'Temperature(ºC)'],
                                        columns=['00:00', '06:00', '12:00', '18:00'])
            file_name = f'{answer}.xlsx'
            patient_data.to_excel(file_name, sheet_name='Day 1')
        patients.append(answer)
        reset_buttons()
        show_data(answer)


# Function defined to allow the removal of a profile
def remove_patient():
    try:
        patients.pop(0)
    except:
        # Error message in case the profile no longer exists
        messagebox.showerror('Not found', 'Error: The file you want to delete it no longer exist!')
    else:
        # Confirmation message
        messagebox.showinfo(message="Patient removed successfully", title="Removal complete")
        reset_buttons()


# Function for the option menu where the profiles can be selected
def button_list():
    variable = tk.StringVar(root)
    variable.set(patients[0])  # default value
    w = ttk.OptionMenu(root, variable, *patients, command=show_data)
    w.place(x=640, y=100, height=20, width=140)


# Function to adapt .xlsx format in order to be represented by Tkinter correctly
def table(name):
    try:
        data_file = pd.read_excel(f'{name}.xlsx')
    except:
        messagebox.showerror('File Error', f'Error: There is no file named{name}.xlsx!')
    else:
        data_file.rename(columns={'Unnamed: 0': name}, inplace=True)
        n_rows = data_file.shape[0]
        n_cols = data_file.shape[1]

        # Extracting columns from the data and
        # creating text widget with some
        # background color
        column_names = data_file.columns
        i = 0
        for j, col in enumerate(column_names):
            text = tk.Text(root, width=18, height=1, bg="#9BC2E6")
            text.grid(row=i, column=j + 300, sticky=tk.E)
            text.insert(tk.INSERT, col)

        # adding all the other rows into the grid
        for i in range(n_rows):
            for j in range(n_cols):
                text = tk.Text(root, width=18, height=1)
                text.grid(row=i + 1, column=j + 300, sticky=tk.E)
                text.insert(tk.INSERT, data_file.loc[i][j])


# Function to generate a simulated electrocardiogram signal resizing it and saving the graph in .png
def ecg(name):
    ecg_data = nk.ecg_simulate(duration=10, method="simple", random_state=randint(0, 1000))
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.plot(ecg_data)
    plt.savefig(f'{name} ecg.png')
    plt.show()
    img = Image.open(f'{name} ecg.png')
    img = img.resize((300, 300))
    img.save(f'{name} ecg.png')
    img = ImageTk.PhotoImage(Image.open(f'{name} ecg.png'))
    ecg_graph = tk.Label(root, image=img)
    ecg_graph.photo = img
    ecg_graph.place(x=10, y=100, height=300, width=300)


# Function to generate a simulated electroencephalogram signal resizing it and saving the graph in .png
def eeg(name):
    eeg_data = nk.eeg_simulate(duration=1, sampling_rate=500, noise=0.2, random_state=randint(0, 1000))
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Spectrum')
    plt.plot(eeg_data)
    plt.savefig(f'{name} eeg.png')
    plt.show()
    img = Image.open(f'{name} eeg.png')
    img = img.resize((300, 300))
    img.save(f'{name} eeg.png')
    img2 = ImageTk.PhotoImage(Image.open(f'{name} eeg.png'))
    eeg_graph = tk.Label(root, image=img2)
    eeg_graph.photo = img2
    eeg_graph.place(x=320, y=100, height=300, width=300)


# Function to generate a simulated respiratory signal resizing it and saving the graph in .png
def rsp(name):
    rsp_data = nk.rsp_simulate(duration=60, sampling_rate=250, respiratory_rate=15, random_state=randint(0, 1000))
    plt.xlabel('Time (ms)')
    plt.ylabel('Volume (1/100)')
    plt.plot(rsp_data)
    plt.savefig(f'{name} rsp.png')
    plt.show()
    img = Image.open(f'{name} rsp.png')
    img = img.resize((620, 250))
    img.save(f'{name} rsp.png')
    img3 = ImageTk.PhotoImage(Image.open(f'{name} rsp.png'))
    rsp_graph = tk.Label(root, image=img3)
    rsp_graph.photo = img3
    rsp_graph.place(x=10, y=410, height=250, width=620)


# Define the main window, name it and give it a size
root = tk.Tk()
root.title("Neonate Monitoring System")
root.geometry("820x680")

# List of patients and list of selectors
patients = ['']
btn = []
reset_buttons()

# Insert the window icons
icon16 = tk.PhotoImage(file="SimpleLogo.png")
icon32 = tk.PhotoImage(file="SimpleLogo.png")
root.iconphoto(False, icon32, icon16)

# Set a background color
root['bg'] = '#DEF9FF'
root.mainloop()
