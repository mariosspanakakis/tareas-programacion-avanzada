# clase que implementa todos los mensajes que se envían del servidor al cliente
class Messager:

    def __init__(self):
        pass

    # preparar el mensaje para la validación del usuario con flags de errores
    def validate_username(self, username: str, accepted: bool, full: bool, errors: dict) -> dict:
        msg = {
            'command': 'respond_validation_login',
            'accepted': accepted,
            'name': username,
            'errors': {
                'full': full,
                'invalid_length': errors['inv_len'],
                'not_alphanumeric': errors['not_alnum'],
                'occupied': errors['occupied']
            }
        }
        return msg

    # actualizar la lista de usuarios en la sala de espera
    def refresh_users(self, usernames: list) -> dict:
        msg = {
            'command': 'refresh_users',
            'users': usernames
        }
        return msg
    
    # actualizar los nombres de los jugadores en el juego
    def set_player_names(self, player_name, opponent_name) -> dict:
        msg = {
                'command': 'set_user_names',
                'user_names': [player_name, opponent_name]
            }
        return msg

    # comenzar un juego nuevo
    def start_game(self) -> dict:
        msg = {
            'command': 'start_game'
        }
        return msg

    # desplicar un valor nuevo en la cuenta regresiva de la sala de espera
    def set_waiting_timer(self, value: int) -> dict:
        msg = {
            'command': 'set_waiting_timer',
            'timer_value': value
        }
        return msg

    # desplicar un valor nuevo en la cuenta regresiva del juego
    def set_round_timer(self, value: int) -> dict:
        msg = {
            'command': 'set_round_timer',
            'timer_value': value
        }
        return msg

    # actualizar las cartas del mano del jugador
    def refresh_hand_cards(self, hand_cards: dict) -> dict:
        msg = {
            'command': 'refresh_hand_cards',
            'hand_cards': hand_cards
        }
        return msg

    # actualizar las cartas del mano del oponente
    def refresh_opponent_cards(self, opponent_cards: dict, reveal: bool) -> dict:
        msg = {
            'command': 'refresh_opponent_cards',
            'opponent_cards': opponent_cards,
            'reveal': reveal
        }
        return msg
    
    # actualizar las cartas activas en el juego
    def refresh_active_cards(self, player_card: dict, opponent_card: dict):
        msg = {
            'command': 'refresh_active_cards',
            'active_cards': [player_card, opponent_card]
        }
        return msg

    def refresh_victory_cards(self, player_card: dict, opponent_card: dict) -> dict:
        msg = {
            'command': 'refresh_victory_cards',
            'victory_cards': [player_card, opponent_card]
        }
        return msg

    # marcar la carta seleccionada por un usuario
    def highlight_card(self, card_id: int) -> dict:
        msg = {
            'command': 'highlight_card',
            'card_id': card_id
        }
        return msg

    # desmarcar todas las cartas de un usuario
    def unhighlight_card(self) -> dict:
        msg = {
            'command': 'highlight_card',
            'card_id': -1
        }
        return msg

    # actualizar el contador de rondas
    def refresh_round_counter(self, value: int) -> dict:
        msg = {
            'command': 'refresh_round',
            'round': value
        }
        return msg

    # mostrar la ventana terminál
    def show_end_window(self, winner: bool) -> dict:
        msg = {
            'command': 'show_end_window',
            'winner': winner
        }
        return msg

    # enviar una mensaje en el chat
    def send_chat_message(self, sender: str, content: str) -> dict:
        msg = {
            'command': 'show_chat_message',
            'sender': sender,
            'content': content
        }
        return msg