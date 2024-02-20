from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import parametros as p


class LogicoPostRonda(QObject):

    sig_enviar_datos = pyqtSignal(bool, dict)
    sig_comenzar_siguiente_ronda = pyqtSignal(dict)
    sig_nueva_ronda = pyqtSignal(bool) # valido

    def __init__(self):
        super().__init__()

        self.datos = {}

        self.playlist = QMediaPlaylist()
        locacion = QUrl.fromLocalFile(p.SONIDO_MUSICA)
        self.playlist.addMedia(QMediaContent(locacion))
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.mediaplayer_musica = QMediaPlayer()
        self.mediaplayer_musica.setVolume(p.VOLUMEN_MUSICA)
        self.mediaplayer_musica.setPlaylist(self.playlist)

    def procesar_datos(self, ganado: bool, datos: dict):
        if ganado:
            match datos['escenario']:
                case 1:
                    ponderador = p.PONDERADOR_DIURNO
                case 2:
                    ponderador = p.PONDERADOR_NOCTURNO
            datos['puntaje'] += int(datos['puntaje'] * ponderador)
            datos['puntaje_historial'] = datos['puntaje_historial'] + datos['puntaje']
        
        self.ganado = ganado
        self.datos = datos
        
        self.sig_enviar_datos.emit(ganado, datos)

    def comenzar_siguiente_ronda(self):
        if not self.ganado:
            self.sig_nueva_ronda.emit(False)
        else:
            self.sig_nueva_ronda.emit(True)
            self.datos['ronda'] += 1
            self.sig_comenzar_siguiente_ronda.emit(self.datos)

    def guardar_datos(self):
        with open(p.PUNTAJES, 'a') as file:
            linea = f"\n{self.datos['usuario']},{self.datos['puntaje_historial']}"
            file.write(linea)
    
    def tocar_musica(self, play: bool):
        if play:
            self.mediaplayer_musica.play()
        else:
            self.mediaplayer_musica.stop()