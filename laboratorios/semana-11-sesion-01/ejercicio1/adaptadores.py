"""Los adaptadores de ReservaU: las piezas que conectan los puertos con
una tecnologia concreta.

- RepositorioSqlite: el puerto RepositorioDeReservas sobre SQLite. Es el
  SQL que estaba dentro de reservas_acopladas.py, sin cambios.
- RepositorioEnMemoria: el mismo puerto sobre un diccionario.
- ApiHttp: traduce una Solicitud HTTP en una llamada al caso de uso, y su
  resultado en una Respuesta.
"""

import sqlite3

from dominio import Reserva
from http_simulado import Respuesta
from puertos import RepositorioDeReservas


class RepositorioSqlite(RepositorioDeReservas):
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)
        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "estudiante TEXT, cancha TEXT, fecha TEXT, hora INTEGER)"
        )

    def ocupada(self, cancha, fecha, hora):
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM reservas WHERE cancha = ? AND fecha = ? AND hora = ?",
            (cancha, fecha, hora),
        ).fetchone()
        return fila[0] > 0

    def contar_del_estudiante(self, estudiante, fecha):
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM reservas WHERE estudiante = ? AND fecha = ?",
            (estudiante, fecha),
        ).fetchone()
        return fila[0]

    def guardar(self, estudiante, cancha, fecha, hora):
        cursor = self.conexion.execute(
            "INSERT INTO reservas (estudiante, cancha, fecha, hora) VALUES (?, ?, ?, ?)",
            (estudiante, cancha, fecha, hora),
        )
        self.conexion.commit()
        return Reserva("r-" + str(cursor.lastrowid), estudiante, cancha, fecha, hora)


class RepositorioEnMemoria(RepositorioDeReservas):
    def __init__(self):
        self.reservas = {}
        self.siguiente_numero = 1

    # TODO 3: implementa ocupada, contar_del_estudiante y guardar sobre
    # el diccionario self.reservas (id -> Reserva). Los ids son "r-1",
    # "r-2", ..., igual que en SQLite.


CODIGOS_POR_MOTIVO = {
    "cancha desconocida": 404,
    "fuera del horario": 422,
    "hora ocupada": 409,
    "limite diario alcanzado": 409,
}


class ApiHttp:
    def __init__(self, reservar_cancha):
        self.reservar_cancha = reservar_cancha

    def manejar(self, solicitud):
        if solicitud.metodo != "POST" or solicitud.ruta != "/v1/reservas":
            return Respuesta(404, {"error": "ruta desconocida"})
        cuerpo = solicitud.cuerpo
        for campo in ["estudiante", "cancha", "fecha", "hora"]:
            if campo not in cuerpo:
                return Respuesta(400, {"error": "faltan campos"})
        resultado = self.reservar_cancha.ejecutar(cuerpo["estudiante"], cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"])
        if resultado["estado"] == "rechazada":
            return Respuesta(CODIGOS_POR_MOTIVO[resultado["motivo"]], {"error": resultado["motivo"]})
        return Respuesta(201, resultado["reserva"].como_diccionario())
