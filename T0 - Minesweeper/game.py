import math
import random
import os
import tablero
import parametros
from user_input import NameUserInput, NumericalUserInput, SectorUserInput
from field import Field
import utility as util


# clase central, maneja todas las funcionalidades del juego
class Game:
    def __init__(self):
        pass

    # empezar el juego
    def start(self):
        print("")
        print("#" * 60)
        print("#####################  STAR  ADVANCED  #####################")
        print("#" * 60)
        self._show_initial_menu()

    # crear una nueva mapa con beastias en locaciónes aleatorios
    def _generate_new_map(self, username: str, field_dimensions: list):
        height  = field_dimensions[0]
        width   = field_dimensions[1]
        # generar células vacías con el contenido ' ' (= oculto)
        cell_contents = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(' ')
            cell_contents.append(row)
        # distribuir bestias en la mapa
        self._num_of_beasts = math.ceil(height * width * parametros.PROB_BESTIA)
        beast_locations = []
        i = 0
        while i in range(self._num_of_beasts):
            loc = [random.randrange(0, height), random.randrange(0, width)]
            # todas las bestias in distintos locaciones
            if loc not in beast_locations:
                beast_locations.append(loc)
                i += 1
        # crear una nueva instancia del tipo Field con los siguientes parametros
        game_parameters = {
            "username":         username,
            "field_dimensions": field_dimensions,
            "beast_locations":  beast_locations,
            "cell_contents":    cell_contents 
        }
        self._field = Field(game_parameters=game_parameters)

    # mostrar el menú de inicio y manejar la entrada
    def _show_initial_menu(self):
        util.print_separation_line(content="Menú de Inicio")
        print("Seleccione una opción:")
        print("[1]: Empezar partida nueva")
        print("[2]: Cargar partida existente")
        print("[3]: Mostrar ranking de puntaje")
        print("[0]: Quitar")

        user_input = NumericalUserInput(options=[0, 1, 2, 3]).get_user_input()
        match user_input:
            # quitar
            case 0:
                quit()
            # empezar nueva partida
            case 1:
                self._start_new_game()
            # cargar partida existente
            case 2:
                self._load_game()
            # mostrar ranking
            case 3:
                self._show_ranking()
                print("")
                print("\t\t\t\t\t\t[0]: Volver")
                if NumericalUserInput(options=[0]).get_user_input() == 0:
                    self._show_initial_menu()

    # mostrar el menú del juego y manejar la entrada
    def _show_game_menu(self):
        util.print_separation_line(content="Menú del Juego")
        print("Usuario:", self._field._username)
        # imprimir el tablero
        tablero.print_tablero(self._field._cell_contents)

        print("Seleccione una opción: ")
        print("[1]: Discubrir sector")
        print("[2]: Guardar partida con nombre", self._field._username)
        print("[0]: Salir partida")

        user_input = NumericalUserInput(options=[0, 1, 2]).get_user_input()
        match user_input:
            # salir
            case 0:
                print("¿Quieres guardar tu partida?")
                print("[1]: Si")
                print("[2]: No")
                print("[0]: Volver")
                user_input = NumericalUserInput([0, 1, 2]).get_user_input()
                match user_input:
                    # volver al Menú del Juego
                    case 0:
                        self._show_game_menu()
                    # salir con guardar
                    case 1:
                        self._save_game()
                        self._show_initial_menu()
                    # salir sin guardar
                    case 2:
                        self._show_initial_menu()
            # discubrir sector
            case 1:
                print("")
                print("Entregar coordinados del sector con letra y número.")
                print("\t\t\t\t\t\t[0]: Volver")
                valid = False
                while not valid:
                    # obtener el input del usuario, el formato correcto se
                    # maneja en la clase SectorUserInput
                    [x, y] = SectorUserInput().get_user_input()
                    # se controla si el sector es válido para discubrir
                    # (parte del tablero y no ya conocido)
                    if (x in range(0, self._field._field_dimensions[0])
                            and y in range(self._field._field_dimensions[1])):
                        if not self._field._cell_contents[x][y] == ' ':
                            print("Este sector ya es conocido.")
                        else:
                            valid = True
                    else:
                        print("Sector afuera del tablero.")
                result = self._field.discover_sector([x, y])
                # no bestia
                if result == 0:
                    # partida ganado
                    if self._field.count_remaining_cells() == 0:
                        tablero.print_tablero(self._field._cell_contents)
                        self._show_end_game(win=1)
                    # partida continua
                    else:
                        self._show_game_menu()
                # bestia, partida perdido
                else:
                    self._field.show_field()
                    self._show_end_game(win=0)
            # guardar partida
            case 2:
                self._save_game()
                self._show_game_menu()

    # empezar una nueva partida con un tablero vacío
    def _start_new_game(self):
        print("")
        print("Entregar tu usuario.")
        print("\t\t\t\t\t\t[0]: Volver")
        username = NameUserInput().get_user_input()
        # volver
        if username == -1:
            self._show_initial_menu()
        print("")
        print("Entregar largo y ancho del tablero.")
        print("\t\t\t\t\t\t[0]: Volver")
        print("El largo debe ser entre 3 y 15.")
        height = NumericalUserInput(options=range(3, 16)).get_user_input()
        # volver
        if not height:
            self._show_initial_menu()
        print("El ancho debe ser entre 3 y 15.")
        width = NumericalUserInput(options=range(3, 16)).get_user_input()
        # volver
        if not width:
            self._show_initial_menu()
        # crear un tablero nuevo con los datos ingresados
        self._generate_new_map(username, [height, width])
        self._show_game_menu()

    # guardar la partida actual con el nombre de usuario
    def _save_game(self):
        # crear la carpeta de partidas, si no ya existe
        if not os.path.exists('partidas/'):
            os.makedirs('partidas/')
        path = ''.join(('partidas/', self._field._username, '.txt'))
        # si existe una partida con este nombre, notificar el usuario
        if os.path.exists(path):
            print("Ya existe una partida con este nombre.")
            print("¿Sustituir el archivo?")
            print("[1]: Si")
            print("[0]: No, volver.")
            user_input = NumericalUserInput(options=[0, 1]).get_user_input()
            match user_input:
                case '0':
                    self._show_game_menu()
                case '1':
                    pass
        # escribir los parametros del juego en el archivo nuevo
        with open(path, 'w') as file:
            # nombre del usuario
            username = str(self._field._username)
            for e in self._field._field_dimensions:
                field_dimensions = ','.join(str(e))
            field_dimensions = ','.join(str(e) for e in self._field._field_dimensions)
            # locaciónes de las bestias
            beast_locations = []
            for i in range(len(self._field._beast_locations)):
                for e in self._field._beast_locations[i]:
                    beast_locations.append(';'.join(str(e)))
            beast_locations = ','.join(str(e) for e in beast_locations)
            for beast in self._field._beast_locations:
                beast_locations = ','.join(';'.join(str(e) for e in beast))
            # contenidos de las casillas
            cell_contents = []
            for i in range(len(self._field._cell_contents)):
                for e in self._field._cell_contents[i]:
                    cell_contents.append(';'.join(str(e)))
            cell_contents = ','.join(str(e) for e in cell_contents)
            for line in self._field._cell_contents:
                cell_contents = ','.join(';'.join(str(e) for e in line))
            # unir los datos en líneas diferentes
            content = '\n'.join([username,
                                 field_dimensions,
                                 beast_locations,
                                 cell_contents])
            file.writelines(content)
        print("Partida guardada!")

    # cargar una partida existente
    def _load_game(self):
        print("")
        print("Entregar nombre de la partida que quieres cargar")
        print("[0]: Volver al menú de inicio")
        game_name = NameUserInput().get_user_input()
        # volver
        if game_name == -1:
            self._show_initial_menu()
        if not os.path.exists(''.join(('partidas/', game_name, '.txt'))):
            print("No existe una partida de este nombre.")
            self._load_game()
        
        # cargar la partida
        print("")
        print("Cargando partida...")
        path = ''.join(('partidas/', game_name, '.txt'))
        with open(path, 'rt') as file:
            lines = file.readlines()
        
        # extraer datos del archivo
        field_dimensions = [int(e) for e in lines[1].strip().split(',')]
        beast_locations = [e.split(';') for e in lines[2].strip().split(',')]
        for i in range(len(beast_locations)):
            beast_locations[i] = [int(e) for e in beast_locations[i]]
        cell_contents = [e.split(';') for e in lines[3].split(',')]
        self._num_of_beasts = len(beast_locations)
        print("Listo!")

        # el usuario puede elegir un nombre nuevo
        print("")
        print("Entregar tu usuario.")
        print("\t\t\t\t\t\t[0]: Volver")
        username = NameUserInput().get_user_input()
        # volver
        if username == -1:
            self._show_initial_menu()

        # crear una nueva instancia del tablero con los siguientes datos
        game_parameters = {
            "username":         username,
            "field_dimensions": field_dimensions,
            "beast_locations":  beast_locations,
            "cell_contents":    cell_contents 
        }
        self._field = Field(game_parameters=game_parameters)
        self._show_game_menu()

    # calcular y guardar el puntaje del jugador
    def _calculate_points(self) -> int:
        # contar las casillas descubiertos
        discovered_sects = 0
        for sector in self._field._cell_contents:
            for element in sector:
                if (element != ' ' and element != 'N'):
                    discovered_sects += 1
        # calcular el puntaje
        puntaje = self._num_of_beasts * discovered_sects * parametros.POND_PUNT
        # guardar el puntaje
        path = ''.join(('puntaje.txt'))
        # crear el archivo si no ya existe
        if not os.path.isfile(path):
            with open('puntaje.txt', 'w'):
                pass
        with open(path, 'a') as file:
            file.write('\n' + str(self._field._username) + ',' + str(puntaje))
        return puntaje

    # mostrar el ranking con las 10 puntaciones más altas
    def _show_ranking(self):
        path = ''.join(('puntaje.txt'))
        # crear el archivo si no ya existe
        if not os.path.isfile(path):
            with open('puntaje.txt', 'w'):
                pass
        with open(path, 'rt') as file:
            lines = file.readlines()
        # extraer y sortar datos
        entries = []
        for line in lines[1:]:
            line = line.strip().split(',')
            entries.append([int(line[1]), line[0]])
        ranking = sorted(entries, reverse=True)[0:10]
        # imprimir ranking
        util.print_separation_line("Ranking")
        print("Puntaje\t- Usuario")
        print("_"*24)
        for rank in ranking:
            print(f"{rank[0]: >7}\t- {rank[1]: <20}")

    # notificar el usuario cuando la partida terminó, si ha ganado o perdido
    # y mostrar su puntaje
    def _show_end_game(self, win):
        print("")
        if win:
            print("Felicidades, has ganado el juego!")
        else:
            print("Qué pena, has perdido.")
        print("Nombre:", self._field._username)
        print("Puntaje:", self._calculate_points())
        print("")
        print("Entregar '0' para volver.")
        if NumericalUserInput(options=[0]).get_user_input() == 0:
            self._show_initial_menu()