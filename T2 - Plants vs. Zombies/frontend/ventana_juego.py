from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont

from frontend.elementos_graficos import TiendaItem

import parametros as p


class VentanaJuego(QWidget):
    
    sig_iniciar_juego = pyqtSignal(dict) # datos
    sig_click_tienda = pyqtSignal(str) # tienda item
    sig_pausar_juego = pyqtSignal()
    sig_avanzar = pyqtSignal()
    sig_click_pantalla = pyqtSignal(int, int) # x, y
    sig_enviar_keypress = pyqtSignal(object)
    sig_enviar_keyrelease = pyqtSignal(object)
    sig_salir_del_juego = pyqtSignal(bool) # ganado
    sig_tocar_musica = pyqtSignal(bool) # play
    sig_mouserelease = pyqtSignal(int, int) # x, y

    def __init__(self):
        super().__init__()
        self.width = p.VENTANA_JUEGO_W
        self.height = p.VENTANA_JUEGO_H
        self.setGeometry(600, 200, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle('Juego')
        self.notificacion = QMessageBox(self)
        self.setMouseTracking(True)
        self.crear_elementos_graficos()

        self.labels_entidades = [
            [],     # zombies
            [],     # plantas
            [],     # guisantes
            [],     # soles
        ]
        self.tamanos_labels = [
            p.IMAGEN_ZOMBIE,
            p.IMAGEN_PLANTA,
            p.IMAGEN_GUISANTE,
            p.IMAGEN_SOL
        ]
    
    def crear_elementos_graficos(self):
        # fonts
        self.font_info = QFont(p.FONT, 16)
        self.font_info.setCapitalization(QFont.SmallCaps)
        self.font_boton_pausa = QFont(p.FONT, 32)
        self.font_boton_pausa.setCapitalization(QFont.SmallCaps)
        self.font_comentario = QFont(p.FONT, 12)

        # imagen del fondo
        self.lbl_fondo = QLabel(self)
        self.lbl_fondo.setPixmap(QPixmap(p.FONDO_INICIAL))
        self.lbl_fondo.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_fondo.setScaledContents(True)
        self.lbl_fondo.setGeometry(0, 0, self.width, self.height)

        # preparar mapa
        self.lbl_mapa = QLabel(self)
        self.lbl_mapa.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_mapa.setStyleSheet(p.STYLESHEET_MAPA)

        # fin del juego
        self.lbl_fin = QLabel('', self)
        self.lbl_fin.setScaledContents(True)
        self.lbl_fin.setAlignment(Qt.AlignCenter)
        self.lbl_fin_comentario = QLabel(f'Gracias, me salvaste\nde los zombies!', self)
        self.lbl_fin_comentario.setFont(QFont(p.FONT, 32))
        self.lbl_fin_comentario.setStyleSheet(p.STYLESHEET_COMENTARIO)
        self.lbl_fin_comentario.move(self.lbl_mapa.x() + 550, self.lbl_mapa.y() + 100)
        self.lbl_fin_comentario.resize(self.lbl_fin_comentario.sizeHint())
        self.lbl_fin_comentario.hide()
        self.lbl_fin_instruccion = QLabel('Pulse alguna tecla para seguir.', self)
        self.lbl_fin_instruccion.setFont(QFont(p.FONT, 16))
        self.lbl_fin_instruccion.setStyleSheet(p.STYLESHEET_COMENTARIO)
        self.lbl_fin_instruccion.resize(self.lbl_fin_instruccion.sizeHint())
        self.lbl_fin_instruccion.hide()

        # crazycruz
        self.lbl_crazycruz = QLabel(self)
        self.lbl_crazycruz.setPixmap(QPixmap(p.CRAZYCRUZ))
        self.lbl_crazycruz.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.lbl_crazycruz.setScaledContents(True)
        self.lbl_crazycruz.setGeometry(self.lbl_mapa.x() + 200, self.lbl_mapa.y() + 500,
            p.IMAGEN_CRAZYCRUZ, p.IMAGEN_CRAZYCRUZ)
        # comentario
        self.lbl_comentario = QLabel('', self)
        self.lbl_comentario.setStyleSheet(p.STYLESHEET_COMENTARIO)
        self.lbl_comentario.move(self.lbl_crazycruz.x() + 200, self.lbl_crazycruz.y() + 150)
        self.lbl_comentario.setFont(self.font_comentario)
        self.lbl_comentario.resize(self.lbl_comentario.sizeHint())
        self.lbl_comentario.hide()

        ########################################## TIENDA ##########################################
        self.vbox_tienda = QVBoxLayout()
        self.lbl_tienda_titulo = QLabel('Tienda', self)
        self.lbl_tienda_titulo.setFont(self.font_info)
        self.lbl_tienda_titulo.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_tienda_titulo.setAlignment(Qt.AlignCenter)

        # lanzaguisante
        self.tienda_lanzaguisante = TiendaItem(item='lanzaguisante',
                                            imagen=p.LANZAGUISANTE_1,
                                            costo=p.COSTO_LANZAGUISANTE, parent=self)
        self.tienda_lanzaguisante.clicked.connect(self.click_tienda)
        self.lbl_lanzaguisante_costo = self.tienda_lanzaguisante.label_costo

        # lanzaguisante hielo
        self.tienda_lanzaguisante_hielo = TiendaItem(item='lanzaguisante_hielo',
                                            imagen=p.LANZAGUISANTE_HIELO_1,
                                            costo=p.COSTO_LANZAGUISANTE_HIELO, parent=self)
        self.tienda_lanzaguisante_hielo.clicked.connect(self.click_tienda)
        self.lbl_lanz_hielo_costo = self.tienda_lanzaguisante_hielo.label_costo

        # girasol
        self.tienda_girasol = TiendaItem(item='girasol', imagen=p.GIRASOL_1,
                                            costo=p.COSTO_GIRASOL, parent=self)
        self.tienda_girasol.clicked.connect(self.click_tienda)
        self.lbl_girasol_costo=self.tienda_girasol.label_costo

        # papa
        self.tienda_papa = TiendaItem(item='papa', imagen=p.PAPA_1, costo=p.COSTO_PAPA, parent=self)
        self.tienda_papa.clicked.connect(self.click_tienda)
        self.lbl_papa_costo = self.tienda_papa.label_costo

        # papa
        self.tienda_pala = TiendaItem(item='pala', imagen=p.PALA, costo=0, parent=self)
        self.tienda_pala.clicked.connect(self.click_tienda)
        self.tienda_pala.label_costo.hide()

        # asemblar
        self.vbox_tienda.addWidget(self.lbl_tienda_titulo)
        self.vbox_tienda.addStretch(2)
        self.vbox_tienda.addWidget(self.tienda_lanzaguisante)
        self.vbox_tienda.addWidget(self.lbl_lanzaguisante_costo)
        self.vbox_tienda.addStretch(1)
        self.vbox_tienda.addWidget(self.tienda_lanzaguisante_hielo)
        self.vbox_tienda.addWidget(self.lbl_lanz_hielo_costo)
        self.vbox_tienda.addStretch(1)
        self.vbox_tienda.addWidget(self.tienda_girasol)
        self.vbox_tienda.addWidget(self.lbl_girasol_costo)
        self.vbox_tienda.addStretch(1)
        self.vbox_tienda.addWidget(self.tienda_papa)
        self.vbox_tienda.addWidget(self.lbl_papa_costo)
        self.vbox_tienda.addStretch(1)
        self.vbox_tienda.addWidget(self.tienda_pala)
        self.vbox_tienda.addStretch(1)

        ################################### PANEL DE INFORMACIÓN ###################################
        self.hbox_info = QHBoxLayout()

        self.lbl_sol_logo = QLabel(self)
        self.lbl_sol_logo.setPixmap(QPixmap(
            p.SOL).scaled(p.IMAGEN_SOL_LOGO, p.IMAGEN_SOL_LOGO, Qt.KeepAspectRatio))
        self.lbl_sol_logo.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_sol_logo.setStyleSheet(p.STYLESHEET_LABEL)

        self.lbl_sol = QLabel('', self)
        self.lbl_sol.setFont(QFont(p.FONT, 32))
        self.lbl_sol.setStyleSheet(p.STYLESHEET_CONTENIDO)
        self.lbl_sol.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # nivel y puntaje
        self.vbox_nivel_puntaje = QVBoxLayout()
        self.hbox_nivel = QHBoxLayout()
        self.lbl_nivel = QLabel('Ronda', self)
        self.lbl_nivel.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_nivel.setFont(self.font_info)
        self.lbl_nivel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_nivel_contenido = QLabel('', self)
        self.lbl_nivel_contenido.setStyleSheet(p.STYLESHEET_CONTENIDO)
        self.lbl_nivel_contenido.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_nivel_contenido.setFont(self.font_info)
        self.hbox_nivel.addWidget(self.lbl_nivel)
        self.hbox_nivel.addWidget(self.lbl_nivel_contenido)
        self.hbox_puntaje = QHBoxLayout()
        self.lbl_puntaje = QLabel('Puntaje', self)
        self.lbl_puntaje.setFont(self.font_info)
        self.lbl_puntaje.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_puntaje.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_puntaje_contenido = QLabel('', self)
        self.lbl_puntaje_contenido.setStyleSheet(p.STYLESHEET_CONTENIDO)
        self.lbl_puntaje_contenido.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_puntaje_contenido.setFont(self.font_info)
        self.hbox_puntaje.addWidget(self.lbl_puntaje)
        self.hbox_puntaje.addWidget(self.lbl_puntaje_contenido)
        self.vbox_nivel_puntaje.addLayout(self.hbox_nivel)
        self.vbox_nivel_puntaje.addLayout(self.hbox_puntaje)

        # separadores
        self.lbl_separador_0 = QLabel(self)
        self.lbl_separador_0.setFixedSize(8, 160)
        self.lbl_separador_0.setStyleSheet(p.STYLESHEET_SEPARADOR)
        self.lbl_separador_1 = QLabel(self)
        self.lbl_separador_1.setFixedSize(8, 160)
        self.lbl_separador_1.setStyleSheet(p.STYLESHEET_SEPARADOR)
        self.lbl_separador_2 = QLabel(self)
        self.lbl_separador_2.setFixedSize(8, 160)
        self.lbl_separador_2.setStyleSheet(p.STYLESHEET_SEPARADOR)

        # zombies
        self.vbox_zombies = QVBoxLayout()
        self.lbl_zombies = QLabel('Zombies', self)
        self.lbl_zombies.setFont(self.font_info)
        self.lbl_zombies.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_zombies.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.hbox_zombies_muertos = QHBoxLayout()
        self.lbl_zombies_muertos = QLabel('destruidos', self)
        self.lbl_zombies_muertos.setFont(self.font_info)
        self.lbl_zombies_muertos.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_zombies_muertos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_zombies_muertos_contenido = QLabel(str(4) + '/' + str(5), self)
        self.lbl_zombies_muertos_contenido.setStyleSheet(p.STYLESHEET_CONTENIDO)
        self.lbl_zombies_muertos_contenido.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.lbl_zombies_muertos_contenido.setFont(self.font_info)
        self.hbox_zombies_muertos.addWidget(self.lbl_zombies_muertos)
        self.hbox_zombies_muertos.addWidget(self.lbl_zombies_muertos_contenido)
        self.hbox_zombies_restantes = QHBoxLayout()
        self.lbl_zombies_restantes = QLabel('restantes', self)
        self.lbl_zombies_restantes.setFont(self.font_info)
        self.lbl_zombies_restantes.setStyleSheet(p.STYLESHEET_LABEL)
        self.lbl_zombies_restantes.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_zombies_restantes_contenido = QLabel(str(1), self)
        self.lbl_zombies_restantes_contenido.setStyleSheet(p.STYLESHEET_CONTENIDO)
        self.lbl_zombies_restantes_contenido.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.hbox_zombies_restantes.addWidget(self.lbl_zombies_restantes)
        self.hbox_zombies_restantes.addWidget(self.lbl_zombies_restantes_contenido)
        self.lbl_zombies_restantes_contenido.setFont(self.font_info)
        self.vbox_zombies.addWidget(self.lbl_zombies)
        self.vbox_zombies.addLayout(self.hbox_zombies_muertos)
        self.vbox_zombies.addLayout(self.hbox_zombies_restantes)

        # botones
        self.btn_pausa = QPushButton('Comenzar', self)
        self.btn_pausa.setFixedSize(p.BOTON_PAUSA_W, p.BOTON_PAUSA_H)
        self.btn_pausa.setStyleSheet(p.STYLESHEET_BUTTON)
        self.btn_pausa.setFont(self.font_boton_pausa)
        self.btn_pausa.clicked.connect(self.pausar_juego)
        self.vbox_avanzar_salir = QVBoxLayout()
        self.btn_avanzar = QPushButton('Avanzar', self)
        self.btn_avanzar.setStyleSheet(p.STYLESHEET_BUTTON)
        self.btn_avanzar.setFont(self.font_info)
        self.btn_avanzar.clicked.connect(self.avanzar)
        self.btn_salir = QPushButton('Salir', self)
        self.btn_salir.clicked.connect(self.salir)
        self.btn_salir.setStyleSheet(p.STYLESHEET_BUTTON)
        self.btn_salir.setFont(self.font_info)
        self.vbox_avanzar_salir.addWidget(self.btn_avanzar)
        self.vbox_avanzar_salir.addWidget(self.btn_salir)

        # asemblar
        self.hbox_info.addWidget(self.lbl_sol_logo)
        self.hbox_info.addWidget(self.lbl_sol)
        self.hbox_info.addWidget(self.lbl_separador_0)
        self.hbox_info.addLayout(self.vbox_nivel_puntaje)
        self.hbox_info.addWidget(self.lbl_separador_1)
        self.hbox_info.addLayout(self.vbox_zombies)
        self.hbox_info.addWidget(self.lbl_separador_2)
        self.hbox_info.addWidget(self.btn_pausa)
        self.hbox_info.addLayout(self.vbox_avanzar_salir)

        ######################################### TABLERO ##########################################
        self.vbox_juego = QVBoxLayout()

        ##################################### ASEMBLAR LAYOUTS #####################################
        self.hbox_main = QHBoxLayout()

        self.hbox_main.addLayout(self.vbox_tienda)
        self.hbox_main.addLayout(self.vbox_juego)
        self.vbox_juego.addWidget(self.lbl_mapa)
        self.vbox_juego.addLayout(self.hbox_info)

        self.setLayout(self.hbox_main)

    # mostrar la ventana con el fondo seleccionado
    def mostrar_ventana(self, datos):
        self.sig_iniciar_juego.emit(datos)
        match datos['escenario']:
            case 1:
                self.lbl_mapa.setPixmap(QPixmap(p.MAPA_ABUELA))
            case 2:
                self.lbl_mapa.setPixmap(QPixmap(p.MAPA_NOCTURNA))
        self.show()
        self.sig_tocar_musica.emit(True)

    # borrar todos los labels de entidades
    def reiniciar_juego(self):
        for i in range(len(self.labels_entidades)):
            for label in self.labels_entidades[i]:
                label.clear()

    def pausar_juego(self):
        self.sig_pausar_juego.emit()
    
    # cambiar el texto del boton pausa
    def cambiar_boton_pausa(self, texto):
        self.btn_pausa.setText(texto)

    def avanzar(self):
        self.sig_avanzar.emit()

    def salir(self):
        self.sig_salir_del_juego.emit(False)
        self.sig_tocar_musica.emit(False)

    def click_tienda(self, item):
        self.sig_click_tienda.emit(item)
    
    # con los datos enviados actualizar el ventana
    def actualizar_ventana(self, datos: dict, entidades: list):
        # actualizar info
        self.lbl_nivel_contenido.setText(str(datos['ronda']))
        self.lbl_sol.setText(str(datos['soles']))
        self.lbl_puntaje_contenido.setText(str(datos['puntaje']))
        self.lbl_zombies_muertos_contenido.setText(str(datos['zombies_destruidos'])
                                                    + '/' + str(datos['zombies']))
        self.lbl_zombies_restantes_contenido.setText(
                                            str(datos['zombies'] - datos['zombies_destruidos']))

        # actualizar labels de entidades, basado en listas en vez de diccionarios
        # para estar más rápido
        for i in range(len(self.labels_entidades)):
            # generar nuevas labels si una entidad no ya existe
            for entidad in entidades[i]:
                if entidad[0] >= len(self.labels_entidades[i]):
                    label = QLabel(self)
                    label.show()
                    self.labels_entidades[i].append(label)
                label = self.labels_entidades[i][entidad[0]]
                # mover entidades que siguien existiendo
                if entidad[4]:
                    label.setFixedSize(self.tamanos_labels[i], self.tamanos_labels[i])
                    label.move(entidad[1], entidad[2] + 10)
                    label.setPixmap(QPixmap(entidad[3]).scaled(self.tamanos_labels[i], self.tamanos_labels[i], Qt.KeepAspectRatio))
                # remover entidades no válidos (muertos/desaparecidos/coleccionados...)
                else:
                    self.labels_entidades[i][entidad[0]].hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            x = event.pos().x()
            y = event.pos().y()
            self.sig_click_pantalla.emit(x, y)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.sig_mouserelease.emit(x, y)

    # avisar al jugador si ha ganado o perdido
    def mostrar_fin_de_ronda(self, ganado):
        if ganado:
            self.lbl_fin.setFixedSize(p.IMAGEN_CRAZYCRUZ_FINAL, p.IMAGEN_CRAZYCRUZ_FINAL)
            self.lbl_fin.move(self.lbl_mapa.x() - 100, self.lbl_mapa.y() + 180)
            self.lbl_fin_instruccion.move(self.lbl_mapa.x() + 550, self.lbl_mapa.y() + 300)
            self.lbl_fin.setPixmap(QPixmap(p.CRAZYCRUZ))
            self.lbl_fin_comentario.show()
        else:
            self.lbl_fin.setFixedSize(p.IMAGEN_TEXTO_FINAL, p.IMAGEN_TEXTO_FINAL)
            self.lbl_fin.move(self.lbl_mapa.x() + 300, self.lbl_mapa.y() + 100)
            self.lbl_fin_instruccion.move(self.lbl_mapa.x() + 850, self.lbl_mapa.y() + 600)
            self.lbl_fin.setPixmap(QPixmap(p.TEXTO_FINAL))
            self.lbl_crazycruz.hide()
        self.lbl_fin.show()
        self.lbl_fin.raise_()
        self.lbl_fin_instruccion.show()
        self.lbl_fin_instruccion.raise_()

    def keyPressEvent(self, event):
        self.sig_enviar_keypress.emit(event)
    
    def keyReleaseEvent(self, event):
        self.sig_enviar_keyrelease.emit(event)

    # cerrar la ventana y preparar los elementos para empezar de nuevo
    def cerrar(self):
        self.lbl_fin.hide()
        self.lbl_fin_comentario.hide()
        self.lbl_fin_instruccion.hide()
        self.lbl_crazycruz.show()
        self.sig_tocar_musica.emit(False)
        self.close()

    # actualizar el comentario de crazycruz que sirve para comunicar con el usuario
    def actualizar_comentario(self, comentario):
        if comentario == '':
            self.lbl_comentario.hide()
        else:
            self.lbl_comentario.show()
            self.lbl_comentario.setText(comentario)
            self.lbl_comentario.resize(self.lbl_comentario.sizeHint())