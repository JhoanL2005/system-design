"""Un reloj simulado, como el de la Semana 9, Sesion 2: la hora la decide
quien lo usa, en minutos desde el inicio de la simulacion.
"""


class RelojSimulado:
    def __init__(self):
        self.minuto = 0

    def ahora(self):
        return self.minuto

    def avanzar(self, minutos):
        self.minuto = self.minuto + minutos
