"""Ejercicio 1: la lista de espera, primero consultando y despues con
Observer.

Parte A (ya escrita, no la cambies): beto quiere la cancha-1 el martes de
18 a 19, que ana tiene reservada. La app de beto consulta cada cierto
numero de segundos si la franja se libero. ana cancela a los 5500 segundos
(poco mas de hora y media). simular_consultas cuenta cuantas consultas hizo la app
hasta que beto se entero.

Parte B (TODO 1 a 3): el calendario avisa cuando una franja se libera, a
quien se haya suscrito. Nadie pregunta.

Corre el archivo con:

    python3 espera_ejercicio1.py

y las pruebas con:

    pytest test_espera_ejercicio1.py
"""

from notificaciones import NotificadorEnMemoria
from reservas import CalendarioDeCancha, FranjaHoraria

SEGUNDO_DE_LA_CANCELACION = 5500


# ---------------------------------------------------------------- Parte A

def simular_consultas(intervalo_segundos):
    calendario = CalendarioDeCancha("cancha-1", "2026-11-10")
    calendario.reservar("r-1", "ana", 18, 19)
    consultas = 0
    segundo = 0
    while True:
        if segundo >= SEGUNDO_DE_LA_CANCELACION and not calendario.esta_libre(18, 19):
            calendario.cancelar("r-1")
        consultas = consultas + 1
        if calendario.esta_libre(18, 19):
            return consultas, segundo
        segundo = segundo + intervalo_segundos


# ---------------------------------------------------------------- Parte B

class ObservadorDeCalendario:
    """Lo que el calendario sabe de quien se suscribe: que tiene este metodo."""

    def al_liberarse(self, cancha, franja):
        raise NotImplementedError


class CalendarioObservable(CalendarioDeCancha):
    # TODO 1: en __init__, ademas de lo que hace CalendarioDeCancha, una
    # lista vacia de observadores. Escribe suscribir(observador), que lo
    # agrega a esa lista.

    # TODO 2: sobrescribe cancelar. Guarda la franja de la reserva, cancela
    # como lo hace CalendarioDeCancha, y despues llama al_liberarse(cancha,
    # franja) de cada observador, en el orden en que se suscribieron.
    pass


class ListaDeEspera(ObservadorDeCalendario):
    def __init__(self, notificador):
        self.notificador = notificador
        self.esperando = {}

    def anotar(self, estudiante, franja):
        # TODO 3: agrega al estudiante al final de la lista de esa franja
        # (self.esperando[franja] es una lista). Despues escribe
        # al_liberarse: si alguien espera esa franja, saca al primero de la
        # lista y le envia, con el notificador:
        #     "Se libero cancha-1 el 2026-11-10 de 18 a 19"
        # Si nadie la espera, no hace nada.
        raise NotImplementedError


if __name__ == "__main__":
    print("Parte A: consultando")
    for intervalo in [30, 300]:
        consultas, segundo = simular_consultas(intervalo)
        print("  Cada", intervalo, "s: beto se entera en el segundo", segundo, "despues de", consultas, "consultas")
    consultas, segundo = simular_consultas(30)
    print("  2000 estudiantes esperando, cada 30 s:", 2000 * consultas, "consultas")

    print("Parte B: con Observer")
    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)
    calendario = CalendarioObservable("cancha-1", "2026-11-10")
    calendario.suscribir(lista)
    calendario.reservar("r-1", "ana", 18, 19)
    calendario.reservar("r-2", "carla", 9, 10)
    lista.anotar("beto", FranjaHoraria("2026-11-10", 18, 19))
    lista.anotar("dani", FranjaHoraria("2026-11-10", 18, 19))

    calendario.cancelar("r-2")
    calendario.cancelar("r-1")
    for destinatario, texto in notificador.enviados:
        print(" ", destinatario, "<-", texto)
    print("  Siguen esperando 18-19:", lista.esperando[FranjaHoraria("2026-11-10", 18, 19)])
