from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont

import parametros as p


class VentanaPostRonda(QWidget):

    sig_procesar_datos = pyqtSignal(bool, dict)
    sig_volver = pyqtSignal()
    sig_comenzar_siguiente_ronda = pyqtSignal()
    sig_guardar_datos = pyqtSignal()
    sig_tocar_musica = pyqtSignal(bool) # play
    sig_abrir_ventana_de_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.width = p.VENTANA_POST_RONDA_W
        self.height = p.VENTANA_POST_RONDA_H
        self.setGeometry(600, 200, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Post Ronda')
        self.notificacion = QMessageBox(self)
        self.crear_elementos_graficos()

    def crear_elementos_graficos(self):
        # fonts
        self.font_titulo = QFont(p.FONT, 42)
        self.font_titulo.setCapitalization(QFont.SmallCaps)
        self.font = QFont(p.FONT, 24)
        self.font.setCapitalization(QFont.SmallCaps)
        # imagen del fondo
        self.lbl_fondo = QLabel(self)
        self.lbl_fondo.setPixmap(QPixmap(p.FONDO_INICIAL))
        self.lbl_fondo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_fondo.setScaledContents(True)
        self.lbl_fondo.setGeometry(0, 0, self.width, self.height)
        # titulo
        self.lbl_titulo = QLabel('Ronda Finalizada', self)
        self.lbl_titulo.setFont(self.font_titulo)
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet(p.STYLESHEET_TITULO)
        # ganado / perdido
        self.lbl_ganado = QLabel('', self)
        self.lbl_ganado.setFont(self.font)
        self.lbl_ganado.setAlignment(Qt.AlignCenter)
        self.lbl_ganado.setStyleSheet(p.STYLESHEET_TITULO)
        # botones
        self.btn_volver = QPushButton('Guardar y Salir', self)
        self.btn_volver.clicked.connect(self.volver_al_inicio)
        self.btn_siguiente = QPushButton('Siguiente Ronda', self)
        self.btn_siguiente.clicked.connect(self.comenzar_siguiente_ronda)
        # labels
        self.lbl_ronda = QLabel('Ronda Actual', self)
        self.lbl_soles = QLabel('Soles Restantes', self)
        self.lbl_zombies = QLabel('Zombies Destruidos', self)
        self.lbl_puntaje = QLabel('Puntaje de Ronda', self)
        self.lbl_puntaje_total = QLabel('Puntaje Total', self)
        self.labels = [self.lbl_ronda, self.lbl_soles, self.lbl_zombies,
                        self.lbl_puntaje, self.lbl_puntaje_total]
        for label in self.labels:
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setStyleSheet(p.STYLESHEET_LABEL)
            label.setFont(self.font)
        self.lbl_ronda_contenido = QLabel('', self)
        self.lbl_soles_contenido = QLabel('', self)
        self.lbl_zombies_contenido = QLabel('', self)
        self.lbl_puntaje_contenido = QLabel('', self)
        self.lbl_puntaje_total_contenido = QLabel('', self)
        self.labels_contenido = [self.lbl_ronda_contenido, self.lbl_soles_contenido,
                        self.lbl_zombies_contenido, self.lbl_puntaje_contenido,
                        self.lbl_puntaje_total_contenido]
        for label in self.labels_contenido:
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            label.setStyleSheet(p.STYLESHEET_CONTENIDO)
            label.setFont(self.font)

        # asemblar
        self.vbox_main = QVBoxLayout()
        self.vbox_main.addWidget(self.lbl_titulo)
        self.vbox_main.addWidget(self.lbl_ganado)
        for i in range(len(self.labels)):
            hbox = QHBoxLayout()
            hbox.addWidget(self.labels[i])
            hbox.addSpacing(40)
            hbox.addWidget(self.labels_contenido[i])
            self.vbox_main.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(self.btn_volver)
        hbox.addStretch(1)
        hbox.addWidget(self.btn_siguiente)
        hbox.addStretch(2)
        self.vbox_main.addLayout(hbox)

        self.setLayout(self.vbox_main)

    def mostrar_ventana(self, ganado, datos):
        self.sig_procesar_datos.emit(ganado, datos)
        self.show()
        self.sig_tocar_musica.emit(True)

    def actualizar_labels(self, ganado: bool, datos: dict):
        if ganado:
            self.lbl_ganado.setText('Tu has ganado!')
        else:
            self.lbl_ganado.setText('Perdiste!')
        self.lbl_ronda_contenido.setText(str(datos['ronda']))
        self.lbl_soles_contenido.setText(str(datos['soles']))
        self.lbl_zombies_contenido.setText(str(datos['zombies_destruidos']))
        self.lbl_puntaje_contenido.setText(str(datos['puntaje']))
        self.lbl_puntaje_total_contenido.setText(str(datos['puntaje_historial']))

    def volver_al_inicio(self):
        self.sig_guardar_datos.emit()
        self.sig_tocar_musica.emit(False)
        self.sig_abrir_ventana_de_inicio.emit()
        self.hide()
    
    def comenzar_siguiente_ronda(self):
        self.sig_comenzar_siguiente_ronda.emit()

    def avisar_nueva_ronda(self, valido):
        if valido:
            self.hide()
            self.sig_tocar_musica.emit(False)
        else:
            self.notificacion.about(self, 'No permitido.', 'Has perdido. No debes seguir jugando.')