"""Ejercicio 2: el pago de la garantia, idempotente con una cabecera
Idempotency-Key.

Corre las pruebas con:

    pytest test_pagos_idempotentes_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from http_simulado import Respuesta


class ApiDePagos:
    def __init__(self, repositorio, pasarela):
        self.repositorio = repositorio
        self.pasarela = pasarela
        self.respuestas_guardadas = {}

    def manejar(self, solicitud):
        if solicitud.metodo == "POST" and solicitud.ruta == "/v1/pagos":
            return self.crear_pago(solicitud)
        return Respuesta(404, {"error": "ruta desconocida"})

    def crear_pago(self, solicitud):
        # TODO: lee la clave con solicitud.cabeceras.get("Idempotency-Key").
        # - Si la solicitud no trae clave, responde 400 con
        #   {"error": "falta Idempotency-Key"}, sin cobrar.
        # - Si la clave ya esta en self.respuestas_guardadas y el cuerpo es
        #   el mismo de la primera vez, devuelve la respuesta guardada, sin
        #   cobrar otra vez. Si el cuerpo es distinto, responde 422 con
        #   {"error": "clave usada con otro cuerpo"}.
        # - Si la clave es nueva: si la reserva no existe, 404 con
        #   {"error": "reserva desconocida"}. Si existe, cobra con
        #   self.pasarela.cobrar(estudiante, monto), arma la respuesta 201
        #   con {"id": id del cobro, "reserva_id": ..., "monto": ...},
        #   guardala junto con el cuerpo de la solicitud, y devuelvela.
        raise NotImplementedError
