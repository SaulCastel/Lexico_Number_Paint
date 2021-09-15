from analizador.lexema import *

class Token:

    def __init__(self,id:str,valor:Lexema) -> None:
        self.id = id
        self.valor = valor

    def toString(self) -> str:
        lex = self.valor
        return f'{self.id} | " {lex.valor} " en: ({str(lex.fila)}, {str(lex.col)})'