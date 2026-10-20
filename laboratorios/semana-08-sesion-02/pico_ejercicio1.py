"""Ejercicio 1: el pico de inicio de semestre contra un solo servidor.

Corre esto para ver el resultado:

    python3 pico_ejercicio1.py

Y las pruebas con:

    pytest test_pico_ejercicio1.py
"""

from servidor import Servidor


def simular_pico(servidor, cantidad, duracion):
    # TODO: envia "cantidad" solicitudes seguidas, cada una con la
    # "duracion" indicada, al mismo servidor, sin avanzar el reloj entre
    # una y otra (llegan todas en el mismo segundo). Cuenta cuantas
    # atendio el servidor y cuantas rechazo, y devuelve las dos cuentas
    # como una tupla (atendidas, rechazadas).

    peticionesAtendidas = 0

    for peticion in range(cantidad):
        if servidor.atender(duracion):
            peticionesAtendidas += 1

    return (peticionesAtendidas, cantidad - peticionesAtendidas)


if __name__ == "__main__":
    print("Escenario A, un servidor de capacidad 100:")
    print(simular_pico(Servidor("unico", 100), 250, 5))

    print("Escenario B, un servidor mas grande, capacidad 300:")
    print(simular_pico(Servidor("grande", 300), 250, 5))

    print("Escenario C, el mismo servidor grande, caido:")
    grande = Servidor("grande", 300)
    grande.caer()
    print(simular_pico(grande, 250, 5))
