# Los intervalos están en milisegundos
INTERVALO_DISPARO = 2000 
INTERVALO_SOLES_GIRASOL = 20000
INTERVALO_TIEMPO_MORDIDA = 5000
# El daño y la vida tienen las mismas medidas
DANO_PROYECTIL = 5
DANO_MORDIDA = 5
VIDA_PLANTA = 100
VIDA_PAPA = 2 * VIDA_PLANTA
VIDA_ZOMBIE = 80
# Número de zombies por carril
N_ZOMBIES = 7
# Porcentaje de ralentización
RALENTIZAR_ZOMBIE = 0.25
# Soles iniciales por ronda
SOLES_INICIALES = 250
# Número de soles generados por planta
CANTIDAD_SOLES = 2
# Número de soles agregados a la cuenta por recolección
SOLES_POR_RECOLECCION = 50
# Número de soles agregados a la cuenta por Cheatcode
SOLES_EXTRA = 25
# Ponderadores de escenarios
PONDERADOR_NOCTURNO = 0.8
PONDERADOR_DIURNO = 0.9
# La velocidad del zombie
VELOCIDAD_ZOMBIE = 2
FACTOR_ZOMBIE_RAPIDO = 1.5
# Puntaje por eliminar zombie
PUNTAJE_ZOMBIE_DIURNO = 50
PUNTAJE_ZOMBIE_NOCTURNO = 100
# Costo por avanzar de ronda
COSTO_AVANZAR = 500
# Costo tiendas
COSTO_LANZAGUISANTE = 50
COSTO_LANZAGUISANTE_HIELO = 100
COSTO_GIRASOL = 50
COSTO_PAPA = 75
# Caracteres de nombre usuario
MIN_CARACTERES = 3
MAX_CARACTERES = 15

# rutas de archivos
FONDO_INICIAL = './sprites/Fondos/fondoMenu.png'
LOGO = './sprites/Elementos de juego/logo.png'
MAPA_ABUELA = './sprites/Fondos/jardinAbuela.png'
MAPA_NOCTURNA = './sprites/Fondos/salidaNocturna.png'
TEXTO_FINAL = './sprites/Elementos de juego/textoFinal.png'
CRAZYCRUZ = './sprites/CrazyRuz/crazyCruz.png'
PUNTAJES = './puntajes.txt'

# imagenes y animaciones de plantas
GIRASOL_1 = './sprites/Plantas/girasol_1.png'
GIRASOL_2 = './sprites/Plantas/girasol_2.png'
ANIMACION_GIRASOL = [GIRASOL_1, GIRASOL_2]
LANZAGUISANTE_1 = './sprites/Plantas/lanzaguisantes_1.png'
LANZAGUISANTE_2 = './sprites/Plantas/lanzaguisantes_2.png'
LANZAGUISANTE_3 = './sprites/Plantas/lanzaguisantes_3.png'
ANIMACION_LANZAGUISANTE = [LANZAGUISANTE_1, LANZAGUISANTE_2, LANZAGUISANTE_3]
LANZAGUISANTE_HIELO_1 = './sprites/Plantas/lanzaguisantesHielo_1.png'
LANZAGUISANTE_HIELO_2 = './sprites/Plantas/lanzaguisantesHielo_2.png'
LANZAGUISANTE_HIELO_3 = './sprites/Plantas/lanzaguisantesHielo_3.png'
ANIMACION_LANZAGUISANTE_HIELO = [LANZAGUISANTE_HIELO_1, LANZAGUISANTE_HIELO_2, LANZAGUISANTE_HIELO_3]
PAPA_1 = './sprites/Plantas/papa_1.png'
PAPA_2 = './sprites/Plantas/papa_2.png'
PAPA_3 = './sprites/Plantas/papa_3.png'
PALA = './sprites/Bonus/pala.png'

# imagenes y animaciones de objetos
SOL = './sprites/Elementos de juego/sol.png'
GUISANTE_1 = './sprites/Elementos de juego/guisante_1.png'
GUISANTE_2 = './sprites/Elementos de juego/guisante_2.png'
GUISANTE_3 = './sprites/Elementos de juego/guisante_3.png'
ANIMACION_GUISANTE = [GUISANTE_1, GUISANTE_2, GUISANTE_3]
GUISANTE_HIELO_1 = './sprites/Elementos de juego/guisanteHielo_1.png'
GUISANTE_HIELO_2 = './sprites/Elementos de juego/guisanteHielo_2.png'
GUISANTE_HIELO_3 = './sprites/Elementos de juego/guisanteHielo_3.png'
ANIMACION_GUISANTE_HIELO = [GUISANTE_HIELO_1, GUISANTE_HIELO_2, GUISANTE_HIELO_3]

# imagenes y animaciones de zombies
WALKER_CAMINAR_1 = './sprites/Zombies/Caminando/zombieNicoWalker_1.png'
WALKER_CAMINAR_2 = './sprites/Zombies/Caminando/zombieNicoWalker_2.png'
WALKER_ANIMACION_CAMINAR = [WALKER_CAMINAR_1, WALKER_CAMINAR_2]
RUNNER_CAMINAR_1 = './sprites/Zombies/Caminando/zombieHernanRunner_1.png'
RUNNER_CAMINAR_2 = './sprites/Zombies/Caminando/zombieHernanRunner_2.png'
RUNNER_ANIMACION_CAMINAR = [RUNNER_CAMINAR_1, RUNNER_CAMINAR_2]
WALKER_COMER_1 = './sprites/Zombies/Comiendo/zombieNicoComiendo_1.png'
WALKER_COMER_2 = './sprites/Zombies/Comiendo/zombieNicoComiendo_2.png'
WALKER_COMER_3 = './sprites/Zombies/Comiendo/zombieNicoComiendo_3.png'
WALKER_ANIMACION_COMER = [WALKER_COMER_1, WALKER_COMER_2, WALKER_COMER_3]
RUNNER_COMER_1 = './sprites/Zombies/Comiendo/zombieHernanComiendo_1.png'
RUNNER_COMER_2 = './sprites/Zombies/Comiendo/zombieHernanComiendo_2.png'
RUNNER_COMER_3 = './sprites/Zombies/Comiendo/zombieHernanComiendo_2.png'
RUNNER_ANIMACION_COMER = [RUNNER_COMER_1, RUNNER_COMER_2, RUNNER_COMER_3]

