import socket
import threading
import json
from PyQt5.QtCore import QObject, pyqtSignal
from cripto import encriptar, desencriptar


class Server(QObject):

    sig_handle_message = pyqtSignal(dict, int) # msg, client_id
    sig_eliminate_user = pyqtSignal(int) # client_id

    def __init__(self, port, host):
        super().__init__()
        self.host = host
        self.port = port
        self.socket_server = None

        self.client_id = 0
        self.sockets = {}

        self.initialize_server()

    # inicialisar los funciones básicos del servidor
    def initialize_server(self):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        self.start_accepting_connections()

    # empezar buscando para clientes
    def start_accepting_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    # buscar y aceptar conexiones con clientes
    def accept_connections_thread(self):
        # para cada nuevo cliente, iniciar un thread para manejar su socket
        try:
            while True:
                client_socket, _ = self.socket_server.accept()
                listening_client_thread = threading.Thread(
                    target=self.listen_client_thread,
                    args=(client_socket, self.client_id, ),
                    daemon=True)
                listening_client_thread.start()
                self.sockets[self.client_id] = client_socket
                self.log(
                    title=f'Cliente',
                    msg=f'Se conectó un nuevo cliente con id {self.client_id}.'
                )
                self.client_id += 1
        except ConnectionError as error:
            self.notify_error(
                title='Cliente',
                msg='Error en la comunicación con un cliente',
                error=error
            )

    # escuchar a las mensajes de un cliente específico
    def listen_client_thread(self, client_socket, client_id):
        try:
            while True:
                msg = self.receive_message(client_socket)
                if msg != "":
                    self.sig_handle_message.emit(msg, client_id)
        except ConnectionError as error:
            self.log(
                    title=f'Cliente',
                    msg=f'Se desconectó el cliente con id {client_id}.'
                )
            self.eliminate_client(client_id, client_socket)
    
    # recibir un mensaje de un cliente
    def receive_message(self, client_socket) -> dict:
        response_bytes_length = client_socket.recv(4)
        response_length = int.from_bytes(response_bytes_length, byteorder='big')
        
        # leer el mensaje del cliente
        response_enc = bytearray()
        while len(response_enc) < response_length:
            block_number_bytes = client_socket.recv(4)
            block_number = int.from_bytes(block_number_bytes, byteorder='little')
            read_length = min(32, response_length - len(response_enc))
            response_enc.extend(client_socket.recv(read_length))

        response = desencriptar(response_enc)
        msg = self.decode_message(msg_bytes=response)
        return msg

    # enviar un mensaje a un cliente
    def send_message(self, msg, client_id):
        socket = self.sockets[client_id]
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
        socket.sendall(msg_bytes)

    # enviar un mensaje a todos los clientes conectados
    def broadcast_message(self, msg: dict):
        for id in self.sockets.keys():
            self.send_message(msg, id)

    # cuando un cliente se desconectó, cerra su socket y eliminalo de los usuarios activos
    def eliminate_client(self, client_id, client_socket):
        try:
            client_socket.close()
            self.sockets.pop(client_id, None)
            self.sig_eliminate_user.emit(client_id)
        except KeyError as error:
            self.notify_error(
                title='Cliente inexistente',
                msg=f'No existe cliente con ID {client_id}.',
                error=error
            )

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

    # escribir un mensaje de log en la consola
    def log(self, title: str, msg: str):
        print(f"\n[LOG] {title}")
        print(f"{msg}")

    # notificar el usuario sobre un error mediante la consola
    def notify_error(self, title: str, msg: str, error):
        print(f"\n[ERROR] {title} ({error})")
        print(f"{msg}")