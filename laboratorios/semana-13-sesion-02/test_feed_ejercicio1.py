import pytest

from actividad import Publicacion
from feed_ejercicio1 import FeedEnEscritura, FeedEnLectura


@pytest.fixture(params=[FeedEnEscritura, FeedEnLectura])
def feed(request):
    return request.param()


def test_el_feed_muestra_lo_que_sigue_de_lo_mas_nuevo_a_lo_mas_viejo(feed):
    feed.seguir("ana", "futbol")
    feed.seguir("ana", "basquet")
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    feed.publicar(Publicacion("p2", "ajedrez", 20, "b"))
    feed.publicar(Publicacion("p3", "basquet", 30, "c"))
    assert [p.id for p in feed.leer("ana")] == ["p3", "p1"]


def test_cantidad(feed):
    feed.seguir("ana", "futbol")
    for i in range(5):
        feed.publicar(Publicacion("p" + str(i), "futbol", i, "x"))
    assert [p.id for p in feed.leer("ana", 2)] == ["p4", "p3"]


def test_quien_no_sigue_nada(feed):
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    assert feed.leer("beto") == []


def test_en_escritura_cuesta_una_escritura_por_seguidor_y_una_lectura():
    feed = FeedEnEscritura()
    for i in range(10):
        feed.seguir("e" + str(i), "futbol")
        feed.seguir("e" + str(i), "basquet")
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    feed.publicar(Publicacion("p2", "basquet", 20, "b"))
    assert feed.almacen.escrituras == 20
    feed.leer("e0")
    assert feed.almacen.lecturas == 1


def test_en_lectura_cuesta_una_escritura_y_una_lectura_por_seguido():
    feed = FeedEnLectura()
    for i in range(10):
        feed.seguir("e" + str(i), "futbol")
        feed.seguir("e" + str(i), "basquet")
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    feed.publicar(Publicacion("p2", "basquet", 20, "b"))
    assert feed.almacen.escrituras == 2
    feed.leer("e0")
    assert feed.almacen.lecturas == 2


def test_en_escritura_quien_sigue_despues_no_ve_lo_anterior():
    feed = FeedEnEscritura()
    feed.publicar(Publicacion("p1", "futbol", 10, "a"))
    feed.seguir("ana", "futbol")
    feed.publicar(Publicacion("p2", "futbol", 20, "b"))
    assert [p.id for p in feed.leer("ana")] == ["p2"]
