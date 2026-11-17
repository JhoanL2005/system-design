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

    def _verificar_evento(self, evento):
        if evento not in EVENTOS:
            raise ValueError("evento desconocido")

    def suscribir(self, evento, observador):
        self._verificar_evento(evento)
        if observador not in self._observadores[evento]:
            self._observadores[evento].append(observador)

    def desuscribir(self, evento, observador):
        self._verificar_evento(evento)
        if observador in self._observadores[evento]:
            self._observadores[evento].remove(observador)

    def reservar(self, id_reserva, estudiante, inicio, fin):
        # Si la reserva se rechaza, el ValueError sale de aqui y no se avisa
        # a nadie.
        super().reservar(id_reserva, estudiante, inicio, fin)
        franja = self.franja_de(id_reserva)
        # Se recorre una copia: un observador puede suscribir o desuscribir
        # a alguien mientras se le avisa.
        for observador in list(self._observadores["ocupada"]):
            observador.al_ocuparse(self.cancha, franja)

    def cancelar(self, id_reserva):
        franja = self.franja_de(id_reserva)
        super().cancelar(id_reserva)
        for observador in list(self._observadores["liberada"]):
            observador.al_liberarse(self.cancha, franja)


class CacheDeDisponibilidad(ObservadorDeReservas):
    def __init__(self):
        self.horas_libres = {}
        self.calculos = 0

    def libres(self, calendario):
        clave = (calendario.cancha, calendario.fecha)
        if clave not in self.horas_libres:
            self.horas_libres[clave] = [
                hora
                for hora in range(HORA_DE_APERTURA, HORA_DE_CIERRE)
                if calendario.esta_libre(hora, hora + 1)
            ]
            self.calculos = self.calculos + 1
        # Una copia, para que quien la reciba no cambie lo guardado.
        return list(self.horas_libres[clave])

    def _invalidar(self, cancha, franja):
        self.horas_libres.pop((cancha, franja.fecha), None)

    def al_ocuparse(self, cancha, franja):
        self._invalidar(cancha, franja)

    def al_liberarse(self, cancha, franja):
        self._invalidar(cancha, franja)


class RegistroDeAuditoria(ObservadorDeReservas):
    def __init__(self):
        self.lineas = []

    def _anotar(self, evento, cancha, franja):
        self.lineas.append(f"{evento} {cancha} {franja.fecha} {franja.inicio}-{franja.fin}")

    def al_ocuparse(self, cancha, franja):
        self._anotar("ocupada", cancha, franja)

    def al_liberarse(self, cancha, franja):
        self._anotar("liberada", cancha, franja)


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
