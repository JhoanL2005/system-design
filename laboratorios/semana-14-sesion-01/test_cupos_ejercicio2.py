"""Pruebas del Ejercicio 2. La primera ya esta escrita. Escribe las demas
una a la vez, en este orden, y antes de cada una haz pasar la anterior:

1. Un estudiante sin reservas puede reservar.
2. Con 2 reservas en la semana, todavia puede.
3. Con 3 reservas en la semana, ya no puede.
4. Las reservas de otra semana no cuentan (2026-11-16 y 2026-11-23 son
   lunes de semanas distintas; 2026-11-22 es el domingo de la semana del 16).
5. Cancelar una reserva libera su lugar.
6. Un equipo oficial puede tener 6 reservas en la semana, pero no 7.
7. Registrar la cuarta reserva lanza ValueError (usa pytest.raises), y
   despues de intentarlo el estudiante sigue con 3.

Anota en la bitacora del README, por cada prueba: con que mensaje fallo,
que cambiaste para que pase, y que refactorizaste.
"""

from cupos_ejercicio2 import CupoSemanal


def test_sin_reservas_puede_reservar():
    cupo = CupoSemanal()
    assert cupo.puede_reservar("ana", "2026-11-16")
