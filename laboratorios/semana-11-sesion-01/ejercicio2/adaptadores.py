"""Los adaptadores de ReservaU, tal como quedaron en el Ejercicio 1, mas
dos nuevos:

- NotificadorEnMemoria: el puerto Notificador sobre una lista, para las
  pruebas y para ver que se envio.
- AdaptadorDeMensajeria: una segunda forma de entrar a la aplicacion, por
  mensajes de texto de un chat.

No modifiques RepositorioSqlite, RepositorioEnMemoria ni ApiHttp.
"""

import sqlite3

from dominio import Reserva, texto_de_hora
from http_simulado import Respuesta
from puertos import Notificador, RepositorioDeReservas


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

    def ocupada(self, cancha, fecha, hora):
        for reserva in self.reservas.values():
            if reserva.cancha == cancha and reserva.fecha == fecha and reserva.hora == hora:
                return True
        return False

    def contar_del_estudiante(self, estudiante, fecha):
        cantidad = 0
        for reserva in self.reservas.values():
            if reserva.estudiante == estudiante and reserva.fecha == fecha:
                cantidad = cantidad + 1
        return cantidad

    def guardar(self, estudiante, cancha, fecha, hora):
        id_reserva = "r-" + str(self.siguiente_numero)
        self.siguiente_numero = self.siguiente_numero + 1
        reserva = Reserva(id_reserva, estudiante, cancha, fecha, hora)
        self.reservas[id_reserva] = reserva
        return reserva


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


class NotificadorEnMemoria(Notificador):
    # TODO 2: guarda cada notificacion en la lista self.enviados como una
    # tupla (estudiante, mensaje), en el orden en que llegan.
    def __init__(self):
        self.enviados = []


class AdaptadorDeMensajeria:
    """Atiende mensajes de un chat. El estudiante escribe, por ejemplo,
    "reservar cancha-1 2026-11-10 18", y recibe un texto de respuesta."""

    def __init__(self, reservar_cancha):
        self.reservar_cancha = reservar_cancha

    def atender(self, estudiante, texto):
        # TODO 3: separa el texto en palabras. Si no son exactamente 4, la
        # primera no es "reservar" o la cuarta no son solo digitos,
        # responde "No entendi. Escribe: reservar <cancha> <fecha> <hora>".
        # Si no, llama al caso de uso y responde
        # "Listo: reserva r-1, cancha-1, 2026-11-10 a las 18:00" o
        # "No se pudo reservar: hora ocupada" (con el motivo que sea).
        raise NotImplementedError
