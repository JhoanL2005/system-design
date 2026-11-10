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


# TODO: escribe Dinero y GarantiaDeReserva.
