import utility as util


# clase general para manejar el formato de entregas del usuario
class UserInput:
    def __init__(self, max_length: int):
        self._max_length = max_length


# user input en forma de string para entregar nombres
class NameUserInput(UserInput):
    def __init__(self):
        super().__init__(max_length=30)
    
    def get_user_input(self) -> str:
        valid = False
        while not valid:
            user_input = input("Tu entrada: ")
            if len(user_input) > self._max_length:
                print("Entrada demasiado larga.")
            else:
                valid = True
        # volver
        if user_input == '0':
            return -1
        # entrada válida
        return user_input


# user input en forma de valores numéricos
class NumericalUserInput(UserInput):
    def __init__(self, options: list):
        # controlar si se necesite uno o dos números
        max_length = 1 + (options[-1] > 9)
        super().__init__(max_length=max_length)
        self._options = options
    
    def get_user_input(self) -> int:
        valid = False
        while not valid:
            user_input = input("Tu entrada: ")
            # volver
            if user_input == '0':
                return 0
            if (len(user_input) > self._max_length
                    or not user_input.isdigit()
                    or int(user_input) not in self._options):
                util.print_invalid_input()
            else:
                valid = True
        return int(user_input)


# user input en forma de coordinados de un sector del tablero
class SectorUserInput(UserInput):
    def __init__(self):
        super().__init__(max_length=3)

    def get_user_input(self) -> list:
        valid = False
        while not valid:
            coordinates = input()
            # volver
            if coordinates == '0':
                return -1
            # secuencia: número de una cifra, letra
            elif(len(coordinates) == 2
                    and coordinates[0].isdigit()
                    and not coordinates[1].isdigit()):
                x = int(coordinates[0])
                y = util.char_to_num(coordinates[1])
                valid = True
            # secuencia: letra, número de una cifra
            elif (len(coordinates) == 2
                    and not coordinates[0].isdigit()
                    and coordinates[1].isdigit()):
                x = int(coordinates[1])
                y = util.char_to_num(coordinates[0])
                valid = True
            # secuencia: número de dos cifras, letra
            elif(len(coordinates) == 3
                    and coordinates[0].isdigit()
                    and coordinates[1].isdigit()
                    and not coordinates[2].isdigit()):
                x = int(''.join((coordinates[0], coordinates[0])))
                y = util.char_to_num(coordinates[2])
                valid = True
            # secuencia: letra, número de dos cifras
            elif (len(coordinates) == 3
                    and not coordinates[0].isdigit()
                    and coordinates[1].isdigit()
                    and coordinates[2].isdigit()):
                x = int(''.join((coordinates[1], coordinates[2])))
                y = util.char_to_num(coordinates[0])
                valid = True
            else:
                util.print_invalid_input()
        return [x, y]