import itertools


# BUG: does not cover messages of length shorter than 3!

def encriptar(msg : bytearray) -> bytearray:
    # calcular el largo del mensaje
    length = len(msg)

    # separar el mensaje en tres partes A, B y C
    A = list([msg[idx] for idx in range(0, length, 3)])
    B = list([msg[idx] for idx in range(1, length, 3)])
    C = list([msg[idx] for idx in range(2, length, 3)])

    # calcular los bytes centrales de B
    lenB = len(B)
    if lenB % 2 == 0:
        B_central = sum([B[int((lenB-1)/2)], B[int((lenB+1)/2)]])
    else:
        B_central = B[int((lenB-1)/2)]
    
    # calcular la suma
    value = A[0] + B_central + C[-1]
   
    # encriptar el mensaje segun la fórmula
    n = int(value % 2 != 0)
    if n:
        msg_enc = [n] + A + C + B
    else:
        msg_enc = [n] + C + A + B

    # retornar el mensaje encriptado
    return bytearray(msg_enc)


def desencriptar(msg : bytearray) -> bytearray:
    # calcular el largo de la mensaje, restar el primer byte
    length = len(msg) - 1

    # calcular los largos de los partes A, B y C
    lenA = int(length/3)
    lenB = int(length/3)
    lenC = int(length/3)
    if length % 3 == 1:
        lenA += 1
    elif length % 3 == 2:
        lenA += 1
        lenB += 1

    # extraer el byte n y cortar el mensaje
    n = msg[0]
    msg = list(msg[1:])

    # extraer los partes A, B y C
    if n:   # suma par
        A = msg[0:lenA]
        B = msg[-lenB:]
        C = msg[lenA:lenA+lenC]
    else:   # suma impar
        A = msg[lenC:lenC+lenA]
        B = msg[-lenB:]
        C = msg[0:lenC]

    # asemblar el mensaje
    msg_dec = [item for items in itertools.zip_longest(A, B, C) for item in items if item]

    # retornar el mensaje desencriptado
    return bytearray(msg_dec)


if __name__ == "__main__":
    # Testear encriptar
    msg_original = bytearray(b'\x05\x08\x03\x02\x04\x03\x05\x09\x05\x09\x01')
    msg_esperado = bytearray(b'\x01\x05\x02\x05\x09\x03\x03\x05\x08\x04\x09\x01')

    msg_encriptado = encriptar(msg_original)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
