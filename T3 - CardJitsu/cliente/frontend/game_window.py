from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap

from utils import data_json


# implementa un QLabel que emita un senal conectado a un click en este label
class ClickableLabel(QLabel):

    clicked = pyqtSignal(int) # id

    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = ClickableLabel.id
        ClickableLabel.id += 1

    def mousePressEvent(self, event):
        self.clicked.emit(self.id)


# implementa un QGridLayout que permite llenar sus contenidos empezando con el primero
class VictoryCardGridLayout(QGridLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_row = 0
        self.current_col = 0

    def getNextItem(self):
        item = self.itemAtPosition(self.current_row, self.current_col)
        if self.current_col == self.columnCount() - 1:
            self.current_col = 0
            self.current_row += 1
        else:
            self.current_col += 1
        return item

    def clear(self):
        self.resetPosition()
        item = self.getNextItem()
        while item:
            item.widget().clear()
            item = self.getNextItem()

    def resetPosition(self):
        self.current_col = 0
        self.current_row = 0


class GameWindow(QWidget):

    sig_click_hand_card = pyqtSignal(int) # id
    sig_confirm_card = pyqtSignal()
    sig_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Ventana de Juego')
        self.notification = QMessageBox(self)
        self.generate_gui()

    def generate_gui(self):
        hbox_main = QHBoxLayout()
        vbox_cartas_victoria = QVBoxLayout()
        vbox_juego = QVBoxLayout()
        hbox_baraja_oponente = QHBoxLayout()
        hbox_juego = QHBoxLayout()
        hbox_baraja_jugador = QHBoxLayout()

        # cartas de victoria
        lbl_cartas_victoria = QLabel('Cartas de Victoria', self)
        lbl_cartas_victoria.setAlignment(Qt.AlignCenter)
        self.grid_vic_jugador = VictoryCardGridLayout()
        positions = [ (i, j) for i in range(data_json('N_ROWS_VICTORY_CARDS'))
                            for j in range(data_json('N_COLS_VICTORY_CARDS'))]
        for position in positions:
            label = QLabel('', self)
            label.resize(data_json('SIZE_VICTORY_CARD'), data_json('SIZE_VICTORY_CARD'))
            self.grid_vic_jugador.addWidget(label, *position)
        self.grid_vic_oponente = VictoryCardGridLayout()
        positions = [(i, j) for i in range(data_json('N_ROWS_VICTORY_CARDS'))
                            for j in range(data_json('N_COLS_VICTORY_CARDS'))]
        for position in positions:
            label = QLabel('', self)
            label.resize(data_json('SIZE_VICTORY_CARD'), data_json('SIZE_VICTORY_CARD'))
            self.grid_vic_oponente.addWidget(label, *position)
        vbox_cartas_victoria.addWidget(lbl_cartas_victoria)
        lbl_opo_cartas = QLabel('Oponente', self)
        lbl_opo_cartas.setAlignment(Qt.AlignCenter)
        vbox_cartas_victoria.addWidget(lbl_opo_cartas)
        vbox_cartas_victoria.addLayout(self.grid_vic_oponente)
        vbox_cartas_victoria.addStretch(1)
        lbl_jug_cartas = QLabel('Jugador', self)
        lbl_jug_cartas.setAlignment(Qt.AlignCenter)
        vbox_cartas_victoria.addWidget(lbl_jug_cartas)
        vbox_cartas_victoria.addLayout(self.grid_vic_jugador)

        # juego
        # barajas
        self.labels_baraja_oponente = {}
        for i in range(data_json('BARAJA_PANTALLA')):
            carta = QLabel(f'Carta {i}', self)
            carta.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            carta.setFixedSize(data_json('CARD_WIDTH'), data_json('CARD_HEIGHT'))
            carta.setScaledContents(True)
            self.labels_baraja_oponente[i] = carta
            hbox_baraja_oponente.addWidget(carta)
        self.labels_baraja_jugador = {}
        for i in range(data_json('BARAJA_PANTALLA')):
            carta = ClickableLabel(f'Carta {i}', self)
            carta.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            carta.setFixedSize(data_json('CARD_WIDTH'), data_json('CARD_HEIGHT'))
            carta.setScaledContents(True)
            carta.clicked.connect(self.hand_card_clicked)
            self.labels_baraja_jugador[i] = carta
            hbox_baraja_jugador.addWidget(carta)
        # boton para confirmar
        self.btn_confirm = QPushButton('Confirmar', self)
        self.btn_confirm.clicked.connect(self.confirm_button_clicked)
        # ronda
        vbox_round = QVBoxLayout()
        lbl_round_title = QLabel('Ronda', self)
        lbl_round_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_round = QLabel(str(1), self)
        self.lbl_round.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_round.addWidget(lbl_round_title)
        vbox_round.addWidget(self.lbl_round)
        # carta actual del oponente
        vbox_carta_oponente = QVBoxLayout()
        self.lbl_carta_oponente = QLabel('', self)
        self.lbl_carta_oponente.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_carta_oponente.setFixedSize(data_json('CARD_WIDTH'), data_json('CARD_HEIGHT'))
        self.lbl_carta_oponente.setScaledContents(True)
        lbl_oponente = QLabel('Oponente', self)
        lbl_oponente.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_nombre_oponente = QLabel('Nombre', self)
        self.lbl_nombre_oponente.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_carta_oponente.addWidget(self.lbl_carta_oponente)
        vbox_carta_oponente.addWidget(lbl_oponente)
        vbox_carta_oponente.addWidget(self.lbl_nombre_oponente)
        # carta actual del jugador
        vbox_carta_jugador = QVBoxLayout()
        self.lbl_carta_jugador = QLabel('', self)
        self.lbl_carta_jugador.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_carta_jugador.setFixedSize(data_json('CARD_WIDTH'), data_json('CARD_HEIGHT'))
        self.lbl_carta_jugador.setScaledContents(True)
        lbl_jugador = QLabel('Jugador', self)
        lbl_jugador.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.lbl_nombre_jugador = QLabel('Nombre', self)
        self.lbl_nombre_jugador.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        vbox_carta_jugador.addWidget(self.lbl_carta_jugador)
        vbox_carta_jugador.addWidget(lbl_jugador)
        vbox_carta_jugador.addWidget(self.lbl_nombre_jugador)
        # timer y boton
        vbox_timer_button = QVBoxLayout()
        self.lbl_timer = QLabel('Timer', self)
        self.lbl_timer.setAlignment(Qt.AlignCenter)
        vbox_timer_button.addWidget(self.lbl_timer)
        vbox_timer_button.addWidget(self.btn_confirm)
        # asemblar layout del juego
        hbox_juego.addStretch(1)
        hbox_juego.addLayout(vbox_round)
        hbox_juego.addStretch(1)
        hbox_juego.addLayout(vbox_carta_oponente)
        hbox_juego.addStretch(1)
        hbox_juego.addLayout(vbox_timer_button)
        hbox_juego.addStretch(1)
        hbox_juego.addLayout(vbox_carta_jugador)
        hbox_juego.addStretch(2)
        
        # asemblar main layout
        hbox_main.addLayout(vbox_juego)
        vbox_juego.addLayout(hbox_baraja_oponente)
        vbox_juego.addLayout(hbox_juego)
        vbox_juego.addLayout(hbox_baraja_jugador)
        hbox_main.addLayout(vbox_cartas_victoria)

        self.setLayout(hbox_main)

    # cambiar los usuarios desplicados
    def set_user_names(self, user_names: list):
        self.lbl_nombre_jugador.setText(user_names[0])
        self.lbl_nombre_oponente.setText(user_names[1])

    # actualizar las cartas del mano del jugador
    def refresh_hand_cards(self, hand_cards: dict):
        for key, card in zip(hand_cards.keys(), hand_cards.values()):
            label = self.labels_baraja_jugador[int(key)]
            if not card:
                label.clear()
                label.setStyleSheet(data_json('STYLE_CARD_EMPTY'))
            else:
                pixmap = self.get_pixmap_for_card(card)
                label.setPixmap(pixmap)
            label.repaint()

    # actualizar las cartas del mano del oponente
    def refresh_opponent_cards(self, opponent_cards: dict, reveal: bool):
        for key, card in zip(opponent_cards.keys(), opponent_cards.values()):
            label = self.labels_baraja_oponente[int(key)]
            if not card:
                label.clear()
                label.setStyleSheet(data_json('STYLE_CARD_EMPTY'))
            else:
                # reveal solo se usaría para implementar el bonus, no es llamado nunca
                if reveal:
                    pixmap = self.get_pixmap_for_card(card)
                else:
                    pixmap = self.get_pixmap_for_card()
                label.setPixmap(pixmap)
            label.repaint()

    # notificar el servidor sobre un click a una carta
    def hand_card_clicked(self, id: int):
        self.sig_click_hand_card.emit(id)

    # confirmar la carta seleccionada
    def confirm_button_clicked(self):
        self.sig_confirm_card.emit()

    # marcar la carta seleccionada, desmarcarla si card_id = -1
    def highlight_hand_card(self, card_id: int):
        for label in self.labels_baraja_jugador.values():
            label.setStyleSheet(data_json('STYLE_CARD_NORMAL'))
        if card_id != -1:
            self.labels_baraja_jugador[card_id].setStyleSheet(data_json('STYLE_CARD_SELECTED'))

    # actualizar las cartas activos de ambos jugadores
    def refresh_active_cards(self, active_cards: list):
        own_card = active_cards[0]
        opponent_card = active_cards[1]

        if own_card:
            pixmap = self.get_pixmap_for_card(own_card)
            self.lbl_carta_jugador.setPixmap(pixmap)

            if opponent_card:
                pixmap = self.get_pixmap_for_card(opponent_card)
                self.lbl_carta_oponente.setPixmap(pixmap)
        else:
            if opponent_card:
                pixmap = self.get_pixmap_for_card()
                self.lbl_carta_oponente.setPixmap(pixmap)
            else:
                self.lbl_carta_jugador.clear()
                self.lbl_carta_jugador.setStyleSheet(data_json('STYLE_CARD_EMPTY'))
                self.lbl_carta_oponente.clear()
                self.lbl_carta_oponente.setStyleSheet(data_json('STYLE_CARD_EMPTY'))
        
        self.lbl_carta_jugador.repaint()
        self.lbl_carta_oponente.repaint()

    # actualizar las cartas de victoria de ambos jugadores
    def refresh_victory_cards(self, victory_cards: list):
        own_vic_cards = victory_cards[0]
        opponent_vic_cards = victory_cards[1]

        self.grid_vic_jugador.clear()
        self.grid_vic_oponente.clear()

        self.grid_vic_jugador.resetPosition()
        self.grid_vic_oponente.resetPosition()

        for card in own_vic_cards:
            label = self.grid_vic_jugador.getNextItem().widget()
            pixmap = self.get_pixmap_for_victory_card(card)
            label.setPixmap(pixmap)

        for card in opponent_vic_cards:
            label = self.grid_vic_oponente.getNextItem().widget()
            pixmap = self.get_pixmap_for_victory_card(card)
            label.setPixmap(pixmap)

    # actualizar el contador de rondas
    def refresh_round(self, round: int):
        self.lbl_round.setText(str(round))

    # actualizar el contador de tiempo
    def refresh_timer(self, value: int):
        self.lbl_timer.setText(str(value))

    # retornar el imagen de la carta dada; si no carta es especificado, retornar una carta oculta
    def get_pixmap_for_card(self, card=dict()) -> QPixmap:
        path = data_json('PATH_CARDS')
        # retornar carta oculta
        if not card:
            card_name = 'back.png'
        # retornar carta visible
        else:
            card_name = card['color'] + '_' + card['elemento'] + '_' + card['puntos'] + '.png'
        pixmap = QPixmap(path + card_name)
        return pixmap
    
    # retornar el imagen de una carta de victoria
    def get_pixmap_for_victory_card(self, card=dict()) -> QPixmap:
        path = data_json('PATH_VICTORY_CARDS')
        card_name = card['elemento'] + '_' + card['color'] + '.png'
        pixmap = QPixmap(path + card_name).scaled(
            data_json('SIZE_VICTORY_CARD'), data_json('SIZE_VICTORY_CARD'), Qt.KeepAspectRatio)
        return pixmap

    # ocultar la ventana
    def hide_window(self, winner: bool):
        self.hide()

    # notificar otras ventanas cuando se cerra la ventana del juego
    def closeEvent(self, event):
        self.sig_closed.emit()