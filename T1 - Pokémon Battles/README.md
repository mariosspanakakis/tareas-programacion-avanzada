# Tarea 1: DCCampeonato 🏃‍♂️🏆

Este es el ```README.md``` de la Tarea 1, realizada por Marios Spanakakis.

## Consideraciones generales :octocat:
Según mis conocimientos y pruebas, el programa cumple todos los requisitos. Se han implementado las funcionalidades básicas, así como la función de bonus.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos (18pts) (22%%)
##### ✅ Diagrama
##### ✅ Definición de clases, atributos, métodos y properties		
##### ✅ Relaciones entre clases

#### Preparación programa: 11 pts (7%)			
##### ✅ Creación de partidas

#### Entidades: 28 pts (19%)
##### 🟠 Programón
Probablemente habría sido mejor implementar los tipos de programones como subclases de una clase abstracta. De cualquier manera, la clase ```Programon``` cumple todas funcionalidades requeridas.
##### ✅ Entrenador
La clase ```Entrenador``` NO contiene el método para mostrar el estado del entrenador. Este método es parte de la clase ```LigaProgramon```, que maneja todos los elementos del juego y toda la interacción con el usuario. Usar ```mostrar_estado_de_entrenador()``` como parte de esta clase me parece más razonable.
##### ✅ Liga
##### ✅ Objetos

#### Interacción Usuario-Programa 57 pts (38%)
##### ✅ General
Todos los menús se realizan gráficamente usando la clase ```UI``` con su método ```menu```. Cada menú tiene opciones para volver y para salir del juego. Los números correspondiente se generan dinámicamente. Algunos menús requieren el usuario para confirmar un cambio de valores antes de ir al siguiente menú.
##### ✅ Menú de Inicio
Muestra todos los entrenadores conocidos, con una liste de los nombres de sus programones. El jugador puede eligir un entrenador para empezar una partida.
##### ✅ Menú Entrenador
Contiene todas opciones requeridas.
##### ✅ Menu Entrenamiento
Este menú informe el jugador sobre su nivel actuál de energía, las gastos para entrenar un programon, y una lista de sus programones. Puede eligir un programón y ver los efectos del entrenamiento. Hay notificación si el programón alcanza en nivel o evoluciona.
##### ✅ Simulación ronda campeonato
Despues de eligir un programón (su luchador, que es guardado como atributo de la clase ```Entrenador```), el jugador va a la simulación. Los luchadores de los otros entrenadores son eligidos al azar. También se generan parejas aleatorios entre cada dos entrenadores. Los parejas con los entrenadores y los programones se muestran. El usuario tiene que confirmar, este lo da tiempo para leer. Después, se muestran los resultados. Sí el jugador ganó, sigue el menú del entrenador, sus programones ganen su bonus y su energía es restaurado. Si perdió, el juego es reinizialisado y sigue el menú de inicio.
##### ✅ Ver estado del campeonato
Muestra los entrenadores que siguien siendo parte del torneo, los perdedores y la ronda actual.
##### ✅ Menú crear objeto
Muestra los tipos de objetos disponibles, su costa y la energía del entrenador actual.
##### ✅ Menú utilizar objeto
El jugador debe eligir un objeto y despues un programón que recibe el objeto. Los efectos se aplican y el jugador es notificado sobre los cambios.
##### 🟠 Ver estado del entrenador
Muestra energía, objetos y programones. El layout podría ser más bonito. 
##### ✅ Robustez
Todos las entradas de usuario se procesan en la funcion ```get_user_input()``` que automáticamente controla el formato y tipo de la entrada y rechaza entradas inválidas.

#### Manejo de archivos: 12 pts (8%)
##### ✅ Archivos CSV
Los archivos ```.csv``` se importan correctamente y de manera dinámica (funcionalidad bonus)
##### ✅ Parámetros
Todos los parametros se guardan en el archivo ```parametros.py```.

#### Bonus: 5 décimas
##### ✅ Mega Evolución
La mega evolución es parte de la clase ```Programon```. Los atributos ```nivel_megaevolucion``` (implementado como property) y ```nombre_megaevolucion``` contienen la información correspondiente. Cundo el nivel del programón alcanze el nivel necesario para evolucionar, el programón cambio sus valores y su nombre. En caso que el nivel se alcanze al principio del programa, el usuario es notificado.
##### ✅ CSV dinámico
Los archivos ```.csv``` se importan dinamicamente. Para lograr eso, un diccionario con los indices de cada columna se genera. Este diccionario se usa para referenciar los columnas cuando los valores se importan. 


## Ejecución :computer:
El único módulo a ejecutar es  ```DCCampeonatoProgramon.py```.  
Usa los módulos que se explicarán en la sección **Librerías propias**
Además, se necesitan los archivos del tipo ```.csv``` que contienen datos de los entidades:
1. ```entrenadores.csv```
2. ```evoluciones.csv```
3. ```objetos.csv```
4. ```programones.csv```
Todos estos archivos se deben localizar en la carpeta root.


## Librerías :books:
### Librerías externas utilizadas
La única librería externa que utilize en este codigo es ```random```. Se usan ```random()```, ```choice()```, ```randrange()``` y ```randint()``` en ubicaciones diferentes para generar valores al azar.

### Librerías propias
Los módulos que fueron creados fueron los siguientes:
1. ```entrenador.py```: Contiene a la clase ```Entrenador``` que representa cada entidad de los entrenadores y maneja su comportamiento
2. ```liga_programon.py```: Contiene a la clase ```LigaProgramon``` que maneja el flujo del juego
3. ```objeto.py```: Contiene a la clase abstracta ```Objeto``` y sus subclases ```Baya```, ```Pocion``` y ```Caramelo``` que representan tipos diferentes de los objetos.
4. ```programon.py```: Contiene a la clase ```Programon``` que maneja el comportamiento de los programones de cada tipo.
5. ```ui.py```: Contiene a la clase ```UI``` que procesa entradas del usuario y además imprime menus y contenidos en la consola.


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/28748520/creating-random-pairs-from-lists>: este está implementado en el archivo ```liga_programon.py``` en las líneas 156 - 162 y sirve para generar parejas de entrenadores al azar.