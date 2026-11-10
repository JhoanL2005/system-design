"""El dominio de Reservas de la Semana 11, Sesion 2, ya resuelto.

FranjaHoraria es un value object; Reserva, una entidad con identidad por
id; CalendarioDeCancha, la raiz del agregado: el calendario de una cancha
en un dia. Agrega dos consultas que esta sesion necesita:

- esta_libre(inicio, fin): True si ninguna reserva se solapa con esa franja.
- franja_de(id_reserva): la FranjaHoraria de una reserva.

No lo modifiques: los tres ejercicios lo usan tal cual.
"""

from dataclasses import dataclass

HORA_DE_APERTURA = 7
HORA_DE_CIERRE = 21
MAXIMO_HORAS_POR_ESTUDIANTE = 2


@dataclass(frozen=True)
class FranjaHoraria:
    fecha: str
    inicio: int
    fin: int

    def __post_init__(self):
        if self.inicio >= self.fin or self.inicio < HORA_DE_APERTURA or self.fin > HORA_DE_CIERRE:
            raise ValueError("franja invalida")

    def duracion(self):
        return self.fin - self.inicio

    def se_solapa_con(self, otra):
        return self.fecha == otra.fecha and self.inicio < otra.fin and otra.inicio < self.fin


class Reserva:
    def __init__(self, id_reserva, estudiante, franja):
        self.id = id_reserva
        self.estudiante = estudiante
        self.franja = franja

    def __eq__(self, otra):
        return self.id == otra.id

    def __hash__(self):
        return hash(self.id)


class CalendarioDeCancha:
    def __init__(self, cancha, fecha):
        self.cancha = cancha
        self.fecha = fecha
        self._reservas = {}

    def horas_de(self, estudiante):
        total = 0
        for reserva in self._reservas.values():
            if reserva.estudiante == estudiante:
                total = total + reserva.franja.duracion()
        return total

    def esta_libre(self, inicio, fin):
        franja = FranjaHoraria(self.fecha, inicio, fin)
        for reserva in self._reservas.values():
            if reserva.franja.se_solapa_con(franja):
                return False
        return True

    def franja_de(self, id_reserva):
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")
        return self._reservas[id_reserva].franja

    def reservar(self, id_reserva, estudiante, inicio, fin):
        franja = FranjaHoraria(self.fecha, inicio, fin)
        if id_reserva in self._reservas:
            raise ValueError("id repetido")
        if not self.esta_libre(inicio, fin):
            raise ValueError("franja ocupada")
        if self.horas_de(estudiante) + franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("limite de horas alcanzado")
        self._reservas[id_reserva] = Reserva(id_reserva, estudiante, franja)

    def cancelar(self, id_reserva):
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")
        self._reservas.pop(id_reserva)

    def reservas(self):
        ordenadas = []
        for hora in range(HORA_DE_APERTURA, HORA_DE_CIERRE):
            for reserva in self._reservas.values():
                if reserva.franja.inicio == hora:
                    ordenadas.append((reserva.id, reserva.estudiante, reserva.franja))
        return ordenadas
