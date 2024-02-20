def print_separation_line(content: str):
    print("")
    print("-" * 60)
    print(content)
    print("")

def print_invalid_input():
    print("Entrada no válida.")

# función que converte una letra a su número Unicode del tabla ASCII
# https://ss64.com/ascii.html
# igualmente para mayúsculos y minúsculos (A = a = 0, B = b = 1, ...)
def char_to_num(char) -> int:
    # letra es mayúsculo
    if ord(char) >= 65 and ord(char) <= 90:
        return ord(char) - 65
    # letra es minúsculo
    elif ord(char) >= 97 and ord(char) <= 122:
        return ord(char) - 97
    # char no es letra
    else:
        return -1