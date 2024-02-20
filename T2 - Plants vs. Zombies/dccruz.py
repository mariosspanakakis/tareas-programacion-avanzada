from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_post_ronda import VentanaPostRonda
from backend.logico_inicio import LogicoInicio
from backend.logico_principal import LogicoPrincipal
from backend.logico_juego import LogicoJuego
from backend.logico_ranking import LogicoRanking
from backend.logico_post_ronda import LogicoPostRonda


class Game(QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.ventana_inicio = VentanaInicio()
        self.logico_inicio = LogicoInicio()
        self.ventana_principal = VentanaPrincipal()
        self.logico_principal = LogicoPrincipal()
        self.ventana_juego = VentanaJuego()
        self.logico_juego = LogicoJuego()
        self.ventana_ranking = VentanaRanking()
        self.logico_ranking = LogicoRanking()
        self.ventana_post_ronda = VentanaPostRonda()
        self.logico_post_ronda = LogicoPostRonda()

        self.conectar_inicio()
        self.conectar_principal()
        self.conectar_juego()
        self.conectar_ranking()
        self.conectar_post_ronda()

    def conectar_inicio(self):
        # frontend -> backend
        self.ventana_inicio.sig_enviar_login.connect(
            self.logico_inicio.validar_login)
        self.ventana_inicio.sig_salir.connect(
            self.exit)
        self.ventana_inicio.sig_mostrar_ranking.connect(
            self.ventana_ranking.mostrar_ventana)
        self.ventana_inicio.sig_tocar_musica.connect(
            self.logico_inicio.tocar_musica)
        # backend -> frontend
        self.logico_inicio.sig_enviar_validacion.connect(
            self.ventana_inicio.recibir_validacion)
        self.logico_inicio.sig_abrir_ventana_principal.connect(
            self.ventana_principal.mostrar_ventana)

    def conectar_principal(self):
        # frontend -> backend
        self.ventana_principal.sig_validar_seleccion.connect(
            self.logico_principal.validar_seleccion)
        self.ventana_principal.sig_tocar_musica.connect(
            self.logico_principal.tocar_musica)
        # backend -> frontend
        self.logico_principal.sig_enviar_validacion.connect(
            self.ventana_principal.recibir_validacion)
        self.logico_principal.sig_abrir_ventana_del_juego.connect(
            self.ventana_juego.mostrar_ventana)

    def conectar_juego(self):
        # frontend -> backend
        self.ventana_juego.sig_iniciar_juego.connect(
            self.logico_juego.iniciar)
        self.ventana_juego.sig_click_tienda.connect(
            self.logico_juego.procesar_click_tienda)
        self.ventana_juego.sig_pausar_juego.connect(
            self.logico_juego.procesar_senal_pausa)
        self.ventana_juego.sig_click_pantalla.connect(
            self.logico_juego.procesar_click_pantalla)
        self.ventana_juego.sig_mouserelease.connect(
            self.logico_juego.procesar_mouserelease)
        self.ventana_juego.sig_enviar_keypress.connect(
            self.logico_juego.procesar_keypress)
        self.ventana_juego.sig_enviar_keyrelease.connect(
            self.logico_juego.procesar_keyrelease)
        self.ventana_juego.sig_avanzar.connect(
            self.logico_juego.procesar_avanzar)
        self.ventana_juego.sig_salir_del_juego.connect(
            self.logico_juego.salir_de_ronda)
        self.ventana_juego.sig_tocar_musica.connect(
            self.logico_juego.tocar_musica)
        # backend -> frontend
        self.logico_juego.sig_actualizar_juego.connect(
            self.ventana_juego.actualizar_ventana)
        self.logico_juego.sig_reiniciar_juego.connect(
            self.ventana_juego.reiniciar_juego)
        self.logico_juego.sig_actualizar_boton_pausa.connect(
            self.ventana_juego.cambiar_boton_pausa)
        self.logico_juego.sig_juego_finalizado.connect(
            self.ventana_juego.mostrar_fin_de_ronda)
        self.logico_juego.sig_abrir_ventana_post_ronda.connect(
            self.ventana_post_ronda.mostrar_ventana)
        self.logico_juego.sig_abrir_ventana_post_ronda.connect(
            self.ventana_juego.cerrar)
        self.logico_juego.sig_enviar_comentario.connect(
            self.ventana_juego.actualizar_comentario)

    def conectar_ranking(self):
        # frontend -> backend
        self.ventana_ranking.sig_consultar_ranking.connect(
            self.logico_ranking.procesar_ranking)
        self.ventana_ranking.sig_volver.connect(
            self.ventana_inicio.mostrar_ventana)
        self.ventana_ranking.sig_tocar_musica.connect(
            self.logico_ranking.tocar_musica)
        # backend -> frontend
        self.logico_ranking.sig_enviar_ranking.connect(
            self.ventana_ranking.mostrar_ranking)

    def conectar_post_ronda(self):
        # frontend -> backend
        self.ventana_post_ronda.sig_procesar_datos.connect(
            self.logico_post_ronda.procesar_datos)
        self.ventana_post_ronda.sig_comenzar_siguiente_ronda.connect(
            self.logico_post_ronda.comenzar_siguiente_ronda)
        self.ventana_post_ronda.sig_guardar_datos.connect(
            self.logico_post_ronda.guardar_datos)
        self.ventana_post_ronda.sig_tocar_musica.connect(
            self.logico_post_ronda.tocar_musica)
        self.ventana_post_ronda.sig_abrir_ventana_de_inicio.connect(
            self.ventana_inicio.mostrar_ventana)
        # backend -> frontend
        self.logico_post_ronda.sig_enviar_datos.connect(
            self.ventana_post_ronda.actualizar_labels)
        self.logico_post_ronda.sig_comenzar_siguiente_ronda.connect(
            self.ventana_juego.mostrar_ventana)
        self.logico_post_ronda.sig_nueva_ronda.connect(
            self.ventana_post_ronda.avisar_nueva_ronda)

    def comenzar(self):
        self.ventana_inicio.mostrar_ventana()