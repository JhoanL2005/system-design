import pytest

from conexiones import ConexionSimulada
from reconexion_ejercicio3 import CanalConHistorial

TEMA = "cancha-1/2026-11-10"
OTRO = "cancha-2/2026-11-10"


def test_numera_por_tema():
    canal = CanalConHistorial()
    a = ConexionSimulada("ana")
    canal.suscribir(TEMA, a)
    assert canal.publicar(TEMA, "ocupada 18-19") == 1
    assert canal.publicar(OTRO, "ocupada 9-10") == 1
    assert canal.publicar(TEMA, "libre 18-19") == 2
    assert a.recibidos == ["1 ocupada 18-19", "2 libre 18-19"]
    assert canal.ultimo_numero(TEMA) == 2
    assert canal.ultimo_numero("cancha-9/2026-11-10") == 0


def test_reconectar_recupera_lo_que_se_perdio():
    canal = CanalConHistorial()
    a = ConexionSimulada("ana")
    canal.suscribir(TEMA, a)
    canal.publicar(TEMA, "ocupada 18-19")
    a.cerrar()
    canal.publicar(TEMA, "ocupada 9-10")
    canal.publicar(TEMA, "libre 18-19")
    nueva = ConexionSimulada("ana")
    canal.reconectar(TEMA, nueva, 1)
    assert nueva.recibidos == ["2 ocupada 9-10", "3 libre 18-19"]
    canal.publicar(TEMA, "ocupada 20-21")
    assert nueva.recibidos[-1] == "4 ocupada 20-21"


def test_reconectar_al_dia_no_envia_nada():
    canal = CanalConHistorial()
    canal.publicar(TEMA, "ocupada 18-19")
    nueva = ConexionSimulada("ana")
    canal.reconectar(TEMA, nueva, 1)
    assert nueva.recibidos == []
    assert canal.suscriptores(TEMA) == 1


def test_reconectar_a_un_tema_sin_mensajes():
    canal = CanalConHistorial()
    nueva = ConexionSimulada("ana")
    canal.reconectar(TEMA, nueva, 0)
    assert nueva.recibidos == []
    assert canal.suscriptores(TEMA) == 1


def test_el_historial_guarda_solo_los_ultimos():
    canal = CanalConHistorial(historial=3)
    for hora in range(7, 13):
        canal.publicar(TEMA, "ocupada " + str(hora) + "-" + str(hora + 1))
    justo = ConexionSimulada("ana")
    canal.reconectar(TEMA, justo, 3)
    assert justo.recibidos == ["4 ocupada 10-11", "5 ocupada 11-12", "6 ocupada 12-13"]


def test_si_se_perdio_algo_que_ya_no_esta_pide_recargar():
    canal = CanalConHistorial(historial=3)
    for hora in range(7, 13):
        canal.publicar(TEMA, "ocupada " + str(hora) + "-" + str(hora + 1))
    atrasada = ConexionSimulada("ana")
    canal.reconectar(TEMA, atrasada, 2)
    assert atrasada.recibidos == ["recargar"]
    assert canal.suscriptores(TEMA) == 1
    canal.publicar(TEMA, "libre 7-8")
    assert atrasada.recibidos == ["recargar", "7 libre 7-8"]


def test_un_numero_del_futuro():
    canal = CanalConHistorial()
    canal.publicar(TEMA, "ocupada 18-19")
    nueva = ConexionSimulada("ana")
    with pytest.raises(ValueError, match="numero desconocido"):
        canal.reconectar(TEMA, nueva, 5)
    assert canal.suscriptores(TEMA) == 0


def test_los_temas_no_se_mezclan_al_reconectar():
    canal = CanalConHistorial()
    canal.publicar(TEMA, "ocupada 18-19")
    canal.publicar(OTRO, "ocupada 9-10")
    canal.publicar(OTRO, "libre 9-10")
    nueva = ConexionSimulada("ana")
    canal.reconectar(OTRO, nueva, 0)
    assert nueva.recibidos == ["1 ocupada 9-10", "2 libre 9-10"]
