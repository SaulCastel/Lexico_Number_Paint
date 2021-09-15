from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from analizador import lexico

def cargar_archivo(*args):
    fileChooser = Tk()
    fileChooser.withdraw()
    route = askopenfilename()
    fileChooser.destroy()
    readfile(route)

def readfile(route):
    entrada = ''
    file = open(route,'r')
    for line in file:
        entrada += line
    file.close()
    lex = lexico.Lexico()
    lex.escanear(entrada)
    print('\t---TOKENS---')
    for t in lex.tokens:
        print("> "+t.toString())
    print('\t---ERRORES---')
    for e in lex.errores:
        print("> "+e.toString())

raiz = Tk()
raiz.title("Number Paint")

mainframe = ttk.Frame(raiz)

#Barra
barra = ttk.Frame(mainframe, borderwidth=5, relief="ridge")

cargar = ttk.Button(barra,text='Cargar',command=cargar_archivo)
analizar = ttk.Button(barra,text='Analizar')
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
imagen = ttk.Label(panel,text='imagen')

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
imagen.grid(row=0,column=0)

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

raiz.mainloop()