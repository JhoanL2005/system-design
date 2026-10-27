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
        # TODO 1: si la cancha no esta en CANCHAS, responde 404 con
        # {"error": "cancha desconocida"}. Si esta, responde 200 con
        # {"cancha": ..., "fecha": ..., "libres": [...]}.
        raise NotImplementedError

    def crear_reserva(self, cuerpo):
        # TODO 2: en este orden,
        # - si falta alguno de CAMPOS_DE_RESERVA en el cuerpo, 400 con
        #   {"error": "faltan campos"};
        # - si la cancha no existe, 404 con {"error": "cancha desconocida"};
        # - si la hora ya esta ocupada, 409 con {"error": "hora ocupada"};
        # - si no, crea la reserva en el repositorio y responde 201 con la
        #   reserva creada (id, estudiante, cancha, fecha, hora).
        raise NotImplementedError

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
