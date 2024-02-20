from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import parametros as p


class LogicoPrincipal(QObject):

    sig_enviar_validacion = pyqtSignal(bool, int) # valido, escenario
    sig_abrir_ventana_del_juego = pyqtSignal(dict) # datos

    def __init__(self):
        super().__init__()

        self.playlist = QMediaPlaylist()
        locacion = QUrl.fromLocalFile(p.SONIDO_MUSICA)
        self.playlist.addMedia(QMediaContent(locacion))
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.mediaplayer_musica = QMediaPlayer()
        self.mediaplayer_musica.setVolume(p.VOLUMEN_MUSICA)
        self.mediaplayer_musica.setPlaylist(self.playlist)
        
    def validar_seleccion(self, usuario, estado_btn_1, estado_btn_2):
        valido = False
        escenario = 0
        
        if estado_btn_1 and not estado_btn_2:
            valido = True
            escenario = 1
        if not estado_btn_1 and estado_btn_2:
            valido = True
            escenario = 2
        
        if valido:
            datos_init = {
                'usuario': usuario,
                'escenario': escenario,
                'ronda': 1,
                'puntaje_historial': 0
            }
            self.sig_abrir_ventana_del_juego.emit(datos_init)

        self.sig_enviar_validacion.emit(valido, escenario)
    
    def tocar_musica(self, play: bool):
        if play:
            self.mediaplayer_musica.play()
        else:
            self.mediaplayer_musica.stop()
