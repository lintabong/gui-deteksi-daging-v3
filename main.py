import ctypes
import tkinter

ctypes.windll.shcore.SetProcessDpiAwareness(1)

from lib.config import Config

from view.title import TitleFrame
from view.loadImage import LoadImageFrame


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        guiConfig = Config()
        configuration = guiConfig.read()

        w = configuration["width"]
        h = configuration["height"]
        x = int((self.winfo_screenwidth()/2) - (w/2))
        y = int((self.winfo_screenheight()/2) - (h/2))

        self.title("GUI Deteksi Daging")
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(False, False)
        # self.overrideredirect(1)

        TitleFrame(self)
        LoadImageFrame(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
