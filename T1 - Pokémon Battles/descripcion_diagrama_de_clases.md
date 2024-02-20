# Diagrama de Clases: DCCampeonato Programón

Este documento explica el razonamiento del diagrama de clases en las misma carpeta. Contiene los siguientes clases:

## ```LigaProgramon```
La clase básico del juego. Contiene todoas las funcionalidades relacionado al flujo del juego y maneja la interacción entre esos. Esta clase contiene atributos para guardar información básica de la partida: los entrenadores, una lista con entrenadores que se eliminaron del campeonato, un campeón, el entrenador seleccionado por el usuario y la ronda actual. Además contiene un elemento de la clase UI que se explicará en el siguiente.

## ```UI```
Una clase que implementa funciónes para interactuar con el usuario. Lo más importante es el método ```menu``` que recibe como parametros el título, el texto y los opciones eligibles de un menú del juego. Todo eso se visualiza en un estilo uniforme. Además, contiene métodos para procesar entregas del usuario, imprimir títulos y esperar para una confirmación del usuario.  
La UI es una composición de la clase juego, se generá sólo una vez con eso.

## ```Entrenador```
La clase ```Entrenador``` es otro composición de la clase juego y se genera para cada uno de los entrenadores disponibles. Guarda el nombre y la energía de cada entrenador. Además contiene listas con todos sus programones y objetos (elementos de subclases que se explican en el siguiente). El único método del entrenador es un método que sirve para crear objetos nuevos.

## ```Programon```
Clase para todos los programones. Guarda nombre, tipo y todos los atributos que describen el programon. La mayoría se implementa como properties. Los métodos controlen el entrenamiento, las batallas, y el comportamiento cuando el programón evoluciona. Cada programón sólo existe cómo atributo de un entrenador, entonces es una composición de eso.

## ```Objeto```
Clase abstracta. Sólo implementa el nombre del objeto y un método abstracto para aplicar este objeto. Sus subclases son:

### ```Baya```
Implementa el comportamiento de la baya. Hereda los atributos de ```Objeto``` y implementa su propio método para aplicar. Cambia la vida del programón.

### ```Pocion```
Implementa el comportamiento de la poción. Hereda los atributos de ```Objeto``` y implementa su propio método para aplicar. Cambia el ataque del programón.

### ```Caramelo```
Hereda los atributos y métodos de ls dos superclases ```Baya``` y ```Pocion```. Su método ```aplicar_objeto()``` llama los dos implementaciones de sus superclases y además cambia la defensa del programón.