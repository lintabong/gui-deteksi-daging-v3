import tkinter

from lib.config import Config

guiConfig = Config()


class TitleFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        configuration = guiConfig.read()
        w  = configuration["titleFrame"]["width"]
        h  = configuration["titleFrame"]["height"]
        bg = configuration["titleFrame"]["background"]

        self.config(width=w, height=h, background=bg)
        self.place(x=0, y=0)

        self.title = tkinter.Label(
            self, 
            bg=bg, 
            text="Hasil Metode Penggabungan Citra Modifikasi Wavelet Haar",
            font=("Arial", 22))
        
        self.title.place(anchor="c", relx=.5, rely=.5)
