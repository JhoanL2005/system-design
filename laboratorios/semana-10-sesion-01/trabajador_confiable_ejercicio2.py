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
        # TODO: recibe un mensaje de self.cola. Si no hay ninguno, devuelve
        # False.
        # Envia el correo al estudiante del cuerpo, con
        # asunto_de_confirmacion(cuerpo).
        # - Si el envio salio bien, confirma el mensaje.
        # - Si fallo y el mensaje ya lleva self.max_intentos intentos,
        #   publica su cuerpo en self.cola_de_muertos y confirmalo en
        #   self.cola, para que no vuelva.
        # - Si fallo y le quedan intentos, no lo confirmes.
        # En los tres casos, devuelve True.
        raise NotImplementedError
