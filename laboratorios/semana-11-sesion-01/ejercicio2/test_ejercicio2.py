from adaptadores import AdaptadorDeMensajeria, ApiHttp, NotificadorEnMemoria, RepositorioEnMemoria
from casos_de_uso import ReservarCancha
from http_simulado import Solicitud


def modulos_que_importa(archivo):
    nombres = []
    with open(archivo, encoding="utf-8") as fuente:
        for linea in fuente:
            partes = linea.split()
            if len(partes) >= 2 and (partes[0] == "import" or partes[0] == "from"):
                nombres.append(partes[1].split(".")[0])
    return nombres


def armar():
    repositorio = RepositorioEnMemoria()
    notificador = NotificadorEnMemoria()
    caso = ReservarCancha(repositorio, notificador)
    return repositorio, notificador, caso


def test_una_reserva_confirmada_notifica_al_estudiante():
    _, notificador, caso = armar()
    caso.ejecutar("ana", "cancha-1", "2026-11-10", 18)
    assert notificador.enviados == [("ana", "Reserva r-1 confirmada: cancha-1, 2026-11-10 a las 18:00")]


def test_una_reserva_rechazada_no_notifica():
    _, notificador, caso = armar()
    caso.ejecutar("ana", "cancha-1", "2026-11-10", 18)
    caso.ejecutar("beto", "cancha-1", "2026-11-10", 18)
    caso.ejecutar("beto", "cancha-9", "2026-11-10", 9)
    assert len(notificador.enviados) == 1


def test_la_hora_de_la_manana_lleva_cero():
    _, notificador, caso = armar()
    caso.ejecutar("ana", "cancha-2", "2026-11-10", 9)
    assert notificador.enviados[0][1] == "Reserva r-1 confirmada: cancha-2, 2026-11-10 a las 09:00"


def test_el_chat_confirma_y_rechaza_con_el_motivo():
    _, _, caso = armar()
    chat = AdaptadorDeMensajeria(caso)
    assert chat.atender("ana", "reservar cancha-1 2026-11-10 18") == "Listo: reserva r-1, cancha-1, 2026-11-10 a las 18:00"
    assert chat.atender("beto", "reservar cancha-1 2026-11-10 18") == "No se pudo reservar: hora ocupada"
    assert chat.atender("beto", "reservar cancha-1 2026-11-10 22") == "No se pudo reservar: fuera del horario"


def test_el_chat_no_entiende_un_mensaje_mal_escrito():
    repositorio, _, caso = armar()
    chat = AdaptadorDeMensajeria(caso)
    ayuda = "No entendi. Escribe: reservar <cancha> <fecha> <hora>"
    assert chat.atender("ana", "quiero la cancha 2 manana") == ayuda
    assert chat.atender("ana", "reservar cancha-1 2026-11-10") == ayuda
    assert chat.atender("ana", "reservar cancha-1 2026-11-10 seis") == ayuda
    assert chat.atender("ana", "cancelar cancha-1 2026-11-10 18") == ayuda
    assert repositorio.reservas == {}


def test_los_dos_adaptadores_comparten_el_mismo_caso_de_uso():
    _, notificador, caso = armar()
    api = ApiHttp(caso)
    chat = AdaptadorDeMensajeria(caso)
    chat.atender("ana", "reservar cancha-1 2026-11-10 18")
    cuerpo = {"estudiante": "beto", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18}
    assert api.manejar(Solicitud("POST", "/v1/reservas", cuerpo)).estado == 409
    cuerpo["hora"] = 19
    assert api.manejar(Solicitud("POST", "/v1/reservas", cuerpo)).estado == 201
    assert len(notificador.enviados) == 2


def test_la_api_http_no_cambio():
    _, _, caso = armar()
    api = ApiHttp(caso)
    cuerpo = {"estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18}
    respuesta = api.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
    assert respuesta.estado == 201
    assert respuesta.cuerpo == {"id": "r-1", "estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18}
    assert api.manejar(Solicitud("POST", "/v1/reservas", {"estudiante": "ana"})).estado == 400


def test_el_caso_de_uso_solo_conoce_el_dominio():
    assert modulos_que_importa("casos_de_uso.py") == ["dominio"]
