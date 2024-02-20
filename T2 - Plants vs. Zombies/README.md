# Tarea 2: DCCruz vs Zombies :zombie::seedling::sunflower:

Este es el ```README.md``` de la Tarea 2, realizada por Marios Spanakakis.

## Consideraciones generales :octocat:
Según mis conocimientos y pruebas, el programa cumple todos los requisitos. Se han implementado las funcionalidades básicas, así como las funciones de bonus.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventanas: 39 pts (40%)
##### ✅ Ventana de Inicio
##### ✅ Ventana de Ranking	
##### ✅ Ventana Principal
##### ✅ Ventana de Juego
Actualiza las posiciones y imagenes de todas las entidades con la función ```actualizar_ventana```. Esto se hace a partir de listas que contienen el estado y la posición de cada objeto.
##### ✅ Ventana Post-ronda

#### Mecánicas de juego: 46 pts (47%)			
##### ✅ Plantas
Se implementan como subclases de una superclase ```Planta``` que implementa las funciones básicas. Cada planta contiene los siguientes atributos básicos: Los coordinados _x_ y _y_, largo y ancho de su imagen, y las properties _vida_ y _valido_. Este último se cambia a False cuando muere la planta. Además, la planta contiene un imagen que se muestra en la ventana de juego. Este imagen se cambia a partir de las animaciones.
La clase ```Lanzaguisante``` además contiene funciones para disparar, que se maneja como un ```QTimer```. Otro timer se usa para cambiar el imagen actual y de esa manera animar el movimiento de la planta. La clase ```LanzaguisanteHielo``` hereda de la clase ```Lanzaguisante```. De una manera similar, las clases ```Girasol``` y ```Papa``` heredan de la clase ```Planta``` y implementan sus proprios funciones.
##### ✅ Zombies
La clase ```Zombie``` implementa todas las funcionalidades necesarios (mover, comer, representar las animaciones, morir), usando QTimers y senales. La clase ```ZombieRapido``` hereda de esa clase.
##### ✅ Escenarios		
##### ✅ Fin de ronda	
##### ✅ Fin de juego	

#### Interacción con el usuario: 22 pts (23%)
##### ✅ Clicks	
Soles se coleccionen con click derecha, las plantas y la pala se usan con click izquierda o con _drag-and-drop_.
##### ✅ Animaciones
Todas las animaciones se realizan de la misma manera: Existe un ```QTimer``` para cada animación que excambia el atributo ```imagen_actual``` de una entidad. La ventana del juego siempre muestra este imagen de cada entidad.

#### Cheatcodes: 8 pts (8%)
Todos los cheatcodes se activan pulsando simultáneamente todas las teclas correspondientes. La implementación usa un ```set``` que guarda todas las teclas apretadas.
##### ✅ Pausa
##### ✅ S + U + N
##### ✅ K + I + L

#### Archivos: 4 pts (4%)
##### ✅ Sprites
##### ✅ Parametros.py

#### Bonus: 9 décimas máximo
##### ✅ Crazy Cruz Dinámico
##### ✅ Pala
##### ✅ Drag and Drop Tienda
##### ✅ Música juego

## Ejecución :computer:
El único módulo a ejecutar es  ```main.py```.  

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. ```PyQt5```: para todos funcionalidades gráficos, las ventanas, el manejamiento de entradas del usuario, timers y el sonido del juego
2. ```random```: ```choice``` y ```randint``` para generar elementos al azar

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes. El *backend* usa los siguientes módulos:
1. ```plantas.py```: Contiene a la superclase ```Planta``` y sus subclases para todos los tipos de plantas.
2. ```zombies.py```: Contiene a la clase ```Zombie``` y su subclase ```ZombieRapido```.
3. ```objetos.py```: Contiene a la superclase ```Objeto``` y sus subclases que representan Soles, Guisantes y Guisantes de Hielo. Además contiene a la clase ```Casilla``` que representa una casilla del tablero y maneja su comportamiento.  
El *frontend* solo usa el módulo:
1. ```elementos_graficos.py```: Contiene a la clase ```TiendaItem``` que inherite de la clase ```QLabel``` y maneja el comportamiento de los items que se venden en la tienda.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
1. El intervalo entre las apariciones de los zombies se multiplica con _12.000_ para generar un tiempo razonable.  

## Referencias de código externo :book:
Para realizar mi tarea no saqué código externo.