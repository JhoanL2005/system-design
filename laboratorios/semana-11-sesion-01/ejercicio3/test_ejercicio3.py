import pytest

from adaptadores import NotificadorEnMemoria, RelojFijo, RepositorioEnMemoria, RepositorioSqlite
from casos_de_uso import CancelarReserva
from dominio import clasificar_cancelacion


def modulos_que_importa(archivo):
    nombres = []
    with open(archivo, encoding="utf-8") as fuente:
        for linea in fuente:
            partes = linea.split()
            if len(partes) >= 2 and (partes[0] == "import" or partes[0] == "from"):
                nombres.append(partes[1].split(".")[0])
    return nombres


def test_clasificar_cancelacion():
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-10", 15) == "a tiempo"
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-10", 16) == "a tiempo"
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-10", 17) == "tardia"
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-10", 18) == "vencida"
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-10", 20) == "vencida"
    assert clasificar_cancelacion("2026-11-10", 7, "2026-11-09", 23) == "a tiempo"
    assert clasificar_cancelacion("2026-11-10", 18, "2026-11-11", 8) == "vencida"


@pytest.fixture(params=["memoria", "sqlite"])
def repositorio(request):
    if request.param == "memoria":
        return RepositorioEnMemoria()
    return RepositorioSqlite(":memory:")


def test_el_repositorio_cumple_el_puerto(repositorio):
    reserva = repositorio.agregar("ana", "cancha-1", "2026-11-10", 18)
    assert reserva.id == "r-1"
    assert repositorio.agregar("beto", "cancha-2", "2026-11-10", 9).id == "r-2"
    encontrada = repositorio.buscar("r-1")
    assert (encontrada.estudiante, encontrada.cancha, encontrada.fecha, encontrada.hora) == ("ana", "cancha-1", "2026-11-10", 18)
    assert repositorio.buscar("r-9") is None
    repositorio.borrar("r-1")
    assert repositorio.buscar("r-1") is None
    assert repositorio.buscar("r-2") is not None
    assert repositorio.penalizaciones_de("ana") == 0
    repositorio.registrar_penalizacion("ana")
    repositorio.registrar_penalizacion("ana")
    assert repositorio.penalizaciones_de("ana") == 2


def armar(repositorio, fecha, hora):
    notificador = NotificadorEnMemoria()
    caso = CancelarReserva(repositorio, RelojFijo(fecha, hora), notificador)
    return caso, notificador


def test_cancelar_a_tiempo(repositorio):
    reserva = repositorio.agregar("ana", "cancha-1", "2026-11-10", 18)
    caso, notificador = armar(repositorio, "2026-11-10", 15)
    assert caso.ejecutar(reserva.id, "ana") == {"estado": "cancelada", "penalizacion": False}
    assert repositorio.buscar(reserva.id) is None
    assert repositorio.penalizaciones_de("ana") == 0
    assert notificador.enviados == [("ana", "Reserva r-1 cancelada")]


def test_cancelar_tarde_penaliza(repositorio):
    reserva = repositorio.agregar("beto", "cancha-2", "2026-11-10", 18)
    caso, notificador = armar(repositorio, "2026-11-10", 17)
    assert caso.ejecutar(reserva.id, "beto") == {"estado": "cancelada", "penalizacion": True}
    assert repositorio.buscar(reserva.id) is None
    assert repositorio.penalizaciones_de("beto") == 1
    assert notificador.enviados == [("beto", "Reserva r-1 cancelada con penalizacion por aviso tardio")]


def test_no_se_cancela_una_reserva_que_ya_empezo(repositorio):
    reserva = repositorio.agregar("ana", "cancha-1", "2026-11-10", 18)
    caso, notificador = armar(repositorio, "2026-11-10", 18)
    assert caso.ejecutar(reserva.id, "ana") == {"estado": "rechazada", "motivo": "la reserva ya empezo"}
    assert repositorio.buscar(reserva.id) is not None
    assert notificador.enviados == []


def test_solo_el_dueno_cancela(repositorio):
    reserva = repositorio.agregar("ana", "cancha-1", "2026-11-10", 18)
    caso, notificador = armar(repositorio, "2026-11-10", 9)
    assert caso.ejecutar(reserva.id, "beto") == {"estado": "rechazada", "motivo": "no es tu reserva"}
    assert repositorio.buscar(reserva.id) is not None
    assert notificador.enviados == []


def test_una_reserva_que_no_existe(repositorio):
    caso, notificador = armar(repositorio, "2026-11-10", 9)
    assert caso.ejecutar("r-9", "ana") == {"estado": "rechazada", "motivo": "reserva desconocida"}
    assert notificador.enviados == []


def test_el_dominio_no_importa_nada():
    assert modulos_que_importa("dominio.py") == []


def test_el_caso_de_uso_solo_conoce_el_dominio():
    assert modulos_que_importa("casos_de_uso.py") == ["dominio"]
