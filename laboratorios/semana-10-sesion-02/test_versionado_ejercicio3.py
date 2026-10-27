from dominio import RepositorioDeReservas
from http_simulado import Cliente, RedInestable, Solicitud
from versionado_ejercicio3 import ApiVersionada

RESERVA_V1 = {"estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}
RESERVA_V2 = {"estudiante": "beto", "cancha": "cancha-2", "fecha": "2026-11-02", "inicio": "09:00", "duracion_min": 60}


def api_nueva():
    return ApiVersionada(RepositorioDeReservas())


def test_el_contrato_de_v1_no_cambia():
    api = api_nueva()
    creada = api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_V1))
    assert creada.estado == 201
    assert creada.cuerpo == {"id": "r-1", "estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}
    leida = api.manejar(Solicitud("GET", "/v1/reservas/r-1"))
    assert leida.cuerpo == creada.cuerpo


def test_v2_crea_con_inicio_y_responde_con_inicio_y_fin():
    respuesta = api_nueva().manejar(Solicitud("POST", "/v2/reservas", RESERVA_V2))
    assert respuesta.estado == 201
    assert respuesta.cuerpo == {"id": "r-1", "estudiante": "beto", "cancha": "cancha-2", "fecha": "2026-11-02",
                                "inicio": "09:00", "fin": "10:00"}


def test_una_reserva_hecha_en_v1_se_lee_en_v2_y_al_reves():
    api = api_nueva()
    api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_V1))
    api.manejar(Solicitud("POST", "/v2/reservas", RESERVA_V2))
    en_v2 = api.manejar(Solicitud("GET", "/v2/reservas/r-1"))
    assert en_v2.estado == 200
    assert en_v2.cuerpo["inicio"] == "18:00"
    assert en_v2.cuerpo["fin"] == "19:00"
    en_v1 = api.manejar(Solicitud("GET", "/v1/reservas/r-2"))
    assert en_v1.cuerpo["hora"] == 9
    assert "inicio" not in en_v1.cuerpo


def test_v2_valida_su_propio_contrato():
    api = api_nueva()
    sin_duracion = {"estudiante": "beto", "cancha": "cancha-2", "fecha": "2026-11-02", "inicio": "09:00"}
    assert api.manejar(Solicitud("POST", "/v2/reservas", sin_duracion)).estado == 400
    noventa = dict(RESERVA_V2)
    noventa["duracion_min"] = 90
    assert api.manejar(Solicitud("POST", "/v2/reservas", noventa)).cuerpo == {"error": "duracion no permitida"}
    media_hora = dict(RESERVA_V2)
    media_hora["inicio"] = "09:30"
    assert api.manejar(Solicitud("POST", "/v2/reservas", media_hora)).cuerpo == {"error": "inicio invalido"}
    assert len(api.repositorio.reservas) == 0


def test_v2_ve_las_horas_ocupadas_por_v1():
    api = api_nueva()
    api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_V1))
    choque = {"estudiante": "beto", "cancha": "cancha-1", "fecha": "2026-11-02", "inicio": "18:00", "duracion_min": 60}
    assert api.manejar(Solicitud("POST", "/v2/reservas", choque)).estado == 409


def test_v2_con_cancha_desconocida_es_404():
    api = api_nueva()
    otra = dict(RESERVA_V2)
    otra["cancha"] = "cancha-9"
    assert api.manejar(Solicitud("POST", "/v2/reservas", otra)).estado == 404
    assert api.manejar(Solicitud("GET", "/v2/reservas/r-99")).estado == 404


def test_borrar_dos_veces_deja_el_mismo_estado():
    api = api_nueva()
    api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_V1))
    primera = api.manejar(Solicitud("DELETE", "/v2/reservas/r-1"))
    assert primera.estado == 204
    assert primera.cuerpo is None
    segunda = api.manejar(Solicitud("DELETE", "/v1/reservas/r-1"))
    assert segunda.estado == 404
    assert len(api.repositorio.reservas) == 0
    assert api.manejar(Solicitud("GET", "/v1/reservas/r-1")).estado == 404


def test_un_delete_reintentado_por_la_red_no_borra_otra_cosa():
    api = api_nueva()
    api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_V1))
    api.manejar(Solicitud("POST", "/v2/reservas", RESERVA_V2))
    cliente = Cliente(RedInestable(api, respuestas_a_perder=2))
    respuesta = cliente.enviar("DELETE", "/v1/reservas/r-1")
    assert respuesta.estado == 404
    assert list(api.repositorio.reservas.keys()) == ["r-2"]


def test_una_version_que_no_existe_es_404():
    assert api_nueva().manejar(Solicitud("POST", "/v3/reservas", RESERVA_V1)).estado == 404
