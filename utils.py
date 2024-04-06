# utils.py #
# utilities for ForeverPad
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import logging
import sys
import json

language_codes = {
    "English": "en",
    "Czech": "cz",
    "Russian": "ru",
    "Spanish": "es"
}

def refresh_s():
    global values
    with open('settings.egg', 'r') as file:
        values = {line.split(': ', 1)[0]: line.split(': ', 1)[1].strip() for line in file if ':' in line}
refresh_s()

class CNB(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__initialized = True

        kwargs["style"] = "CNB"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            if index != 0:
                self.forget(index)
                logging.info('removed tab')
            else:
                logging.info('event: quit')
                self.forget(index)
                sys.exit()

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CNB", [("CNB.client", {"sticky": "nswe"})])
        style.layout("CNB.Tab", [
            ("CNB.tab", {
                "sticky": "nswe",
                "children": [
                    ("CNB.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CNB.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CNB.label", {"side": "left", "sticky": ''}),
                                    ("CNB.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

class Tab:
    def __init__(self, parent, file_path=None, content="", name=""):
        refresh_s()
        logging.info('reloaded settings.egg')
        self.parent = parent
        self.file_path = file_path
        if values["BOLD"] == "True":
            bold = "bold"
        else:
            bold = "normal"
        self.text_area = scrolledtext.ScrolledText(parent,
                                                   wrap=tk.WORD,
                                                   width=50,
                                                   height=25,
                                                   font=(str(values['FONT']), int(values['FONT_SIZE']), bold))
        self.text_area.pack(expand=True, fill='both')
        self.text_area.insert(tk.END, content)
        self.tab = self.text_area
        logging.info('created tab')

class SearchReplaceWindow:
    def __init__(self, parent, text_widget):
        self.language = language_codes.get(values["LANG"], "en")
        self.load_translations()

        self.parent = parent
        self.text_widget = text_widget

        self.window = tk.Toplevel(parent)
        self.window.title("Search/Replace")
        self.window.geometry("265x130")
        self.window.resizable(False,False)

        self.search_label = tk.Label(self.window, text="Search:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = tk.Entry(self.window, width=20)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        self.replace_label = tk.Label(self.window, text="Replace:")
        self.replace_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.replace_entry = tk.Entry(self.window, width=20)
        self.replace_entry.grid(row=1, column=1, padx=5, pady=5)

        self.search_button = tk.Button(self.window, text="Search", command=self.search_text)
        self.search_button.grid(row=100, column=100, padx=14, pady=5, sticky="se")
        self.replace_button = tk.Button(self.window, text="Replace", command=self.replace_text)
        self.replace_button.grid(row=99, column=100, padx=14, pady=5, sticky="se")

    def search_text(self):
        self.window.bell()
        search_text = self.search_entry.get()
        if search_text:
            start_pos = self.text_widget.search(search_text, "1.0", tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.text_widget.tag_remove("search", "1.0", tk.END)
                self.text_widget.tag_add("search", start_pos, end_pos)
                self.text_widget.mark_set(tk.INSERT, start_pos)
                self.text_widget.tag_config('search', foreground='red')
                self.text_widget.see(start_pos)
                self.text_widget.focus_set()
            else: messagebox.showwarning(self.translate[self.language]["warn"],self.translate[self.language]["notext"])

    def replace_text(self):
        self.window.bell()
        self.text_widget.tag_config('search', foreground='white')
        search_text = self.search_entry.get()
        replace_text = self.replace_entry.get()
        if search_text and replace_text:
            start_pos = self.text_widget.search(search_text, "1.0", tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.text_widget.delete(start_pos, end_pos)
                self.text_widget.insert(start_pos, replace_text)
        else: messagebox.showwarning(self.translate[self.language]["warn"],self.translate[self.language]["notext"])

    def load_translations(self):
        with open('translate.json', 'r', encoding='utf-8') as file:
            self.translate = json.load(file)
        logging.info('loaded translations')
