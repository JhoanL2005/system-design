"""La suite de pruebas que ReservaU heredo del equipo anterior. No la
modifiques: el Ejercicio 1 la clasifica y la mide.

    pytest test_suite_heredada.py --durations=0
"""

from dominio import puntos_por_cancelar, semana_de
from entorno_e2e import NavegadorSimulado


def test_reservar_una_cancha():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    assert navegador.reservar("r1", "2026-11-17")["estado"] == 201


def test_la_cuarta_reserva_de_la_semana_se_rechaza():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-16")
    navegador.reservar("r2", "2026-11-17")
    navegador.reservar("r3", "2026-11-18")
    respuesta = navegador.reservar("r4", "2026-11-19")
    assert respuesta["estado"] == 409
    assert respuesta["cuerpo"]["error"] == "cupo semanal agotado"


def test_otra_semana_tiene_cupo_nuevo():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-20")
    navegador.reservar("r2", "2026-11-21")
    navegador.reservar("r3", "2026-11-22")
    assert navegador.reservar("r4", "2026-11-23")["estado"] == 201


def test_el_cupo_es_de_cada_estudiante():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-16")
    navegador.reservar("r2", "2026-11-17")
    navegador.reservar("r3", "2026-11-18")
    navegador.iniciar_sesion("beto")
    assert navegador.reservar("r4", "2026-11-18")["estado"] == 201


def test_cancelar_una_reserva():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-17")
    assert navegador.cancelar("r1", 3000)["estado"] == 200


def test_cancelar_tarde_suma_puntos():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-17")
    navegador.cancelar("r1", 30)
    assert navegador.ver_puntos() == 2


def test_cancelar_con_tiempo_no_suma_puntos():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-17")
    navegador.cancelar("r1", 3000)
    assert navegador.ver_puntos() == 0


def test_tres_puntos_bloquean():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-17")
    navegador.cancelar("r1", 30)
    navegador.reservar("r2", "2026-11-18")
    navegador.cancelar("r2", 600)
    respuesta = navegador.reservar("r3", "2026-11-19")
    assert respuesta["estado"] == 409
    assert respuesta["cuerpo"]["error"] == "estudiante bloqueado"


def test_cancelar_una_reserva_que_no_existe():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    assert navegador.cancelar("no-existe", 3000)["estado"] == 404


def test_cancelar_libera_el_cupo():
    navegador = NavegadorSimulado()
    navegador.iniciar_sesion("ana")
    navegador.reservar("r1", "2026-11-16")
    navegador.reservar("r2", "2026-11-17")
    navegador.reservar("r3", "2026-11-18")
    navegador.cancelar("r3", 3000)
    assert navegador.reservar("r4", "2026-11-19")["estado"] == 201


def test_la_semana_va_de_lunes_a_domingo():
    assert semana_de("2026-11-16") == semana_de("2026-11-22")
    assert semana_de("2026-11-22") != semana_de("2026-11-23")


def test_los_tramos_de_puntos():
    assert puntos_por_cancelar(1440) == 0
    assert puntos_por_cancelar(120) == 1
    assert puntos_por_cancelar(119) == 2
