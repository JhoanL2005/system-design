from espacios_ejercicio1 import (
    EspacioSimple,
    GrupoDeRecursos,
    armar_campus,
    armar_campus_por_niveles,
    buscar_libres_preguntando,
)


def test_la_busqueda_por_niveles_no_ve_los_pisos():
    assert buscar_libres_preguntando(armar_campus_por_niveles(), 18, 19) == ["cancha-2", "cancha-3"]


def test_un_espacio_simple():
    sala = EspacioSimple("sala-101", 4)
    assert sala.libres(18, 19) == ["sala-101"]
    sala.calendario.reservar("r-1", "ana", 18, 19)
    assert sala.libres(18, 19) == []
    assert sala.libres(9, 10) == ["sala-101"]
    assert sala.capacidad_total() == 4


def test_un_grupo_vacio():
    vacio = GrupoDeRecursos("Edificio en construccion")
    assert vacio.libres(18, 19) == []
    assert vacio.capacidad_total() == 0


def test_el_campus_completo_con_los_pisos():
    campus, biblioteca = armar_campus()
    assert campus.libres(18, 19) == ["cancha-2", "cancha-3", "sala-101", "sala-201"]
    assert campus.libres(9, 10) == ["cancha-1", "cancha-2", "cancha-3", "sala-101", "sala-102", "sala-201"]
    assert campus.capacidad_total() == 52


def test_cualquier_nodo_responde_igual():
    campus, biblioteca = armar_campus()
    assert biblioteca.libres(18, 19) == ["sala-101", "sala-201"]
    assert biblioteca.capacidad_total() == 18


def test_un_nivel_mas_no_cambia_la_busqueda():
    ala = GrupoDeRecursos("Ala norte")
    ala.agregar(EspacioSimple("sala-301", 5))
    piso_3 = GrupoDeRecursos("Piso 3")
    piso_3.agregar(ala)
    campus, biblioteca = armar_campus()
    biblioteca.agregar(piso_3)
    assert campus.libres(18, 19) == ["cancha-2", "cancha-3", "sala-101", "sala-201", "sala-301"]
    assert campus.capacidad_total() == 57


def test_el_grupo_no_pregunta_el_tipo_de_sus_hijos():
    with open("espacios_ejercicio1.py") as archivo:
        codigo = archivo.read()
    parte_b = codigo.split("# ---------------------------------------------------------------- Parte B")[1]
    assert "isinstance" not in parte_b
