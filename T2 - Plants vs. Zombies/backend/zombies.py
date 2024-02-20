from PyQt5.QtCore import QTimer

import parametros as p


class Zombie:

    id = 0

    def __init__(self, x, y, senal_morder, senal_morir):
        self.id = Zombie.id
        Zombie.id += 1

        self.x = x
        self.y = y
        self._vida = p.VIDA_ZOMBIE
        self.velocidad = p.VELOCIDAD_ZOMBIE
        self.animacion_caminar = p.WALKER_ANIMACION_CAMINAR
        self.animacion_comer = p.WALKER_ANIMACION_COMER
        self.estado = 0
        self.idx_animacion = 0
        self.ralentizado = False

        self.comida = None
        self.pausado = False
        self._valido = True

        self.imagen_actual = p.WALKER_CAMINAR_1

        self.senal_morder = senal_morder
        self.senal_morir = senal_morir

        self.timer_mover = QTimer()
        self.timer_mover.setInterval(p.TIEMPO_MOVIMIENTO_ZOMBIE)
        self.timer_mover.timeout.connect(self.mover)
        self.timer_mover.start()

        self.timer_animar = QTimer()
        self.timer_animar.setInterval(p.TIEMPO_ANIMACION_ZOMBIE)
        self.timer_animar.timeout.connect(self.animar)
        self.timer_animar.start()

        self.timer_comer = QTimer()
        self.timer_comer.setInterval(p.INTERVALO_TIEMPO_MORDIDA)
        self.timer_comer.timeout.connect(self.comer)
        self.timer_comer.start()

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
        if value == False:
            self.senal_morir.emit()

    def mover(self):
        if self.valido and self.estado == 0 and not self.pausado:
            self.x -= self.velocidad

    def comer(self):
        if self.valido and self.estado == 1 and self.comida and not self.pausado:
            self.senal_morder.emit(self.comida.id)

    def animar(self):
        # caminando
        if self.estado == 0 and not self.pausado:
            if self.idx_animacion < len(self.animacion_caminar) - 1:
                self.idx_animacion += 1
            else:
                self.idx_animacion = 0
            self.imagen_actual = self.animacion_caminar[self.idx_animacion]
            
        # comiendo
        if self.estado == 1 and not self.pausado:
            if self.idx_animacion < len(self.animacion_comer) - 1:
                self.idx_animacion += 1
            else:
                self.idx_animacion = 0
            self.imagen_actual = self.animacion_comer[self.idx_animacion]
        
    def ralentizar(self):
        if not self.ralentizado:
            self.ralentizado = True
            self.velocidad -= int(self.velocidad * p.RALENTIZAR_ZOMBIE)
            

class ZombieRapido(Zombie):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocidad = int(p.VELOCIDAD_ZOMBIE * p.FACTOR_ZOMBIE_RAPIDO)

        self.animacion_caminar = p.RUNNER_ANIMACION_CAMINAR
        self.animacion_comer = p.RUNNER_ANIMACION_COMER