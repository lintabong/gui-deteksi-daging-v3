import os
import tkinter
import cv2
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import END
from tkinter import filedialog

from lib.config import Config
from lib import image_processing

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
        self.sizeImg  = 270

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
                value=i+1).place(x=10, y=10+(30*i))
            
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

        f1 = tkinter.Frame(f0, width=567, height=342, background="#a8a7a7")
        f1.place(x=5, y=5)

        self.hisFrame = tkinter.Frame(f1, width=567, height=342)
        self.hisFrame.place(x=0, y=0)

    def resultFrame(self):
        f0 = tkinter.LabelFrame(self, width=615, height=157, background=self.bg, text="  Hasil  ")
        f0.place(x=10, y=560)

        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Prediksi").place(x=10,y=10)

        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Akurasi").place(x=10,y=40)
        
        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Kategori").place(x=10,y=70)
        
        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Entropi").place(x=210,y=10)

        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Standar deviasi").place(x=210,y=40)
        
        tkinter.Label(
            f0, 
            bg=self.bg, 
            text="Index Kualiti").place(x=210,y=70)
        
        self.inputPrediction = tkinter.Entry(f0, width=12)
        self.inputAccuration = tkinter.Entry(f0, width=12)
        self.inputCategory   = tkinter.Entry(f0, width=12)

        self.inputEntropy = tkinter.Entry(f0, width=12)
        self.inputDeviation = tkinter.Entry(f0, width=12)
        self.inputQuality   = tkinter.Entry(f0, width=12)

        self.inputPrediction.place(x=80,y=10)
        self.inputAccuration.place(x=80,y=40)
        self.inputCategory.place(x=80,y=70)

        self.inputEntropy.place(x=320,y=10)
        self.inputDeviation.place(x=320,y=40)
        self.inputQuality.place(x=320,y=70)

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

    def loadImage(self):
        fileToRead = ["*.png", "*.jpeg", "*jpg"]

        file = filedialog.askopenfile(
            mode = "r", 
            filetypes = [("Image file", fileToRead)]
        )

        if file:
            self.pathfile = os.path.abspath(file.name)

            self.nameField.insert(0, self.pathfile)

            img = cv2.imread(self.pathfile)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray,70,255,0)

            pilimg = Image.fromarray(img)
            pilimg = pilimg.resize((self.sizeImg, self.sizeImg))
            pilimg = ImageTk.PhotoImage(pilimg)

            pilimg2 = Image.fromarray(gray)
            pilimg2 = pilimg2.resize((self.sizeImg, self.sizeImg))
            pilimg2 = ImageTk.PhotoImage(pilimg2)

            pilimg3 = Image.fromarray(thresh)
            pilimg3 = pilimg3.resize((self.sizeImg, self.sizeImg))
            pilimg3 = ImageTk.PhotoImage(pilimg3)

            self.image1 = tkinter.Label(self, image=pilimg)
            self.image2 = tkinter.Label(self, image=pilimg2)
            self.image3 = tkinter.Label(self, image=pilimg3)
            
            self.image1.image = pilimg
            self.image2.image = pilimg2
            self.image3.image = pilimg3

            self.image1.place(x=360, y=10)
            self.image2.place(x=653, y=10)
            self.image3.place(x=945, y=10)

            self.analysisText = image_processing.GLCM(img)
            self.textureAnalysisFrame()

            print(self.method.get())

            # get result
            label, accuracy = image_processing.predict(self.pathfile)
            category        = image_processing.get_category(self.analysisText[1][5])
            H               = image_processing.entropy(round(accuracy, 3))
            sd              = (100 - round(accuracy, 3))/5

            self.inputPrediction.delete(0, END)
            self.inputAccuration.delete(0, END)
            self.inputCategory.delete(0, END)
            self.inputEntropy.delete(0, END)
            self.inputDeviation.delete(0, END)
            self.inputQuality.delete(0, END)

            self.inputPrediction.insert(0, label)
            self.inputAccuration.insert(0, round(accuracy, 3))
            self.inputCategory.insert(0, category)
            self.inputEntropy.insert(0, round(H, 3))
            self.inputDeviation.insert(0, round(sd, 3))
            self.inputQuality.insert(0, round(accuracy, 3))

            # plot histogram
            vals = img.mean(axis=2).flatten()

            fig = Figure(figsize=(4.4, 2.5), dpi=100)
            fig.add_subplot(111).hist(vals, 255)
            
            canvas = FigureCanvasTkAgg(fig,  master=self.hisFrame)  
            canvas.draw()
            canvas.get_tk_widget().place(x=10, y=10)