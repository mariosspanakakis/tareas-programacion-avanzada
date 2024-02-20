# Tarea 0: Star Advanced :school_satchel:

Este es el ```README.md``` de la Tarea 0, realizada por Marios Spanakakis.

## Consideraciones generales :octocat:

Según mis conocimientos y pruebas, el programa cumple todos los requisitos. Se han implementado las funcionalidades básicas, así como la función de bonus.

### Estructura de Implementación:

El programa está escrito de forma orientada a objetos. En el centro está la clase ```Game```, que regula el juego. El tablero está representado por su propia clase ```Field```, que almacena el estado actual del campo de juego y regula el descubrimiento de un sector.
Además, hay una clase ```UserInput``` con tres subclases para diferentes tipos de entrada de usuario. El objeto de ```Game``` se inicializa al inicio del programa. En cuanto el usuario inicia una nueva partida o carga una partida pasada, se crea el objeto de ```Field``` correspondiente. Los objetos para procesar la entrada del usuario se crean según sea necesario.


## Cosas Implementadas y no Implementadas :white_check_mark:

### ✅ Menús:

**Menú de Inicio:**  
Contiene todas las opciones requeridas.  
Función correspondiente:  
```game.py```: ```_show_initial_menu()```

**Menú del Juego:**  
Contiene todas las opciones requeridas.  
Función correspondiente:  
```game.py```: ```_show_game_menu()```

### ✅ Fluyo del Juego:

**Crear Nueva Partida:**  
EL usuario puede entregar su nombre y el largo y ancho del tablero. Se comprueba la validez de todas las entradas.  
Funciones correspondientes:  
```game.py```: ```_start_new_game()```  
```game.py```: ```_generate_new_map()```

**Descubrimiento de Sectores:**  
Acepta en cualquier orden: Un número de una o dos dígitos, y una letra, mayúsculo o minúsculo. Controla si el sector es parte del tablero y si ya está conocido. El sector se revela y muestra el número de bestias vecinas, como se pide. Si el sector contiene una bestia, el jugador pierde. Si no hay bestias en la vecindad, se revelan todas las células circundantes (función de bonus). Las casillas restantes se calculan siempre, en caso que el jugador ha descubierto el último sector.  
Funciones correspondientes:  
```field.py```: ```discover_sector()```  
```field.py```: ```_count_remaining_cells()```

**Fin del Juego:**  
Al fin del juego, el jugador es notificado y su puntaje está mostrado y guardado. El jugador puede volver al Menú de Inicio. En caso que el jugador pierdó, el tablero se revele.  
Funciones correspondientes:  
```game.py```: ```_show_end_game()```  
```field.py```: ```_show_field()```

**Guardar Partida:**  
El usuario puede guardar su partida directamente del Menú del Juego, o cuando sale la partida. Si ya existe una partida con este nombre, se informa al usuario que este archivo se sobrescribirá. Los datos del juego son guardados en un archivo del tipo ```.txt``` con el nombre del usuario. El archivo contiene cuatros líneas con la siguiente información: nombre, dimensiones del tablero, locaciones de las bestias y los estados de las células.  
Función correspondiente:  
```game.py```: ```_save_game_()```

**Cargar Partida:**  
Para cargar una partida, el usuario tiene que entregar el nombre de la partida. Si existe el archivo correspondiente, se extraen los datos. Para ello, se lee línea por línea y se convierten los datos correspondientes en valores numéricos, que se utilizan para crear un nuevo objeto del tipo ```Field```.  
Función correspondiente:  
```game.py```: ```_load_game_()```

**Manejar el Puntaje:**  
El puntaje se calcula al fin de un juego. Se informe el usuario su puntaje y el valor se guarda en el archivo ```puntaje.txt``` en una nueva línea. Este archivo contiene el puntaje de todas las partidas que se realizaron. Para mostrar el ranking, se extraen los datos de este archivo, se almacenan en una lista, se ordenan y se muestran las puntuaciones más altas con el usuario correspondiente.  
Funciones correspondientes:  
```game.py```: ```_calculate_points()```  
```game.py```: ```_show_ranking()```

### ✅ Forma del Código:

**PEP8:**  
Cumple todos los requisitos.

**Modularización**  
Ninguna archivo contiene más de 400 líneas de código. Sería posible modularizar el código más, pero la distribución actual me parece razonable. 


## Ejecución :computer:
El único módulo de la tarea que debe ser ejecutado por el usuario es  ```StarAdvanced.py```.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```math```: ```ceil()``` para calcular el número de bestias
2. ```random```: ```randrange()``` para distribuir las bestias aleatorio
3. ```os```: ```path.exists()```, ```path.isfile()```, ```makedirs()``` para manejar los archivos que almacenan los datos del juego

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```game.py```: Contiene a la clase ```Game``` que maneja todos los menús y la lógica del juego
2. ```field.py```: Contiene a la clase ```Field``` que maneja las funcionalidades relacionados al tablero
3. ```user_input.py```: Contiene a la clase ```UserInput``` y tres subclasses para manejar diferentes entregadas del usuario
4. ```utility.py```: Contiene funciones básicas que ayudan en el resto del programa


## Referencias de código externo :book:
Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory>: este está implementado en el archivo ```game.py``` en la línea <168>. Sirve para asegurar que la carpeta ```partidas``` existe, y si no, crear la carpeta.
2. \<https://thispointer.com/how-to-append-text-or-lines-to-a-file-in-python/>: este está implementado en el archivo ```game.py``` en la línea <264> y sirve para append líneas a un archivo que ya existe.
3. \<https://www.simplilearn.com/tutorials/python-tutorial/list-to-string-in-python#:~:text=To%20convert%20a%20list%20to%20a%20string%2C%20use%20Python%20List,and%20return%20it%20as%20output>: este está implementado en el archivo ```game.py``` en las líneas <185, 190 y 195> para extrair y convertir los datos del juego.