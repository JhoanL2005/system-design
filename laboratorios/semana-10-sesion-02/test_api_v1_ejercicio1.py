from dominio import PasarelaDePagos, RepositorioDeReservas
from http_simulado import Cliente, RedInestable, Solicitud
from api_v1_ejercicio1 import ApiReservaU

RESERVA_ANA = {"estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}


def api_nueva():
    return ApiReservaU(RepositorioDeReservas(), PasarelaDePagos())


def test_disponibilidad_de_una_cancha_existente():
    respuesta = api_nueva().manejar(Solicitud("GET", "/v1/canchas/cancha-1/disponibilidad/2026-11-02"))
    assert respuesta.estado == 200
    assert respuesta.cuerpo["cancha"] == "cancha-1"
    assert len(respuesta.cuerpo["libres"]) == 14


def test_disponibilidad_de_una_cancha_que_no_existe():
    respuesta = api_nueva().manejar(Solicitud("GET", "/v1/canchas/cancha-9/disponibilidad/2026-11-02"))
    assert respuesta.estado == 404


def test_crear_una_reserva_responde_201_con_la_reserva():
    respuesta = api_nueva().manejar(Solicitud("POST", "/v1/reservas", RESERVA_ANA))
    assert respuesta.estado == 201
    assert respuesta.cuerpo == {"id": "r-1", "estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}


def test_crear_una_reserva_sin_todos_los_campos_es_400():
    api = api_nueva()
    respuesta = api.manejar(Solicitud("POST", "/v1/reservas", {"estudiante": "ana", "cancha": "cancha-1"}))
    assert respuesta.estado == 400
    assert len(api.repositorio.reservas) == 0


def test_crear_una_reserva_en_una_cancha_que_no_existe_es_404():
    cuerpo = {"estudiante": "ana", "cancha": "cancha-9", "fecha": "2026-11-02", "hora": 18}
    assert api_nueva().manejar(Solicitud("POST", "/v1/reservas", cuerpo)).estado == 404


def test_una_hora_ocupada_es_409_y_se_ve_en_la_disponibilidad():
    api = api_nueva()
    api.manejar(Solicitud("POST", "/v1/reservas", RESERVA_ANA))
    otra = {"estudiante": "beto", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}
    assert api.manejar(Solicitud("POST", "/v1/reservas", otra)).estado == 409
    libres = api.manejar(Solicitud("GET", "/v1/canchas/cancha-1/disponibilidad/2026-11-02")).cuerpo["libres"]
    assert 18 not in libres


def test_un_post_reintentado_por_la_red_cobra_dos_veces():
    repositorio = RepositorioDeReservas()
    pasarela = PasarelaDePagos()
    reserva = repositorio.crear("ana", "cancha-1", "2026-11-02", 18)
    cliente = Cliente(RedInestable(ApiReservaU(repositorio, pasarela), respuestas_a_perder=1))
    respuesta = cliente.enviar("POST", "/v1/pagos", {"reserva_id": reserva["id"], "monto": 5.0})
    assert respuesta.estado == 201
    assert len(pasarela.cobros) == 2
