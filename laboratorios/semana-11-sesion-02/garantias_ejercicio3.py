"""Ejercicio 3: la garantia de una reserva, en el contexto de Pagos.

Al reservar, ReservaU retiene una garantia en la tarjeta del estudiante.
Despues pasa una de dos cosas, una sola vez: se devuelve completa (el
estudiante jugo o cancelo a tiempo), o se cobra una parte o el total (no se
presento). En Pagos al estudiante se le llama titular: es la persona que
paga, no la que juega.

Dinero: value object inmutable con dos campos, centavos (int) y moneda
(str, tres letras, como "USD"). Se usa en centavos para no sumar dolares
con decimales de punto flotante.
- Al crearse: centavos negativo, ValueError("monto negativo"); moneda que
  no tiene exactamente tres letras, ValueError("moneda invalida").
- sumar(otro) y restar(otro): un Dinero nuevo. Con monedas distintas,
  ValueError("monedas distintas"). Si restar daria negativo, el
  ValueError("monto negativo") del propio Dinero.
- es_mayor_que(otro): True o False. Con monedas distintas, ValueError.
- texto(): por ejemplo "USD 5.00" o "USD 12.05".

GarantiaDeReserva: la raiz de un agregado. Se construye con
(id_garantia, id_reserva, titular, monto); id_reserva es el texto "r-1",
no un objeto Reserva. Empieza con estado "retenida" y cobrado igual a 0
en la moneda del monto.
- devolver(): pasa a "devuelta" y devuelve el Dinero a reintegrar.
- cobrar(monto_cobrado): pasa a "cobrada", guarda monto_cobrado en
  cobrado, y devuelve el Dinero a reintegrar (el monto menos lo cobrado).
  Si monto_cobrado es mayor que el monto, ValueError("el cobro supera la
  garantia").
- Si la garantia ya no esta "retenida", devolver() y cobrar() lanzan
  ValueError("la garantia ya fue resuelta").
- Dos garantias con el mismo id_garantia son la misma garantia.
Cuando un metodo lanza, la garantia queda exactamente como estaba.

Corre las pruebas con:

    pytest test_garantias_ejercicio3.py
"""

from dataclasses import dataclass


RETENIDA = "retenida"
DEVUELTA = "devuelta"
COBRADA = "cobrada"


@dataclass(frozen=True)
class Dinero:
    """Value object: un monto en centavos y su moneda. Inmutable."""

    centavos: int
    moneda: str

    def __post_init__(self):
        if self.centavos < 0:
            raise ValueError("monto negativo")
        if not (isinstance(self.moneda, str) and len(self.moneda) == 3 and self.moneda.isalpha()):
            raise ValueError("moneda invalida")

    def _verificar_misma_moneda(self, otro):
        if self.moneda != otro.moneda:
            raise ValueError("monedas distintas")

    def sumar(self, otro):
        self._verificar_misma_moneda(otro)
        return Dinero(self.centavos + otro.centavos, self.moneda)

    def restar(self, otro):
        self._verificar_misma_moneda(otro)
        # Si da negativo, el propio Dinero lanza ValueError("monto negativo").
        return Dinero(self.centavos - otro.centavos, self.moneda)

    def es_mayor_que(self, otro):
        self._verificar_misma_moneda(otro)
        return self.centavos > otro.centavos

    def texto(self):
        return f"{self.moneda} {self.centavos // 100}.{self.centavos % 100:02d}"


class GarantiaDeReserva:
    """Raiz del agregado de la garantia, en el contexto de Pagos.

    Guarda la reserva solo por su id (un texto): la Reserva pertenece a otro
    agregado, en otro bounded context.
    """

    def __init__(self, id_garantia, id_reserva, titular, monto):
        self.id_garantia = id_garantia
        self.id_reserva = id_reserva
        self.titular = titular
        self.monto = monto
        self._estado = RETENIDA
        self._cobrado = Dinero(0, monto.moneda)

    # estado y cobrado se leen desde afuera, pero solo cambian por
    # devolver() y cobrar().
    @property
    def estado(self):
        return self._estado

    @property
    def cobrado(self):
        return self._cobrado

    def _verificar_retenida(self):
        if self._estado != RETENIDA:
            raise ValueError("la garantia ya fue resuelta")

    def devolver(self):
        self._verificar_retenida()
        self._estado = DEVUELTA
        return self.monto

    def cobrar(self, monto_cobrado):
        # Primero todas las verificaciones y cuentas; el estado se cambia
        # al final, cuando ya nada puede lanzar.
        self._verificar_retenida()
        if monto_cobrado.es_mayor_que(self.monto):  # lanza si otra moneda
            raise ValueError("el cobro supera la garantia")
        a_reintegrar = self.monto.restar(monto_cobrado)

        self._cobrado = monto_cobrado
        self._estado = COBRADA
        return a_reintegrar

    def __eq__(self, otra):
        if not isinstance(otra, GarantiaDeReserva):
            return NotImplemented
        return self.id_garantia == otra.id_garantia

    def __hash__(self):
        return hash(self.id_garantia)

    def __repr__(self):
        return (
            f"GarantiaDeReserva({self.id_garantia!r}, {self.id_reserva!r}, "
            f"{self.titular!r}, {self.monto.texto()!r}, estado={self._estado!r})"
        )
