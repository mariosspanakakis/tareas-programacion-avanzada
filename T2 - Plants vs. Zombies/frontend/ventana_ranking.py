from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont

import parametros as p


class VentanaRanking(QWidget):

    sig_consultar_ranking = pyqtSignal()
    sig_volver = pyqtSignal()
    sig_tocar_musica = pyqtSignal(bool) # play

    def __init__(self):
        super().__init__()
        self.width = p.VENTANA_RANKING_W
        self.height = p.VENTANA_RANKING_H
        self.setGeometry(600, 200, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Ranking')
        self.notificacion = QMessageBox(self)
        self.crear_elementos_graficos()

    def crear_elementos_graficos(self):
        # fonts
        self.font_titulo = QFont(p.FONT, 22)
        self.font_titulo.setCapitalization(QFont.SmallCaps)
        self.font_ranking = QFont(p.FONT, 16)
        self.font_ranking.setCapitalization(QFont.SmallCaps)
        # imagen del fondo
        self.lbl_fondo = QLabel(self)
        self.lbl_fondo.setPixmap(QPixmap(p.FONDO_INICIAL))
        self.lbl_fondo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_fondo.setScaledContents(True)
        self.lbl_fondo.setGeometry(0, 0, self.width, self.height)
        # titulo
        self.lbl_titulo = QLabel('Ranking de Puntajes', self)
        self.lbl_titulo.setFont(self.font_titulo)
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet(p.STYLESHEET_TITULO)
        # boton para volver
        self.btn_volver = QPushButton('Menú de Inicio', self)
        self.btn_volver.setStyleSheet(p.STYLESHEET_BUTTON)
        self.btn_volver.clicked.connect(self.volver_al_inicio)

        # ranking
        self.labels_nombre = {
            i: QLabel('', self) for i in range(p.N_PLACAMIENTOS_RANKING)
        }
        self.labels_puntaje = {
            i: QLabel('', self) for i in range(p.N_PLACAMIENTOS_RANKING)
        }
        for i in range(p.N_PLACAMIENTOS_RANKING):
            self.labels_nombre[i].setFont(self.font_ranking)
            self.labels_nombre[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.labels_nombre[i].setStyleSheet(p.STYLESHEET_RANKING)
            self.labels_puntaje[i].setFont(self.font_ranking)
            self.labels_puntaje[i].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.labels_puntaje[i].setStyleSheet(p.STYLESHEET_RANKING)

        self.hboxes = []
        for i in range(p.N_PLACAMIENTOS_RANKING):
            hbox = QHBoxLayout()
            hbox.addWidget(self.labels_nombre[i])
            hbox.addSpacing(40)
            hbox.addWidget(self.labels_puntaje[i])
            self.hboxes.append(hbox)

        # layouts
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.lbl_titulo)
        for hbox in self.hboxes:
            self.vbox.addLayout(hbox)
        self.vbox.addWidget(self.btn_volver)
        self.setLayout(self.vbox)
    
    def mostrar_ranking(self, rankings: list):
        for i in range(len(rankings)):
            self.labels_nombre[i].setText(rankings[i][1])
            self.labels_puntaje[i].setText(str(rankings[i][0]))

    def mostrar_ventana(self):
        self.sig_consultar_ranking.emit()
        self.show()
        self.sig_tocar_musica.emit(True)

    def volver_al_inicio(self):
        self.close()
        self.sig_tocar_musica.emit(False)
        self.sig_volver.emit()