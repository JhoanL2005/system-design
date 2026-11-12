"""Ejercicio 2: el agregado CalendarioDeCancha.

Un CalendarioDeCancha es el calendario de una cancha en un dia, con todas
sus reservas adentro. Es la raiz del agregado: nadie de afuera crea,
mueve ni borra una Reserva directamente; todo pasa por sus metodos, y
cada metodo deja el calendario cumpliendo sus dos reglas:

- Dos reservas del calendario no se solapan.
- Un estudiante no tiene mas de MAXIMO_HORAS_POR_ESTUDIANTE horas
  reservadas en este calendario.

Cuando una operacion romperia una regla, el metodo lanza ValueError con el
motivo y no cambia nada. Usa FranjaHoraria y Reserva de
franja_ejercicio1.py, completo.

Corre las pruebas con:

    pytest test_calendario_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from franja_ejercicio1 import FranjaHoraria, Reserva

MAXIMO_HORAS_POR_ESTUDIANTE = 2


class CalendarioDeCancha:
    def __init__(self, cancha, fecha):
        self.cancha = cancha
        self.fecha = fecha
        self._reservas = {}

    def horas_de(self, estudiante):
        total = 0 
        for reserva in self._reservas.values():
            if reserva.estudiante == estudiante:
                total += reserva.franja.duracion()
        return total

    def choca_con_otra(self, franja):
        for reserva in self._reservas.values():
            if reserva.franja.se_solapa_con(franja):


    def reservar(self, id_reserva, estudiante, inicio, fin):
        franja = FranjaHoraria(self.fecha, inicio, fin)

        if id_reserva in self._reservas:
            raise ValueError("Reserva con ID duplicado")
        if self.horas_de(estudiante) + franja.duracion > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("Maximo de hor")
        if self.choca_con_otra(franja):
            raise ValueError("Franja ocupada")

        self._reservas[id_reserva] = Reserva(id_reserva, estudiante, franja)

    def mover(self, id_reserva, nuevo_inicio, nuevo_fin):
        if id_reserva not in self._reservas:
            raise ValueError("Reserva Desconocida")

        reserva = self._reservas[id_reserva]
        nueva_franja = FranjaHoraria(self.fecha, nuevo_inicio, nuevo_fin)
        if self.choca_con_otra(nueva_franja):
            raise ValueError("Franja ocupada")

        horas_actuales = self.horas_de(reserva.estudiante) - self.franja.duracion()
        if horas_actuales + nueva_franja.duracion() > MAXIMO_HORAS_POR_ESTUDIANTE:
            raise ValueError("Horas maximas alcanzadas")

        
    def cancelar(self, id_reserva):
        # TODO 4: borra la reserva. Si el id no existe:
        # ValueError("reserva desconocida").
        raise NotImplementedError

    def reservas(self):
        # TODO 5: devuelve las reservas como una lista de tuplas
        # (id, estudiante, franja), ordenada por hora de inicio. Nada de
        # lo que devuelvas puede servir para cambiar el calendario desde
        # afuera.
        raise NotImplementedError
