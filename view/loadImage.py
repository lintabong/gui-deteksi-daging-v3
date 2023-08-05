import sys
import os
import tkinter
import ctypes
import cv2
import threading
from tkinter import END
from openpyxl import Workbook
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import filedialog

from lib.config import Config
from lib.image_processing import GLCM


guiConfig = Config()

class LoadImageFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        configuration = guiConfig.read()

        self.w  = configuration["loadImageFrame"]["width"]
        self.h  = configuration["loadImageFrame"]["height"]
        self.bg = configuration["loadImageFrame"]["background"]

        self.th = configuration["titleFrame"]["height"]

        self.config(width=self.w, height=self.h, background=self.bg)
        self.place(x=0, y=self.th)

        self.pathfile = ""
        self.method   = tkinter.IntVar()

        self.analysisText = [["", "0", "45", "90", "135", "rata-rata"],
                             ["Kontras", "", "", "", "", ""],
                             ["Korelasi", "", "", "", "", ""],
                             ["Energi", "", "", "", "", ""],
                             ["Homogenitas", "", "", "", "", ""]]

        self.nameField = tkinter.Entry(
            self,
            width=133,
        )

        self.nameField.place(x=150, y=305)

        tkinter.Button(
            self, 
            text="Browse", 
            width=12, 
            command=self.loadImage).place(x=10, y=300)

        self.imageFrame()
        self.methodFrame()
        self.textureAnalysisFrame()
        self.histogramFrame()
        self.resultFrame()
        
    def imageFrame(self):
        self.sizeImg = 270
        image = Image.open("src/blank.png")
        image = image.resize((self.sizeImg, self.sizeImg))
        image = ImageTk.PhotoImage(image)

        self.image1 = tkinter.Label(self, image=image)
        self.image2 = tkinter.Label(self, image=image)
        self.image3 = tkinter.Label(self, image=image)
        
        self.image1.image = image
        self.image2.image = image
        self.image3.image = image

        self.image1.place(x=360, y=10)
        self.image2.place(x=653, y=10)
        self.image3.place(x=945, y=10)

    def loadImage(self):
        fileToRead = ["*.png", "*.jpeg", "*jpg"]

        file = filedialog.askopenfile(
            mode = "r", 
            filetypes = [("Image file", fileToRead)]
        )

        if file:
            self.pathfile = os.path.abspath(file.name)

            self.nameField.insert(0, self.pathfile)

            img = Image.open(self.pathfile)
            img = img.resize((self.sizeImg, self.sizeImg))
            img = ImageTk.PhotoImage(img)

            self.image1 = tkinter.Label(self, image=img)
            self.image2 = tkinter.Label(self, image=img)
            self.image3 = tkinter.Label(self, image=img)
            
            self.image1.image = img
            self.image2.image = img
            self.image3.image = img

            self.image1.place(x=360, y=10)
            self.image2.place(x=653, y=10)
            self.image3.place(x=945, y=10)

            configuration = guiConfig.read()

            configuration["user"]["pathfile"] = self.pathfile

            guiConfig.write(configuration)

            img = cv2.imread(self.pathfile)
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        
            h, w = gray.shape
            ymin, ymax, xmin, xmax = h//3, h*2//3, w//3, w*2//3
            crop = gray[ymin:ymax, xmin:xmax]
                        
            resize = cv2.resize(crop, (0,0), fx=0.5, fy=0.5)

            self.analysisText  = GLCM(resize)

            self.textureAnalysisFrame()

            print(self.method.get())

    def methodFrame(self):
        methodframe = tkinter.LabelFrame(self, width=330, height=270, background=self.bg, text="  Metode  ")
        methodframe.place(x=10, y=10)

        listMethod = ["Haar", "Daubechies", "Coiflet", "Symlet", "Meyer", "Morlet", "Mexican Hat"]
        
        for i in range(7):
            tkinter.Radiobutton(
                methodframe, 
                text=listMethod[i], 
                variable=self.method, 
                background=self.bg,
                highlightbackground=self.bg,
                value=i+1, 
                command=self.getMethod).place(x=10, y=10+(30*i))
            
        self.method.set(1)

    def textureAnalysisFrame(self):
        f0 = tkinter.LabelFrame(self, width=615, height=220, background=self.bg, text="  Analisis Tekstur  ")
        f0.place(x=10, y=340)

        f1 = tkinter.Frame(f0, width=600, height=178, background="#a8a7a7")
        f1.place(x=5, y=5)
        
        for i in range(6):
            for j in range(5):
                f2 = tkinter.Frame(f1, height=30, width=95 , background="#ffffff")
                tkinter.Label(f2, bg="#ffffff", text=self.analysisText[j][i]).place(anchor="c", relx=.5, rely=.5)
                f2.place(x=5+(99*i), y=5+(34*j))

    def histogramFrame(self):
        f0 = tkinter.LabelFrame(self, width=584, height=380, background=self.bg, text="  Histogram  ")
        f0.place(x=635, y=340)

        # f1 = tkinter.Frame(f0, width=600, height=178, background="#a8a7a7")
        # f1.place(x=5, y=5)

    def resultFrame(self):
        f0 = tkinter.LabelFrame(self, width=615, height=157, background=self.bg, text="  Hasil  ")
        f0.place(x=10, y=560)

        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Prediksi").place(x=10,y=10)
            # font=("Arial", 22))

        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Akurasi").place(x=10,y=40)
        
        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Kategori").place(x=10,y=70)
        
        self.inputPrediction = tkinter.Entry(f0, width=15)
        self.inputAccuration = tkinter.Entry(f0, width=15)
        self.inputCategory   = tkinter.Entry(f0, width=15)

        self.inputPrediction.place(x=110,y=10)
        self.inputAccuration.place(x=110,y=40)
        self.inputCategory.place(x=110,y=70)

        tkinter.Button(
            f0, 
            text="Save", 
            width=12, 
            height=2).place(x=470, y=2)
        
        tkinter.Button(
            f0, 
            text="History", 
            width=12, 
            height=2).place(x=470, y=62)



    def getMethod(self):
        setMethod = self.method.get()
