"""Una version minima de HTTP, para probar una API sin levantar un
servidor. Ya esta completa: no la modifiques.

- Solicitud: metodo ("GET", "POST", "DELETE"), ruta ("/v1/reservas"),
  cuerpo (un diccionario o None) y cabeceras (un diccionario).
- Respuesta: estado (201, 404, ...) y cuerpo (un diccionario o None).
- RedInestable: entrega cada solicitud a la API, que siempre la procesa,
  pero pierde las primeras "respuestas_a_perder" respuestas en el camino
  de vuelta. Para el cliente, una respuesta perdida es un tiempo de
  espera agotado: no sabe si la API alcanzo a procesar la solicitud.
- Cliente: envia una solicitud y, si no llega respuesta, la reenvia
  identica (mismo metodo, ruta, cuerpo y cabeceras), hasta max_intentos
  veces. Devuelve la primera respuesta que llega, o None.
"""


class Solicitud:
    def __init__(self, metodo, ruta, cuerpo=None, cabeceras=None):
        self.metodo = metodo
        self.ruta = ruta
        self.cuerpo = cuerpo
        if cabeceras is None:
            cabeceras = {}
        self.cabeceras = cabeceras


class Respuesta:
    def __init__(self, estado, cuerpo=None):
        self.estado = estado
        self.cuerpo = cuerpo


class RedInestable:
    def __init__(self, api, respuestas_a_perder=0):
        self.api = api
        self.respuestas_a_perder = respuestas_a_perder
        self.solicitudes_entregadas = 0

    def enviar(self, solicitud):
        respuesta = self.api.manejar(solicitud)
        self.solicitudes_entregadas = self.solicitudes_entregadas + 1
        if self.respuestas_a_perder > 0:
            self.respuestas_a_perder = self.respuestas_a_perder - 1
            return None
        return respuesta


class Cliente:
    def __init__(self, red, max_intentos=4):
        self.red = red
        self.max_intentos = max_intentos

    def enviar(self, metodo, ruta, cuerpo=None, cabeceras=None):
        solicitud = Solicitud(metodo, ruta, cuerpo, cabeceras)
        for _ in range(self.max_intentos):
            respuesta = self.red.enviar(solicitud)
            if respuesta is not None:
                return respuesta
        return None
