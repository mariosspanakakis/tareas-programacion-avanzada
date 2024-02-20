from PyQt5.QtCore import QObject, pyqtSignal, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import parametros as p


class LogicoInicio(QObject):

    sig_enviar_validacion = pyqtSignal(bool, set)
    sig_abrir_ventana_principal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.playlist = QMediaPlaylist()
        locacion = QUrl.fromLocalFile(p.SONIDO_MUSICA)
        self.playlist.addMedia(QMediaContent(locacion))
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.mediaplayer_musica = QMediaPlayer()
        self.mediaplayer_musica.setVolume(p.VOLUMEN_MUSICA)
        self.mediaplayer_musica.setPlaylist(self.playlist)

    # enviar los datos ingresados al backend
    def validar_login(self, usuario: str):
        valido = False
        
        errores = set()
        if not usuario:
            errores.add('vacio')
        else:    
            if len(usuario) < p.MIN_CARACTERES:
                errores.add('corto')
            elif len(usuario) > p.MAX_CARACTERES:
                errores.add('largo')
            if not usuario.isalnum():
                errores.add('no_alfanumerico')

        if not errores:
            valido = True
            self.sig_abrir_ventana_principal.emit(usuario)
        
        self.sig_enviar_validacion.emit(valido, errores)

    # manejar la musica
    def tocar_musica(self, play: bool):
        if play:
            self.mediaplayer_musica.play()
        else:
            self.mediaplayer_musica.stop()