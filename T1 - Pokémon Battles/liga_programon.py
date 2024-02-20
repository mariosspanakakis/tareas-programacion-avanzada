from ui import UI
from entrenador import Entrenador
import parametros as p
import random


class LigaProgramon:
    def __init__(self):
        self.__reset()
        # elemento ui para interactuar con el usuario
        self.ui = UI()
        self.ui.imprimir_titulo(titulo="DCCampeonato Programón")
    
    ############################################################################
    def __reset(self):
        self.entrenadores = []
        self.perdedores = []
        self.ronda_actual = 0
        self.campeon = None

        # cargar entrenadores
        with open(p.PATH_ENTRENADORES) as file:
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
            programones = line[ids['programones']].split(';')
            energia = int(line[ids['energia']])
            objetos = line[ids['objetos']].split(';')
            entrenador = Entrenador(nombre=nombre, energia=energia,
                                    programones=programones, objetos=objetos)
            self.entrenadores.append(entrenador)
        # el entrenador seleccionado por el usuario
        self.jugador = None

    ############################################################################
    def menu_de_inicio(self):
        titulo = "Menú de Inicio"
        texto = [f"Seleccionar un entrenador para jugar!"]
        opciones = [entrenador.nombre for entrenador in self.entrenadores]

        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=False, salir=True)
        
        self.jugador = self.entrenadores[input - 1]
        self.menu_de_entrenador()

    ############################################################################
    def menu_de_entrenador(self):
        titulo = "Menú del Entrenador"
        texto = [f"Entrenador: {self.jugador.nombre}"]
        opciones = [
            "Entrenar Programones",
            "Simular Ronda",
            "Resumir Campeonato",
            "Crear Objetos",
            "Utilizar Objeto",
            "Mostrar Estado del Entrenador"
        ]

        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True)
        match input:
            # volver al menú de inicio
            case -1:
                self.menu_de_inicio()
            # entrenamiento
            case 1:
                self.menu_de_entrenamiento()
            # simular ronda
            case 2:
                self.simular_ronda()
            # resumir campeonato
            case 3:
                self.resumir_campeonato()
            # crear objetos
            case 4:
                self.crear_objetos()
            # utilizar objetos
            case 5:
                self.utilizar_objeto()
            # mostrar estado del entrenador
            case 6:
                self.mostrar_estado_del_entrenador()

    ############################################################################
    def menu_de_entrenamiento(self):
        titulo = "Menú de Entrenamiento"
        texto = [
            f"{self.jugador.nombre} tiene {self.jugador.energia} energía.",
            f"Entrenar un programón cuesta {p.ENERGIA_ENTRENAMIENTO}."
        ]
        opciones = [programon.nombre for programon in self.jugador.programones]

        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True)
        if input == -1:
            self.menu_de_entrenador()
        
        # energia no es suficiente
        if self.jugador.energia < p.ENERGIA_ENTRENAMIENTO:
            print(f"{self.jugador.nombre} no tiene suficiente energía!")
            self.ui.esperar_confirmacion()
            self.menu_de_entrenador()
        # energia es suficiente
        self.jugador.energia -= p.ENERGIA_ENTRENAMIENTO
        programon = self.jugador.programones[input - 1]
        print("")
        print(f"{self.jugador.nombre} usó {p.ENERGIA_ENTRENAMIENTO} "
            + f"energía para entrenar su {programon.nombre}.")
        programon.entrenar()
        self.ui.esperar_confirmacion()
        self.menu_de_entrenamiento()

    ############################################################################
    def simular_ronda(self):
        titulo = "Simulación de Ronda"
        texto = [f"Elige tu luchador!"]
        opciones = [
            (f"{prog.nombre:<30} NIV: {prog.nivel:<3} "
            + f"VID: {prog.vida:<3} ATQ: {prog.ataque:<3} "
            + f"DEF: {prog.defensa:<3} VEL: {prog.velocidad:<3}")
            for prog in self.jugador.programones
        ]

        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True)
        if input == -1:
            self.menu_de_entrenador()
        # eligir programon para luchar
        self.jugador.luchador = self.jugador.programones[input-1]
        print(f"{self.jugador.nombre}:"
                + f"'{self.jugador.luchador.nombre}, te eligo!'\n")

        # imprimir ronda
        self.ronda_actual += 1
        print(f"Esta es la ronda {self.ronda_actual} de 4!")
        
        # generar lista de adversios actuales, excluyendo los perdidores
        adversios = [
            entrenador for entrenador in self.entrenadores
            if entrenador not in self.perdedores
        ]
        # eligir los luchadores de los otros entrenadores al azar
        for adversio in adversios:
            if adversio != self.jugador:
                adversio.luchador = random.choice(adversio.programones)
        
        # generar parejas al azar
        parejas = []
        while adversios:
            # eligir dos entrenadores
            entrenador_1 = adversios.pop(random.randrange(0, len(adversios)))
            entrenador_2 = adversios.pop(random.randrange(0, len(adversios)))
            pareja = [entrenador_1, entrenador_2]
            parejas.append(pareja)
        print("¡Las batallas empiezan! Parejas de esta ronda:")
        # imprimir los combinaciones de batalla
        for pareja in parejas:
            str_1 = f"{pareja[0].nombre} con {pareja[0].luchador.nombre}"
            str_2 = f"{pareja[1].nombre} con {pareja[1].luchador.nombre}"
            print(f"{str_1:>50} vs. {str_2:<50}")
        self.ui.esperar_confirmacion()

        # simular las batallas
        ganadores = []
        for pareja in parejas:
            # calcular el puntaje de cada programon para determinar el ganador
            luchador_1 = pareja[0].luchador
            luchador_2 = pareja[1].luchador
            puntaje_1 = luchador_1.luchar(tipo_del_adversio=luchador_2.tipo)
            puntaje_2 = luchador_2.luchar(tipo_del_adversio=luchador_1.tipo)
            # anadir el ganador a la lista de los ganadores
            id_ganador = puntaje_2 > puntaje_1
            ganadores.append(pareja[id_ganador])
            # anadir el perdedor a la lista de las perdedores
            self.perdedores.append(pareja[not id_ganador])
        
        # imprimir los resultados
        print("¡Las batallas se realizaron! Estos son los ganadores:")
        for ganador in ganadores:
            ganador.energia = p.ENERGIA_MAX
            ganador.luchador.ganar_batalla()
            print(f"  {ganador.nombre}")
        print(f"El resto de los entrenadores se retiran del torneo...\n")

        # caso que jugador ha ganado
        if self.jugador in ganadores:
            if self.ronda_actual == 4:
                print(f"¡{self.jugador.nombre} es el campión del torneo.")
                print(f"Se merece el título de mejor entrenador del mundo!")
                self.ui.esperar_confirmacion()
                self.__reset()
                self.menu_de_inicio()
            else: 
                print(f"¡{self.jugador.nombre} ganó y sigue en el torneo!")
                self.ui.esperar_confirmacion()
                self.menu_de_entrenador()

        # caso que jugador ha perdido
        print(f"¡Que pena! {self.jugador.nombre} perdió "
            + f"y es eliminado del torneo por esta vez.")
        self.ui.esperar_confirmacion()
        self.__reset()
        self.menu_de_inicio()

    ############################################################################
    def resumir_campeonato(self):
        titulo = "Resúmen del Campeonato"
        texto = [
            f"Rondas realizadas: {self.ronda_actual} de 4",
            f"Entrenadores que siguien participando en el torneo:",
        ]
        for entrenador in self.entrenadores:
            if entrenador not in self.perdedores:
                texto += [f"  {entrenador.nombre}"]

        texto += [f"Entrenadores que han sido eliminado:"]
        if not self.perdedores:
            texto += [f"  Hasta ahora, no hay perdedores."]
        else:
            texto += [f"  {ent.nombre}" for ent in self.perdedores]

        input = self.ui.menu(titulo=titulo, texto=texto, opciones=[],
                        volver=True, salir=True)
        if input == -1:
            self.menu_de_entrenador()

    ############################################################################
    def crear_objetos(self):
        titulo = "Crear Objetos"
        texto = [
            f"{self.jugador.nombre} tiene {self.jugador.energia} energía.",
            f"¿Qué tipo de objeto quieres crear?\n",
        ]
        opciones = [
            f"Baya (cuesta {p.GASTO_ENERGIA_BAYA} energía)",
            f"Poción (cuesta {p.GASTO_ENERGIA_POCION} energía)",
            f"Caramelo (cuesta {p.GASTO_ENERGIA_CARAMELO} energía)"
        ]
        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True)
        
        # crear un objeto del tipo eligido
        match input:
            case -1:
                self.menu_de_entrenador()
            case 1:
                # energia no es suficiente
                if self.jugador.energia < p.GASTO_ENERGIA_BAYA:
                    print(f"{self.jugador.nombre} no tiene suficiente energía!")
                    self.ui.esperar_confirmacion()
                    self.crear_objetos()
                # energia es suficiente
                self.jugador.energia -= p.GASTO_ENERGIA_BAYA
                print(f"{self.jugador.nombre} gastó {p.GASTO_ENERGIA_BAYA} "
                    + f"energía para intentar crear una baya.")
                self.jugador.crear_objeto(tipo_para_crear='baya')
            case 2:
                # energia no es suficiente
                if self.jugador.energia < p.GASTO_ENERGIA_POCION:
                    print(f"{self.jugador.nombre} no tiene suficiente energía!")
                    self.ui.esperar_confirmacion()
                    self.crear_objetos()
                # energia es suficiente
                self.jugador.energia -= p.GASTO_ENERGIA_POCION
                print(f"{self.jugador.nombre} gastó {p.GASTO_ENERGIA_POCION} "
                    + f"energía para intentar crear una poción.")
                self.jugador.crear_objeto(tipo_para_crear='pocion')
            case 3:
                # energia no es suficiente
                if self.jugador.energia < p.GASTO_ENERGIA_CARAMELO:
                    print(f"{self.jugador.nombre} no tiene suficiente energía!")
                    self.ui.esperar_confirmacion()
                    self.crear_objetos()
                # energia es suficiente
                self.jugador.energia -= p.GASTO_ENERGIA_CARAMELO
                print(f"{self.jugador.nombre} gastó {p.GASTO_ENERGIA_CARAMELO} "
                    + f"energía para intentar crear un caramelo.")
                self.jugador.crear_objeto(tipo_para_crear='caramelo')
        
        self.ui.esperar_confirmacion()
        self.crear_objetos()

    ############################################################################
    def utilizar_objeto(self):
        # seleccionar objeto
        titulo = "Utilizar Objetos"
        if not self.jugador.objetos:
            texto = [f"{self.jugador.nombre} no posee objetos."]
            opciones = []
        else:
            texto = ["Seleccionar un objeto para usar:"]
            opciones = [f"{objeto.nombre} ({objeto.tipo})"
                    for objeto in self.jugador.objetos]
        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True)
        if input == -1:
            self.menu_de_entrenador()
        else:
            objeto = self.jugador.objetos[input-1]

        # seleccionar programon
        titulo = ""
        texto = [f"¿A qué programón quieres dar este {objeto.nombre}?"]
        opciones = [f"{prog.nombre}" for prog in self.jugador.programones]
        input = self.ui.menu(titulo=titulo, texto=texto, opciones=opciones,
                        volver=True, salir=True, mostrar_titulo=False)
        if input == -1:
            self.menu_de_entrenador()
        else:
            programon = self.jugador.programones[input-1]
            self.jugador.objetos.remove(objeto)
        
        # aplicar objeto y imprimir resultado
        print("")
        print(f"{self.jugador.nombre} dio un {objeto.nombre} "
            + f"a su {programon.nombre}.")
        objeto.aplicar_objeto(programon=programon)

        self.ui.esperar_confirmacion()
        self.utilizar_objeto()

    ############################################################################
    def mostrar_estado_del_entrenador(self):
        titulo = f"Estado del Entrenador"
        texto = [
            f"Nombre: {self.jugador.nombre}",
            f"Energía: {self.jugador.energia}",
            f"Objetos:"
        ]
        texto += [f"  {obj.nombre} ({obj.tipo})" for obj in self.jugador.objetos]
        texto += [f"Programones:"]
        texto += [f"  {prog.nombre:<30} tipo: {prog.tipo:<6} "
            + f"NIV: {prog.nivel:<3} "
            + f"VID: {prog.vida:<3} ATQ: {prog.ataque:<3} "
            + f"DEF: {prog.defensa:<3} VEL: {prog.velocidad:<3}"
            for prog in self.jugador.programones]
        input = self.ui.menu(titulo=titulo, texto=texto, opciones=[],
                        volver=True, salir=True)
        if input == -1:
            self.menu_de_entrenador()