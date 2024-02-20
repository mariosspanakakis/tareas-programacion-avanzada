from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QRadioButton, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont

import parametros as p


class VentanaPrincipal(QWidget):

    sig_validar_seleccion = pyqtSignal(str, bool, bool)
    sig_tocar_musica = pyqtSignal(bool) # play

    def __init__(self):
        super().__init__()
        self.width = p.VENTANA_PRINCIPAL_W
        self.height = p.VENTANA_PRINCIPAL_H
        self.setGeometry(600, 200, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Setup')
        self.notificacion = QMessageBox(self)
        self.crear_elementos_graficos()

    def crear_elementos_graficos(self):
        # fonts
        self.font_titulo = QFont(p.FONT, 22)
        self.font_titulo.setCapitalization(QFont.SmallCaps)
        self.font_opciones = QFont(p.FONT, 16)
        self.font_opciones.setCapitalization(QFont.SmallCaps)
        # imagen del fondo
        self.lbl_fondo = QLabel(self)
        self.lbl_fondo.setPixmap(QPixmap(p.FONDO_INICIAL))
        self.lbl_fondo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_fondo.setScaledContents(True)
        self.lbl_fondo.setGeometry(0, 0, self.width, self.height)
        # titulo
        self.lbl_titulo = QLabel('Ambiente del Juego', self)
        self.lbl_titulo.setFont(self.font_titulo)
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet(p.STYLESHEET_TITULO)
        # mapa 1
        self.lbl_lvl_1 = QLabel(self)
        self.lbl_lvl_1.setPixmap(QPixmap(p.MAPA_ABUELA))
        self.lbl_lvl_1.setAlignment(Qt.AlignCenter)
        self.lbl_lvl_1.setStyleSheet(p.STYLESHEET_MAPA)
        self.btn_lvl_1 = QRadioButton('Jardin de la Abuela', self)
        self.btn_lvl_1.setFont(self.font_opciones)
        self.btn_lvl_1.setStyleSheet(p.STYLESHEET_BUTTON)
        self.vbox_1 = QVBoxLayout()
        self.vbox_1.addWidget(self.lbl_lvl_1)
        self.vbox_1.addWidget(self.btn_lvl_1)
        # mapa 2
        self.lbl_lvl_2 = QLabel(self)
        self.lbl_lvl_2.setPixmap(QPixmap(p.MAPA_NOCTURNA))
        self.lbl_lvl_2.setAlignment(Qt.AlignCenter)
        self.lbl_lvl_2.setStyleSheet(p.STYLESHEET_MAPA)
        self.btn_lvl_2 = QRadioButton('Salida Nocturna', self)
        self.btn_lvl_2.setFont(self.font_opciones)
        self.btn_lvl_2.setStyleSheet(p.STYLESHEET_BUTTON)
        self.vbox_2 = QVBoxLayout()
        self.vbox_2.addWidget(self.lbl_lvl_2)
        self.vbox_2.addWidget(self.btn_lvl_2)
        # empezar juego
        self.btn_start = QPushButton('Jugar', self)
        self.btn_start.setStyleSheet(p.STYLESHEET_BUTTON)
        self.btn_start.setFont(self.font_opciones)
        self.btn_start.clicked.connect(self.comenzar_juego)
        # layouts para los mapas
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox_1)
        self.hbox.addLayout(self.vbox_2)
        # layout principal
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.lbl_titulo)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.btn_start)

        self.setLayout(self.vbox)

    def comenzar_juego(self):
        self.sig_validar_seleccion.emit(self.usuario,
                                        self.btn_lvl_1.isChecked(),
                                        self.btn_lvl_2.isChecked())

    def recibir_validacion(self, valido, mapa):
        if valido:
            self.hide()
            self.sig_tocar_musica.emit(False)
        else:
            mensaje = 'Elige una mapa para comenzar!'
            self.notificacion.about(self, 'Entrada no válida', mensaje)

    def mostrar_ventana(self, usuario):
        self.show()
        self.sig_tocar_musica.emit(True)
        self.usuario = usuario