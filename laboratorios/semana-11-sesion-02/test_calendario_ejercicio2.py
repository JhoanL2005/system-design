import pytest

from calendario_ejercicio2 import CalendarioDeCancha
from franja_ejercicio1 import FranjaHoraria


def calendario():
    return CalendarioDeCancha("cancha-1", "2026-11-10")


def test_reservar_y_listar_en_orden():
    c = calendario()
    c.reservar("r-2", "beto", 18, 19)
    c.reservar("r-1", "ana", 9, 10)
    assert c.reservas() == [
        ("r-1", "ana", FranjaHoraria("2026-11-10", 9, 10)),
        ("r-2", "beto", FranjaHoraria("2026-11-10", 18, 19)),
    ]


def test_no_se_solapan():
    c = calendario()
    c.reservar("r-1", "ana", 18, 20)
    with pytest.raises(ValueError, match="franja ocupada"):
        c.reservar("r-2", "beto", 19, 20)
    c.reservar("r-3", "beto", 20, 21)
    assert len(c.reservas()) == 2


def test_limite_de_horas_por_estudiante():
    c = calendario()
    c.reservar("r-1", "ana", 8, 9)
    with pytest.raises(ValueError, match="limite de horas alcanzado"):
        c.reservar("r-2", "ana", 10, 12)
    c.reservar("r-3", "ana", 10, 11)
    assert c.horas_de("ana") == 2
    assert c.horas_de("beto") == 0


def test_id_repetido():
    c = calendario()
    c.reservar("r-1", "ana", 8, 9)
    with pytest.raises(ValueError, match="id repetido"):
        c.reservar("r-1", "beto", 10, 11)


def test_una_franja_invalida_no_entra():
    c = calendario()
    with pytest.raises(ValueError, match="franja invalida"):
        c.reservar("r-1", "ana", 20, 22)
    assert c.reservas() == []


def test_el_orden_de_las_verificaciones():
    c = calendario()
    c.reservar("r-1", "ana", 8, 10)
    with pytest.raises(ValueError, match="id repetido"):
        c.reservar("r-1", "ana", 9, 10)
    with pytest.raises(ValueError, match="franja ocupada"):
        c.reservar("r-2", "ana", 9, 10)


def test_mover_respeta_las_reglas_y_no_choca_consigo_misma():
    c = calendario()
    c.reservar("r-1", "ana", 18, 20)
    c.reservar("r-2", "beto", 15, 16)
    c.mover("r-1", 19, 21)
    assert c.reservas()[1] == ("r-1", "ana", FranjaHoraria("2026-11-10", 19, 21))
    with pytest.raises(ValueError, match="franja ocupada"):
        c.mover("r-1", 15, 17)
    with pytest.raises(ValueError, match="reserva desconocida"):
        c.mover("r-9", 8, 9)


def test_mover_no_permite_pasar_el_limite():
    c = calendario()
    c.reservar("r-1", "ana", 8, 9)
    c.reservar("r-2", "ana", 12, 13)
    with pytest.raises(ValueError, match="limite de horas alcanzado"):
        c.mover("r-1", 8, 10)
    c.mover("r-1", 9, 10)
    assert c.horas_de("ana") == 2


def test_una_operacion_rechazada_no_cambia_nada():
    c = calendario()
    c.reservar("r-1", "ana", 18, 19)
    antes = c.reservas()
    with pytest.raises(ValueError):
        c.mover("r-1", 6, 8)
    with pytest.raises(ValueError):
        c.reservar("r-2", "ana", 18, 20)
    assert c.reservas() == antes


def test_cancelar():
    c = calendario()
    c.reservar("r-1", "ana", 18, 19)
    c.cancelar("r-1")
    assert c.reservas() == []
    c.reservar("r-2", "beto", 18, 19)
    with pytest.raises(ValueError, match="reserva desconocida"):
        c.cancelar("r-1")


def test_lo_que_devuelve_reservas_no_cambia_el_calendario():
    c = calendario()
    c.reservar("r-1", "ana", 18, 19)
    lista = c.reservas()
    lista.append(("r-9", "intruso", FranjaHoraria("2026-11-10", 18, 19)))
    lista.clear()
    assert len(c.reservas()) == 1
