"""Ejercicio 2: dos eventos y tres observadores.

El calendario de una cancha ahora avisa dos cosas distintas:

- "ocupada": se confirmo una reserva (despues de reservar).
- "liberada": se cancelo una reserva (despues de cancelar).

Cada observador se suscribe solo a los eventos que le importan, con
suscribir(evento, observador), y el calendario llama, segun el evento,
al_ocuparse(cancha, franja) o al_liberarse(cancha, franja). Hay tres
observadores:

- ListaDeEspera, la del Ejercicio 1 (por eso este ejercicio necesita
  espera_ejercicio1.py completo).
- CacheDeDisponibilidad: guarda, por (cancha, fecha), la lista de horas
  libres, para no recorrer el calendario en cada consulta. Cada vez que el
  calendario de esa cancha cambia, borra lo guardado.
- RegistroDeAuditoria: anota cada cambio como una linea de texto.

Corre el archivo con:

    python3 eventos_ejercicio2.py

y las pruebas con:

    pytest test_eventos_ejercicio2.py
"""

from espera_ejercicio1 import ListaDeEspera
from notificaciones import NotificadorEnMemoria
from reservas import HORA_DE_APERTURA, HORA_DE_CIERRE, CalendarioDeCancha, FranjaHoraria

EVENTOS = ("ocupada", "liberada")


class ObservadorDeReservas:
    def al_ocuparse(self, cancha, franja):
        raise NotImplementedError

    def al_liberarse(self, cancha, franja):
        raise NotImplementedError


class CalendarioConEventos(CalendarioDeCancha):
    def __init__(self, cancha, fecha):
        super().__init__(cancha, fecha)
        self._observadores = {"ocupada": [], "liberada": []}

    def suscribir(self, evento, observador):
        # TODO 1: ValueError("evento desconocido") si el evento no esta en
        # EVENTOS. Si el observador ya esta suscrito a ese evento, no lo
        # agregues otra vez. Escribe tambien desuscribir(evento,
        # observador), que lo quita si esta.
        raise NotImplementedError

    # TODO 2: sobrescribe reservar: reserva como CalendarioDeCancha y,
    # despues, avisa al_ocuparse(cancha, franja) a los suscritos a
    # "ocupada". Una reserva rechazada no avisa a nadie.

    # TODO 3: sobrescribe cancelar: lo mismo que en el Ejercicio 1, pero
    # solo a los suscritos a "liberada".


class CacheDeDisponibilidad(ObservadorDeReservas):
    def __init__(self):
        self.horas_libres = {}
        self.calculos = 0

    def libres(self, calendario):
        # TODO 4: si (calendario.cancha, calendario.fecha) ya esta en
        # self.horas_libres, devuelve lo guardado. Si no, calcula la lista
        # de horas h, de HORA_DE_APERTURA a HORA_DE_CIERRE - 1, en que
        # calendario.esta_libre(h, h + 1), suma 1 a self.calculos, la
        # guarda y la devuelve. Escribe tambien al_ocuparse y al_liberarse:
        # las dos borran lo guardado para (cancha, franja.fecha), si hay
        # algo.
        raise NotImplementedError


class RegistroDeAuditoria(ObservadorDeReservas):
    def __init__(self):
        self.lineas = []

    # TODO 5: al_ocuparse agrega "ocupada cancha-1 2026-11-10 18-19" a
    # self.lineas, y al_liberarse, "liberada cancha-1 2026-11-10 18-19",
    # con la cancha y la franja que reciben.


if __name__ == "__main__":
    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)
    cache = CacheDeDisponibilidad()
    auditoria = RegistroDeAuditoria()

    calendario = CalendarioConEventos("cancha-1", "2026-11-10")
    calendario.suscribir("liberada", lista)
    calendario.suscribir("ocupada", cache)
    calendario.suscribir("liberada", cache)
    calendario.suscribir("ocupada", auditoria)
    calendario.suscribir("liberada", auditoria)

    calendario.reservar("r-1", "ana", 18, 19)
    lista.anotar("beto", FranjaHoraria("2026-11-10", 18, 19))
    print("Libres:", cache.libres(calendario))
    print("Libres otra vez:", cache.libres(calendario))
    calendario.cancelar("r-1")
    print("Libres despues de cancelar:", cache.libres(calendario))
    calendario.reservar("r-2", "beto", 18, 19)
    print("Libres despues de que beto reserva:", cache.libres(calendario))
    print("Veces que se recorrio el calendario:", cache.calculos)
    print("Avisos:", notificador.enviados)
    print("Auditoria:")
    for linea in auditoria.lineas:
        print(" ", linea)
