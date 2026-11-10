"""Un notificador en memoria, como el adaptador de prueba de la Semana 11,
Sesion 1. Guarda cada mensaje en vez de mandar un correo.
"""


class NotificadorEnMemoria:
    def __init__(self):
        self.enviados = []

    def enviar(self, destinatario, texto):
        self.enviados.append((destinatario, texto))
