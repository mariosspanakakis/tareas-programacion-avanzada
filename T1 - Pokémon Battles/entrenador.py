from programon import Programon
from objeto import Baya, Pocion, Caramelo
import parametros as p
import random


class Entrenador:
    def __init__(self, nombre: str, energia: int, programones: list,
                    objetos: list):
        self.nombre = nombre
        self.__energia = energia
        # generar la lista de programones
        self.programones = []
        with open(p.PATH_PROGRAMONES, 'rt') as file:
            lines = file.readlines()
        # bonus funcionalidad: usar los nombres de los columnos
        ids = {}
        i = 0
        for elem in lines[0].strip().split(','):
            ids[elem] = i
            i += 1
        for line in lines[1:]:
            line = line.strip().split(',')
            nombre = line[ids['nombre']]
            tipo = line[ids['tipo']]
            nivel = int(line[ids['nivel']])
            vida = int(line[ids['vida']])
            ataque = int(line[ids['ataque']])
            defensa = int(line[ids['defensa']])
            velocidad = int(line[ids['velocidad']])

            if nombre in programones:
                programon = Programon(nombre=nombre, tipo=tipo, nivel=nivel,
                                vida=vida, ataque=ataque,
                                defensa=defensa, velocidad=velocidad)
                self.programones.append(programon)
        # generar la lista de objetos
        self.objetos = []
        with open(p.PATH_OBJETOS, 'rt') as file:
            lines = file.readlines()
        # bonus funcionalidad: usar los nombres de los columnos
        ids = {}
        i = 0
        for elem in lines[0].strip().split(','):
            ids[elem] = i
            i += 1
        for line in lines[1:]:
            line = line.strip().split(',')
            nombre = line[ids['nombre']]
            tipo = line[ids['tipo']]

            if nombre in objetos:
                match tipo:
                    case 'baya':
                        objeto = Baya(nombre=nombre)
                    case 'pocion':
                        objeto = Pocion(nombre=nombre)
                    case 'caramelo':
                        objeto = Caramelo(nombre=nombre)
                self.objetos.append(objeto)
        # el programon que participa en los batallas
        self.luchador = None

    # energia    
    @property
    def energia(self):
        return self.__energia
    @energia.setter
    def energia(self, valor):
        valor = min(valor, p.ENERGIA_MAX)
        valor = max(valor, p.ENERGIA_MIN)
        self.__energia = valor
    
    # crear un objeto nuevo
    def crear_objeto(self, tipo_para_crear: str):
        # importar todos los objetos disponibles
        objetos_disponibles = {
            'baya': [],
            'pocion': [],
            'caramelo': []
        }
        with open(p.PATH_OBJETOS, 'rt') as file:
            lines = file.readlines()
        # bonus funcionalidad: usar los nombres de los columnos
        ids = {}
        i = 0
        for elem in lines[0].strip().split(','):
            ids[elem] = i
            i += 1
        for line in lines[1:]:
            line = line.strip().split(',')
            nombre = line[ids['nombre']]
            tipo = line[ids['tipo']]
            objetos_disponibles[tipo].append(nombre)
        
        # dependiente de su tipo, crear un objeto
        match tipo_para_crear:
            case 'baya':
                print("Intentando crear una baya...")
                if random.random() < p.PROB_EXITO_BAYA:
                    print("... exitoso!")
                    objeto_nuevo = random.choice(objetos_disponibles['baya'])
                    self.objetos.append(Baya(nombre=objeto_nuevo))
                    print(f"{self.nombre} ganó el objeto {objeto_nuevo}.")
                else:
                    print("Desafortunadamente, eso no funcionó.")
            case 'pocion':
                print("Intentando crear una poción...")
                if random.random() < p.PROB_EXITO_POCION:
                    print("... exitoso!")
                    objeto_nuevo = random.choice(objetos_disponibles['pocion'])
                    self.objetos.append(Pocion(nombre=objeto_nuevo))
                    print(f"{self.nombre} ganó el objeto {objeto_nuevo}.")
                else:
                    print("Desafortunadamente, eso no funcionó.")
            case 'caramelo':
                print("Intentando crear un caramelo...")
                if random.random() < p.PROB_EXITO_CARAMELO:
                    print("... exitoso!")
                    objeto_nuevo = random.choice(objetos_disponibles['caramelo'])
                    self.objetos.append(Caramelo(nombre=objeto_nuevo))
                    print(f"{self.nombre} ganó el objeto {objeto_nuevo}.")
                else:
                    print("Desafortunadamente, eso no funcionó.")