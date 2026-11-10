import dataclasses

import pytest

from franja_ejercicio1 import FranjaHoraria, Reserva


def test_dos_franjas_con_los_mismos_datos_son_iguales():
    assert FranjaHoraria("2026-11-10", 18, 19) == FranjaHoraria("2026-11-10", 18, 19)
    assert FranjaHoraria("2026-11-10", 18, 19) != FranjaHoraria("2026-11-11", 18, 19)


def test_una_franja_no_se_puede_modificar():
    franja = FranjaHoraria("2026-11-10", 18, 19)
    with pytest.raises(dataclasses.FrozenInstanceError):
        franja.inicio = 7


def test_una_franja_invalida_no_llega_a_existir():
    with pytest.raises(ValueError):
        FranjaHoraria("2026-11-10", 20, 18)
    with pytest.raises(ValueError):
        FranjaHoraria("2026-11-10", 18, 18)
    with pytest.raises(ValueError):
        FranjaHoraria("2026-11-10", 6, 8)
    with pytest.raises(ValueError):
        FranjaHoraria("2026-11-10", 20, 22)
    assert FranjaHoraria("2026-11-10", 7, 21).duracion() == 14


def test_solapamiento():
    base = FranjaHoraria("2026-11-10", 18, 20)
    assert base.se_solapa_con(FranjaHoraria("2026-11-10", 19, 21))
    assert base.se_solapa_con(FranjaHoraria("2026-11-10", 17, 19))
    assert base.se_solapa_con(FranjaHoraria("2026-11-10", 18, 20))
    assert base.se_solapa_con(FranjaHoraria("2026-11-10", 15, 21))
    assert not base.se_solapa_con(FranjaHoraria("2026-11-10", 20, 21))
    assert not base.se_solapa_con(FranjaHoraria("2026-11-10", 16, 18))
    assert not base.se_solapa_con(FranjaHoraria("2026-11-11", 18, 20))


def test_una_franja_sirve_como_clave_de_diccionario():
    ocupadas = {FranjaHoraria("2026-11-10", 18, 19): "ana"}
    assert ocupadas[FranjaHoraria("2026-11-10", 18, 19)] == "ana"


def test_dos_reservas_con_el_mismo_id_son_la_misma():
    reserva = Reserva("r-1", "ana", FranjaHoraria("2026-11-10", 18, 19))
    movida = Reserva("r-1", "ana", FranjaHoraria("2026-11-10", 9, 10))
    assert reserva == movida


def test_dos_reservas_iguales_con_distinto_id_son_distintas():
    franja = FranjaHoraria("2026-11-10", 18, 19)
    assert Reserva("r-1", "ana", franja) != Reserva("r-2", "ana", franja)


def test_una_reserva_sigue_siendo_la_misma_despues_de_moverla():
    reserva = Reserva("r-1", "ana", FranjaHoraria("2026-11-10", 18, 19))
    vistas = {reserva}
    reserva.franja = FranjaHoraria("2026-11-10", 9, 10)
    assert reserva in vistas
