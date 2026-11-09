"""Ejercicio 3: una version 2 de la API de reservas que conviva con la
version 1 sin romper a sus clientes, y un DELETE idempotente.

La version 1 ya esta completa y tiene clientes que dependen de ella: la
app del celular, que no todos los estudiantes actualizan, manda y espera
"hora" como un entero. La version 2 la pidio el equipo de la web: quiere
"inicio" como texto ("18:00"), recibir "duracion_min" para cuando las
canchas se puedan reservar por mas de una hora, y ver "fin" en la
respuesta. Las dos versiones leen y escriben las mismas reservas.

Corre las pruebas con:

    pytest test_versionado_ejercicio3.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from dominio import CANCHAS, HORAS_DEL_DIA
from http_simulado import Respuesta

CAMPOS_V1 = ["estudiante", "cancha", "fecha", "hora"]
CAMPOS_V2 = ["estudiante", "cancha", "fecha", "inicio", "duracion_min"]


def texto_de_hora(hora):
    if hora < 10:
        return "0" + str(hora) + ":00"
    return str(hora) + ":00"


def hora_de_texto(texto):
    partes = texto.split(":")
    if len(partes) != 2 or partes[1] != "00" or not partes[0].isdigit():
        return None
    hora = int(partes[0])
    if hora not in HORAS_DEL_DIA:
        return None
    return hora


def representar_v1(reserva):
    return {
        "id": reserva["id"],
        "estudiante": reserva["estudiante"],
        "cancha": reserva["cancha"],
        "fecha": reserva["fecha"],
        "hora": reserva["hora"],
    }


def representar_v2(reserva):
    # La forma interna no cambia (hora entera): la version 2 solo la
    # traduce. Hoy todas las reservas duran una hora.
    return {
        "id": reserva["id"],
        "estudiante": reserva["estudiante"],
        "cancha": reserva["cancha"],
        "fecha": reserva["fecha"],
        "inicio": texto_de_hora(reserva["hora"]),
        "fin": texto_de_hora(reserva["hora"] + 1),
    }


class ApiVersionada:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def manejar(self, solicitud):
        partes = solicitud.ruta.strip("/").split("/")
        version = partes[0]
        recurso = partes[1:]
        if version != "v1" and version != "v2":
            return Respuesta(404, {"error": "version desconocida"})
        if solicitud.metodo == "POST" and recurso == ["reservas"]:
            if version == "v1":
                return self.crear_reserva_v1(solicitud.cuerpo)
            return self.crear_reserva_v2(solicitud.cuerpo)
        if len(recurso) == 2 and recurso[0] == "reservas":
            if solicitud.metodo == "GET" and version == "v1":
                return self.obtener_reserva_v1(recurso[1])
            if solicitud.metodo == "GET":
                return self.obtener_reserva_v2(recurso[1])
            if solicitud.metodo == "DELETE":
                return self.borrar_reserva(recurso[1])
        return Respuesta(404, {"error": "ruta desconocida"})

    def crear_reserva_v1(self, cuerpo):
        for campo in CAMPOS_V1:
            if campo not in cuerpo:
                return Respuesta(400, {"error": "faltan campos"})
        if cuerpo["cancha"] not in CANCHAS:
            return Respuesta(404, {"error": "cancha desconocida"})
        if self.repositorio.ocupada(cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"]):
            return Respuesta(409, {"error": "hora ocupada"})
        reserva = self.repositorio.crear(cuerpo["estudiante"], cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"])
        return Respuesta(201, representar_v1(reserva))

    def obtener_reserva_v1(self, id_reserva):
        reserva = self.repositorio.buscar(id_reserva)
        if reserva is None:
            return Respuesta(404, {"error": "reserva desconocida"})
        return Respuesta(200, representar_v1(reserva))

    def crear_reserva_v2(self, cuerpo):
        for campo in CAMPOS_V2:
            if campo not in cuerpo:
                return Respuesta(400, {"error": "faltan campos"})
        if cuerpo["duracion_min"] != 60:
            return Respuesta(400, {"error": "duracion no permitida"})
        hora = hora_de_texto(cuerpo["inicio"])
        if hora is None:
            return Respuesta(400, {"error": "inicio invalido"})
        if cuerpo["cancha"] not in CANCHAS:
            return Respuesta(404, {"error": "cancha desconocida"})
        # Se traduce a la forma interna (hora entera) antes de tocar el
        # repositorio, asi v2 ve las horas ocupadas por v1 y al reves.
        if self.repositorio.ocupada(cuerpo["cancha"], cuerpo["fecha"], hora):
            return Respuesta(409, {"error": "hora ocupada"})
        reserva = self.repositorio.crear(cuerpo["estudiante"], cuerpo["cancha"], cuerpo["fecha"], hora)
        return Respuesta(201, representar_v2(reserva))

    def obtener_reserva_v2(self, id_reserva):
        reserva = self.repositorio.buscar(id_reserva)
        if reserva is None:
            return Respuesta(404, {"error": "reserva desconocida"})
        return Respuesta(200, representar_v2(reserva))

    def borrar_reserva(self, id_reserva):
        # Lo usan las dos versiones: borrar no depende de la forma del dato.
        if self.repositorio.buscar(id_reserva) is None:
            return Respuesta(404, {"error": "reserva desconocida"})
        self.repositorio.borrar(id_reserva)
        return Respuesta(204)
