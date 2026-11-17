"""Pruebas de aceptacion del Ejercicio 2. No las abras ni las corras hasta
terminar la lista de test_cupos_ejercicio2.py: son la especificacion
completa, escrita por otra persona, y sirven para saber si tus pruebas
dejaron algo afuera. No las modifiques.

    pytest test_aceptacion_cupos.py
"""

import pytest

from cupos_ejercicio2 import CupoSemanal


def test_el_cupo_es_de_tres_por_semana():
    cupo = CupoSemanal()
    cupo.registrar("r1", "ana", "2026-11-16")
    cupo.registrar("r2", "ana", "2026-11-18")
    assert cupo.puede_reservar("ana", "2026-11-22")
    cupo.registrar("r3", "ana", "2026-11-22")
    assert not cupo.puede_reservar("ana", "2026-11-20")


def test_el_domingo_y_el_lunes_siguiente_son_semanas_distintas():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar("r" + str(i), "ana", "2026-11-22")
    assert not cupo.puede_reservar("ana", "2026-11-22")
    assert cupo.puede_reservar("ana", "2026-11-23")


def test_el_cupo_es_por_estudiante():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar("r" + str(i), "ana", "2026-11-17")
    assert cupo.puede_reservar("beto", "2026-11-17")


def test_cancelar_libera_y_se_puede_volver_a_reservar():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar("r" + str(i), "ana", "2026-11-17")
    cupo.cancelar("r1")
    assert cupo.puede_reservar("ana", "2026-11-19")
    cupo.registrar("r9", "ana", "2026-11-19")
    assert not cupo.puede_reservar("ana", "2026-11-19")


def test_cancelar_en_una_semana_no_libera_otra():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar("a" + str(i), "ana", "2026-11-17")
    cupo.registrar("b0", "ana", "2026-11-24")
    cupo.cancelar("b0")
    assert not cupo.puede_reservar("ana", "2026-11-17")


def test_equipo_oficial_tiene_seis():
    cupo = CupoSemanal()
    cupo.registrar_equipo_oficial("futbol-usfq")
    for i in range(6):
        assert cupo.puede_reservar("futbol-usfq", "2026-11-17")
        cupo.registrar("f" + str(i), "futbol-usfq", "2026-11-17")
    assert not cupo.puede_reservar("futbol-usfq", "2026-11-17")


def test_registrar_sin_cupo_lanza_y_no_registra():
    cupo = CupoSemanal()
    for i in range(3):
        cupo.registrar("r" + str(i), "ana", "2026-11-17")
    with pytest.raises(ValueError, match="cupo semanal agotado"):
        cupo.registrar("r3", "ana", "2026-11-18")
    cupo.cancelar("r0")
    assert cupo.puede_reservar("ana", "2026-11-18")
    cupo.registrar("r4", "ana", "2026-11-18")
    assert not cupo.puede_reservar("ana", "2026-11-18")


def test_cancelar_una_reserva_desconocida_lanza():
    cupo = CupoSemanal()
    with pytest.raises(ValueError):
        cupo.cancelar("no-existe")
