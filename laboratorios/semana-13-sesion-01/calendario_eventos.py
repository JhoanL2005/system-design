"""El calendario que avisa eventos, de la Semana 12, Sesion 1, ya resuelto.

CalendarioConEventos avisa "ocupada" (despues de reservar) y "liberada"
(despues de cancelar) a los observadores suscritos a cada evento, con
al_ocuparse(cancha, franja) y al_liberarse(cancha, franja).

No lo modifiques: los tres ejercicios lo usan tal cual.
"""

from reservas import CalendarioDeCancha

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
        if evento not in EVENTOS:
            raise ValueError("evento desconocido")
        if observador not in self._observadores[evento]:
            self._observadores[evento].append(observador)

    def desuscribir(self, evento, observador):
        if evento in EVENTOS and observador in self._observadores[evento]:
            self._observadores[evento].remove(observador)

    def reservar(self, id_reserva, estudiante, inicio, fin):
        super().reservar(id_reserva, estudiante, inicio, fin)
        franja = self.franja_de(id_reserva)
        for observador in self._observadores["ocupada"]:
            observador.al_ocuparse(self.cancha, franja)

    def cancelar(self, id_reserva):
        franja = self.franja_de(id_reserva)
        super().cancelar(id_reserva)
        for observador in self._observadores["liberada"]:
            observador.al_liberarse(self.cancha, franja)
