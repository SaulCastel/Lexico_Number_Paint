class Error:
    def __init__(self,fila:int,col:int,caracter:str) -> None:
        self.fila = fila
        self.col = col
        self.caracter = caracter

    def toString(self) -> str:
        c = self.caracter.replace('\n',r'\n')
        return f'en: ({str(self.fila)}, {str(self.col)}) -> " {c} "'