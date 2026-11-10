"""Ejercicio 1, punto de partida: la API de reservas de ReservaU tal como
esta hoy. Una sola clase recibe la solicitud HTTP, aplica las reglas de
negocio y guarda en la base de datos. La base de datos es SQLite, que
viene con Python (modulo sqlite3): no hace falta instalar nada.

No lo modifiques: es el comportamiento que la version por capas tiene que
conservar. Corre esto para verlo:

    python3 reservas_acopladas.py
"""

import sqlite3

from http_simulado import Respuesta, Solicitud

CANCHAS = ["cancha-1", "cancha-2", "cancha-3"]
HORAS_DEL_DIA = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
MAXIMO_RESERVAS_POR_DIA = 2


class ApiDeReservasAcoplada:
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "estudiante TEXT, cancha TEXT, fecha TEXT, hora INTEGER)"
        )

    def manejar(self, solicitud):
        if solicitud.metodo != "POST" or solicitud.ruta != "/v1/reservas":
            return Respuesta(404, {"error": "ruta desconocida"})
        cuerpo = solicitud.cuerpo
        for campo in ["estudiante", "cancha", "fecha", "hora"]:
            if campo not in cuerpo:
                return Respuesta(400, {"error": "faltan campos"})
        if cuerpo["cancha"] not in CANCHAS:
            return Respuesta(404, {"error": "cancha desconocida"})
        if cuerpo["hora"] not in HORAS_DEL_DIA:
            return Respuesta(422, {"error": "fuera del horario"})
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM reservas WHERE cancha = ? AND fecha = ? AND hora = ?",
            (cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"]),
        ).fetchone()
        if fila[0] > 0:
            return Respuesta(409, {"error": "hora ocupada"})
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM reservas WHERE estudiante = ? AND fecha = ?",
            (cuerpo["estudiante"], cuerpo["fecha"]),
        ).fetchone()
        if fila[0] >= MAXIMO_RESERVAS_POR_DIA:
            return Respuesta(409, {"error": "limite diario alcanzado"})
        cursor = self.conexion.execute(
            "INSERT INTO reservas (estudiante, cancha, fecha, hora) VALUES (?, ?, ?, ?)",
            (cuerpo["estudiante"], cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"]),
        )
        self.conexion.commit()
        return Respuesta(201, {
            "id": "r-" + str(cursor.lastrowid),
            "estudiante": cuerpo["estudiante"],
            "cancha": cuerpo["cancha"],
            "fecha": cuerpo["fecha"],
            "hora": cuerpo["hora"],
        })


SOLICITUDES_DE_PRUEBA = [
    {"estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18},
    {"estudiante": "beto", "cancha": "cancha-1", "fecha": "2026-11-10", "hora": 18},
    {"estudiante": "ana", "cancha": "cancha-2", "fecha": "2026-11-10", "hora": 9},
    {"estudiante": "ana", "cancha": "cancha-3", "fecha": "2026-11-10", "hora": 10},
    {"estudiante": "beto", "cancha": "cancha-9", "fecha": "2026-11-10", "hora": 10},
    {"estudiante": "beto", "cancha": "cancha-2", "fecha": "2026-11-10", "hora": 22},
    {"estudiante": "beto", "cancha": "cancha-2"},
]


if __name__ == "__main__":
    api = ApiDeReservasAcoplada(":memory:")
    for cuerpo in SOLICITUDES_DE_PRUEBA:
        respuesta = api.manejar(Solicitud("POST", "/v1/reservas", cuerpo))
        print(respuesta.estado, respuesta.cuerpo)
