"""Ejercicio 3: reservas recurrentes, con TDD en pareja.

Los equipos de ReservaU entrenan siempre el mismo dia a la misma hora, y
hoy tienen que reservar semana por semana. La funcionalidad nueva:
reservar la misma franja cada semana, durante varias semanas, de una vez.

AgendaDeCancha(cancha) guarda un CalendarioDeCancha (reservas.py, no lo
modifiques) por cada fecha, y lo crea la primera vez que se pide.

- calendario(fecha): el CalendarioDeCancha de esa fecha.
- reservar_cada_semana(id_base, estudiante, fecha_inicial, inicio, fin,
  semanas): intenta reservar la franja en fecha_inicial y en la misma
  fecha de las semanas siguientes (fecha_inicial + 7 dias, + 14, ...),
  hasta completar `semanas` intentos. Devuelve una lista con un par
  (fecha, resultado) por semana, en orden. El resultado es:
    - "reservada", si se reservo, con id id_base + "-" + el numero de
      semana, empezando en 1 ("entreno-1", "entreno-2", ...);
    - "ocupada", si la franja ya estaba reservada esa fecha (esa semana se
      salta, y las demas siguen);
    - "limite", si con esa reserva el estudiante pasaria el maximo de
      horas por dia (MAXIMO_HORAS_POR_ESTUDIANTE).
  semanas tiene que estar entre 1 y 12; si no, ValueError, sin reservar
  nada.

No hay codigo ni pruebas de partida. Trabajen en pareja, en ping-pong: una
persona escribe una prueba que falla, la otra escribe el codigo minimo
que la hace pasar y despues la siguiente prueba, y asi, cambiando de rol.
Refactoricen con todas las pruebas en verde. Antes de escribir la primera
prueba, escriban su lista de pruebas en el README.

Para sumar 7 dias a una fecha "AAAA-MM-DD":

    from datetime import date, timedelta
    (date.fromisoformat(fecha) + timedelta(days=7)).isoformat()

Corran las pruebas con:

    pytest test_recurrentes_ejercicio3.py
"""
