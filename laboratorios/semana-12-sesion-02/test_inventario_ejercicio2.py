import pytest

from inventario_ejercicio2 import Grupo, Reservable, armar_campus, reservar_en


def test_una_hoja():
    proyector = Reservable("proyector-1", "proyector")
    assert proyector.buscar("proyector", 18, 19) == ["proyector-1"]
    assert proyector.buscar("sala", 18, 19) == []
    assert proyector.contar("proyector") == 1
    assert proyector.contar("sala") == 0
    proyector.reservar("r-1", "ana", 18, 19)
    assert proyector.buscar("proyector", 18, 19) == []


def test_buscar_por_tipo_en_todo_el_campus():
    campus = armar_campus()
    assert campus.buscar("proyector", 18, 19) == ["proyector-1", "proyector-2"]
    assert campus.buscar("cancha", 9, 10) == ["cancha-1", "cancha-2"]
    assert campus.buscar("casillero", 9, 10) == []


def test_contar():
    campus = armar_campus()
    assert campus.contar("balon") == 2
    assert campus.contar("sala") == 2
    assert campus.contar("casillero") == 0
    assert Grupo("vacio").contar("sala") == 0


def test_encontrar_en_cualquier_nivel():
    campus = armar_campus()
    assert campus.encontrar("balon-2").nombre == "balon-2"
    assert campus.encontrar("sala-101").tipo == "sala"
    assert campus.encontrar("proyector-9") is None


def test_reservar_por_nombre_cambia_la_busqueda():
    campus = armar_campus()
    reservar_en(campus, "proyector-1", "r-1", "ana", 18, 19)
    assert campus.buscar("proyector", 18, 19) == ["proyector-2"]
    assert campus.buscar("proyector", 9, 10) == ["proyector-1", "proyector-2"]
    with pytest.raises(ValueError, match="recurso desconocido"):
        reservar_en(campus, "proyector-9", "r-2", "ana", 18, 19)


def test_rutas_desde_la_raiz_y_desde_un_subarbol():
    campus = armar_campus()
    reservar_en(campus, "balon-1", "r-1", "beto", 18, 19)
    assert campus.rutas("balon", 18, 19, "") == ["Campus Cumbaya / Complejo deportivo / Bodega / balon-2"]
    biblioteca = campus.hijos[1]
    assert biblioteca.rutas("proyector", 18, 19, "") == [
        "Biblioteca / Prestamos / proyector-1",
        "Biblioteca / Prestamos / proyector-2",
    ]


def test_un_tipo_nuevo_no_cambia_ningun_metodo():
    campus = armar_campus()
    casilleros = Grupo("Casilleros")
    casilleros.agregar(Reservable("casillero-1", "casillero"))
    campus.hijos[1].agregar(casilleros)
    assert campus.buscar("casillero", 9, 10) == ["casillero-1"]
    assert campus.rutas("casillero", 9, 10, "") == ["Campus Cumbaya / Biblioteca / Casilleros / casillero-1"]
