from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import parametros as p


class LogicoRanking(QObject):

    sig_enviar_ranking = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        self.playlist = QMediaPlaylist()
        locacion = QUrl.fromLocalFile(p.SONIDO_MUSICA)
        self.playlist.addMedia(QMediaContent(locacion))
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.mediaplayer_musica = QMediaPlayer()
        self.mediaplayer_musica.setVolume(p.VOLUMEN_MUSICA)
        self.mediaplayer_musica.setPlaylist(self.playlist)

    def procesar_ranking(self):
        lista_puntaje = []
        with open(p.PUNTAJES, 'rt') as file:
            lineas = file.readlines()
            for linea in lineas:
                contenido = linea.strip().split(',')
                puntaje = [int(contenido[1]), contenido[0]]
                lista_puntaje.append(puntaje)
        lista_puntaje.sort(reverse=True)
        self.sig_enviar_ranking.emit(lista_puntaje[0:p.N_PLACAMIENTOS_RANKING])

    def tocar_musica(self, play: bool):
        if play:
            self.mediaplayer_musica.play()
        else:
            self.mediaplayer_musica.stop()