import tablero


class Field:
    def __init__(self, game_parameters: dict):
        self._username          = game_parameters['username']
        self._field_dimensions  = game_parameters['field_dimensions']
        self._beast_locations   = game_parameters['beast_locations']
        self._cell_contents     = game_parameters['cell_contents']

    # descubrir sector
    # devolver 0 si no contiene bestia y 1 si contiene bestia
    def discover_sector(self, sector: list) -> bool:
        x = sector[0]
        y = sector[1]
        # si la casilla contiene una bestia, devolver 1
        if sector in self._beast_locations:
            self._cell_contents[x][y] = "N"
            return 1
        # si no contiene bestia, contar las bestias en casillas rodeadas
        number_of_adjacent_beasts = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # no considerar coordinaderos fuera del tablero
                if((x + i not in range(self._field_dimensions[0]))
                        or (y + j not in range(self._field_dimensions[1]))):
                    continue
                if([x + i, y + j] in self._beast_locations
                        and not (i == 0 and j == 0)):
                    number_of_adjacent_beasts += 1
        self._cell_contents[x][y] = number_of_adjacent_beasts
        # descubrir otros sectores, si estan seguros
        if number_of_adjacent_beasts == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    # skip coordinaderos fuera del tablero y sectores conocidos
                    if((x + i not in range(self._field_dimensions[0]))
                            or (y + j not in range(self._field_dimensions[1]))
                            or not self._cell_contents[x + i][y + j] == ' '):
                        continue
                    # implementación recursivo
                    self.discover_sector([x + i, y + j])
        return 0

    # contar las células que deben ser descubrido
    def count_remaining_cells(self):
        counter = 0
        for i in range(self._field_dimensions[0]):
            for j in range(self._field_dimensions[1]):
                if self._cell_contents[i][j] == ' ':
                    counter += 1
        return counter - len(self._beast_locations)
    
    # revelar todas las bestias en el tablero actual
    def show_field(self):
        for sector in self._beast_locations:
            self._cell_contents[sector[0]][sector[1]] = 'N'
        tablero.print_tablero(self._cell_contents)
