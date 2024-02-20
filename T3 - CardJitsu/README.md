# Tarea 3: DCCard-Jitsu 🐧🥋

Este es el ```README.md``` de la Tarea 1, realizada por Marios Spanakakis.

## Consideraciones generales :octocat:
Según mis conocimientos y pruebas, el programa cumple todos los requisitos. Se han implementado las funcionalidades básicas, así como la función de bonus.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 26 pts (19%)
##### ✅ Protocolo	
##### ✅ Correcto uso de Sockets		
##### 🟠 Conexión
No se usan _locks_ para el manejo de los clientes.
##### ✅ Manejo de Clientes	
##### ✅ Desconexión Repentina

#### Arquitectura Cliente - Servidor: 31 pts (23%)			
##### ✅ Roles
El servidor contiene al modulo ```Logic```, que maneja todas las funcionalidades del juego. El cliente recibe mensajes, maneja el interfaz gráfica (mediante el modulo ```Interface```), y envia las entregas del usuario al servidor.	
##### ✅ Consistencia		
##### ✅ Logs

#### Manejo de Bytes: 27 pts (20%)
##### ✅ Codificación			
##### ✅ Decodificación			
##### ✅ Encriptación		
##### ✅ Desencriptación	
##### ✅ Integración

#### Interfaz Gráfica: 27 pts (20%)	
##### ✅ Ventana de Inicio		
##### ✅ Sala de Espera			
##### ✅ Ventana del Juego							
##### ✅ Ventana Final

#### Reglas de DCCard-Jitsu: 17 pts (13%)
##### ✅ Inicio del Juego			
##### ✅ Ronda				
##### ✅ Termino del Juego

#### Archivos: 8 pts (6%)
Todos los archivos se usan como pedido por el enunciado, y en los lugares especificados.
##### ✅ parámetros.json		
Porque el formato ```.json``` no permite cambios de línea, este archivo no cumple el límite de 100 carácteres per línea.
##### ✅ cartas.py	
##### ✅ cripto.py

#### Bonus: 8 décimas máximo
##### ❌ Cheatcodes	
##### ❌ Bienestar	
##### ✅ Chat
Se implementa un chat con los funcionalidades pedidas.

## Ejecución :computer:
Es necesario ejecutar el servidor al primer. Para eso, se debe localizar en la carpeta ```T3/servidor/``` y ejecutar el archivo ```main.py```. Después, se pueden conectar clientes, ejecutando el ```main.py``` en la carpeta ```T3/cliente/```.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. ```random```: Se usa ```choice()``` para eligir una carta al azar, si un jugador no lanzara una carta.
2. ```time```: Se usa la función ```sleep()``` para generar una pausa durante la evaluación de la ronda.
3. ```sys```: Se usa ```exit()``` para manejar el fin del programa.
4. ```PyQt5```: Se usan varios funciones y submodulos para generar la interfaz gráfica.
5. ```itertools```: Se usa ```zip_longest()``` en ```cripto.py``` para asemblar el mensaje encriptado.

### Librerías propias
Por otro lado, los módulos que fueron creados para el servidor fueron los siguientes:
1. ```servidor.py```: Contiene a la clase ```Servidor```, que maneja la comunicación con los clientes. Solo se usa para la comunicación, sin implementar ninguna función del juego.
2. ```logic.py```: Contiene a la clase ```Logic```, que es el cerebro del juego. Maneja todo el comportamiento y el flujo del juego.
3. ```player.py```: Contiene a la clase ```Player```. Esa implementa funcionalidades relacionados al jugador, como la reinicialización para el juego o la elección de cartas.
4. ```messager.py```: Clase adicionál que sirve para generar el contenido de mensajes del servidor a los clientes.

Para el cliente, se han creado los siguientes módulos:
1. ```backend/cliente.py```: Implementa la clase ```Cliente``` que sirve como medio de comunicación con el servidor. Igualmente, no implementa funciones del juego. Solo recibe y envia mensajes.
2. ```backend/interface.py```: Implementa el _backend_ del cliente en la clase ```Interface```. Sirve para recibir mensajes, distribuir contenido en las varias ventanas, y recibir entregas del usuario.
3. ```frontend/game_window.py```: Implementa la ventana del juego en la clase ```GameWindow```. Además, contiene a dos clases adicionales: La primera es ```ClickableLabel```, que hereda de la clase ```QLabel``` y implementa un evento que se emite cuando el usuario haga clic en este label. Se usa para la selección de cartas. La segunda clase es ```VictoryCardGridLayout```. Esa se usa para desplicar las cartas de victoria del usuario. Hereda del ```QGridLayout``` y implementa la funcionalidad de llenar el layout empezando con su primer elemento.
3. ```frontend/*_window.py```: Implementan las otras ventanas para el inicio, la sala de espera y el fin del juego. Además existe una ventana para desplicar una mensaje de error cuando se desconecta el servidor, y una ventana que implementa el chat.

Para ambos, se usan los módulos ```cripto.py``` y ```utils.py```. El primer implementa la encriptación y descriptación de mensajes, el segundo implementa un método para acesar al archivo ```parametros.json```.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://stackoverflow.com/questions/50955182/which-qlabel-was-pressed-by-mousepressevent: Implementa un ```QLabel``` con indice que permite reconocer su contenido. Está implementado en el archivo ```cliente/frontend/game_window.py``` en las líneas 10 - 22.
2. https://stackoverflow.com/questions/9660080/how-does-one-fill-a-qgridlayout-from-top-left-to-right: Implementa una ```QGridLayout``` que permite llenar sus ocntenidos empezando con el primero. Está implementado en el archivo ```cliente/frontend/game_window.py``` en las líneas 26 - 52.