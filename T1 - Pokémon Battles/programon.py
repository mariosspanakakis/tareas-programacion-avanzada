import parametros as p
from random import randint


class Programon():
    def __init__(self, nombre: str, tipo: str, nivel: int,
                    vida: int, ataque: int,
                    defensa: int, velocidad: int):
        self.nombre = nombre
        self.tipo = tipo
        self.__nivel = nivel
        self.__experiencia = 0
        self.__vida = vida
        self.__ataque = ataque
        self.__defensa = defensa
        self.__velocidad = velocidad

        with open(p.PATH_EVOLUCIONES, 'rt') as file:
            lines = file.readlines()
        # bonus funcionalidad: usar los nombres de los columnos
        ids = {}
        i = 0
        for elem in lines[0].strip().split(','):
            ids[elem] = i
            i += 1
        # buscar la entrada en el archivo de evoluciones
        for line in lines[1:]:
            line = line.strip().split(',')
            if line[ids['nombre']] == self.nombre:
                self.__nivel_megaevolucion = int(line[ids['nivel']])
                self.nombre_megaevolucion = line[ids['evolucion']]
        # en caso que el nivel por la evolucion está alcanzado, evolucionar
        if self.nivel >= self.nivel_megaevolucion:
            print("")
            print(f"{self.nombre} ya tiene el nivel necesario para su "
                f" megaevolución.")
            self.evolucionar()
    
    # nivel
    @property
    def nivel(self):
        return self.__nivel
    @nivel.setter
    def nivel(self, valor):
        valor = min(valor, p.NIVEL_MAX)
        valor = max(valor, p.NIVEL_MIN)
        self.__nivel = valor
    
    # nivel megaevolucion
    @property
    def nivel_megaevolucion(self):
        return self.__nivel_megaevolucion
    @nivel_megaevolucion.setter
    def nivel_megaevolucion(self, valor):
        valor = min(valor, p.NIVEL_MAX)
        valor = max(valor, p.NIVEL_MIN)
        self.__nivel_megaevolucion = valor

    # experiencia
    @property
    def experiencia(self):
        return self.__experiencia
    @experiencia.setter
    def experiencia(self, valor):
        valor = max(valor, p.EXPERIENCIA_MIN)
        self.__experiencia = valor
        # si la experiencia alcanza su máximo, aumentar en nivel
        if self.__experiencia > p.EXPERIENCIA_MAX:
            # guardar valores actuales
            vida_ant = self.vida
            ata_ant = self.ataque
            def_ant = self.defensa
            vel_ant = self.velocidad
            self.__experiencia -= p.EXPERIENCIA_MAX
            self.nivel += 1
            self.vida += randint(p.AUMENTO_ENTRENAMIENTO_MIN,
                                    p.AUMENTO_ENTRENAMIENTO_MAX)
            self.ataque += randint(p.AUMENTO_ENTRENAMIENTO_MIN,
                                    p.AUMENTO_ENTRENAMIENTO_MAX)
            self.defensa += randint(p.AUMENTO_ENTRENAMIENTO_MIN,
                                    p.AUMENTO_ENTRENAMIENTO_MAX)
            self.velocidad += randint(p.AUMENTO_ENTRENAMIENTO_MIN,
                                    p.AUMENTO_ENTRENAMIENTO_MAX)
            print("")
            print(f"{self.nombre} ha aumentado al nivel {self.nivel}!")
            print(f"Vida:\t\t{vida_ant:>4} -> {self.vida:<4}")
            print(f"Ataque:\t\t{ata_ant:>4} -> {self.ataque:<4}")
            print(f"Defensa:\t{def_ant:>4} -> {self.defensa:<4}")
            print(f"Velocidad:\t{vel_ant:>4} -> {self.velocidad:<4}")
            # evolucionar
            if self.nivel == self.nivel_megaevolucion:
                print(f"Oh... ¡tu Pokemon está evolucionando!")
                print("...")
                self.evolucionar()


    # vida
    @property
    def vida(self):
        return self.__vida
    @vida.setter
    def vida(self, valor):
        valor = min(valor, p.VIDA_MAX)
        valor = max(valor, p.VIDA_MIN)
        self.__vida = valor
    
    # ataque
    @property
    def ataque(self):
        return self.__ataque
    @ataque.setter
    def ataque(self, valor):
        valor = min(valor, p.ATAQUE_MAX)
        valor = max(valor, p.ATAQUE_MIN)
        self.__ataque = valor
    
    # defensa
    @property
    def defensa(self):
        return self.__defensa
    @defensa.setter
    def defensa(self, valor):
        valor = min(valor, p.DEFENSA_MAX)
        valor = max(valor, p.DEFENSA_MIN)
        self.__defensa = valor

    # velocidad
    @property
    def velocidad(self):
        return self.__velocidad
    @velocidad.setter
    def velocidad(self, valor):
        valor = min(valor, p.VELOCIDAD_MAX)
        valor = max(valor, p.VELOCIDAD_MIN)
        self.__velocidad = valor
    
    # ganar experiencia por entrenamiento
    def entrenar(self):
        aumento = randint(p.AUMENTO_EXPERIENCIA_MIN, p.AUMENTO_EXPERIENCIA_MAX)
        print(f"{self.nombre} ganó un total de {aumento} experiencia!")
        self.experiencia += aumento
        if self.nivel == p.NIVEL_MAX:
            self.experiencia = p.EXPERIENCIA_MIN
            print(f"{self.nombre} ha alcanzado el nivel máximo.")

    def luchar(self, tipo_del_adversio: str) -> float:
        # calcular la ventaja de tipo
        ventaja_de_tipo = 0
        match tipo_del_adversio:
            case 'agua':
                if self.tipo == 'planta':
                    ventaja_de_tipo = 1
                elif self.tipo == 'fuego':
                    ventaja_de_tipo = -1
            case 'fuego':
                if self.tipo == 'agua':
                    ventaja_de_tipo = 1
                elif self.tipo == 'planta':
                    ventaja_de_tipo = -1
            case 'planta':
                if self.tipo == 'fuego':
                    ventaja_de_tipo = 1
                elif self.tipo == 'agua':
                    ventaja_de_tipo = -1
        
        # calcular el puntaje de victoria
        puntaje = max(0, (self.vida * p.POND_VIDA
                            + self.nivel * p.POND_NIVEL
                            + self.ataque * p.POND_ATAQUE
                            + self.defensa * p.POND_DEFENSA
                            + self.velocidad * p.POND_VELOCIDAD
                            + ventaja_de_tipo * p.POND_VENTAJA))
        return puntaje
    
    # aumentar los valores cuando una batalla ha sido ganado
    def ganar_batalla(self):
        match self.tipo:
            case 'agua':
                self.velocidad += p.AUMENTO_VELOCIDAD_AGUA
            case 'fuego':
                self.ataque += p.AUMENTO_ATAQUE_FUEGO
            case 'planta':
                self.vida += p.AUMENTO_VIDA_PLANTA

    def evolucionar(self):
        print(f"{self.nombre} evolucionó a {self.nombre_megaevolucion}!")
        self.nombre = self.nombre_megaevolucion
        self.vida += p.MEGA_VIDA
        self.ataque += p.MEGA_ATAQUE
        self.defensa += p.MEGA_DEFENSA
        self.velocidad += p.MEGA_VELOCIDAD