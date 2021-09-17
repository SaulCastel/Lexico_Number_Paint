from analizador.error import Error
from analizador.token import *
from analizador.lexema import *

class Lexico:
    
    def __init__(self) -> None:
        self.estado = 0
        self.conteo = 0
        self.fila = 1
        self.col = 1
        self.prefijo = ''
        self.entrada = list()
        self.flujo = list()
        self.tokens = list()
        self.errores = list()
        self.imgs = list()
        self.img = dict()
        self.contenedor = list()
        self.subcont = list()
        self.reserved = [   
                            'TITULO','ANCHO',
                            'ALTO','FILAS',
                            'COLUMNAS','CELDAS',
                            'COLORES','FILTROS',
                            'TRUE','FALSE',
                            'MIRRORX','MIRRORY',
                            'DOUBLEMIRROR'
                        ]

    def escanear(self,entrada):
        self.str_to_list(entrada)
        while len(self.entrada) > 0:
            if self.getSeparador():
                continue
            elif self.getSimbolo():
                continue
            elif self.getId():
                token = Token(self.prefijo,self.getLexema())
                self.addToken(token)
            elif self.getCadena():
                token = Token('Cadena',self.getLexema())
                self.addToken(token)
            elif self.getNumero():
                token = Token('Numero',self.getLexema())
                self.addToken(token)
            elif self.getHex():
                token = Token('ValorHex',self.getLexema())
                self.addToken(token)
            elif self.getDivisor():
                token = Token('Divisor',self.getLexema())
                self.addToken(token)
            else: #Hay un error léxico
                self.error()
        if len(self.errores) == 0:
            self.imgs.append(self.img)

    def str_to_list(self,entrada):
        chars = list()
        for c in entrada:
            chars.append(c)
        self.entrada = chars
        self.flujo = chars
    
    def sigChar(self) -> str:
        return self.entrada[0]

    def getLexema(self) -> Lexema:
        inicio = self.col - self.conteo
        lexema = Lexema(self.prefijo,self.fila,inicio)
        self.prefijo = ''
        self.conteo = 0
        return lexema

    def getId(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar().isupper():
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                reservada = self.prefijo
                if self.sigChar().isupper():
                    self.transicion(1)
                elif self.getSeparador():
                    if reservada in self.reserved:    
                        if reservada == 'TRUE' or reservada == 'FALSE':
                            self.subcont.append(reservada)
                        elif reservada == 'MIRRORX' or reservada == 'MIRRORY' or reservada == 'DOUBLEMIRROR':
                            self.subcont.append(reservada)
                        elif reservada == 'FILTROS':
                            self.subcont = list()
                            self.seccion = reservada
                        else:
                            self.seccion = reservada
                        return True
                    else:
                        return False
                else:
                    if reservada in self.reserved:    
                        if reservada == 'TRUE' or reservada == 'FALSE':
                            self.subcont.append(reservada)
                        elif reservada == 'MIRRORX' or reservada == 'MIRRORY' or reservada == 'DOUBLEMIRROR':
                            self.subcont.append(reservada)
                        elif reservada == 'FILTROS':
                            self.subcont = list()
                            self.seccion = reservada
                        else:
                            self.seccion = reservada
                        return True
                    else:
                        return False
                
    def getCadena(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '"':
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                c = self.sigChar()
                if c != '"' and c != '\n':
                    self.transicion(1)
                elif c == '"':
                    self.transicion(2)
                else:
                    return False
            elif self.estado == 2:
                self.subcont.append(self.prefijo)
                return True

    def getNumero(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar().isdigit():
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                if self.sigChar().isdigit():
                    self.transicion(1)
                elif self.getSeparador():
                    self.subcont.append(self.prefijo)
                    return True
                else:
                    self.subcont.append(self.prefijo)
                    return True

    def getHex(self) -> bool:
        self.regresar()
        while 1:
            if self.estado == 0:
                if self.sigChar() == '#':
                    self.transicion(1)
                else:
                    return False
            if self.estado == 1:
                for i in range(6):
                    if self.sigChar().isalnum():
                        self.transicion(1)
                        continue
                    else:
                        return False
                else:
                    self.estado = 2
            if self.estado == 2:
                self.subcont.append(self.prefijo)
                return True

    def getDivisor(self) -> bool:
        self.regresar()
        for i in range(4):
            if self.sigChar() == '@':
                self.transicion(0)
            else:
                return False
        else:
            if len(self.errores) == 0:
                self.imgs.append(self.img)
                self.img = dict()
            return True

    def getSimbolo(self) -> bool:
        self.regresar()
        tipo = ''
        while 1:
            if self.estado == 0:
                if self.sigChar() == '=':
                    tipo = 'Igual'
                    self.transicion(1)
                elif self.sigChar() == '{':
                    tipo = 'LlaveApertura'
                    self.transicion(1)
                    self.contenedor = list()
                elif self.sigChar() == '}':
                    tipo = 'LlaveCierre'
                    self.transicion(1)
                elif self.sigChar() == "[":
                    tipo = 'CorcheteApertura'
                    self.transicion(1)
                    self.subcont = list()
                elif self.sigChar() == "]":
                    tipo = 'CorcheteCierre'
                    self.transicion(1)
                    self.contenedor.append(self.subcont)
                elif self.sigChar() == ';':
                    tipo = 'Punto&Coma'
                    self.transicion(1)
                    self.img[self.seccion] = self.asignarValor() #Añadir llave:valor
                elif self.sigChar() == ',':
                    tipo = 'Coma'
                    self.transicion(1)
                else:
                    return False
            elif self.estado == 1:
                token = Token(tipo,self.getLexema())
                self.addToken(token)
                return True

    def getSeparador(self) -> bool:
        c = self.sigChar()
        if c == ' ' or c == '\t':
            self.consumir()
            return True
        elif self.sigChar() == '\n':
            self.consumir()
            self.updateCount()
            return True
        else:
            return False
        
    def transicion(self,estado:int):
        self.prefijo += self.consumir()
        self.estado = estado
    
    def consumir(self) -> str:
        self.col += 1
        self.conteo += 1
        return self.flujo.pop(0)

    def updateCount(self):
        self.fila += 1
        self.col = 1
        self.conteo = 0

    def addToken(self,t:Token):
        self.tokens.append(t)
        self.entrada = self.flujo
        self.estado = 0

    def regresar(self):
        self.flujo = self.entrada
        self.estado = 0

    def error(self):
        caracter = self.consumir()
        self.entrada = self.flujo
        err = Error(self.fila,self.col,caracter)
        self.errores.append(err)
        self.estado = 0

    def asignarValor(self):
        if len(self.contenedor) == 0:
            self.contenedor.append(self.subcont)
        if self.seccion == 'COLORES':
            colores = dict()
            for color in self.contenedor:
                colores[color[0]] = color[1]
            self.subcont = list()
            self.contenedor = list()
            return colores
        elif self.seccion == 'FILTROS':
            valor = self.subcont
            self.subcont = list()
            self.contenedor = list()
            return valor
        elif len(self.contenedor) == 1 and len(self.subcont) == 1:
            valor = self.subcont.pop()
            self.subcont = list()
            self.contenedor = list()
            return valor
        else:
            valor = self.contenedor
            self.subcont = list()
            self.contenedor = list()
            return valor