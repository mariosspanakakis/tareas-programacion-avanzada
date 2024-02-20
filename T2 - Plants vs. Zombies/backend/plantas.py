from PyQt5.QtCore import QTimer
from random import randint

import parametros as p


class Planta:

    id = 0

    def __init__(self, x, y, pausado):

        self.id = Planta.id
        Planta.id += 1

        self.x = x
        self.y = y
        self.w = p.IMAGEN_PLANTA
        self.h = p.IMAGEN_PLANTA
        self._vida = p.VIDA_PLANTA
        self._valido = True
        self.pausado = pausado
        self.imagen_actual = ''

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if valor <= 0:
            valor = 0
            self.valido = False
        self._vida = valor

    @property
    def valido(self):
        return self._valido

    @valido.setter
    def valido(self, value):
        if self._valido != value:
            self._valido = value

class Lanzaguisante(Planta):

    def __init__(self, senal_disparar, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.senal_disparar = senal_disparar
        self.imagen_actual = p.LANZAGUISANTE_1
        self.animacion = p.ANIMACION_LANZAGUISANTE
        self.idx_animacion = 0

        self.tipo_disparo = 0       # guisante normal
    
        # timer para la animacion de disparar
        self.timer_animacion = QTimer()
        self.timer_animacion.setInterval(p.TIEMPO_ANIMACION_DISPARO)
        self.timer_animacion.timeout.connect(self.animar_disparo)

        # timer para disparar regularmente
        self.timer_disparar = QTimer()
        self.timer_disparar.setInterval(p.INTERVALO_DISPARO)
        self.timer_disparar.timeout.connect(self.disparar)
        self.timer_disparar.start()

    def disparar(self):
        if not self.pausado:
            self.idx_animacion = 0
            self.timer_animacion.start()

    def animar_disparo(self):
        if self.valido and not self.pausado:
            if self.idx_animacion in range(len(self.animacion)):
                self.imagen_actual = self.animacion[self.idx_animacion]
                self.idx_animacion += 1
            else:
                self.imagen_actual = self.animacion[0]
                self.timer_animacion.stop()
            # disparar
            if self.idx_animacion == 2:
                self.senal_disparar.emit(self.x, self.y, self.tipo_disparo)


class LanzaguisanteHielo(Lanzaguisante):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.imagen_actual = p.LANZAGUISANTE_HIELO_1
        self.animacion = p.ANIMACION_LANZAGUISANTE_HIELO
        self.idx_animacion = 0
        self.tipo_disparo = 1       # guisante hielo


class Girasol(Planta):

    def __init__(self, senal_generar_sol, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.senal_generar_sol = senal_generar_sol
        self.imagen_actual = p.GIRASOL_1
        self.animacion = p.ANIMACION_GIRASOL
        self.idx_animacion = 0
    
        # timer para la animacion de movimiento
        self.timer_animacion = QTimer()
        self.timer_animacion.setInterval(p.TIEMPO_ANIMACION_GIRASOL)
        self.timer_animacion.timeout.connect(self.animar_movimiento)
        self.timer_animacion.start()

        # timer para generar soles
        self.timer_soles = QTimer()
        self.timer_soles.setInterval(p.INTERVALO_SOLES_GIRASOL)
        self.timer_soles.timeout.connect(self.generar_soles)
        self.timer_soles.start()

    def animar_movimiento(self):
        if self.valido and not self.pausado:
            if self.idx_animacion not in range(len(self.animacion)):
                self.idx_animacion = 0
            self.imagen_actual = self.animacion[self.idx_animacion]
            self.idx_animacion += 1

    def generar_soles(self):
        if self.valido and not self.pausado:
            for _ in range(p.CANTIDAD_SOLES):
                x = self.x + randint(-p.DISTANCIA_APARACION_SOLES, p.DISTANCIA_APARACION_SOLES)
                y = self.y + randint(-p.DISTANCIA_APARACION_SOLES, p.DISTANCIA_APARACION_SOLES)
                self.senal_generar_sol.emit(x, y)


class Papa(Planta):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._vida = p.VIDA_PAPA
        self.imagen_actual = p.PAPA_1

        self.timer_imagen = QTimer()
        self.timer_imagen.setInterval(p.TIEMPO_ACTUALISACION_JUEGO)
        self.timer_imagen.timeout.connect(self.cambiar_imagen)
        self.timer_imagen.start()
    
    def cambiar_imagen(self):
        if self.vida < int(p.VIDA_PAPA * 1/3):
            self.imagen_actual = p.PAPA_3

        elif self.vida < int(p.VIDA_PAPA * 2/3):
            self.imagen_actual = p.PAPA_2