# pdk.py #
# plugin development kit

import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

def show_warning(title, message):
    messagebox.showwarning(title, message)

def show_info(title, message):
    messagebox.showinfo(title, message)

def show_error(title, message):
    messagebox.showerror(title, message)

def prompt_input(title, prompt):
    return simpledialog.askstring(title, prompt)

def prompt_confirmation(title, message):
    return messagebox.askyesno(title, message)

def open_file_dialog(title, filetypes):
    file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
    return file_path

def save_file_dialog(title, filetypes):
    file_path = filedialog.asksaveasfilename(title=title, filetypes=filetypes)
    return file_path

def show_question(title, message):
    return messagebox.askquestion(title, message)

def show_critical(title, message):
    return messagebox.showerror(title, message, icon='critical')

def show_warning_icon(title, message):
    return messagebox.showwarning(title, message, icon='warning')

def show_info_icon(title, message):
    return messagebox.showinfo(title, message, icon='info')

def prompt_password(title, prompt):
    return simpledialog.askstring(title, prompt, show='*')

def select_directory(title):
    directory_path = filedialog.askdirectory(title=title)
    return directory_path

def choose_color(title):
    color = colorchooser.askcolor(title=title)
    return color

def open_multiple_files_dialog(title, filetypes):
    file_paths = filedialog.askopenfilenames(title=title, filetypes=filetypes)
    return file_paths

def save_file_as_dialog(title, filetypes):
    file_path = filedialog.asksaveasfile(title=title, filetypes=filetypes)
    return file_path