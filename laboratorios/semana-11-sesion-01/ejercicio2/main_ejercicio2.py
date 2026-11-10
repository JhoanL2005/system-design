"""Arma ReservaU con dos formas de entrar, la API HTTP y el chat, sobre el
mismo caso de uso y el mismo repositorio. Corre:

    python3 main_ejercicio2.py
"""

from adaptadores import AdaptadorDeMensajeria, ApiHttp, NotificadorEnMemoria, RepositorioSqlite
from casos_de_uso import ReservarCancha
from http_simulado import Solicitud

if __name__ == "__main__":
    repositorio = RepositorioSqlite(":memory:")
    notificador = NotificadorEnMemoria()
    # TODO 4: crea un solo ReservarCancha con el repositorio y el
    # notificador, y pasaselo a los dos adaptadores.
    reservar_cancha = None
    api = ApiHttp(reservar_cancha)
    chat = AdaptadorDeMensajeria(reservar_cancha)

    print(chat.atender("ana", "reservar cancha-1 2026-11-10 18"))
    respuesta = api.manejar(Solicitud("POST", "/v1/reservas", {"estudiante": "beto", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18}))
    print("HTTP", respuesta.estado, respuesta.cuerpo)
    print(chat.atender("beto", "reservar cancha-2 2026-11-10 9"))
    print(chat.atender("beto", "quiero la cancha 2 manana"))
    print("Notificaciones:")
    for estudiante, mensaje in notificador.enviados:
        print(" ", estudiante, "->", mensaje)
