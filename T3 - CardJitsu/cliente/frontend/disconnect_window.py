from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from utils import data_json


class DisconnectWindow(QWidget):

    sig_quit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = data_json('WINDOW_W_S')
        self.height = data_json('WINDOW_H_S')
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Desconectado')
        self.generate_gui()
    
    def generate_gui(self):
        self.lbl_text = QLabel('El servidor se ha desconectado.', self)
        self.lbl_text.setAlignment(Qt.AlignCenter)
        self.btn_quit = QPushButton('Salir', self)
        self.btn_quit.clicked.connect(self.quit_application)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.lbl_text)
        vbox.addWidget(self.btn_quit)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def quit_application(self):
        self.sig_quit.emit()