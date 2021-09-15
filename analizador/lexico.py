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

    def escanear(self,entrada):
        self.str_to_list(entrada)
        while len(self.entrada) > 0:
            if self.getSeparador():
                continue
            elif self.getSimbolo():
                continue
            elif self.getId():
                token = Token('Id',self.getLexema())
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
                if self.getSeparador():
                    return True
                elif self.sigChar().isupper():
                    self.transicion(1)
                else:
                    return True

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
                if self.getSeparador():
                    return True
                elif self.sigChar().isdigit():
                    self.transicion(1)
                else:
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
                return True

    def getDivisor(self) -> bool:
        self.regresar()
        for i in range(4):
            if self.sigChar() == '@':
                self.transicion(0)
            else:
                return False
        else:
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
                elif self.sigChar() == '}':
                    tipo = 'LlaveCierre'
                    self.transicion(1)
                elif self.sigChar() == "[":
                    tipo = 'CorcheteApertura'
                    self.transicion(1)
                elif self.sigChar() == "]":
                    tipo = 'CorcheteCierre'
                    self.transicion(1)
                elif self.sigChar() == ';':
                    tipo = 'Punto&Coma'
                    self.transicion(1)
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