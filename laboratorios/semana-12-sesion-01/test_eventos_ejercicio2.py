import pytest

from espera_ejercicio1 import ListaDeEspera
from eventos_ejercicio2 import CacheDeDisponibilidad, CalendarioConEventos, ObservadorDeReservas, RegistroDeAuditoria
from notificaciones import NotificadorEnMemoria
from reservas import FranjaHoraria

DIECIOCHO = FranjaHoraria("2026-11-10", 18, 19)


class Contador(ObservadorDeReservas):
    def __init__(self):
        self.ocupadas = 0
        self.liberadas = 0

    def al_ocuparse(self, cancha, franja):
        self.ocupadas = self.ocupadas + 1

    def al_liberarse(self, cancha, franja):
        self.liberadas = self.liberadas + 1


def calendario():
    return CalendarioConEventos("cancha-1", "2026-11-10")


def test_evento_desconocido():
    c = calendario()
    with pytest.raises(ValueError, match="evento desconocido"):
        c.suscribir("movida", Contador())


def test_cada_observador_recibe_solo_sus_eventos():
    c = calendario()
    solo_ocupada = Contador()
    los_dos = Contador()
    c.suscribir("ocupada", solo_ocupada)
    c.suscribir("ocupada", los_dos)
    c.suscribir("liberada", los_dos)
    c.reservar("r-1", "ana", 18, 19)
    c.cancelar("r-1")
    assert (solo_ocupada.ocupadas, solo_ocupada.liberadas) == (1, 0)
    assert (los_dos.ocupadas, los_dos.liberadas) == (1, 1)


def test_suscribir_dos_veces_avisa_una():
    c = calendario()
    contador = Contador()
    c.suscribir("ocupada", contador)
    c.suscribir("ocupada", contador)
    c.reservar("r-1", "ana", 18, 19)
    assert contador.ocupadas == 1


def test_desuscribir():
    c = calendario()
    contador = Contador()
    c.suscribir("liberada", contador)
    c.desuscribir("liberada", contador)
    c.reservar("r-1", "ana", 18, 19)
    c.cancelar("r-1")
    assert contador.liberadas == 0


def test_una_reserva_rechazada_no_avisa():
    c = calendario()
    contador = Contador()
    c.suscribir("ocupada", contador)
    c.reservar("r-1", "ana", 18, 19)
    with pytest.raises(ValueError, match="franja ocupada"):
        c.reservar("r-2", "beto", 18, 19)
    assert contador.ocupadas == 1


def test_la_cache_no_recalcula_si_nada_cambio():
    c = calendario()
    cache = CacheDeDisponibilidad()
    c.reservar("r-1", "ana", 18, 19)
    assert 18 not in cache.libres(c)
    assert 18 not in cache.libres(c)
    assert cache.calculos == 1


def test_la_cache_se_invalida_con_los_dos_eventos():
    c = calendario()
    cache = CacheDeDisponibilidad()
    c.suscribir("ocupada", cache)
    c.suscribir("liberada", cache)
    assert 18 in cache.libres(c)
    c.reservar("r-1", "ana", 18, 19)
    assert 18 not in cache.libres(c)
    c.cancelar("r-1")
    assert 18 in cache.libres(c)
    assert cache.calculos == 3


def test_la_cache_de_otra_cancha_no_se_toca():
    c1 = calendario()
    c2 = CalendarioConEventos("cancha-2", "2026-11-10")
    cache = CacheDeDisponibilidad()
    c1.suscribir("ocupada", cache)
    cache.libres(c1)
    cache.libres(c2)
    c1.reservar("r-1", "ana", 18, 19)
    cache.libres(c2)
    assert cache.calculos == 2


def test_auditoria():
    c = calendario()
    auditoria = RegistroDeAuditoria()
    c.suscribir("ocupada", auditoria)
    c.suscribir("liberada", auditoria)
    c.reservar("r-1", "ana", 18, 19)
    c.cancelar("r-1")
    assert auditoria.lineas == ["ocupada cancha-1 2026-11-10 18-19", "liberada cancha-1 2026-11-10 18-19"]


def test_la_lista_de_espera_del_ejercicio_1_funciona_con_liberada():
    c = calendario()
    notificador = NotificadorEnMemoria()
    lista = ListaDeEspera(notificador)
    c.suscribir("liberada", lista)
    c.reservar("r-1", "ana", 18, 19)
    lista.anotar("beto", DIECIOCHO)
    c.cancelar("r-1")
    assert notificador.enviados == [("beto", "Se libero cancha-1 el 2026-11-10 de 18 a 19")]
