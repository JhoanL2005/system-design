"""Una version minima de HTTP, para probar una API sin levantar un
servidor. Ya esta completa: no la modifiques.

- Solicitud: metodo ("GET", "POST", "DELETE"), ruta ("/v1/reservas"),
  cuerpo (un diccionario o None) y cabeceras (un diccionario).
- Respuesta: estado (201, 404, ...) y cuerpo (un diccionario o None).
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
