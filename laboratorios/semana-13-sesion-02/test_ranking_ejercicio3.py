from actividad import Publicacion
from ranking_ejercicio3 import OrdenadorDeFeed

AHORA = 10000


def ids(publicaciones):
    return [p.id for p in publicaciones]


def test_puntaje_con_interacciones_equipo_propio_y_horas():
    ordenador = OrdenadorDeFeed({"p1": 40}, {"ana": ["futbol-arq"]})
    viejo_propio = Publicacion("p1", "futbol-arq", AHORA - 125, "Partido")
    assert ordenador.puntaje(viejo_propio, "ana", AHORA) == 41
    assert ordenador.puntaje(viejo_propio, "beto", AHORA) == 41 / 3
    nuevo = Publicacion("p2", "ajedrez", AHORA - 5, "Torneo")
    assert ordenador.puntaje(nuevo, "ana", AHORA) == 1


def test_lo_nuevo_sin_interacciones_queda_debajo_de_tu_partido():
    ordenador = OrdenadorDeFeed({"partido": 40}, {"ana": ["futbol-arq"]})
    partido = Publicacion("partido", "futbol-arq", AHORA - 180, "Partido")
    entrenamiento = Publicacion("entreno", "basquet", AHORA - 5, "Entrenamiento")
    assert ids(ordenador.ordenar([entrenamiento, partido], "ana", AHORA, 10)) == ["partido", "entreno"]


def test_empates_por_momento_y_por_id():
    ordenador = OrdenadorDeFeed({}, {})
    a = Publicacion("b", "x", AHORA - 10, "")
    b = Publicacion("a", "y", AHORA - 10, "")
    c = Publicacion("c", "z", AHORA - 20, "")
    assert ids(ordenador.ordenar([c, a, b], "ana", AHORA, 10)) == ["a", "b", "c"]


def test_cantidad():
    ordenador = OrdenadorDeFeed({"p1": 5, "p2": 3}, {})
    publicaciones = [Publicacion("p" + str(i), "autor-" + str(i), AHORA, "") for i in range(4)]
    assert ids(ordenador.ordenar(publicaciones, "ana", AHORA, 2)) == ["p1", "p2"]


def test_nunca_tres_seguidas_del_mismo_autor():
    ordenador = OrdenadorDeFeed({"a1": 9, "a2": 8, "a3": 7, "b1": 1}, {})
    publicaciones = [
        Publicacion("a1", "futbol", AHORA, ""),
        Publicacion("a2", "futbol", AHORA, ""),
        Publicacion("a3", "futbol", AHORA, ""),
        Publicacion("b1", "basquet", AHORA, ""),
    ]
    assert ids(ordenador.ordenar(publicaciones, "ana", AHORA, 10)) == ["a1", "a2", "b1", "a3"]


def test_si_no_queda_otro_autor_va_igual():
    ordenador = OrdenadorDeFeed({"a1": 9, "a2": 8, "a3": 7}, {})
    publicaciones = [
        Publicacion("a3", "futbol", AHORA, ""),
        Publicacion("a1", "futbol", AHORA, ""),
        Publicacion("a2", "futbol", AHORA, ""),
    ]
    assert ids(ordenador.ordenar(publicaciones, "ana", AHORA, 10)) == ["a1", "a2", "a3"]


def test_ordenar_no_cambia_la_lista_recibida():
    ordenador = OrdenadorDeFeed({}, {})
    publicaciones = [Publicacion("p1", "x", AHORA, ""), Publicacion("p2", "y", AHORA - 60, "")]
    ordenador.ordenar(publicaciones, "ana", AHORA, 1)
    assert ids(publicaciones) == ["p1", "p2"]


def test_espacios_mas_reservados_en_la_ultima_semana():
    ordenador = OrdenadorDeFeed({}, {})
    semana = 7 * 24 * 60
    reservas = [
        ("cancha-1", AHORA - 10),
        ("cancha-1", AHORA - 20),
        ("sala-101", AHORA - 30),
        ("sala-101", AHORA - 40),
        ("cancha-2", AHORA - 50),
        ("cancha-2", AHORA - semana),
        ("cancha-3", AHORA - semana + 1),
        ("cancha-3", AHORA + 5),
    ]
    assert ordenador.espacios_mas_reservados(reservas, AHORA, 3) == [("cancha-1", 2), ("sala-101", 2), ("cancha-2", 1)]
    assert ordenador.espacios_mas_reservados(reservas, AHORA, 10)[-1] == ("cancha-3", 1)
    assert ordenador.espacios_mas_reservados([], AHORA, 3) == []
