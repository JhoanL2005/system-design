"""Ejercicio 1: un value object y una entidad de ReservaU.

- FranjaHoraria: una franja de una cancha en un dia, de la hora inicio a
  la hora fin (fin no incluida: de 18 a 19 es una hora). Dos franjas con
  los mismos datos son la misma franja.
- Reserva: una reserva concreta, con su id. Dos reservas con el mismo id
  son la misma reserva, aunque se haya movido a otra franja.

Corre esto para ver el resultado:

    python3 franja_ejercicio1.py

Y las pruebas con:

    pytest test_franja_ejercicio1.py
"""

HORA_DE_APERTURA = 7
HORA_DE_CIERRE = 21


# TODO 1: convierte FranjaHoraria en un value object inmutable con
# @dataclass(frozen=True) (from dataclasses import dataclass), con tres
# campos: fecha (str), inicio (int) y fin (int). Borra el __init__: el
# decorador lo genera.
class FranjaHoraria:
    def __init__(self, fecha, inicio, fin):
        self.fecha = fecha
        self.inicio = inicio
        self.fin = fin

    # TODO 2: un metodo __post_init__(self) que lance
    # ValueError("franja invalida") si inicio no es menor que fin, si
    # inicio es menor que HORA_DE_APERTURA o si fin es mayor que
    # HORA_DE_CIERRE.

    def duracion(self):
        return self.fin - self.inicio

    def se_solapa_con(self, otra):
        # TODO 3: True si las dos franjas son del mismo dia y comparten al
        # menos una parte de su intervalo. De 18 a 19 y de 19 a 20 no se
        # solapan.
        return False


class Reserva:
    def __init__(self, id_reserva, estudiante, franja):
        self.id = id_reserva
        self.estudiante = estudiante
        self.franja = franja

    # TODO 4: un metodo __eq__(self, otra) que compare solo los ids, y un
    # metodo __hash__(self) que devuelva hash(self.id).


if __name__ == "__main__":
    franja_a = FranjaHoraria("2026-11-10", 18, 19)
    franja_b = FranjaHoraria("2026-11-10", 18, 19)
    print("franja_a == franja_b:", franja_a == franja_b)
    print("Se solapan 18-20 y 19-21:", FranjaHoraria("2026-11-10", 18, 20).se_solapa_con(FranjaHoraria("2026-11-10", 19, 21)))
    print("Se solapan 18-19 y 19-20:", FranjaHoraria("2026-11-10", 18, 19).se_solapa_con(FranjaHoraria("2026-11-10", 19, 20)))

    reserva = Reserva("r-1", "ana", franja_a)
    la_misma_leida_otra_vez = Reserva("r-1", "ana", FranjaHoraria("2026-11-10", 9, 10))
    otra_igualita = Reserva("r-2", "ana", franja_a)
    print("r-1 == r-1 movida:", reserva == la_misma_leida_otra_vez)
    print("r-1 == r-2 en la misma franja:", reserva == otra_igualita)

    franja_invalida = FranjaHoraria("2026-11-10", 20, 18)
    print("Franja de 20 a 18, duracion:", franja_invalida.duracion())
