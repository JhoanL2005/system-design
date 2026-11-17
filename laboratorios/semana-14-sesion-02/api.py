"""La API de ReservaU, simulada como en la Semana 10: una peticion es un
diccionario con "metodo", "ruta" y "cuerpo", y la respuesta, uno con
"estado" (el codigo HTTP) y "cuerpo".

- POST /reservas, con {"id", "estudiante", "fecha"}: 201, o 409 con el
  motivo del rechazo.
- DELETE /reservas/<id>, con {"minutos_de_anticipacion"}: 200, o 404.
- GET /estudiantes/<estudiante>/puntos: 200 con {"puntos"}.
"""


class ApiDeReservas:
    def __init__(self, servicio):
        self.servicio = servicio

    def manejar(self, peticion):
        metodo = peticion["metodo"]
        partes = peticion["ruta"].strip("/").split("/")
        cuerpo = peticion.get("cuerpo", {})
        if metodo == "POST" and partes == ["reservas"]:
            motivo = self.servicio.motivo_de_rechazo(cuerpo["estudiante"], cuerpo["fecha"])
            if motivo is not None:
                return {"estado": 409, "cuerpo": {"error": motivo}}
            self.servicio.reservar(cuerpo["id"], cuerpo["estudiante"], cuerpo["fecha"])
            return {"estado": 201, "cuerpo": {"id": cuerpo["id"]}}
        if metodo == "DELETE" and len(partes) == 2 and partes[0] == "reservas":
            if self.servicio.repositorio.buscar(partes[1]) is None:
                return {"estado": 404, "cuerpo": {"error": "reserva desconocida"}}
            self.servicio.cancelar(partes[1], cuerpo["minutos_de_anticipacion"])
            return {"estado": 200, "cuerpo": {}}
        if metodo == "GET" and len(partes) == 3 and partes[0] == "estudiantes" and partes[2] == "puntos":
            return {"estado": 200, "cuerpo": {"puntos": self.servicio.repositorio.puntos_de(partes[1])}}
        return {"estado": 404, "cuerpo": {"error": "ruta desconocida"}}
