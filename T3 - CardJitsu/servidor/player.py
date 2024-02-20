from utils import data_json
from cartas import get_penguins
from collections import deque
from random import choice


# implementa todas las funcionalidades relacionados al jugador
class Player:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.cards = deque()
        self.hand_cards = {}
        self.selected_card = None
        self.active_card = None
        self.victory_cards = []
        self.winner = False

        self.reinitialize_for_game()

    # reiniciar los estados del jugador para un nuevo juego
    def reinitialize_for_game(self):
        # distribuir cartas aleatorias al mazo del jugador
        self.cards = deque()
        random_cards = get_penguins()
        for card in random_cards.values():
            self.cards.append(card)
        # vaciar las cartas de mano y tomar nuevas
        self.hand_cards = {}
        for i in range(data_json('BARAJA_PANTALLA')):
            self.hand_cards[i] = None
        self.victory_cards = []
        self.winner = False
    
    # reiniciar los estados del jugador para una nueva ronda
    def reinitialize_for_round(self):
        self.selected_card = None
        self.active_card = None
        self.draw_hand_cards()

    # tomar cartas hasta alcanzar el número máximo de cartas de la mano
    def draw_hand_cards(self):
        for i in range(data_json('BARAJA_PANTALLA')):
            if not self.hand_cards[i]:
                card = self.cards.popleft()
                self.hand_cards[i] = card

    # seleccionar una carta especifica de las cartas del mano, o una al azar
    def select_card(self, card_id=None):
        if card_id is None:
            card_id = choice(list(self.hand_cards.keys()))
        self.selected_card = self.hand_cards[card_id]

    # confirmar la carta seleccionada y jugarla
    def confirm_selected_card(self):
        if self.active_card is None:
            # jugar la carta
            self.active_card = self.selected_card
            # buscar la carta y eliminarla del mano
            for card_id, card in self.hand_cards.items():
                if card == self.selected_card:
                    self.hand_cards[card_id] = None
                    break
            self.selected_card = None
    
    # anadir la carta activa a las cartas de victoria
    def gain_victory_card(self):
        self.victory_cards.append(self.active_card)
        #self.active_card = None
        self.winner = self.check_win()

    # tomar la carta activa y ponerla al término del mazo
    def take_active_card(self):
        self.cards.append(self.active_card)
        #self.active_card = None

    # comprobar si el jugador ha ganado la partida
    def check_win(self) -> bool:
        red = set()
        blue = set()
        green = set()

        for card in self.victory_cards:
            match card['color']:
                case 'rojo':
                    red.add(card['elemento'])
                case 'azul':
                    blue.add(card['elemento'])
                case 'verde':
                    green.add(card['elemento'])
        
        elements = set(['fuego', 'agua', 'nieve'])
        colorsets = [red, blue, green]

        # condición 1: tres cartas del mismo elemento
        if red & blue & green:
            return True
        # condición 2: tres cartas de diferentes elementos
        elif self.search_cards(elements, colorsets, found_elements=set()):
            return True
        # cartas de victoria no cumplen con la condición de ganar
        else:
            return False

    # comprobar si existen cartas de tres tipos diferentes en los sets
    def search_cards(self, elements: set, colorsets: list, found_elements: set) -> bool:
        for element in elements:
            for colorset in colorsets:
                if element in colorset:
                    found_elements.add(element)
                    rem_elements = elements.copy()
                    rem_elements.remove(element)
                    rem_colorsets = colorsets.copy()
                    rem_colorsets.remove(colorset)
                    if len(found_elements) == 3:
                        return True
                    else:
                        return self.search_cards(rem_elements, rem_colorsets, found_elements)
        return False

    # imprimir el nombre del jugador
    def __repr__(self) -> str:
        return self.name