import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import logging
import json

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

class PluginsMenu:
    def __init__(self, parent):
        self.parent = parent
        # rip 5492429745 lines
        if values["LANG"] == "English": self.language = "en"
        elif values["LANG"] == "Czech": self.language = "cz"
        elif values["LANG"] == "Russian": self.language = "ru"
        else: self.language = "en"
        logging.info('settings: loaded languages')
        ######################
        self.load_translations()
        self.ohio = tk.Toplevel(parent.settings_window)
        self.ohio.title(self.translate[self.language]["downloader"])
        self.ohio.geometry('400x300')

        self.main_frame = ttk.Frame(self.ohio)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.plugins_frame = tk.Frame(self.ohio)
        self.plugins_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.plugins_listbox = tk.Listbox(self.plugins_frame, selectmode=tk.SINGLE)
        self.plugins_listbox.pack(fill=tk.BOTH, expand=True)

        self.download_button = ttk.Button(self.main_frame, text=self.translate[self.language]["pkgdownload"], command=self.download_plugin)
        self.download_button.pack(side=tk.BOTTOM, anchor=tk.SE)

        self.plugin_name_label = tk.Label(self.main_frame, text="-", font=("Arial", 12, "bold"))
        self.plugin_name_label.pack(anchor=tk.NW, padx=10, pady=10)

        self.plugin_description_label = tk.Label(self.main_frame, text="-", wraplength=350)
        self.plugin_description_label.pack(anchor=tk.NW, padx=10)

        self.plugins_listbox.bind("<<ListboxSelect>>", self.callback)

        self.refresh_plugins_list()
        self.get_plugin_data()

    def get_plugin_data(self):
        url = "https://raw.githubusercontent.com/TheLocalMoon/ForeverPlugins/main/plugins/data.json"
        response = requests.get(url)
        if response.status_code == 200:
            self.json_data = response.json()
        else:
            logging.error("fail: ", response.status_code)

    def callback(self, event=None):
        try:
            plugin_info = self.json_data[self.plugins_listbox.get(self.plugins_listbox.curselection()[0])]
            self.plugin_name_label.config(text=plugin_info["name"])
            self.plugin_description_label.config(text=plugin_info["description"])
        except:
            self.plugin_name_label.config(text="")
            self.plugin_description_label.config(text="No description provided.")

    def load_translations(self):
        with open('translate.json', 'r', encoding='utf-8') as file:
            self.translate = json.load(file)
        logging.info('settings: loaded translations')

    def refresh_plugins_list(self):
        try:
            plugins_url = "https://api.github.com/repos/TheLocalMoon/ForeverPlugins/contents/plugins"
            response = requests.get(plugins_url)
            response.raise_for_status()
            files_info = response.json()

            self.plugins_listbox.delete(0, tk.END)
            for file_info in files_info:
                if file_info["name"].endswith(".py"):
                    self.plugins_listbox.insert(tk.END, file_info["name"])
        except Exception as e:
            messagebox.showerror(self.translate[self.language]["error"], f"{self.translate[self.language]["failedpkg"]}: {e}")

    def download_plugin(self):
        selected_index = self.plugins_listbox.curselection()
        if not selected_index:
            messagebox.showerror(self.translate[self.language]["error"], self.translate[self.language]["pspd"])
            return

        try:
            selected_plugin = self.plugins_listbox.get(selected_index)
            plugin_url = f"https://raw.githubusercontent.com/TheLocalMoon/ForeverPlugins/main/plugins/{selected_plugin}"
            response = requests.get(plugin_url)
            response.raise_for_status()

            plugins_dir = "plugins/"
            os.makedirs(plugins_dir, exist_ok=True)

            with open(os.path.join(plugins_dir, selected_plugin), "wb") as f:
                f.write(response.content)

            messagebox.showinfo(self.translate[self.language]["gg"], f"{self.translate[self.language]["plugin"]} '{selected_plugin}' {self.translate[self.language]["downsucc"]}.")
        except Exception as e:
            messagebox.showerror(self.translate[self.language]["error"], f"{self.translate[self.language]["failpkg"]} '{selected_plugin}': {e}")