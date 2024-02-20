from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from utils import data_json


class WaitingWindow(QWidget):

    sig_send_logout = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = data_json('WINDOW_W_S')
        self.height = data_json('WINDOW_H_S')
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Sala de Espera')
        self.notification = QMessageBox(self)
        self.generate_gui()
    
    def generate_gui(self):
        self.btn_volver = QPushButton('Volver', self)
        self.btn_volver.clicked.connect(self.send_logout)

        self.lbl_timer = QLabel('10', self)
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        self.lbl_user_1 = QLabel('User 1', self)
        self.lbl_user_1.setAlignment(Qt.AlignCenter)
        self.lbl_user_2 = QLabel('User 2', self)
        self.lbl_user_2.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(self.lbl_user_1)
        hbox.addWidget(self.lbl_user_2)

        vbox.addStretch(1)
        vbox.addWidget(self.lbl_timer)
        vbox.addLayout(hbox)
        vbox.addWidget(self.btn_volver)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def send_logout(self):
        self.sig_send_logout.emit()

    # desplicar los usuarios que estan esperando
    def refresh_users(self, usernames: dict):
        users = list(usernames.values())
        if len(usernames) == 1:
            self.lbl_user_1.setText(users[0])
            self.lbl_user_2.setText('...')
            self.lbl_timer.setText('Esperando otro jugador...')
        elif len(usernames) == 2:
            self.lbl_user_1.setText(users[0])
            self.lbl_user_2.setText(users[1])

    # actualizar el contador del tiempo
    def refresh_timer(self, time: int):
        self.lbl_timer.setText(str(time))

    def show_window(self):
        self.show()

    def show_error(self, title, msg):
        self.notification.about(self, title, msg)