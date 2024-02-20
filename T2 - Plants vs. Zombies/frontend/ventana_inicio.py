from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont

import parametros as p


class VentanaInicio(QWidget):

    sig_enviar_login = pyqtSignal(str)
    sig_mostrar_ranking = pyqtSignal()
    sig_salir = pyqtSignal()
    sig_tocar_musica = pyqtSignal(bool) # play

    def __init__(self):
        super().__init__()
        self.width = p.VENTANA_INICIO_W
        self.height = p.VENTANA_INICIO_H
        self.setGeometry(600, 200, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Inicio')
        self.notificacion = QMessageBox(self)
        self.crear_elementos_graficos()
    
    def crear_elementos_graficos(self):
        # fonts
        self.font_opciones = QFont(p.FONT, 16)
        self.font_opciones.setCapitalization(QFont.SmallCaps)

        # imagen del fondo
        self.lbl_fondo = QLabel(self)
        self.lbl_fondo.setPixmap(QPixmap(p.FONDO_INICIAL))
        self.lbl_fondo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_fondo.setScaledContents(True)
        self.lbl_fondo.setGeometry(0, 0, self.width, self.height)
        
        # logo
        self.lbl_logo = QLabel(self)
        self.lbl_logo.setAlignment(Qt.AlignCenter)
        self.lbl_logo.setPixmap(QPixmap(p.LOGO))

        # ingresa del usuario
        self.edt_usuario = QLineEdit(self)
        self.edt_usuario.setAlignment(Qt.AlignCenter)
        self.edt_usuario.setPlaceholderText('Ingresa su nombre')
        self.edt_usuario.setStyleSheet(p.STYLESHEET_EDIT)

        # boton para enviar login
        self.btn_login = QPushButton('Login', self)
        self.btn_login.clicked.connect(self.enviar_login)
        self.btn_login.setStyleSheet(p.STYLESHEET_BUTTON)

        # boton para mostrar ranking
        self.btn_ranking = QPushButton('Ranking', self)
        self.btn_ranking.clicked.connect(self.mostrar_ranking)
        self.btn_ranking.setStyleSheet(p.STYLESHEET_BUTTON)

        # boton para salir
        self.btn_salir = QPushButton('Salir', self)
        self.btn_salir.clicked.connect(self.salir)
        self.btn_salir.setStyleSheet(p.STYLESHEET_BUTTON)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.lbl_logo)
        vbox.addWidget(self.edt_usuario)
        vbox.addWidget(self.btn_login)
        vbox.addWidget(self.btn_ranking)
        vbox.addWidget(self.btn_salir)

        self.setLayout(vbox)

    def enviar_login(self):
        self.sig_enviar_login.emit(self.edt_usuario.text())
        self.sig_tocar_musica.emit(False)

    def mostrar_ranking(self):
        self.sig_mostrar_ranking.emit()
        self.sig_tocar_musica.emit(False)
        self.hide()

    def salir(self):
        self.sig_salir.emit()
        self.sig_tocar_musica.emit(False)

    def recibir_validacion(self, valido: bool, errores: set):
        if valido:
            self.close()
        # notificar el jugador si el usuario no cumple las restricciones
        else:
            mensaje = ''
            if 'vacio' in errores:
                mensaje += f'Usuario no debe ser vacío.\n'
            if 'corto' in errores:
                mensaje += f'Usuario debe tener al menos {p.MIN_CARACTERES} caracteres.\n'
            if 'largo' in errores:
                mensaje += f'Usuario debe tener al maximo {p.MAX_CARACTERES} caracteres.\n'
            if 'no_alfanumerico' in errores:
                mensaje += f'Usuario debe ser alfanumérico.\n'

            self.notificacion.about(self, 'Entrada no válida', mensaje)
    
    def mostrar_ventana(self):
        self.show()
        self.sig_tocar_musica.emit(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.enviar_login()