"""Una cola de mensajes en memoria, con la misma forma de trabajo que
Amazon SQS. Ya esta completa: no la modifiques.

- publicar(cuerpo) deja un mensaje en la cola y devuelve su id.
- recibir() entrega el siguiente mensaje disponible y lo oculta: queda
  "en proceso", invisible para cualquier otro consumidor, pero NO se
  borra. Devuelve None si no hay mensajes disponibles.
- confirmar(id_mensaje) borra definitivamente un mensaje en proceso. Es
  la forma de decirle a la cola "ya termine con este".
- vencer_visibilidad() simula que se agoto el tiempo de visibilidad:
  todo mensaje que se recibio y nunca se confirmo vuelve a estar
  disponible, al frente de la cola. En SQS esto pasa solo, despues de
  unos segundos; aqui la prueba decide cuando.

Cada mensaje es un diccionario con tres claves: "id", "cuerpo" (lo que
se publico) e "intentos" (cuantas veces se recibio).
"""


class ColaDeMensajes:
    def __init__(self, nombre):
        self.nombre = nombre
        self.disponibles = []
        self.en_proceso = {}
        self.siguiente_id = 1

    def publicar(self, cuerpo):
        mensaje = {"id": self.siguiente_id, "cuerpo": cuerpo, "intentos": 0}
        self.siguiente_id = self.siguiente_id + 1
        self.disponibles.append(mensaje)
        return mensaje["id"]

    def recibir(self):
        if len(self.disponibles) == 0:
            return None
        mensaje = self.disponibles.pop(0)
        mensaje["intentos"] = mensaje["intentos"] + 1
        self.en_proceso[mensaje["id"]] = mensaje
        return mensaje

    def confirmar(self, id_mensaje):
        self.en_proceso.pop(id_mensaje, None)

    def vencer_visibilidad(self):
        devueltos = list(self.en_proceso.values())
        self.en_proceso = {}
        self.disponibles = devueltos + self.disponibles

    def cantidad_disponibles(self):
        return len(self.disponibles)

    def cantidad_en_proceso(self):
        return len(self.en_proceso)
