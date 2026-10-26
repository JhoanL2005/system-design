"""Ejercicio 3: dos estrategias de escritura, write-through para las
reservas y write-back para el contador de visitas.

Corre las pruebas con:

    pytest test_estrategias_escritura_ejercicio3.py

No cambies los nombres de las clases ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class DisponibilidadWriteThrough:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.cache = {}

    def disponibilidad(self, cancha, fecha):
        clave = (cancha, fecha)
        if clave not in self.cache:
            self.cache[clave] = self.repositorio.consultar_disponibilidad(cancha, fecha)
        return self.cache[clave]

    def reservar(self, cancha, fecha, hora):
        libres = self.repositorio.consultar_disponibilidad(cancha, fecha)
        if hora not in libres:
            return False
        self.repositorio.registrar_reserva(cancha, fecha, hora)
        clave = (cancha, fecha)
        if clave in self.cache:
            self.cache[clave] = [h for h in self.cache[clave] if h != hora]
        return True


class VisitasWriteBack:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.pendientes = {}

    def registrar_visita(self, cancha):
        self.pendientes[cancha] = self.pendientes.get(cancha, 0) + 1

    def visitas(self, cancha):
        return self.repositorio.visitas_de(cancha) + self.pendientes.get(cancha, 0)

    def vaciar(self):
        for cancha, cantidad in self.pendientes.items():
            self.repositorio.sumar_visitas(cancha, cantidad)
        self.pendientes = {}

    def caer(self):
        # Simula que el proceso del cache se reinicia: lo que no se vacio
        # al repositorio se pierde. Ya esta completo.
        self.pendientes = {}