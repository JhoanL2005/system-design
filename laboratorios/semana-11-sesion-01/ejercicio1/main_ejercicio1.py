"""Arma ReservaU por capas y le manda las mismas solicitudes que a
reservas_acopladas.py. Corre:

    python3 main_ejercicio1.py

Cambia RepositorioSqlite(":memory:") por RepositorioEnMemoria() en una
sola linea, y vuelve a correrlo.
"""

from adaptadores import ApiHttp, RepositorioEnMemoria, RepositorioSqlite
from casos_de_uso import ReservarCancha
from http_simulado import Solicitud
from reservas_acopladas import SOLICITUDES_DE_PRUEBA

if __name__ == "__main__":
    repositorio = RepositorioSqlite(":memory:")
    api = ApiHttp(ReservarCancha(repositorio))
    for cuerpo in SOLICITUDES_DE_PRUEBA:
        respuesta = api.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        print(respuesta.estado, respuesta.cuerpo)
