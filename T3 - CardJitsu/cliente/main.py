import sys
from PyQt5.QtWidgets import QApplication
from utils import data_json

from backend.cliente import Client
from backend.interface import Interface
from frontend.initial_window import InitialWindow
from frontend.waiting_window import WaitingWindow
from frontend.game_window import GameWindow
from frontend.end_window import EndWindow
from frontend.disconnect_window import DisconnectWindow
from frontend.chat_window import ChatWindow

if __name__ == "__main__":
    host = data_json("HOST")
    port = data_json("PORT")

    try:
        app = QApplication(sys.argv)

        client = Client(port, host)
        interface = Interface(app)

        initial_window = InitialWindow()
        waiting_window = WaitingWindow()
        game_window = GameWindow()
        end_window = EndWindow()
        disconnect_window = DisconnectWindow()
        chat_window = ChatWindow()

        # conectar señales del interfaz
        client.sig_handle_message.connect(
            interface.handle_message)
        interface.sig_send_message_to_server.connect(
            client.send_message)
        client.sig_server_disconnect.connect(
            interface.handle_server_disconnect)
        interface.sig_show_disconnect_window.connect(
            disconnect_window.show)
        interface.sig_show_disconnect_window.connect(
            initial_window.hide)
        interface.sig_show_disconnect_window.connect(
            waiting_window.hide)
        interface.sig_show_disconnect_window.connect(
            game_window.hide)
        interface.sig_show_disconnect_window.connect(
            end_window.hide)

        # conectar señales de la ventana inicial
        # frontend -> backend
        initial_window.sig_send_login.connect(
            interface.handle_user_login)
        # backend -> frontend
        interface.sig_show_initial_window.connect(
            initial_window.show_window)
        interface.sig_show_initial_window.connect(
            waiting_window.hide)
        interface.sig_login_refused.connect(
            initial_window.show_login_refused)
        
        # conectar señales de la ventana de espera
        # frontend -> backend
        waiting_window.sig_send_logout.connect(
            interface.handle_user_logout)
        # backend -> frontend
        interface.sig_show_waiting_window.connect(
            waiting_window.show_window)
        interface.sig_show_waiting_window.connect(
            initial_window.hide)
        interface.sig_refresh_users.connect(
            waiting_window.refresh_users)
        interface.sig_refresh_waiting_timer.connect(
            waiting_window.refresh_timer)

        # conectar señales de la ventana del juego
        # backend -> frontend
        interface.sig_show_game_window.connect(
            game_window.show)
        interface.sig_show_game_window.connect(
            chat_window.show_window)
        interface.sig_show_game_window.connect(
            waiting_window.hide)
        interface.sig_refresh_hand_cards.connect(
            game_window.refresh_hand_cards)
        interface.sig_refresh_opponent_cards.connect(
            game_window.refresh_opponent_cards)
        interface.sig_highlight_card.connect(
            game_window.highlight_hand_card)
        interface.sig_refresh_active_cards.connect(
            game_window.refresh_active_cards)
        interface.sig_set_user_names.connect(
            game_window.set_user_names)
        interface.sig_refresh_victory_cards.connect(
            game_window.refresh_victory_cards)
        interface.sig_refresh_round.connect(
            game_window.refresh_round)
        interface.sig_refresh_round_timer.connect(
            game_window.refresh_timer)
        # frontend -> backend
        game_window.sig_click_hand_card.connect(
            interface.handle_click_hand_card)
        game_window.sig_confirm_card.connect(
            interface.handle_click_confirm)

        # conectar señales de la ventana terminál
        # backend -> frontend
        interface.sig_show_end_window.connect(
            end_window.show_window)
        interface.sig_show_end_window.connect(
            game_window.hide_window)
        interface.sig_show_end_window.connect(
            chat_window.hide)
        # frontend -> backend
        end_window.sig_return.connect(
            initial_window.show)

        # manejar desconexión
        disconnect_window.sig_quit.connect(
            app.quit)

        # manejar chat
        chat_window.sig_send_message.connect(
            interface.handle_chat_message)
        interface.sig_show_chat_message.connect(
            chat_window.add_message)
        game_window.sig_closed.connect(
            app.closeAllWindows)

        sys.exit(app.exec_())

    except ConnectionError as error:
        print(f"Ocurrió un error: {error}")
    except KeyboardInterrupt:
        print(f"\nCerrando cliente...")
        sys.exit()