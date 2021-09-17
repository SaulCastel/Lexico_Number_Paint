import requests
import PIL.ImageTk
import PIL.Image
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from analizador import lexico
import json

class GUI:

    def __init__(self,raiz:Tk) -> None:

        mainframe = ttk.Frame(raiz)

        #Barra
        barra = ttk.Frame(mainframe, borderwidth=5, relief="ridge")

        cargar = ttk.Button(barra,text='Cargar',command=self.cargar_archivo)
        analizar = ttk.Button(barra,text='Analizar',command=self.readfile)
        reportes = ttk.Button(barra,text='Reportes')
        salir = ttk.Button(barra,text='Salir')

        #Container
        container = ttk.Frame(mainframe, borderwidth=5, relief="ridge")

        #SideBar
        sidebar = ttk.Frame(container, borderwidth=5, relief="ridge")

        original = ttk.Button(sidebar,text='Original')
        mirrorx = ttk.Button(sidebar,text='Mirror X')
        mirrory = ttk.Button(sidebar,text='Mirror Y')
        DMirror = ttk.Button(sidebar,text='D. Mirror')

        #Panel
        panel = ttk.Frame(container, borderwidth=5, relief="ridge")
        self.imagen = ttk.Label(panel)
        self.setImage('GUI/PixelArtGuatemala.png')

        mainframe.grid(row=0,column=0,sticky=NSEW)
        barra.grid(row=1,column=1,sticky=EW)
        cargar.grid(row=1,column=1,sticky=EW)
        analizar.grid(row=1,column=2,sticky=EW)
        reportes.grid(row=1,column=3,sticky=EW)
        salir.grid(row=1,column=4,sticky=EW)
        container.grid(row=2,column=1,sticky=NSEW)
        sidebar.grid(row=1,column=1,sticky=NS)
        original.grid(row=1,column=1)
        mirrorx.grid(row=2,column=1)
        mirrory.grid(row=3,column=1)
        DMirror.grid(row=4,column=1)
        panel.grid(row=1,column=2,sticky=NSEW)
        self.imagen.grid(row=0,column=0)

        raiz.rowconfigure(0,weight=1)
        raiz.columnconfigure(0,weight=1)
        mainframe.columnconfigure(1,weight=1)
        mainframe.rowconfigure(2,weight=1)
        barra.columnconfigure(1,weight=1)
        barra.columnconfigure(2,weight=1)
        barra.columnconfigure(3,weight=1)
        barra.columnconfigure(4,weight=1)
        container.rowconfigure(1,weight=1)
        container.columnconfigure(2,weight=1)

    def setImage(self,route):
        self.img = PIL.ImageTk.PhotoImage(PIL.Image.open(route).resize((400,400)))
        self.imagen['image'] = self.img
    
    def cargar_archivo(self,*args):
        fileChooser = Tk()
        fileChooser.withdraw()
        self.route = askopenfilename()
        fileChooser.destroy()
        print(self.route)

    def readfile(self,*args):
        entrada = ''
        try:
            file = open(self.route,'r')
            for line in file:
                entrada += line
            file.close()
            self.lex = lexico.Lexico()
            self.lex.escanear(entrada)
            if len(self.lex.errores) == 0:
                for img in self.lex.imgs:
                    #print(json.dumps(img,indent=4))
                    self.sendImage(img)
                    print(f'>> Imagen: {img["TITULO"]} renderizada en HTML')
            else:
                print('\t---ERRORES---')
                for e in self.lex.errores:
                    print(">",e.toString(),sep=" ")
                self.sendErrores()
        except FileNotFoundError:
            print('> No se encontró ningun archivo')

    def sendImage(self,img):
        r = requests.post('http://127.0.0.1:5000/postImage',json=img)
        print(r.content)

    def sendTokens(self):
        requests.post('http://127.0.0.1:5000/postTokens',data=self.lex.tokens)

    def sendErrores(self):
        requests.post('http://127.0.0.1:5000/postErrores',data=self.lex.errores)