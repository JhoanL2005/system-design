"""Ejercicio 2: un trabajador que no pierde mensajes aunque se caiga, y
que no reintenta para siempre un mensaje que nunca va a salir.

Corre las pruebas con:

    pytest test_trabajador_confiable_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from servicios import asunto_de_confirmacion


class TrabajadorConfiable:
    def __init__(self, cola, correo, cola_de_muertos, max_intentos):
        self.cola = cola
        self.correo = correo
        self.cola_de_muertos = cola_de_muertos
        self.max_intentos = max_intentos

    def procesar_uno(self):
        mensaje = self.cola.recibir()
        if mensaje is None:
            return False
        cuerpo = mensaje["cuerpo"]
        # Primero se envia y despues se confirma: si el trabajador cae entre
        # las dos lineas, el mensaje sigue en la cola y vuelve cuando vence
        # su visibilidad (entrega "al menos una vez").
        enviado = self.correo.enviar(cuerpo["estudiante"], asunto_de_confirmacion(cuerpo))
        if enviado:
            self.cola.confirmar(mensaje["id"])
        elif mensaje["intentos"] >= self.max_intentos:
            # Agoto sus intentos: primero se publica en la cola de mensajes
            # muertos y recien despues se confirma, para no perderlo.
            self.cola_de_muertos.publicar(cuerpo)
            self.cola.confirmar(mensaje["id"])
        # Si fallo y le quedan intentos, no se confirma: vuelve a la cola.
        return True
