from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from utils import data_json


class EndWindow(QWidget):

    sig_return = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = data_json('WINDOW_W_S')
        self.height = data_json('WINDOW_H_S')
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Ventana Terminál')
        self.notification = QMessageBox(self)
        self.generate_gui()
    
    def generate_gui(self):
        self.lbl_text = QLabel('', self)
        self.lbl_text.setAlignment(Qt.AlignCenter)
        self.btn_return = QPushButton('Volver', self)
        self.btn_return.clicked.connect(self.return_to_initial_window)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.lbl_text)
        vbox.addWidget(self.btn_return)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def return_to_initial_window(self):
        self.sig_return.emit()
        self.hide()

    def show_window(self, winner: bool):
        if winner:
            self.lbl_text.setText('¡Felicidades, has ganado!')
        else:
            self.lbl_text.setText('Que pena, tu perdiste...')
        self.show()

    def show_error(self, title, msg):
        self.notification.about(self, title, msg)