# sonidos
SONIDO_RISA_1 = "./sonidos/crazyCruz_1.wav"
SONIDO_RISA_2 = "./sonidos/crazyCruz_2.wav"
SONIDO_RISA_3 = "./sonidos/crazyCruz_3.wav"
SONIDO_RISA_4 = "./sonidos/crazyCruz_4.wav"
SONIDO_RISA_5 = "./sonidos/crazyCruz_5.wav"
SONIDO_RISA_6 = "./sonidos/crazyCruz_6.wav"
SONIDOS_RISA = [SONIDO_RISA_1, SONIDO_RISA_2, SONIDO_RISA_3,
                SONIDO_RISA_4, SONIDO_RISA_5, SONIDO_RISA_6]
SONIDO_MUSICA = "./sonidos/musica.wav"  # QUE ES ESO
SONIDO_MUSICA_2 = "./sonidos/musica2.wav"
VOLUMEN_MUSICA = 20
VOLUMEN_RISA = 100

# tamano de objetos en el juego
IMAGEN_PLANTA = 90
IMAGEN_GUISANTE = 70
IMAGEN_SOL = 80
IMAGEN_ZOMBIE = 110
IMAGEN_SOL_LOGO = 120
IMAGEN_TEXTO_FINAL = 600
IMAGEN_CRAZYCRUZ = 200
IMAGEN_CRAZYCRUZ_FINAL = 500
IMAGEN_TIENDA = 100

# tamano de ventanas
VENTANA_INICIO_W = 1200
VENTANA_INICIO_H = 800
VENTANA_PRINCIPAL_W = 1200
VENTANA_PRINCIPAL_H = 800
VENTANA_JUEGO_W = 1600
VENTANA_JUEGO_H = 900
VENTANA_RANKING_W = 1200
VENTANA_RANKING_H = 800
VENTANA_POST_RONDA_W = 1200
VENTANA_POST_RONDA_H = 800

BOTON_PAUSA_W = 300
BOTON_PAUSA_H = 130

# tablero
TABLERO_X = 434
TABLERO_Y = 275
TABLERO_W = 740
TABLERO_H = 200
N_FILAS = 2
N_COLUMNAS = 10
CASILLA_W = int(TABLERO_W/N_COLUMNAS)
CASILLA_H = int(TABLERO_H/N_FILAS)

# otro
N_PLACAMIENTOS_RANKING = 5
RANGO_GUISANTES = 2000
FACTOR_INTERVALO_ZOMBIE = 12000
VELOCIDAD_GUISANTE = 1
DISTANCIA_APARACION_SOLES = 250
INTERVALO_APARICION_SOLES = 10000

# intervalos de los timers
TIEMPO_ANIMACION_DISPARO = 200
TIEMPO_ANIMACION_GIRASOL = 400
TIEMPO_ANIMACION_ZOMBIE = 400
TIEMPO_MOVIMIENTO_ZOMBIE = 100
TIEMPO_ANIMACION_ROMPER_GUISANTE = 100
TIEMPO_ACTUALISACION_JUEGO = 10
TIEMPO_MOSTRAR_COMENTARIO = 4000

# estilo grafico
FONT = 'Arial'
STYLESHEET_LABEL = f'''color: white;
                    background-color: rgba(255, 255, 255, 100);
                    border-color: white;
                    border-radius: 10px;'''
STYLESHEET_CONTENIDO = f'''color: white;
                    background-color: rgba(255, 255, 255, 0);
                    border-style: outset;
                    border-width: 0; 
                    border-color: white;
                    border-radius: 10px;'''
STYLESHEET_MAPA = f'''color: white;
                    background-color: rgba(255, 255, 255, 50);
                    border-style: outset;
                    border-width: 8; 
                    border-radius: 10px;
                    border-color: white;'''
STYLESHEET_COMENTARIO = f'''color: black;
                    background-color: rgba(255, 255, 255, 200);
                    border-style: outset;
                    border-width: 2; 
                    border-color: black;
                    border-radius: 10px;'''
STYLESHEET_TITULO = f'''color: white;
                    background-color: none;
                    font-size: 42pt;
                    font-family: {FONT};'''
STYLESHEET_RANKING = f'''color: white;
                    background-color: rgba(255, 255, 255, 50);
                    font-size: 20pt;
                    font-family: {FONT};'''
STYLESHEET_SEPARADOR = f'''color: white;
                    background-color: white;
                    border-radius: 4px;'''
STYLESHEET_BUTTON = f'''color: white; background-color: rgba(255, 255, 255, 50);
                    border-radius: 10px; border-style: outset; border-width: 4; 
                    border-color: white; font-size: 16pt; font-family: {FONT};'''
STYLESHEET_EDIT = f'''color: white; background-color: rgba(255, 255, 255, 50);
                    border-radius: 10px; border-style: outset; border-width: 4; 
                    border-color: white; font-size: 16pt; font-family: {FONT};'''