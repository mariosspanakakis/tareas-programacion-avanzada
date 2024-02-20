import parametros as p


class UI:
    def __init__(self):
        pass
    
    # imprimir un menu con los parametros del usuario;
    # los parametros 'volver' y 'salir' determinan si los opciones
    # correspondientes se muestran en el menú
    def menu(self, titulo: str, texto: list, opciones: list,
                    volver: bool, salir: bool, mostrar_titulo=True) -> int:
        
        if mostrar_titulo:
            self.imprimir_titulo(titulo=titulo)

        # imprimir texto
        print("")
        for line in texto:
            print(line)
        print("")

        # imprimir opciones
        counter = 0
        for opcion in opciones:
            counter += 1
            str = f"[{counter}]"
            print(f"  {str:>4} {opcion}")
        # anadir volver y salir, si requerido
        if volver:
            counter += 1
            str = f"Volver [{counter}]"
            print(f"{str:>100}")
        if salir:
            counter += 1
            str = f"Salir [{counter}]"
            print(f"{str:>100}")
        print("")
        
        # procesar y devolver la entrada del usuario
        input = self.get_input(entrada_valida=range(1, counter + 1))
        # siempre devolver -1 para la opción 'volver'
        if volver and input == counter - 1 + (not salir):
            return -1
        if salir and input == counter:
            quit()
        return input
        
    # procesar input del usuario, controlar su validida
    def get_input(self, entrada_valida: list):
        while 1:
            user_input = input("Elige una opcíon: ")
            if user_input.isdigit() and int(user_input) in entrada_valida:
                return int(user_input)
            else:
                print("Entrada no válida.")
    
    # esperar para una confirmación, entonces el usuario tiene tiempo para leer
    def esperar_confirmacion(self):
        print("")
        input("¿Confirmar?")
        print("")
    
    # imprimir el titulo en un formato uniforme
    def imprimir_titulo(self, titulo: str):
        print("")
        lon = len(titulo)
        pad = lon%2 != 0
        num = int((int(p.NUM_GUIONES_LINEA) - lon - 2) / 2)
        print("-" * num + " " + titulo + " " + "-" * (num + pad))
        print("-" * int(p.NUM_GUIONES_LINEA))