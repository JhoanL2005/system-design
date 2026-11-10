import pytest

from cancha_divisible_ejercicio3 import CanchaDivisible
from inventario_ejercicio2 import armar_campus, reservar_en


def campus_con_cancha_3():
    campus = armar_campus()
    campus.hijos[0].agregar(CanchaDivisible("cancha-3"))
    return campus


def test_libre_completa_y_por_mitades():
    cancha = CanchaDivisible("cancha-3")
    assert cancha.buscar("cancha", 18, 19) == ["cancha-3"]
    assert cancha.buscar("media cancha", 18, 19) == ["cancha-3-a", "cancha-3-b"]
    assert cancha.buscar("sala", 18, 19) == []


def test_contar():
    cancha = CanchaDivisible("cancha-3")
    assert (cancha.contar("cancha"), cancha.contar("media cancha"), cancha.contar("sala")) == (1, 2, 0)


def test_una_mitad_reservada_ocupa_la_completa():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3-a", "r-1", "ana", 18, 19)
    assert campus.buscar("cancha", 18, 19) == ["cancha-1", "cancha-2"]
    assert campus.buscar("media cancha", 18, 19) == ["cancha-3-b"]
    assert "cancha-3" in campus.buscar("cancha", 9, 10)


def test_reservar_la_completa_ocupa_las_dos_mitades():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3", "r-1", "ana", 18, 19)
    assert campus.buscar("media cancha", 18, 19) == []
    assert campus.encontrar("cancha-3-a").calendario.reservas()[0][0] == "r-1-a"
    assert campus.encontrar("cancha-3-b").calendario.reservas()[0][0] == "r-1-b"


def test_no_se_reserva_la_completa_si_una_mitad_esta_ocupada():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3-b", "r-1", "ana", 18, 19)
    with pytest.raises(ValueError, match="franja ocupada"):
        reservar_en(campus, "cancha-3", "r-2", "beto", 18, 19)
    assert campus.encontrar("cancha-3-a").calendario.reservas() == []


def test_el_limite_se_verifica_en_las_dos_mitades_sin_dejar_media_reserva():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3-b", "r-1", "ana", 8, 10)
    with pytest.raises(ValueError, match="limite de horas alcanzado"):
        reservar_en(campus, "cancha-3", "r-2", "ana", 18, 19)
    assert campus.encontrar("cancha-3-a").calendario.reservas() == []


def test_ocupada_se_reporta_antes_que_el_limite():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3-a", "r-1", "ana", 8, 10)
    reservar_en(campus, "cancha-3-b", "r-2", "beto", 18, 19)
    with pytest.raises(ValueError, match="franja ocupada"):
        reservar_en(campus, "cancha-3", "r-3", "ana", 18, 19)


def test_encontrar():
    cancha = CanchaDivisible("cancha-3")
    assert cancha.encontrar("cancha-3") is cancha
    assert cancha.encontrar("cancha-3-b").nombre == "cancha-3-b"
    assert cancha.encontrar("cancha-4") is None


def test_rutas_en_el_campus():
    campus = campus_con_cancha_3()
    reservar_en(campus, "cancha-3-a", "r-1", "ana", 18, 19)
    assert campus.rutas("media cancha", 18, 19, "") == ["Campus Cumbaya / Complejo deportivo / cancha-3 / cancha-3-b"]
    assert campus.rutas("cancha", 9, 10, "")[-1] == "Campus Cumbaya / Complejo deportivo / cancha-3"
