from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication


class Interface(QObject):

    sig_send_message_to_server = pyqtSignal(dict)
    sig_login_refused = pyqtSignal(dict)

    sig_refresh_users = pyqtSignal(dict)
    sig_refresh_waiting_timer = pyqtSignal(int)
    sig_refresh_hand_cards = pyqtSignal(dict)
    sig_refresh_opponent_cards = pyqtSignal(dict, bool)
    sig_highlight_card = pyqtSignal(int)
    sig_refresh_active_cards = pyqtSignal(list)
    sig_set_user_names = pyqtSignal(list)
    sig_refresh_victory_cards = pyqtSignal(list)
    sig_refresh_round = pyqtSignal(int)
    sig_refresh_round_timer = pyqtSignal(int)
    sig_show_chat_message = pyqtSignal(str, str)

    sig_show_initial_window = pyqtSignal()
    sig_show_waiting_window = pyqtSignal()
    sig_show_game_window = pyqtSignal()
    sig_show_end_window = pyqtSignal(bool)
    sig_show_disconnect_window = pyqtSignal()

    def __init__(self, application: QApplication):
        super().__init__()
        self.application = application

    # manejar mensajes recibidos del servidor
    def handle_message(self, msg: dict):
        command = msg['command']
        match command:
            case 'respond_validation_login':
                if not msg['accepted']:
                    self.sig_login_refused.emit(msg['errors'])
                else:
                    self.sig_show_waiting_window.emit()
            case 'refresh_users':
                self.sig_refresh_users.emit(msg['users'])
            case 'set_waiting_timer':
                self.sig_refresh_waiting_timer.emit(msg['timer_value'])
            case 'start_game':
                self.sig_show_game_window.emit()
            case 'refresh_hand_cards':
                self.sig_refresh_hand_cards.emit(msg['hand_cards'])
            case 'refresh_opponent_cards':
                self.sig_refresh_opponent_cards.emit(msg['opponent_cards'], msg['reveal'])
            case 'highlight_card':
                self.sig_highlight_card.emit(msg['card_id'])
            case 'refresh_active_cards':
                self.sig_refresh_active_cards.emit(msg['active_cards'])
            case 'set_user_names':
                self.sig_set_user_names.emit(msg['user_names'])
            case 'refresh_victory_cards':
                self.sig_refresh_victory_cards.emit(msg['victory_cards'])
            case 'refresh_round':
                self.sig_refresh_round.emit(msg['round'])
            case 'set_round_timer':
                self.sig_refresh_round_timer.emit(msg['timer_value'])
            case 'show_end_window':
                self.sig_show_end_window.emit(msg['winner'])
            case 'show_chat_message':
                self.sig_show_chat_message.emit(msg['sender'], msg['content'])

    # manejar el login de un usuario, recibido de una ventana
    def handle_user_login(self, username: str):
        msg = {
            'command': 'validate_login',
            'username': username
        }
        self.sig_send_message_to_server.emit(msg)
    
    # manejar la salida de un usuario
    def handle_user_logout(self):
        msg = {
            'command': 'user_logout'
        }
        self.sig_send_message_to_server.emit(msg)
        self.sig_show_initial_window.emit()

    # manejar un clic a una carta
    def handle_click_hand_card(self, id: int):
        msg = {
            'command': 'handle_click_hand_card',
            'id': id
        }
        self.sig_send_message_to_server.emit(msg)
    
    # manejar la confirmación de una carta
    def handle_click_confirm(self):
        msg = {
            'command': 'confirm_card'
        }
        self.sig_send_message_to_server.emit(msg)

    # manejar la disconección del servidor
    def handle_server_disconnect(self):
        self.sig_show_disconnect_window.emit()

    # manejar un mensaje nuevo en el chat
    def handle_chat_message(self, content: str):
        msg = {
            'command': 'chat_message',
            'content': content
        }
        self.sig_send_message_to_server.emit(msg)