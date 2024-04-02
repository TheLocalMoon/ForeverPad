# main.py #
import tkinter as tk
import re
import os
import json
import sys
import logging
import importlib.util
from tkinter import scrolledtext, filedialog, messagebox, Menu, ttk
from settings_window import SettingsWindow
from base64 import b64encode, b64decode

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s] [%(levelname)s]: %(message)s',
                    level=logging.DEBUG, datefmt='%I:%M:%S')

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

logging.info('loaded settings.egg')

# https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook/39459376#39459376
class CNB(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""
    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

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

        element =  self.identify(event.x, event.y)
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

class ForeverPad:
    def __init__(self, root):
        self.root = root
        # rip 5492429745 lines
        if values["LANG"] == "English": self.language = "en"
        elif values["LANG"] == "Czech": self.language = "cz"
        elif values["LANG"] == "Russian": self.language = "ru"
        else: self.language = "en"
        ######################
        self.load_translations()
        self.root.title("ForeverPad")
        self.root.geometry('800x450')
        self.root.iconbitmap("icon.ico")
        #self.root.resizable(False, False) 

        # theme stuff
        self.style = ttk.Style()

        self.tabs = CNB(root)
        self.tabs.pack(expand=True, fill='both')
        self.tabs.bind('<Button-3>', self.show_tab_context_menu)

        self.tabcount = 1
        self.tabos = self.add_tab()
        self.tabos.text_area.bind('<Button-3>', self.show_context_menu)

        self.font_size = int(values['FONT_SIZE'])
        self.font_type = values['FONT']

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label=self.translate[self.language]["new"], command=self.add_tab)
        self.file_menu.add_command(label=self.translate[self.language]["open"], command=self.open_file)
        self.file_menu.add_command(label=self.translate[self.language]["save"], command=self.save_file)
        self.file_menu.add_command(label=self.translate[self.language]["saveas"], command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.translate[self.language]["exit"], command=self.exit_app)
        self.menu_bar.add_cascade(label=self.translate[self.language]["file"], menu=self.file_menu)

        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label=self.translate[self.language]["cut"], command=self.cut)
        self.edit_menu.add_command(label=self.translate[self.language]["copy"], command=self.copy)
        self.edit_menu.add_command(label=self.translate[self.language]["paste"], command=self.paste)
        self.menu_bar.add_cascade(label=self.translate[self.language]["edit"], menu=self.edit_menu)

        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.status_bar_visible = True
        self.view_menu.add_command(label=self.translate[self.language]["tsbar"], command=self.toggle_status_bar)
        self.menu_bar.add_cascade(label=self.translate[self.language]["view"], menu=self.view_menu)

        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label=self.translate[self.language]["about"], command=self.show_about)
        self.help_menu.add_command(label=self.translate[self.language]["settings"], command=self.open_settings)
        self.menu_bar.add_cascade(label="···", menu=self.help_menu)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label=self.translate[self.language]["cut"], command=self.cut)
        self.context_menu.add_command(label=self.translate[self.language]["copy"], command=self.copy)
        self.context_menu.add_command(label=self.translate[self.language]["paste"], command=self.paste)

        self.manipulation_menu = Menu(self.context_menu, tearoff=0)
        self.manipulation_menu.add_command(label=self.translate[self.language]["upper"], command=self.uppercase)
        self.manipulation_menu.add_command(label=self.translate[self.language]["lower"], command=self.lowercase)
        self.manipulation_menu.add_command(label=self.translate[self.language]["title"], command=self.titlecase)
        self.manipulation_menu.add_separator()
        self.manipulation_menu.add_command(label=self.translate[self.language]["encb64"], command=self.encode)
        self.manipulation_menu.add_command(label=self.translate[self.language]["decb64"], command=self.decode)
        self.manipulation_menu.add_command(label=self.translate[self.language]["bin"], command=self.binary)
        self.context_menu.add_cascade(label=self.translate[self.language]["mani"], menu=self.manipulation_menu)

        self.tab_context_menu = Menu(self.root, tearoff=0)
        self.tab_context_menu.add_command(label=self.translate[self.language]["del"], command=self.delete_tab)

        self.root.pack_propagate(False)

        self.statusos = self.create_status_bar()
        self.toggle_theme()
        
        logging.info('created window')

        self.load_plugins()

    def load_plugins(self):
        plugins = {}
        
        ydk_file = os.path.join("plugins", "ydk.py")
        if os.path.isfile(ydk_file):
            logging.info(f"loading ydk.py: {ydk_file}")
            spec = importlib.util.spec_from_file_location("ydk_module", ydk_file)
            ydk_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(ydk_module)
            plugins["ydk.py"] = ydk_module
            logging.info(f"ydk.py loaded")

        plugin_dir = os.path.abspath("plugins")
        sys.path.insert(0, plugin_dir)

        for filename in os.listdir("plugins"):
            if filename == "ydk.py":
                continue
            if filename.endswith(".py"):
                plugin_path = os.path.join("plugins", filename)
                logging.info(f"loading plugin: {plugin_path}")

                spec = importlib.util.spec_from_file_location("plugin_module", plugin_path)
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)

                plugins[filename] = plugin_module

                logging.info(f"plugin {plugin_path} loaded")

        sys.path.remove(plugin_dir)

        return plugins

    def load_translations(self):
        with open('translate.json', 'r', encoding='utf-8') as file:
            self.translate = json.load(file)
        logging.info('loaded translations')

    def show_tab_context_menu(self, event):
        logging.info('event: tab context menu')
        clicked_tab = self.tabs.tk.call(self.tabs._w, "identify", "tab", event.x, event.y)
        if clicked_tab != "":
            self.tab_context_menu.post(event.x_root, event.y_root)

    def delete_tab(self):
        current_tab_index = self.tabs.index("current")
        if current_tab_index != 0:
            self.tabs.forget(current_tab_index)
            logging.info('removed tab')
        else:
            logging.info('event: quit')
            self.tabs.forget(current_tab_index)
            self.exit_app()

    def refreshtab(self, event):
        logging.info('refreshed tab')
        self.root.update()
        refresh_s()
        self.statusos.destroy()
        selected_tab_name = self.tabs.select()
        selected_tab_frame = self.tabs.nametowidget(selected_tab_name)
        self.toggle_status_bar()

        for child in selected_tab_frame.winfo_children():
            if child.winfo_name() == '!scrolledtext':
                self.tab = child
                self.toggle_status_bar()
                break
        
    def add_tab(self, file_path=None, content="", name=None):
        if name != None:
            tab = Tab(self.tabs, file_path, content, name=name)
            self.tabs.add(tab.text_area, text=name)
        else:
            tab = Tab(self.tabs, file_path, content, name=None)
            self.tabs.add(tab.text_area, text=f"{self.translate[self.language]["untitled"]} {self.tabcount}")
        self.tabs.select(len(self.tabs.tabs()) - 1)
        self.tab = tab.text_area

        self.tab.bind("<Button-1>",self.update_indicators)
        self.tab.bind('<KeyRelease>', self.update_indicators)
        self.tab.bind('<Control-BackSpace>', self.delete_word)
        self.tab.bind('<Control-MouseWheel>', self.update_font_size)

        if self.tabcount != 1:
            self.create_status_bar()

        self.root.update()
        self.tabcount += 1
        return tab

    def uppercase(self):
        logging.info('event: uppercase')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = text.upper()
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def lowercase(self):
        logging.info('event: lowercase')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = text.lower()
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def titlecase(self):
        logging.info('event: titlecase')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = text.title()
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def encode(self):
        logging.info('event: encoded in base64')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = b64encode(text.encode('ascii'))
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def decode(self):
        logging.info('event: decoded from base64')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = b64decode(text)
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def toBinary(self, a):
        l,m=[],[]
        for i in a:
            l.append(ord(i))
        for i in l:
            m.append(int(bin(i)[2:]))
        return m

    def binary(self):
        logging.info('event: encoded in binary')
        try:
            text = self.tab.selection_get()
            if re.search(r'\w+', text):
                self.tab.delete("sel.first", "sel.last")
                new_text = self.toBinary(text)
                self.tab.insert("insert", new_text)
                self.root.update()
        except: pass

    def show_context_menu(self, event):
        logging.info('event: context menu')
        self.context_menu.post(event.x_root, event.y_root)

    def toggle_theme(self):
        logging.info('toggled theme')
        if values['THEME'] == 'Dark':
            self.change_theme(dark=True)
        else:
            self.change_theme(dark=False)

    def change_theme(self, dark=False):
        if dark:
            self.root.config(bg='#3f3f3f')
            self.tab.config(bg='#3f3f3f', fg='white')
            self.status_bar.config(bg='#202020', fg='white')
            self.line_label.config(bg='#202020', fg='white')
        else:
            self.root.config(bg='white')
            self.tab.config(bg='white', fg='black')
            self.status_bar.config(bg='white', fg='black')
            self.line_label.config(bg='white', fg='black')

    def open_settings(self):
        SettingsWindow(self)

    def apply_settings(self, font_size, font_type, theme, bold=str):
        logging.info('applied settings')
        self.font_size = font_size
        self.font_type = font_type
        self.theme = theme
        self.bold = bold
        if self.bold == "True": self.bold = "bold"
        else: self.bold = "normal"

        self.tab.config(font=(self.font_type, self.font_size, self.bold))
        if self.theme == "Dark":
            self.change_theme(dark=True)
        else:
            self.change_theme(dark=False)

    def update_font_size(self, event=None):
        logging.warning('there was supposed to be albert enstein mathematics but i removed it cuz broken')
        messagebox.showwarning(self.translate[self.language]["warn"],self.translate[self.language]["seterror"])

    def delete_word(self, event=None):
        logging.info('event: removed word')
        cursor_index = self.tab.index(tk.INSERT)
        if cursor_index == '1.0':
            return
        while True:
            prev_char = self.tab.get(cursor_index + ' - 1 chars')
            if prev_char == ' ' or prev_char == '\n':
                break
            else:
                self.tab.delete(cursor_index + ' - 1 chars')
                cursor_index = self.tab.index(tk.INSERT)
        self.tab.insert(cursor_index, ' ')

    def update_indicators(self, event=None):
        #logging.info('event: updated indicators')
        self.root.update()
        cursor_pos = self.tab.index(tk.INSERT)
        if cursor_pos:
            line, col = cursor_pos.split('.')
            length = len(self.tab.get("1.0", "end-1c"))
            chairs = self.tab.index("end-1c")
            self.line_label.config(text=f"{self.translate[self.language]["length"]}.: {length}  {self.translate[self.language]["lines"]}.: {chairs.split('.')[0]}  | {self.translate[self.language]["col"]}.: {col}  {self.translate[self.language]["lpos"]}.: {length+1}")

    def create_status_bar(self):
        logging.info('created status bar')
        self.status_bar = tk.Label(self.tab, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.line_label = tk.Label(self.status_bar, text=f"{self.translate[self.language]["length"]}.: 1  {self.translate[self.language]["lines"]}.: 1   |  {self.translate[self.language]["col"]}.: 1  {self.translate[self.language]["lpos"]}.: 1  {self.translate[self.language]["lpos"]}.: 1")
        self.line_label.pack(side=tk.LEFT, padx=(2, 0))
        self.update_indicators()
        self.toggle_theme()
        return self.status_bar

    def open_file(self):
        logging.info('event: open file')
        file_path = filedialog.askopenfilename(filetypes=[({self.translate[self.language]["tfile"]}, "*.txt"), ({self.translate[self.language]["afile"]}, "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.add_tab(name=os.path.split(file_path)[1], content=content)
                self.refreshtab(None)

    def save_file(self):
        logging.info('event: save file')
        selected_tab_name = self.tabs.select()
        selected_tab_frame = self.tabs.nametowidget(selected_tab_name)
        current_tab = None
        for child in selected_tab_frame.winfo_children():
            if isinstance(child, scrolledtext.ScrolledText):
                current_tab = child
                break

        if current_tab is None:
            return

        if hasattr(current_tab, "file_path") and current_tab.file_path:
            with open(current_tab.file_path, "w") as file:
                file.write(current_tab.get("1.0", tk.END))
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[(self.translate[self.language]["tfile"], "*.txt"), (self.translate[self.language]["afile"], "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(current_tab.get("1.0", tk.END))
                current_tab.file_path = file_path
                self.tabs.tab(selected_tab_name, text=os.path.split(file_path)[1])

    def exit_app(self):
        logging.info('event: exit app')
        if self.tab.get("1.0", "end-1c"):
            response = messagebox.askyesnocancel(self.translate[self.language]["exit"], self.translate[self.language]["sbe"])
            if response is None:
                return
            elif response:
                self.save_file()

        self.root.destroy()

    def restart(self):
        logging.info('event: restart')
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def cut(self):
        logging.info('cut')
        self.tab.event_generate("<<Cut>>")

    def copy(self):
        logging.info('copy')
        self.tab.event_generate("<<Copy>>")

    def paste(self):
        logging.info('paste')
        self.tab.event_generate("<<Paste>>")
        self.root.after(50, self.scroll_to_end)

    def scroll_to_end(self):
        self.tab.see(tk.END)

    def toggle_status_bar(self):
        logging.info('event: toggle status bar')
        if self.status_bar_visible == True:
            self.status_bar.destroy()
        else:
            self.create_status_bar()
        self.status_bar_visible = not self.status_bar_visible

    def show_about(self):
        logging.info('event: show about')
        messagebox.showinfo("About", f"""ForeverPad
{self.translate[self.language]["inspr"]}
{self.translate[self.language]["madeby"]}

{self.translate[self.language]["lastpos"]}""")

def main():
    root = tk.Tk()
    app = ForeverPad(root)
    root.mainloop()

if __name__ == "__main__":
    main()
