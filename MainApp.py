import tkinter as tk
from tkinter import ttk
from ctypes import windll
import os


windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.geometry("800x600")
#root.resizable(width=False, height=False)
#root.minsize(800, 600)
root.title("Equ Solver")
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)

window_var = tk.StringVar()


def onclick():
    window = window_var.get()
    if(window == "System Solver"):
        os.system("python LWindow.py")
    elif(window == "Root Finder"):
        os.system("python NLWindow.py")
    else:
        print("Please choose a window.")



#system solver
#root finder

#combobox selector
ttk.Label(root, text="Choose a window: ").grid(row=0, column=0)
opselect = ttk.Combobox(root, textvariable=window_var, state="readonly", values=['System Solver', 'Root Finder'], )
opselect.grid(row=0, column=1)

#button
ttk.Button(root, text="Go!", command=onclick).grid(row=1, column=0, columnspan=2)





root.geometry("")

root.mainloop()