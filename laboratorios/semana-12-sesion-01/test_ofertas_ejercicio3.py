import pytest

from eventos_ejercicio2 import CalendarioConEventos
from notificaciones import NotificadorEnMemoria
from ofertas_ejercicio3 import ListaDeEsperaConPlazo
from reloj import RelojSimulado

OFERTA = "Tienes 15 minutos para aceptar cancha-1 2026-11-10 18-19"


def armar(minutos=15):
    reloj = RelojSimulado()
    notificador = NotificadorEnMemoria()
    calendario = CalendarioConEventos("cancha-1", "2026-11-10")
    lista = ListaDeEsperaConPlazo(calendario, notificador, reloj, minutos)
    calendario.suscribir("liberada", lista)
    calendario.suscribir("ocupada", lista)
    calendario.reservar("r-1", "ana", 18, 19)
    return calendario, lista, notificador, reloj


def test_anotar_dos_veces_o_una_franja_libre():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    with pytest.raises(ValueError, match="ya esta en la lista"):
        lista.anotar("beto", 18, 19)
    with pytest.raises(ValueError, match="la franja esta libre"):
        lista.anotar("beto", 9, 10)


def test_al_liberarse_se_ofrece_al_primero():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    assert notificador.enviados == [("beto", OFERTA)]


def test_los_minutos_del_constructor_aparecen_en_el_mensaje():
    calendario, lista, notificador, reloj = armar(minutos=5)
    lista.anotar("beto", 18, 19)
    calendario.cancelar("r-1")
    assert notificador.enviados == [("beto", "Tienes 5 minutos para aceptar cancha-1 2026-11-10 18-19")]


def test_aceptar_a_tiempo_reserva():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    calendario.cancelar("r-1")
    reloj.avanzar(15)
    lista.aceptar("beto", 18, 19, "r-2")
    assert [(r[0], r[1]) for r in calendario.reservas()] == [("r-2", "beto")]
    assert notificador.enviados == [("beto", OFERTA)]


def test_solo_acepta_quien_tiene_la_oferta():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    with pytest.raises(ValueError, match="no tienes una oferta"):
        lista.aceptar("dani", 18, 19, "r-2")
    with pytest.raises(ValueError, match="no tienes una oferta"):
        lista.aceptar("beto", 9, 10, "r-2")


def test_una_oferta_vencida_no_se_acepta_y_pasa_al_siguiente():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    reloj.avanzar(16)
    with pytest.raises(ValueError, match="oferta vencida"):
        lista.aceptar("beto", 18, 19, "r-2")
    lista.revisar_vencidas()
    assert notificador.enviados == [
        ("beto", OFERTA),
        ("beto", "Vencio tu oferta de cancha-1 2026-11-10 18-19"),
        ("dani", OFERTA),
    ]
    reloj.avanzar(10)
    lista.aceptar("dani", 18, 19, "r-2")
    assert [(r[0], r[1]) for r in calendario.reservas()] == [("r-2", "dani")]


def test_revisar_sin_vencidas_no_hace_nada():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    calendario.cancelar("r-1")
    reloj.avanzar(15)
    lista.revisar_vencidas()
    assert notificador.enviados == [("beto", OFERTA)]


def test_quien_pasaria_el_limite_se_salta():
    calendario, lista, notificador, reloj = armar()
    calendario.reservar("r-2", "beto", 8, 10)
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    assert notificador.enviados == [
        ("beto", "No puedes tomar cancha-1 2026-11-10 18-19: pasarias el limite de horas"),
        ("dani", OFERTA),
    ]


def test_una_reserva_directa_cierra_la_oferta():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    calendario.reservar("r-9", "eva", 17, 19)
    assert notificador.enviados == [
        ("beto", OFERTA),
        ("beto", "La franja cancha-1 2026-11-10 18-19 ya no esta disponible"),
    ]
    with pytest.raises(ValueError, match="no tienes una oferta"):
        lista.aceptar("beto", 18, 19, "r-2")


def test_aceptar_no_se_avisa_a_si_mismo_que_la_franja_se_ocupo():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    calendario.cancelar("r-1")
    lista.aceptar("beto", 18, 19, "r-2")
    assert notificador.enviados == [("beto", OFERTA)]


def test_cuando_la_reserva_aceptada_se_cancela_sigue_la_fila():
    calendario, lista, notificador, reloj = armar()
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 18, 19)
    calendario.cancelar("r-1")
    lista.aceptar("beto", 18, 19, "r-2")
    calendario.cancelar("r-2")
    assert notificador.enviados[-1] == ("dani", OFERTA)


def test_una_reserva_rechazada_al_aceptar_no_cierra_otras_ofertas():
    calendario, lista, notificador, reloj = armar()
    calendario.reservar("r-3", "carla", 9, 10)
    lista.anotar("beto", 18, 19)
    lista.anotar("dani", 9, 10)
    calendario.cancelar("r-1")
    calendario.cancelar("r-3")
    lista.aceptar("beto", 18, 19, "r-4")
    lista.aceptar("dani", 9, 10, "r-5")
    assert len(calendario.reservas()) == 2
