from actividad import Publicacion
from hibrido_ejercicio2 import FeedHibrido


def armar():
    feed = FeedHibrido(umbral=2)
    for estudiante in ["ana", "beto", "carla"]:
        feed.seguir(estudiante, "final")
    feed.seguir("ana", "futbol")
    feed.seguir("beto", "futbol")
    return feed


def test_masivo():
    feed = armar()
    assert feed.es_masivo("final")
    assert not feed.es_masivo("futbol")
    assert not feed.es_masivo("nadie-lo-sigue")


def test_un_autor_masivo_se_escribe_una_vez():
    feed = armar()
    feed.publicar(Publicacion("p1", "final", 10, "a"))
    assert feed.almacen.escrituras == 1


def test_un_autor_comun_se_copia_a_cada_seguidor():
    feed = armar()
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    assert feed.almacen.escrituras == 2


def test_leer_junta_lo_propio_con_lo_masivo():
    feed = armar()
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    feed.publicar(Publicacion("p2", "final", 20, "b"))
    feed.publicar(Publicacion("p3", "futbol", 30, "c"))
    assert [p.id for p in feed.leer("ana")] == ["p3", "p2", "p1"]
    assert [p.id for p in feed.leer("carla")] == ["p2"]


def test_leer_cuesta_una_lectura_mas_por_cada_masivo_que_sigue():
    feed = armar()
    feed.publicar(Publicacion("p1", "final", 10, "a"))
    feed.leer("ana")
    assert feed.almacen.lecturas == 2


def test_cantidad():
    feed = armar()
    for i in range(4):
        feed.publicar(Publicacion("f" + str(i), "final", i, "x"))
        feed.publicar(Publicacion("c" + str(i), "futbol", 10 + i, "x"))
    assert [p.id for p in feed.leer("ana", 3)] == ["c3", "c2", "c1"]
