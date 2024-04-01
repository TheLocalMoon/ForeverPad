import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as fontus
import json
import logging
import constants
import os

# default settings
if not os.path.exists('settings.egg'):
    with open('settings.egg', 'w') as file:
        file.write(f"""SETTING -
FONT: {constants.DEFAULT_FONT_TYPE}
FONT_SIZE: {constants.DEFAULT_FONT_SIZE}
THEME: {constants.DEFAULT_THEME}
BOLD: {constants.DEF_BOLD}
LANG: {constants.ENG}
DEBUG: {constants.DEF_DEBUG}""")
    logging.info('Created settings.egg')

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s] [%(levelname)s]: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')

values = {}
def refresh_s():
    global values
    with open('settings.egg', 'r') as file:
        for line in file:
            line = line.strip()
            if line and ':' in line:
                key, value = line.split(': ', 1)
                values[key] = value
refresh_s()

if values["DEBUG"] != "True":
    logging.disable(logging.INFO)

logging.info('settings: loaded settings.egg')

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent

        # rip 5492429745 lines
        if values["LANG"] == "English": self.language = "en"
        elif values["LANG"] == "Czech": self.language = "cz"
        else: self.language = "en"
        logging.info('settings: loaded languages')
        ######################
        self.load_translations()
        self.settings_window = tk.Toplevel(parent.root)
        self.settings_window.title(self.translate[self.language]["settings"])
        self.settings_window.geometry('400x200')

        self.notebook = ttk.Notebook(self.settings_window)

        self.text_tab = tk.Frame(self.notebook)
        self.window_tab = tk.Frame(self.notebook)
        self.other_tab = tk.Frame(self.notebook)

        self.notebook.add(self.window_tab, text=self.translate[self.language]["window"])
        self.notebook.add(self.text_tab, text=self.translate[self.language]["text"])
        self.notebook.add(self.other_tab, text=self.translate[self.language]["other"])

        self.notebook.pack(expand=1, fill='both')

        self.create_text_settings()
        self.create_window_settings()
        self.create_other_settings()

        self.apply_button = ttk.Button(self.settings_window, text=self.translate[self.language]["apply"], command=self.apply_settings)
        self.apply_button.pack(pady=10)
        logging.info('settings: created window')

    def load_translations(self):
        with open('translate.json', 'r', encoding='utf-8') as file:
            self.translate = json.load(file)
        logging.info('settings: loaded translations')

    def create_other_settings(self):
        self.lang_var = tk.StringVar(self.other_tab)
        self.lang_var.set(values["LANG"])

        self.lang_label = ttk.Label(self.other_tab, text=self.translate[self.language]["lang"])
        self.lang_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.lang_entry = ttk.Combobox(self.other_tab, textvariable=self.lang_var, values=["English","Czech","Russian"])
        self.lang_entry.grid(row=1, column=1, pady=10)
        logging.info('settings: event: create other settings')

        if values["DEBUG"] == "True":
            valb=1
        else: valb=0 #no wae hazbin hotel reference
        self.debug_var = tk.IntVar(value=valb)

        self.debug_entry = ttk.Checkbutton(self.other_tab, text=self.translate[self.language]["debug"], variable=self.debug_var, onvalue=1, offvalue=0)
        self.debug_entry.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    def create_text_settings(self):
        self.font_size_label = ttk.Label(self.text_tab, text=self.translate[self.language]["fsize"])
        self.font_size_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.font_size_var = tk.StringVar(value=values["FONT_SIZE"])
        self.font_size_entry = ttk.Entry(self.text_tab, textvariable=self.font_size_var)
        self.font_size_entry.grid(row=0, column=1, padx=10, pady=10)

        self.font_type_label = ttk.Label(self.text_tab, text=self.translate[self.language]["font"])
        self.font_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        available_fonts = fontus.families()

        self.font_var = tk.StringVar(self.text_tab)
        self.font_var.set(values["FONT"])

        self.font_type_entry = ttk.Combobox(self.text_tab, textvariable=self.font_var, values=available_fonts)
        self.font_type_entry.grid(row=1, column=1, pady=5)

        if values["BOLD"] == "True":
            valb=1
        else: valb=0 #no wae hazbin hotel reference
        self.bold_var = tk.IntVar(value=valb)

        self.bold_entry = ttk.Checkbutton(self.text_tab, text=self.translate[self.language]["bold"], variable=self.bold_var, onvalue=1, offvalue=0)
        self.bold_entry.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        logging.info('settings: event: create text settings')

    def create_window_settings(self):
        self.theme_label = ttk.Label(self.window_tab, text=self.translate[self.language]["theme"])
        self.theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_var = tk.StringVar(value=str(values["THEME"]))
        self.theme_combobox = ttk.Combobox(self.window_tab, textvariable=self.theme_var, values=[self.translate[self.language]["light"], self.translate[self.language]["dark"]])
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=10)
        logging.info('settings: event: create window settings')

    def apply_settings(self):
        font_size = int(self.font_size_var.get())
        font_type = self.font_var.get()
        theme = self.theme_var.get()
        bold = self.bold_var.get()
        language = self.lang_var.get()
        if bold == 0:
            bold = "False"
        else:
            bold = "True"

        debug = self.debug_var.get()
        if debug == 0:
            debug = "False"
        else:
            debug = "True"

        if language != values["LANG"] or debug != values["DEBUG"]:
            willrest = True
            messagebox.showwarning(self.translate[self.language]["warn"],self.translate[self.language]["langchang"])
        else:
            willrest = False

        with open('settings.egg', 'w') as file:
            file.write(f"""SETTING -
FONT: {font_type}
FONT_SIZE: {font_size}
THEME: {theme}
BOLD: {bold}
LANG: {language}
DEBUG: {debug}""")
            file.close()

        refresh_s()

        try:
            self.parent.apply_settings(font_size, font_type, theme, bold)
            logging.info('settings: applied settings')
        except Exception as e:
            logging.error('settings: ' + e)
            #messagebox.showerror(self.translate[self.language]["err"],self.translate[self.language]["sperr"])
        
        if willrest:
            logging.info('settings: restarting app')
            self.parent.restart()
        else:
            logging.info('settings: closed')
            self.settings_window.destroy()
