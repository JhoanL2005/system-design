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
        # TODO 1: cuantas horas suman las reservas del estudiante en este
        # calendario.
        raise NotImplementedError

    def reservar(self, id_reserva, estudiante, inicio, fin):
        # TODO 2: crea la FranjaHoraria con la fecha del calendario (si es
        # invalida, su propio ValueError basta) y, en este orden:
        # - id ya usado en este calendario: ValueError("id repetido");
        # - se solapa con otra reserva: ValueError("franja ocupada");
        # - el estudiante pasaria de MAXIMO_HORAS_POR_ESTUDIANTE:
        #   ValueError("limite de horas alcanzado").
        # Si todo se cumple, guarda la Reserva en self._reservas por su id.
        raise NotImplementedError

    def mover(self, id_reserva, nuevo_inicio, nuevo_fin):
        # TODO 3: cambia la franja de una reserva existente, con las mismas
        # dos reglas, sin comparar la reserva consigo misma.
        # Si el id no existe: ValueError("reserva desconocida").
        raise NotImplementedError

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
