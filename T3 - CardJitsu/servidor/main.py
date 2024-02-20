import sys
from PyQt5.QtWidgets import QApplication
from servidor import Server
from logic import Logic
from utils import data_json

if __name__ == "__main__":
    host = data_json("HOST")
    port = data_json("PORT")

    try:
        app = QApplication(sys.argv)
        server = Server(port, host)
        logic = Logic()

        logic.sig_log_event.connect(
            server.log)
        server.sig_handle_message.connect(
            logic.handle_message)
        logic.sig_send_message_to_client.connect(
            server.send_message)
        logic.sig_broadcast_message.connect(
            server.broadcast_message)
        server.sig_eliminate_user.connect(
            logic.eliminate_user)

        print("Presione [Esc] -> [Ctrl] + [C] para cerrar el servidor.")
        while True:
            input()
    
    except KeyboardInterrupt:
        server.socket_server.close()
        app.exit()
        sys.exit()