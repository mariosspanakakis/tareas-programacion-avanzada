from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont

import parametros as p


# clase que contiene a todas las funcionalidades para manejar las items que se ofrecen en la tienda
class TiendaItem(QLabel):

    clicked = pyqtSignal(str)

    def __init__(self, item, imagen, costo, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font = QFont(p.FONT, 16)
        self.font.setCapitalization(QFont.SmallCaps)

        self.item = item
        self.logo = QPixmap(imagen).scaled(p.IMAGEN_TIENDA, p.IMAGEN_TIENDA, Qt.KeepAspectRatio)
        self.setPixmap(self.logo)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(p.STYLESHEET_LABEL)

        self.label_costo = QLabel(str(costo), self)
        self.label_costo.setAlignment(Qt.AlignCenter)
        self.label_costo.setFont(self.font)
        self.label_costo.setStyleSheet(p.STYLESHEET_CONTENIDO)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item)