"""Ejercicio 1: el contrato REST de las reservas de ReservaU, y lo que
le pasa a un POST cuando la red pierde la respuesta.

Corre esto para ver el resultado:

    python3 api_v1_ejercicio1.py

Y las pruebas con:

    pytest test_api_v1_ejercicio1.py
"""

from dominio import CANCHAS, PasarelaDePagos, RepositorioDeReservas
from http_simulado import Cliente, RedInestable, Respuesta

CAMPOS_DE_RESERVA = ["estudiante", "cancha", "fecha", "hora"]


class ApiReservaU:
    def __init__(self, repositorio, pasarela):
        self.repositorio = repositorio
        self.pasarela = pasarela

    def manejar(self, solicitud):
        partes = solicitud.ruta.strip("/").split("/")
        if partes[0] != "v1":
            return Respuesta(404, {"error": "ruta desconocida"})
        recurso = partes[1:]
        if solicitud.metodo == "GET" and len(recurso) == 4 and recurso[0] == "canchas" and recurso[2] == "disponibilidad":
            return self.consultar_disponibilidad(recurso[1], recurso[3])
        if solicitud.metodo == "POST" and recurso == ["reservas"]:
            return self.crear_reserva(solicitud.cuerpo)
        if solicitud.metodo == "POST" and recurso == ["pagos"]:
            return self.crear_pago(solicitud.cuerpo)
        return Respuesta(404, {"error": "ruta desconocida"})

    def consultar_disponibilidad(self, cancha, fecha):

        if cancha not in CANCHAS:
            return Respuesta(404, {"error": "cancha desconocida"})

        return Respuesta(201, {"cancha": cancha, "fecha": fecha, "libres": self.repositorio.libres(cancha, fecha)})

    def crear_reserva(self, cuerpo):
        for campo in CAMPOS_DE_RESERVA:
            if campo not in cuerpo:
                return Respuesta(400, {"error": "faltan campos obligatorios"})

        if cuerpo["cancha"] not in CANCHAS:
            return Respuesta(404, {"error": "cancha desconocida"})

        if self.repositorio.ocupada(cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"]):
            return Respuesta(409, {"error": "fecha y hora ocupadas"})

        reserva = self.repositorio.crear(cuerpo["estudiante"], cuerpo["cancha"], cuerpo["fecha"], cuerpo["hora"])
        return Respuesta(201, reserva)
        
    def crear_pago(self, cuerpo):
        reserva = self.repositorio.buscar(cuerpo["reserva_id"])
        if reserva is None:
            return Respuesta(404, {"error": "reserva desconocida"})
        id_cobro = self.pasarela.cobrar(reserva["estudiante"], cuerpo["monto"])
        return Respuesta(201, {"id": id_cobro, "reserva_id": reserva["id"], "monto": cuerpo["monto"]})


if __name__ == "__main__":
    repositorio = RepositorioDeReservas()
    pasarela = PasarelaDePagos()
    api = ApiReservaU(repositorio, pasarela)

    cliente = Cliente(RedInestable(api))
    respuesta = cliente.enviar("GET", "/v1/canchas/cancha-1/disponibilidad/2026-11-02")
    print("GET disponibilidad:", respuesta.estado, len(respuesta.cuerpo["libres"]), "horas libres")
    respuesta = cliente.enviar("GET", "/v1/canchas/cancha-9/disponibilidad/2026-11-02")
    print("GET disponibilidad de cancha-9:", respuesta.estado, respuesta.cuerpo)

    reserva_ana = {"estudiante": "ana", "cancha": "cancha-1", "fecha": "2026-11-02", "hora": 18}
    respuesta = cliente.enviar("POST", "/v1/reservas", reserva_ana)
    print("POST reserva de ana:", respuesta.estado, respuesta.cuerpo["id"])
    respuesta = cliente.enviar("POST", "/v1/reservas", {"estudiante": "beto", "cancha": "cancha-1"})
    print("POST reserva sin fecha ni hora:", respuesta.estado, respuesta.cuerpo)

    print()
    print("Una red que pierde la primera respuesta")
    cliente = Cliente(RedInestable(api, respuestas_a_perder=1))
    reserva_beto = {"estudiante": "beto", "cancha": "cancha-2", "fecha": "2026-11-02", "hora": 9}
    respuesta = cliente.enviar("POST", "/v1/reservas", reserva_beto)
    print("POST reserva de beto, lo que recibe el cliente:", respuesta.estado, respuesta.cuerpo)
    print("Reservas en el repositorio:", len(repositorio.reservas))

    print()
    print("Una red que pierde las dos primeras respuestas")
    cliente = Cliente(RedInestable(api, respuestas_a_perder=2))
    respuesta = cliente.enviar("POST", "/v1/pagos", {"reserva_id": "r-1", "monto": 5.0})
    print("POST pago de ana, lo que recibe el cliente:", respuesta.estado, respuesta.cuerpo)
    print("Cobros en la pasarela:", len(pasarela.cobros))
