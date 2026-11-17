import pytest

from calendario_eventos import CalendarioConEventos
from canales_ejercicio1 import Canales, PublicadorDeDisponibilidad, tema_de
from conexiones import ConexionSimulada

FECHA = "2026-11-10"
TEMA_1 = "cancha-1/2026-11-10"
TEMA_2 = "cancha-2/2026-11-10"


def test_publicar_llega_solo_a_los_suscritos_del_tema():
    canales = Canales()
    a = ConexionSimulada("ana")
    b = ConexionSimulada("beto")
    canales.suscribir(TEMA_1, a)
    canales.suscribir(TEMA_2, b)
    assert canales.publicar(TEMA_1, "hola") == 1
    assert a.recibidos == ["hola"]
    assert b.recibidos == []


def test_un_tema_sin_suscriptores():
    canales = Canales()
    assert canales.publicar(TEMA_1, "hola") == 0
    assert canales.suscriptores(TEMA_1) == 0


def test_suscribir_dos_veces_recibe_una():
    canales = Canales()
    a = ConexionSimulada("ana")
    canales.suscribir(TEMA_1, a)
    canales.suscribir(TEMA_1, a)
    canales.publicar(TEMA_1, "hola")
    assert a.recibidos == ["hola"]


def test_desuscribir():
    canales = Canales()
    a = ConexionSimulada("ana")
    canales.suscribir(TEMA_1, a)
    canales.desuscribir(TEMA_1, a)
    canales.desuscribir(TEMA_2, a)
    assert canales.publicar(TEMA_1, "hola") == 0
    assert a.recibidos == []


def test_una_conexion_cerrada_no_cuenta_como_entregada():
    canales = Canales()
    a = ConexionSimulada("ana")
    b = ConexionSimulada("beto")
    canales.suscribir(TEMA_1, a)
    canales.suscribir(TEMA_1, b)
    b.cerrar()
    assert canales.publicar(TEMA_1, "hola") == 1


def test_el_calendario_publica_en_su_tema():
    canales = Canales()
    publicador = PublicadorDeDisponibilidad(canales, FECHA)
    calendario = CalendarioConEventos("cancha-1", FECHA)
    calendario.suscribir("ocupada", publicador)
    calendario.suscribir("liberada", publicador)
    a = ConexionSimulada("ana")
    otra = ConexionSimulada("beto")
    canales.suscribir(tema_de("cancha-1", FECHA), a)
    canales.suscribir(TEMA_2, otra)
    calendario.reservar("r-1", "carla", 18, 20)
    calendario.cancelar("r-1")
    assert a.recibidos == ["ocupada 18-20", "libre 18-20"]
    assert otra.recibidos == []
    assert publicador.ultimos_entregados == 1


def test_una_reserva_rechazada_no_publica():
    canales = Canales()
    publicador = PublicadorDeDisponibilidad(canales, FECHA)
    calendario = CalendarioConEventos("cancha-1", FECHA)
    calendario.suscribir("ocupada", publicador)
    a = ConexionSimulada("ana")
    canales.suscribir(TEMA_1, a)
    calendario.reservar("r-1", "carla", 18, 19)
    with pytest.raises(ValueError):
        calendario.reservar("r-2", "dani", 18, 19)
    assert a.recibidos == ["ocupada 18-19"]
