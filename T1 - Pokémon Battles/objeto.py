from abc import ABC, abstractmethod
from programon import Programon
import parametros as p
from random import randint


class Objeto(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    # aplicar el objeto a un programon y imprimir los cambios de sus valores
    @abstractmethod
    def aplicar_objeto(self):
        pass


class Baya(Objeto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'baya'
        self.costo = p.GASTO_ENERGIA_BAYA
    
    def aplicar_objeto(self, programon: Programon):
        vida_ant = programon.vida
        dif = randint(p.AUMENTO_VIDA_MIN, p.AUMENTO_VIDA_MAX)
        programon.vida += dif
        print(f"  Vida: {vida_ant:>3} -> {programon.vida:<3} (+{dif})")


class Pocion(Objeto):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'pocion'
        self.costo = p.GASTO_ENERGIA_POCION
    
    def aplicar_objeto(self, programon: Programon):
        ataque_ant = programon.ataque
        dif = randint(p.AUMENTO_ATAQUE_MIN, p.AUMENTO_ATAQUE_MAX)
        programon.ataque += dif
        print(f"  Ataque: {ataque_ant:>3} -> {programon.ataque:<3} (+{dif})")


class Caramelo(Baya, Pocion):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'caramelo'
        self.costo = p.GASTO_ENERGIA_POCION
    
    def aplicar_objeto(self, programon: Programon):
        Baya.aplicar_objeto(self, programon=programon)
        Pocion.aplicar_objeto(self, programon=programon)
        defensa_ant = programon.defensa
        dif = randint(p.AUMENTO_DEFENSA_MIN, p.AUMENTO_DEFENSA_MAX)
        programon.defensa += dif
        print(f"  Defensa: {defensa_ant:>3} -> {programon.defensa:<3} (+{dif})")