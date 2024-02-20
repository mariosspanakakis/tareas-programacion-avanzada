from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QScrollArea
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

from utils import data_json


class ChatWindow(QWidget):

    sig_send_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('DCChat')
        self.generate_gui()

        self.labels_messages = []
    
    def generate_gui(self):
        self.edt_message = QLineEdit(self)
        self.edt_message.setAlignment(Qt.AlignLeft)
        self.btn_send = QPushButton('Enviar', self)
        self.btn_send.clicked.connect(self.send_message)

        hbox_message = QHBoxLayout()
        hbox_message.addWidget(self.edt_message)
        hbox_message.addWidget(self.btn_send)

        self.widget = QWidget(self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.widget)

        self.chat_vbox = QVBoxLayout()
        self.chat_vbox.addStretch(1)
        self.widget.setLayout(self.chat_vbox)

        vbox = QVBoxLayout()
        vbox.addWidget(self.scroll_area)
        vbox.addLayout(hbox_message)

        self.setLayout(vbox)

    # vaciar y mostrar la ventana del chat
    def show_window(self):
        for label in self.labels_messages:
            label.clear()
        self.show()

    # anadir un mensaje al chat
    def add_message(self, msg: str, sender: str):
        label = QLabel(sender + ':\n' + msg, self)
        label.setWordWrap(True)
        label.setStyleSheet(data_json('STYLE_CHAT_MESSAGE'))
        self.chat_vbox.insertWidget(self.chat_vbox.count()-1, label)
        self.labels_messages.append(label)
        self.scroll_area.ensureWidgetVisible(label)

    # enviar un mensaje al servidor
    def send_message(self):
        msg = self.edt_message.text()
        self.edt_message.clear()
        if msg != '':
            self.sig_send_message.emit(msg)

    # enviar un mensaje usando 'Enter'
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.send_message()