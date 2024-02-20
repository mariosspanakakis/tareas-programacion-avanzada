from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from utils import data_json


class InitialWindow(QWidget):

    sig_send_login = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.width = data_json('WINDOW_W_S')
        self.height = data_json('WINDOW_H_S')
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Ventana Inicial')
        self.notification = QMessageBox(self)
        self.generate_gui()
    
    def generate_gui(self):
        self.edt_username = QLineEdit(self)
        self.edt_username.setAlignment(Qt.AlignCenter)
        self.edt_username.setPlaceholderText('Ingresa su nombre')

        self.btn_login = QPushButton('Login', self)
        self.btn_login.clicked.connect(self.send_login)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.edt_username)
        vbox.addWidget(self.btn_login)
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.show()

    # enviar el mensaje del login
    def send_login(self):
        self.sig_send_login.emit(self.edt_username.text())

    # desplicar el mensaje de error, si el usuario no cumple los requisitos
    def show_login_refused(self, errors: dict):
        if errors['full']:
            title = 'No espacio libre'
            msg = f'No hay espacio libre en el juego.\n'
            msg += f'Espera a que un jugador abandone el juego.'
        else:
            title = 'Usuario inválido'
            msg = ''
            if errors['invalid_length']:
                msg += f'El largo del usuario no es válido.\n'
            if errors['not_alphanumeric']:
                msg += f'El usuario debe ser alfanumérico.\n'
            if errors['occupied']:
                msg += f'El usuario ya se usa.\n'
        self.show_error(title, msg)

    def show_window(self):
        self.show()

    def show_error(self, title, msg):
        self.notification.about(self, title, msg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_login()