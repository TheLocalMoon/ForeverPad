# pylog.py #
# for ForeverPad
from datetime import datetime

class log:
    def __init__(self):
        #super().__init__()
        self.on = True

        print(f"[{datetime.now()}] [READY] PyLOG ready")
    
    def info(self, message):
        if self.on: print(f"[{datetime.now()}] [INFO]: {message}")

    def warning(self, message):
        if self.on: print(f"[{datetime.now()}] [WARN]: {message}")

    def error(self, message):
        if self.on: print(f"[{datetime.now()}] [ERROR]: {message}")

    def disable(self):
        self.on = False