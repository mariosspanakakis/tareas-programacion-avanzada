from PyQt5.QtCore import pyqtSignal, QObject
import socket
import threading
import json
from cripto import encriptar, desencriptar


class Client(QObject):

    sig_handle_message = pyqtSignal(dict)
    sig_server_disconnect = pyqtSignal()

    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.init_client()

    # iniciar los funciones básicos del cliente
    def init_client(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.start_listening()

        except ConnectionError as error:
            self.notify_error(
                title='Conexión terminada',
                msg='Se ha terminada la conexión al servidor.',
                error=error
            )
            self.client_socket.close()
            exit()

    # empezar escuchando al servidor
    def start_listening(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    # escuchar constantemente al servidor
    def listen_thread(self):
        try:
            while True:
                msg = self.receive_message()
                if msg:
                    self.sig_handle_message.emit(msg)
        except ConnectionError as error:
            self.notify_error(
                title='Servidor desconectado',
                msg='El servidor se ha desconectado.',
                error=error
            )
            self.sig_server_disconnect.emit()

    # enviar un mensaje al servidor
    def send_message(self, msg: dict):
        # codificar y luego encriptar el mensaje
        msg_bytes = self.encode_message(msg_dict=msg)
        msg_enc = encriptar(msg_bytes)

        # calcular el largo de la mensaje
        msg_length = len(msg_enc)
        msg_length_bytes = msg_length.to_bytes(4, byteorder='big')

        msg_bytes = bytearray()
        msg_bytes.extend(msg_length_bytes)
        
        # separar el mensaje en bloques de 32 bytes
        bytes_packaged = 0
        counter = 0
        while bytes_packaged < msg_length:
            blocksize = min(32, msg_length - bytes_packaged)
            block = msg_enc[bytes_packaged:bytes_packaged + blocksize]
            msg_bytes.extend(counter.to_bytes(4, 'little'))
            msg_bytes.extend(bytes(block))
            counter += 1
            bytes_packaged += blocksize
        self.client_socket.sendall(msg_bytes)

    # recibir un mensaje del servidor
    def receive_message(self):
        response_bytes_length = self.client_socket.recv(4)
        response_length = int.from_bytes(response_bytes_length, byteorder='big')
        
        # leer el mensaje del cliente
        response_enc = bytearray()
        while len(response_enc) < response_length:
            block_number_bytes = self.client_socket.recv(4)
            block_number = int.from_bytes(block_number_bytes, byteorder='little')
            read_length = min(32, response_length - len(response_enc))
            response_enc.extend(self.client_socket.recv(read_length))

        response = desencriptar(response_enc)
        msg = self.decode_message(msg_bytes=response)
        return msg

    # codificar un diccionario para enviarlo al servidor
    def encode_message(self, msg_dict: dict) -> bytearray:
        try:
            msg_json = json.dumps(msg_dict)
            msg_bytes = msg_json.encode()
            return msg_bytes
        except json.JSONDecodeError as error:
            self.notify_error(
                title='Codificación',
                msg='No se pudo codificar el mensaje.',
                error=error
            )
            return b''

    # descodificar un diccionario recibido
    def decode_message(self, msg_bytes: bytes) -> dict:
        try:
            msg = json.loads(msg_bytes)
            return msg
        except json.JSONDecodeError as error:
            self.notify_error(
                title='Decodificación',
                msg='No se pudo decodificar el mensaje.',
                error=error
            )
            return {}

    # enviar un mensaje en el terminal
    def notify_error(self, title: str, msg: str, error):
        print(f"\n[ERROR] {title} ({error})")
        print(f"{msg}")