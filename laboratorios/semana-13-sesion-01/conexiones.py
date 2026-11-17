"""Conexiones simuladas, como el HTTP simulado de la Semana 10.

Una ConexionSimulada representa la conexion abierta (un WebSocket) entre
el servidor y la app de un estudiante. El servidor la usa para enviarle
mensajes cuando quiera, sin que la app pregunte. Si la app se cierra o el
telefono pierde la senal, la conexion queda cerrada y enviar devuelve
False.

No lo modifiques: los tres ejercicios lo usan tal cual.
"""


class ConexionSimulada:
    def __init__(self, usuario):
        self.usuario = usuario
        self.recibidos = []
        self._abierta = True

    def esta_abierta(self):
        return self._abierta

    def cerrar(self):
        self._abierta = False

    def enviar(self, mensaje):
        if not self._abierta:
            return False
        self.recibidos.append(mensaje)
        return True
