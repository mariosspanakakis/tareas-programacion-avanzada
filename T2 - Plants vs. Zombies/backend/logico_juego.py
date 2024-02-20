from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from random import choice, randint

import parametros as p
from backend.plantas import Lanzaguisante, LanzaguisanteHielo, Girasol, Papa
from backend.zombies import Zombie, ZombieRapido
from backend.objetos import Casilla, Guisante, GuisanteHielo, Sol
from aparicion_zombies import intervalo_aparicion


class LogicoJuego(QObject):

    sig_reiniciar_juego = pyqtSignal()
    sig_actualizar_juego = pyqtSignal(dict, list) # datos, entidades
    sig_disparar = pyqtSignal(int, int, int) # x, y, tipo
    sig_generar_sol = pyqtSignal(int, int) # x, y
    sig_actualizar_boton_pausa = pyqtSignal(str)
    sig_juego_finalizado = pyqtSignal(bool) # ganado
    sig_abrir_ventana_post_ronda = pyqtSignal(bool, dict) # ganado, datos
    sig_morder_planta = pyqtSignal(int) # id_planta
    sig_enviar_comentario = pyqtSignal(str) # comentario
    sig_morir_zombie = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self._cantidad_soles = 0

        self.ponderador = None
        self.intervalo_zombie = 1
        self.numero_de_zombies = p.N_ZOMBIES * 2            # N_ZOMBIES por carril
        self.item_para_comprar = None
        self.ganado = False
        self.keys = set()

        self.zombies = []
        self.plantas = []
        self.guisantes = []
        self.soles = []

        self.casillas = []
        for fil in range(p.N_FILAS):
            for col in range(p.N_COLUMNAS):
                casilla = Casilla(idx_x=col, idx_y=fil)
                self.casillas.append(casilla)

        self.timers = []
        self.timer_actualizar = QTimer()
        self.timer_actualizar.setInterval(p.TIEMPO_ACTUALISACION_JUEGO)
        self.timer_actualizar.timeout.connect(self.actualizar_juego)
        self.timers.append(self.timer_actualizar)

        self.timer_zombie = QTimer()
        self.timer_zombie.timeout.connect(self.generar_zombie)
        self.timers.append(self.timer_zombie)

        self.timer_soles = QTimer()
        self.timer_soles.setInterval(p.INTERVALO_APARICION_SOLES)
        self.timer_soles.timeout.connect(self.generar_sol_en_mapa)
        self.timers.append(self.timer_soles)

        self.timer_comentario = QTimer()
        self.timer_comentario.setSingleShot(True)
        self.timer_comentario.setInterval(p.TIEMPO_MOSTRAR_COMENTARIO)
        self.timer_comentario.timeout.connect(self.reset_comentario)

        # conectar senales internas
        self.sig_disparar.connect(self.generar_guisante)
        self.sig_generar_sol.connect(self.generar_sol)
        self.sig_morder_planta.connect(self.procesar_mordisco)
        self.sig_morir_zombie.connect(self.procesar_zombie_muerto)

        self.mediaplayer = QMediaPlayer()
        self.mediaplayer.setVolume(p.VOLUMEN_RISA)
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(p.SONIDO_MUSICA)))
        self.playlist.setPlaybackMode(QMediaPlaylist.PlaybackMode.Loop)
        self.mediaplayer_musica = QMediaPlayer()
        self.mediaplayer_musica.setVolume(p.VOLUMEN_MUSICA)
        self.mediaplayer_musica.setPlaylist(self.playlist)
    
    @property
    def cantidad_soles(self):
        return self._cantidad_soles

    @cantidad_soles.setter
    def cantidad_soles(self, valor):
        if valor < 0:
            valor = 0
        self._cantidad_soles = valor

    ################################## MANEJAR EL FLUJO DEL JUEGO ##################################
    # iniciar el juego con los datos nuevos
    def iniciar(self, datos_init):
        self.usuario = datos_init['usuario']
        self.escenario = datos_init['escenario']
        self.ronda = datos_init['ronda']
        self.cantidad_soles = p.SOLES_INICIALES
        self.zombies_destruidos = 0
        self.zombies_aparecidos = 0
        self.puntaje = 0
        self.puntaje_historial = datos_init['puntaje_historial']

        match self.escenario:
            case 1: self.ponderador = p.PONDERADOR_DIURNO
            case 2: self.ponderador = p.PONDERADOR_NOCTURNO
        
        self.comenzado = False
        self.pausado = True
        self.finalizado = False
        self.ganado = False
        for casilla in self.casillas:
            casilla.vacio = True

        self.sig_actualizar_boton_pausa.emit('Comenzar')
        self.sig_reiniciar_juego.emit()
            
        self.intervalo_zombie = intervalo_aparicion(self.ronda, self.ponderador)
        self.timer_zombie.setInterval(int(self.intervalo_zombie * p.FACTOR_INTERVALO_ZOMBIE))

        self.actualizar_juego()
        
        for timer in self.timers:
            timer.start()
    
    # actualizar la ventana y controlar las mecánicas del juego
    def actualizar_juego(self):
        # enviar datos actuales del juego a la ventana
        datos_actualizar = {
            "ronda": self.ronda,
            "soles": self.cantidad_soles,
            "puntaje": self.puntaje,
            "zombies": self.numero_de_zombies,
            "zombies_destruidos": self.zombies_destruidos
        }
        # enviar nueavas posiciones y estados de los entidades al ventana
        entidades = [[], [], [], []]
        for zombie in self.zombies:
            entidades[0].append([zombie.id, zombie.x, zombie.y, zombie.imagen_actual, zombie.valido])
        for planta in self.plantas:
            entidades[1].append([planta.id, planta.x, planta.y, planta.imagen_actual, planta.valido])
        for guis in self.guisantes:
            entidades[2].append([guis.id, guis.x, guis.y, guis.imagen_actual, guis.valido])
        for sol in self.soles:
            entidades[3].append([sol.id, sol.x, sol.y, sol.imagen_actual, sol.valido])
        self.sig_actualizar_juego.emit(datos_actualizar, entidades)
        # checkear colisiones entre zombies y plantas
        for zombie in self.zombies:
            zombie.estado = 0
            zombie.comida = None
            for planta in self.plantas:
                if (zombie.x - planta.x > 0 and zombie.x - planta.x < 50
                        and zombie.y == planta.y and planta.valido):
                    zombie.estado = 1 # empezar comer
                    zombie.comida = planta
        # checkear colisiones entre guisantes y zombies
        for zombie in [zombie for zombie in self.zombies if zombie.valido]:
            for guisante in [guisante for guisante in self.guisantes if not guisante.rompido]:
                if (zombie.x - guisante.x > 0
                        and zombie.x - guisante.x < 30
                        and zombie.y == guisante.y):
                    guisante.romper()
                    zombie.vida -= guisante.dano
                    if guisante.tipo == 1:
                        zombie.ralentizar()
        # checkear si todos los zombies han sido destruido
        if self.zombies_destruidos >= self.numero_de_zombies:
            self.finalizar_ronda(ganado=True)
        # checkear si los zombies han invado la casa
        for zombie in self.zombies:
            if zombie.x < p.TABLERO_X - 50:
                self.finalizar_ronda(ganado=False)

    # procesar el senal para la pausa
    def procesar_senal_pausa(self):
        if not self.finalizado:
            self.comenzado = True
            self.pausado = not self.pausado
            self.pausar(self.pausado)
            if self.pausado:
                self.sig_actualizar_boton_pausa.emit("Seguir")
            else:
                self.sig_actualizar_boton_pausa.emit("Pausar")

    # empezar y terminar la pausa
    def pausar(self, pausado):
        self.pausado = pausado
        if pausado and not self.finalizado:
            self.mediaplayer_musica.pause()
        else:
            self.mediaplayer_musica.play()
        for entidad in (self.zombies + self.plantas + self.guisantes):
            entidad.pausado = pausado

    def finalizar_ronda(self, ganado):
        self.ganado = ganado
        if not self.finalizado:
            self.sig_juego_finalizado.emit(ganado)
            for timer in self.timers:
                timer.stop()
        self.finalizado = True
        for entidad in (self.zombies + self.plantas + self.guisantes + self.soles):
            entidad.valido = False
        self.pausar(pausado=True)

    def salir_de_ronda(self):
        if not self.finalizado:
            self.ganado = False
            self.abrir_ventana_post_ronda()
    
    def procesar_avanzar(self):
        if not self.finalizado:
            if self.cantidad_soles >= p.COSTO_AVANZAR:
                self.cantidad_soles -= p.COSTO_AVANZAR
                self.finalizar_ronda(ganado=True)
            else:
                self.enviar_comentario("Te faltan las soles para avanzar. Tienes que luchar!")
    
    def abrir_ventana_post_ronda(self):
        datos_fin = {
                'usuario': self.usuario,
                'escenario': self.escenario,
                'ronda': self.ronda,
                'soles': self.cantidad_soles,
                'zombies_destruidos': self.zombies_destruidos,
                'puntaje': self.puntaje,
                'puntaje_historial': self.puntaje_historial
            }
        self.sig_abrir_ventana_post_ronda.emit(self.ganado, datos_fin)

    ###################################### GENERAR ENTIDADES #######################################
    # plantar una planta en una casilla
    def generar_planta(self, casilla: Casilla):
        match self.item_para_comprar:
            case 'lanzaguisante':
                planta = Lanzaguisante(x=casilla.x, y=casilla.y,
                                senal_disparar=self.sig_disparar, pausado=self.pausado)
            case 'lanzaguisante_hielo':
                planta = LanzaguisanteHielo(x=casilla.x, y=casilla.y,
                                senal_disparar=self.sig_disparar, pausado=self.pausado)
            case 'girasol':
                planta = Girasol(x=casilla.x, y=casilla.y,
                                senal_generar_sol=self.sig_generar_sol, pausado=self.pausado)
            case 'papa':
                planta = Papa(x=casilla.x, y=casilla.y, pausado=self.pausado)
        self.plantas.append(planta)
        self.item_para_comprar = None
        casilla.vacio = False

    # generar un guisante (o un guisante de hielo) en la posicion [x, y]
    def generar_guisante(self, x, y, tipo):
        if tipo == 0: guisante = Guisante(x=x+20, y=y, pausado = self.pausado)
        elif tipo == 1: guisante = GuisanteHielo(x=x+20, y=y, pausado = self.pausado)
        self.guisantes.append(guisante)

    # generar dos nuevos zombies en la mapa
    def generar_zombie(self):
        if self.pausado or self.zombies_aparecidos >= self.numero_de_zombies: return
        else:
            # generar un zombie en cada fila del tablero
            for fila in [0, 1]:
                self.intervalo_zombie = intervalo_aparicion(self.ronda, self.ponderador)
                x = p.TABLERO_X + p.TABLERO_W + 300
                y = p.TABLERO_Y + fila * p.CASILLA_H
                tipo_zombie = choice([0, 1])
                if tipo_zombie == 0:
                    zombie = Zombie(x, y, self.sig_morder_planta, self.sig_morir_zombie)
                else:
                    zombie = ZombieRapido(x, y, self.sig_morder_planta, self.sig_morir_zombie)
                self.zombies.append(zombie)
                self.zombies_aparecidos += 1

    # generar un sol en la posicion [x, y]
    def generar_sol(self, x, y):
        sol = Sol(x, y, self.pausado)
        self.soles.append(sol)
    
    # generar un sol en un lugar aleatoriamente del mapa
    def generar_sol_en_mapa(self):
        if not self.pausado and not self.escenario == 2:
            x = randint(300, p.VENTANA_JUEGO_W - 100)
            y = randint(200, p.VENTANA_JUEGO_H - 300)
            self.generar_sol(x=x, y=y)

    ################################# MANEJAR MECÀNICAS DEL JUEGO ##################################
    # validar si es posible plantar una planta en una casilla (o excavar una planta de esa casilla) 
    def validar_compra(self, casilla):
        if self.comenzado and self.pausado:
            self.enviar_comentario("No debes hacerlo durante la pausa.")
            return False
        # excavar
        if self.item_para_comprar == 'pala':
            if not casilla.vacio:
                self.excavar_planta(casilla)
                return False
        # comprar
        else:
            if not casilla.vacio:
                self.enviar_comentario("Este lugar ya está ocupada.")
                return False
            match self.item_para_comprar:
                case None:
                    self.enviar_comentario("Elige una planta en la tienda antes de plantar.")
                    return False
                case 'lanzaguisante': precio = p.COSTO_LANZAGUISANTE
                case 'lanzaguisante_hielo': precio = p.COSTO_LANZAGUISANTE_HIELO
                case 'girasol': precio = p.COSTO_GIRASOL
                case 'papa': precio = p.COSTO_PAPA
            if precio > self.cantidad_soles:
                self.enviar_comentario("No tienes suficientes soles para comprar eso...")
                return False
            self.cantidad_soles -= precio
            return True

    def excavar_planta(self, casilla):
        for planta in self.plantas:
            if planta.x == casilla.x and planta.y == casilla.y:
                planta.valido = False
                casilla.vacio = True

    # reducir la vida de una planta que es mordido y remover la planta cuando muere
    def procesar_mordisco(self, id):
        planta = self.plantas[id]
        planta.vida -= p.DANO_MORDIDA
        if planta.vida == 0:
            self.enviar_comentario("Oh no, han comido a una planta...")
            for casilla in self.casillas:
                if casilla.x == planta.x and casilla.y == planta.y:
                    casilla.vacio = True

    def procesar_zombie_muerto(self):
        self.zombies_destruidos += 1
        self.enviar_comentario("Uno menos!")
        match self.escenario:
            case 1:
                self.puntaje += p.PUNTAJE_ZOMBIE_DIURNO
            case 2:
                self.puntaje += p.PUNTAJE_ZOMBIE_NOCTURNO
        locacion = QUrl.fromLocalFile(choice(p.SONIDOS_RISA))
        self.mediaplayer.setMedia(QMediaContent(locacion))
        self.mediaplayer.play()

    ############################# MANEJAR COMUNICACION CON EL USUARIO ##############################
    # procesar el mouse press event para coleccionar los soles
    def procesar_click_pantalla(self, x, y):
        for sol in self.soles:
            if sol.valido:
                collision = self.checkear_click(x=x, y=y, obj=sol)
                if collision:
                    self.cantidad_soles += p.SOLES_POR_RECOLECCION
                    sol.valido = False
    
    # procesar el mouse release event para hacer el drag and drop con las plantas
    def procesar_mouserelease(self, x, y):
        for casilla in self.casillas:
            if self.checkear_click(x, y, casilla) and self.validar_compra(casilla):
                self.generar_planta(casilla)

    # validar si un click es en dentro de un objeto
    def checkear_click(self, x, y, obj):
        return x > obj.x and x < obj.x + obj.w and y > obj.y and y < obj.y + obj.h
    
    # guardar el nombre del TiendaItem que ha sido clickeado
    def procesar_click_tienda(self, item):
        self.item_para_comprar = item

    # reaccionar a entradas sobre el teclado y manejar cheat codes
    def procesar_keypress(self, event):
        self.keys.add(event.key())
        # pausa
        if Qt.Key_P in self.keys:
            self.procesar_senal_pausa()
        # cheat code S + U + N
        if Qt.Key_S in self.keys and Qt.Key_U in self.keys and Qt.Key_N in self.keys:
            self.cantidad_soles += p.SOLES_EXTRA
            self.enviar_comentario("Uh-hu, extra plata para ti...")
        # cheat code K + I + L
        if Qt.Key_K in self.keys and Qt.Key_I in self.keys and Qt.Key_L in self.keys:
            for zombie in self.zombies:
                zombie.valido = False
            self.zombies_destruidos = self.numero_de_zombies
        # confirmar fin de ronda
        if self.finalizado:
            self.abrir_ventana_post_ronda()

    def procesar_keyrelease(self, event):
        self.keys.remove(event.key())

    # enviar un comentario de CrazyCruz para comunicar con el usuario
    def enviar_comentario(self, comentario):
        self.sig_enviar_comentario.emit(comentario)
        self.timer_comentario.start()
    
    # borrar el comentario
    def reset_comentario(self):
        self.sig_enviar_comentario.emit('')
    
    # manejar la musica
    def tocar_musica(self, play: bool):
        if play:
            self.mediaplayer_musica.play()
        else:
            self.mediaplayer_musica.stop()