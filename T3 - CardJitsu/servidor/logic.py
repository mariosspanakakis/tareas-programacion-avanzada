from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from time import sleep
from utils import data_json
from player import Player
from messager import Messager


class Logic(QObject):

    sig_log_event = pyqtSignal(str, str) # title, msg
    sig_send_message_to_client = pyqtSignal(dict, int) # msg, client_id
    sig_broadcast_message = pyqtSignal(dict) # msg

    def __init__(self):
        super().__init__()

        self.players = {}
        self._round_running = False
        self.game_running = False
        self.round = 1

        self._timer_value_waiting = data_json('CUENTA_REGRESIVA_INICIO')
        self.timer_waiting_room = QTimer()
        self.timer_waiting_room.setInterval(1000)
        self.timer_waiting_room.timeout.connect(self.actualize_waiting_timer)

        self._timer_value_round = data_json('CUENTA_REGRESIVA_RONDA')
        self.timer_round = QTimer()
        self.timer_round.setInterval(1000)
        self.timer_round.timeout.connect(self.actualize_round_timer)

        self.messager = Messager()

    @property
    def timer_value_waiting(self):
        return self._timer_value_waiting
    
    @timer_value_waiting.setter
    def timer_value_waiting(self, value):
        self._timer_value_waiting = max(0, value)

    @property
    def timer_value_round(self):
        return self._timer_value_round
    
    @timer_value_round.setter
    def timer_value_round(self, value):
        self._timer_value_round = max(0, value)

    @property
    def round_running(self):
        return self._round_running
    
    @round_running.setter
    def round_running(self, run: bool):
        # comenzar una ronda
        if not self.round_running and run:
            self.timer_round.start()
        # terminar una ronda
        elif self.round_running and not run:
            self.timer_round.stop()
            self.reset_round_timer()
        self._round_running = run

    # eliminar el nombre de un usuario que se ha desconectado
    def eliminate_user(self, id):
        self.players.pop(id, None)
        self.refresh_users()
        # si un usuario se desconecta durante un juego, el otro jugador gana automaticamente
        if self.game_running:
            remaining_player = list(self.players.values())[0]
            remaining_player.winner = True
            self.check_end_condition()

    # ejecutar la acción seleccionada y enviar una respuesta
    def handle_message(self, msg: dict, client_id: int):
        command = msg['command']
        match command:
            case 'validate_login':
                self.validate_login(msg['username'], client_id)
            case 'user_logout':
                self.eliminate_user(client_id)
            case 'handle_click_hand_card':
                self.select_hand_card(msg['id'], client_id)
            case 'confirm_card':
                self.confirm_selected_card(client_id)
            case 'chat_message':
                self.receive_chat_message(msg['content'], client_id)

    # actualizar el diccionario de jugadores
    def refresh_users(self):
        usernames = {}
        for player in self.players.values():
            usernames[player.id] = player.name
        msg = self.messager.refresh_users(usernames)
        self.sig_broadcast_message.emit(msg)

        # comenzar la cuenta regresiva
        if len(self.players) == 2:
            self.reset_waiting_timer()
            self.timer_waiting_room.start()
        
        # reinicialisar la cuenta regresiva
        else:
            self.reset_waiting_timer()
            if self.timer_waiting_room.isActive():
                self.timer_waiting_room.stop()

    # actualizar la cuenta regresiva para la sala de espera
    def actualize_waiting_timer(self):
        self.timer_value_waiting -= 1
        self.set_waiting_timer(self.timer_value_waiting)

        # si el tiempo de espera se acabó, empezar una ronda
        if self.timer_value_waiting == 0 and not self.game_running:
            self.timer_waiting_room.stop()
            self.reset_waiting_timer()
            self.initialize_game()
            self.set_user_names()
            msg = self.messager.start_game()
            self.sig_log_event.emit(
                'Comienza de Ronda',
                f"Comenzó una nueva ronda con los jugadores {[u for u in self.players.values()]}.")
            self.sig_broadcast_message.emit(msg)

    # cambiar el valor del timer que se muestra en la pantalla del usuario
    def set_waiting_timer(self, value: int):
        msg = self.messager.set_waiting_timer(value)
        self.sig_broadcast_message.emit(msg)

    # cambiar el valor de la cuenta regresiva a su valor inicial
    def reset_waiting_timer(self):
        self.timer_value_waiting = data_json('CUENTA_REGRESIVA_INICIO')
        self.set_waiting_timer(self.timer_value_waiting)

    # actualizar la cuenta regresiva para el juego
    def actualize_round_timer(self):
        self.timer_value_round -= 1
        self.set_round_timer(self.timer_value_round)
        # jugar cartas al azar si un jugador no ha seleccionado una carta
        if self.timer_value_round == 0:
            for player in self.players.values():
                if not player.active_card:
                    self.sig_log_event.emit(
                        'Tiempo se acabó',
                        f"El jugador {player.name} no jugó una carta a tiempo.")
                    player.select_card()
                    self.confirm_selected_card(player.id, mandatory=True)
            self.evaluate_round()
    
    # cambiar el valor del timer que se muestra en la pantalla del usuario
    def set_round_timer(self, value: int):
        msg = self.messager.set_round_timer(value)
        self.sig_broadcast_message.emit(msg)
        
    # cambiar el valor de la cuenta regresiva a su valor inicial
    def reset_round_timer(self):
        self.timer_value_round = data_json('CUENTA_REGRESIVA_RONDA')
        self.set_round_timer(self.timer_value_round)
    
    # validar el usuario elegido por el cliente
    def validate_login(self, username: str, client_id: int):
        errors = {'inv_len': False, 'not_alnum': False, 'occupied': False}
        full = False

        # controlar el usuario ingresado
        if (len(username) < data_json('USERNAME_LEN_MIN')
                or len(username) > data_json('USERNAME_LEN_MAX')):
            errors['inv_len'] = True
        if not username.isalnum():
            errors['not_alnum'] = True
        for player in self.players.values():
            if username.casefold() == player.name.casefold():
                errors['occupied'] = True

        # escribir un log si la entrada del usuario no era válida
        if True in errors.values():
            self.sig_log_event.emit(
                'Ingresa de Usuario',
                f'Cliente {client_id} ingresó el usuario "{username}". Entrada no válida.')
        else:
            self.sig_log_event.emit(
                'Ingresa de Usuario',
                f'Cliente {client_id} ingresó el usuario "{username}". Entrada válida.')
            # controlar si hay un cupo libre en la sala de espera
            full = not self.validate_availability(client_id)
        
        # si no hay errores, agregar el usuario al juego
        if True in errors.values():
            accepted = False
        else:
            accepted = True
            player = Player(username, client_id)
            self.players[client_id] = player
            self.refresh_users()
        msg = self.messager.validate_username(username, accepted, full, errors)
        self.sig_send_message_to_client.emit(msg, client_id)

    # validar si hay espacio libre en la sala de espera
    def validate_availability(self, client_id: int) -> bool:
        available = len(self.players) < 2
        if available:
            self.sig_log_event.emit(
                'Intento de Ingreso',
                f'Cliente {client_id} intentó entrar a la sala de espera. Hay espacio libre.')
        else:
            self.sig_log_event.emit(
                'Intento de Ingreso',
                f'Cliente {client_id} intentó entrar a la sala de espera. No hay espacio libre.')
        return available

    # inicializar una partida nueva
    def initialize_game(self):
        self.round = 0
        self.game_running = True
        # distribuir cartas a cada jugador y luego mostrarlos en la pantalla
        for player in self.players.values():
            player.reinitialize_for_game()
            self.refresh_hand_cards(player.id)
            self.refresh_opponent_cards(player.id, reveal_cards=False)
        self.refresh_victory_cards()
        self.refresh_active_cards()
        self.start_new_round()

    # cambiar los usuarios que se muestran en la pantalla del usuario
    def set_user_names(self):
        for client_id in self.players.keys():
            opponent_id = self.get_opponent_id(client_id)
            msg = self.messager.set_player_names(self.players[client_id].name,
                                                    self.players[opponent_id].name)
            self.sig_send_message_to_client.emit(msg, client_id)

    # actualizar las cartas del jugador
    def refresh_hand_cards(self, client_id):
        msg = self.messager.refresh_hand_cards(self.players[client_id].hand_cards)
        self.sig_send_message_to_client.emit(msg, client_id)

    # actualizar las cartas del oponente
    def refresh_opponent_cards(self, client_id, reveal_cards=False):
        opponent_id = self.get_opponent_id(client_id)
        opponent_cards = self.players[opponent_id].hand_cards
        msg = self.messager.refresh_opponent_cards(opponent_cards, reveal_cards)
        self.sig_send_message_to_client.emit(msg, client_id)

    # buscar y retornar el ID del oponente
    def get_opponent_id(self, client_id: int) -> int:
        for id in self.players.keys():
            if id != client_id:
                opponent_id = id
        return opponent_id
    
    # guardar la carta eligido por el usuario
    def select_hand_card(self, card_id: int, client_id: int):
        player = self.players[client_id]
        # solo seleccionar si el jugador ya no ha jugado una carta
        if not player.active_card:
            player.select_card(card_id)
            # marcar la carta seleccionada
            msg = self.messager.highlight_card(card_id)
            self.sig_send_message_to_client.emit(msg, client_id)

    # ugar la carta seleccionada de un jugador
    def confirm_selected_card(self, client_id, mandatory=False):
        player = self.players[client_id]
        player.confirm_selected_card()
        # enviar un log
        self.sig_log_event.emit(
            'Carta lanzada',
            f"El jugador {player.name} lanzó una carta del tipo {player.active_card['elemento']}.")
        # unhighlight la carta
        msg = self.messager.unhighlight_card()
        self.sig_send_message_to_client.emit(msg, client_id)
        # actualizar todas las cartas en el juego para el jugador y el oponente
        opponent_id = self.get_opponent_id(client_id)
        self.refresh_opponent_cards(opponent_id)
        self.refresh_hand_cards(client_id)
        self.refresh_active_cards()

        if not mandatory and all([player.active_card for player in self.players.values()]):
            self.evaluate_round()

    # enviar la informacion sobre la carta actual a los clientes
    def refresh_active_cards(self):
        for client_id in self.players.keys():
            opponent_id = self.get_opponent_id(client_id)
            player_card = self.players[client_id].active_card
            opponent_card = self.players[opponent_id].active_card
            msg = self.messager.refresh_active_cards(player_card, opponent_card)
            self.sig_send_message_to_client.emit(msg, client_id)

    # evaluar los resultados de una ronda finalizada
    def evaluate_round(self):
        self.round_running = False
        sleep(data_json('DELAY_EVALUATING'))
        ids = [player.id for player in self.players.values()]
        playerA = self.players[ids[0]]
        playerB = self.players[ids[1]]
        cardA = playerA.active_card
        cardB = playerB.active_card
        ganador = None

        # elementos iguales
        if cardA['elemento'] == cardB['elemento']:
            if cardA['puntos'] > cardB['puntos']:
                ganador = playerA
            elif cardB['puntos'] > cardA['puntos']:
                ganador = playerB
        # elementos diferentes
        else:
            match cardA['elemento']:
                case 'fuego':
                    match cardB['elemento']:
                        case 'nieve': ganador = playerA
                        case 'agua': ganador = playerB
                case 'nieve':
                    match cardB['elemento']:
                        case 'fuego': ganador = playerB
                        case 'agua': ganador = playerA
                case 'agua':
                    match cardB['elemento']:
                        case 'fuego': ganador = playerA
                        case 'nieve': ganador = playerB

        # ingresar el resultado para cada jugador y resetear sus valores
        for player in self.players.values():
            if player == ganador:
                player.gain_victory_card()
            else:
                player.take_active_card()

        if ganador:
            self.sig_log_event.emit(
                'Ronda terminada',
                f"Terminó la ronda. Ganador: {ganador.name}.")
        else:
            self.sig_log_event.emit(
                'Ronda terminada',
                f"Terminó la ronda. Empate, no hay ganador.")

        # comprobar si hay un ganador del juego o si la partida sigue
        ended = self.check_end_condition()
        if not ended:
            self.start_new_round()
        else:
            self.sig_log_event.emit(
                'Juego terminado',
                f"{ganador.name} ganó el juego")
    
    # comenzar una ronda nueva con los mismos jugadores
    def start_new_round(self):
        self.round_running = True
        # cada jugador saca nuevas cartas
        for player in self.players.values():
            player.reinitialize_for_round()
            # actualizar los cartas en la pantalla
            opponent_id = self.get_opponent_id(player.id)
            self.refresh_hand_cards(player.id)
            self.refresh_opponent_cards(opponent_id)
            
        self.refresh_victory_cards()
        self.refresh_active_cards()

        # actualizar contador de rondas
        self.round += 1
        msg = self.messager.refresh_round_counter(self.round)
        self.sig_broadcast_message.emit(msg)

    # desplicar las cartas de victoria de cada jugador
    def refresh_victory_cards(self):
        # send a message to each client
        for client_id in self.players.keys():
            opponent_id = self.get_opponent_id(client_id)
            player_cards = self.players[client_id].victory_cards
            opponent_cards = self.players[opponent_id].victory_cards
            msg = self.messager.refresh_victory_cards(player_cards, opponent_cards)
            self.sig_send_message_to_client.emit(msg, client_id)

    # comprobar si el juego termina
    def check_end_condition(self) -> bool:
        # no hay ganador
        if not True in [player.winner for player in self.players.values()]:
            return False
        # hay ganador, terminar el juego
        else:
            self.round_running = False
            self.game_running = False
            # notificar los usuarios sobre el fin del juego
            for player in self.players.values():
                msg = self.messager.show_end_window(player.winner)
                self.sig_send_message_to_client.emit(msg, player.id)
            # eliminar todos los usuarios del juego
            for player in self.players.copy().values():
                self.eliminate_user(player.id)
            return True

    # recibir y distribuir un mensaje en el chat
    def receive_chat_message(self, content: str, client_id: int):
        name = self.players[client_id].name
        msg = self.messager.send_chat_message(content, name)
        self.sig_broadcast_message.emit(msg)