from PyQt5.QtCore import QTimer

import parametros as p


# clase que contiene la informacion sobre una casilla del tablero
class Casilla:

    id = 0

    def __init__(self, idx_x, idx_y, vacio=True):
        self.id = Casilla.id
        Casilla.id += 1

        # cada casilla tiene un index, un tamano fijo y una posicion
        self.idx_x = idx_x
        self.idx_y = idx_y
        self.w = p.CASILLA_W
        self.h = p.CASILLA_H
        self.x = p.TABLERO_X + p.CASILLA_W * idx_x
        self.y = p.TABLERO_Y + p.CASILLA_H * idx_y
        self.vacio = vacio


# superclase para todos los objetos, implementa los estados valido y pausado
class Objeto:

    def __init__(self, x, y, pausado):

        self.x = x
        self.y = y
        self._valido = True
        self.pausado = pausado
    
    @property
    def valido(self):
        return self._valido

    @valido.setter
    def valido(self, value):
        if self._valido != value:
            self._valido = value


class Sol(Objeto):

    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = Sol.id
        Sol.id += 1

        self.w = p.IMAGEN_SOL
        self.h = p.IMAGEN_SOL
        self.imagen_actual = p.SOL


class Guisante(Objeto):

    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = Guisante.id
        Guisante.id += 1

        self.w = p.IMAGEN_GUISANTE
        self.h = p.IMAGEN_GUISANTE
        self.dano = p.DANO_PROYECTIL

        self.tipo = 0

        self.rompido = False

        self.imagen_actual = p.GUISANTE_1
        self.animacion = p.ANIMACION_GUISANTE
        self.idx_animacion = 0
        
        self.timer_mover = QTimer()
        self.timer_mover.setInterval(p.TIEMPO_ACTUALISACION_JUEGO)
        self.timer_mover.timeout.connect(self.mover)
        self.timer_mover.start()

        self.timer_romper = QTimer()
        self.timer_romper.setInterval(p.TIEMPO_ANIMACION_ROMPER_GUISANTE)
        self.timer_romper.timeout.connect(self.animar_romper)

    def mover(self):
        if self.x >= p.RANGO_GUISANTES:
            self.valido = False
            self.timer_mover.stop()
        if not self.pausado and self.valido:
            self.x += int(p.VELOCIDAD_GUISANTE * p.TIEMPO_ACTUALISACION_JUEGO)

    def romper(self):
        self.rompido = True
        self.idx_animacion = 1
        self.timer_mover.stop()
        self.timer_romper.start()

    def animar_romper(self):
        if not self.pausado:
            if self.idx_animacion in range(len(self.animacion)):
                self.imagen_actual = self.animacion[self.idx_animacion]
                self.idx_animacion += 1
            else:
                self.valido = False
                self.timer_mover.stop()
                self.timer_romper.stop()
    

class GuisanteHielo(Guisante):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imagen_actual = p.GUISANTE_HIELO_1
        self.animacion = p.ANIMACION_GUISANTE_HIELO

        self.tipo = 1