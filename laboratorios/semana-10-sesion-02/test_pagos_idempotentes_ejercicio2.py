from dominio import PasarelaDePagos, RepositorioDeReservas
from http_simulado import Cliente, RedInestable, Solicitud
from pagos_idempotentes_ejercicio2 import ApiDePagos


def armar():
    repositorio = RepositorioDeReservas()
    pasarela = PasarelaDePagos()
    reserva = repositorio.crear("ana", "cancha-1", "2026-11-02", 18)
    return ApiDePagos(repositorio, pasarela), pasarela, reserva["id"]


def test_sin_clave_responde_400_y_no_cobra():
    api, pasarela, id_reserva = armar()
    respuesta = api.manejar(Solicitud("POST", "/v1/pagos", {"reserva_id": id_reserva, "monto": 5.0}))
    assert respuesta.estado == 400
    assert len(pasarela.cobros) == 0


def test_con_la_red_perdiendo_tres_respuestas_cobra_una_sola_vez():
    api, pasarela, id_reserva = armar()
    cliente = Cliente(RedInestable(api, respuestas_a_perder=3))
    respuesta = cliente.enviar("POST", "/v1/pagos", {"reserva_id": id_reserva, "monto": 5.0},
                               {"Idempotency-Key": "pago-ana-r1"})
    assert respuesta.estado == 201
    assert respuesta.cuerpo == {"id": "cobro-1", "reserva_id": id_reserva, "monto": 5.0}
    assert len(pasarela.cobros) == 1


def test_la_misma_clave_devuelve_la_misma_respuesta():
    api, pasarela, id_reserva = armar()
    cuerpo = {"reserva_id": id_reserva, "monto": 5.0}
    primera = api.manejar(Solicitud("POST", "/v1/pagos", cuerpo, {"Idempotency-Key": "k1"}))
    segunda = api.manejar(Solicitud("POST", "/v1/pagos", cuerpo, {"Idempotency-Key": "k1"}))
    assert segunda.estado == primera.estado == 201
    assert segunda.cuerpo == primera.cuerpo


def test_claves_distintas_son_dos_pagos_distintos():
    api, pasarela, id_reserva = armar()
    cuerpo = {"reserva_id": id_reserva, "monto": 5.0}
    api.manejar(Solicitud("POST", "/v1/pagos", cuerpo, {"Idempotency-Key": "k1"}))
    api.manejar(Solicitud("POST", "/v1/pagos", cuerpo, {"Idempotency-Key": "k2"}))
    assert len(pasarela.cobros) == 2


def test_la_misma_clave_con_otro_cuerpo_es_422():
    api, pasarela, id_reserva = armar()
    api.manejar(Solicitud("POST", "/v1/pagos", {"reserva_id": id_reserva, "monto": 5.0}, {"Idempotency-Key": "k1"}))
    respuesta = api.manejar(Solicitud("POST", "/v1/pagos", {"reserva_id": id_reserva, "monto": 50.0}, {"Idempotency-Key": "k1"}))
    assert respuesta.estado == 422
    assert len(pasarela.cobros) == 1


def test_una_reserva_que_no_existe_es_404_y_no_cobra():
    api, pasarela, id_reserva = armar()
    respuesta = api.manejar(Solicitud("POST", "/v1/pagos", {"reserva_id": "r-99", "monto": 5.0}, {"Idempotency-Key": "k1"}))
    assert respuesta.estado == 404
    assert len(pasarela.cobros) == 0
